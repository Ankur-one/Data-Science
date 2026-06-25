"""
╔══════════════════════════════════════════════════════════════╗
║     FACE EMOTION RECOGNITION — FAST TRAINING VERSION        ║
║     Dataset : C:\\Users\\2005a\\FED\\archive                   ║
║     Optimized for MAXIMUM speed on CPU & GPU                ║
╚══════════════════════════════════════════════════════════════╝

SPEED OPTIMIZATIONS APPLIED:
  ✅ GPU auto-detection + memory growth enabled
  ✅ Mixed precision (float16) — 2-3x faster on GPU
  ✅ tf.data pipeline — faster than ImageDataGenerator
  ✅ Prefetch + cache + parallel map loading
  ✅ SeparableConv2D — same accuracy, 5-10x fewer FLOPs
  ✅ GlobalAveragePooling2D — replaces Flatten (fewer params)
  ✅ Larger batch size on GPU (128)
  ✅ All CPU cores used for data loading
  ✅ EarlyStopping — no wasted epochs

HOW TO RUN IN VS CODE:
  Step 1:  pip install -r requirements.txt
  Step 2:  python face_emotion_recognition.py
  Step 3:  Choose from the menu
"""

# ══════════════════════════════════════════════════════════════
#  STEP 1 — ENVIRONMENT (must be before TF import)
# ══════════════════════════════════════════════════════════════
import os, sys, time, warnings
os.environ['TF_CPP_MIN_LOG_LEVEL']   = '2'
os.environ['TF_ENABLE_ONEDNN_OPTS']  = '1'
os.environ['OMP_NUM_THREADS']        = str(os.cpu_count())
os.environ['TF_NUM_INTEROP_THREADS'] = str(os.cpu_count())
os.environ['TF_NUM_INTRAOP_THREADS'] = str(os.cpu_count())
warnings.filterwarnings('ignore')

# ══════════════════════════════════════════════════════════════
#  STEP 2 — IMPORTS
# ══════════════════════════════════════════════════════════════
import cv2
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns

import tensorflow as tf
from tensorflow.keras import mixed_precision
from tensorflow.keras.models import Sequential, load_model
from tensorflow.keras.layers import (
    Conv2D, SeparableConv2D, MaxPooling2D,
    Dense, Dropout, BatchNormalization,
    GlobalAveragePooling2D
)
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.callbacks import (
    EarlyStopping, ReduceLROnPlateau,
    ModelCheckpoint, TensorBoard
)
from sklearn.metrics import classification_report, confusion_matrix

# ══════════════════════════════════════════════════════════════
#  STEP 3 — CONFIGURATION
# ══════════════════════════════════════════════════════════════
BASE_DIR   = r'C:\Users\2005a\FED\archive'
TRAIN_DIR  = os.path.join(BASE_DIR, 'train')
TEST_DIR   = os.path.join(BASE_DIR, 'test')
MODEL_PATH = 'emotion_model_best.h5'
FINAL_PATH = 'emotion_model_FINAL.h5'
LOG_DIR    = 'logs'

IMG_SIZE   = 48
EPOCHS     = 20
LR         = 0.001
AUTOTUNE   = tf.data.AUTOTUNE

COLORS = ['#E74C3C','#E67E22','#F1C40F','#2ECC71',
          '#3498DB','#9B59B6','#1ABC9C']

EMOTION_BGR = {
    'angry'   : (0,   0,   255),
    'disgust' : (0,   128, 0  ),
    'fear'    : (128, 0,   128),
    'happy'   : (0,   215, 255),
    'neutral' : (200, 200, 200),
    'sad'     : (255, 100, 0  ),
    'surprise': (0,   255, 100)
}

# ══════════════════════════════════════════════════════════════
#  STEP 4 — GPU / CPU SETUP
# ══════════════════════════════════════════════════════════════
def setup_hardware():
    print("\n" + "="*60)
    print("  HARDWARE DETECTION")
    print("="*60)
    gpus = tf.config.list_physical_devices('GPU')

    if gpus:
        try:
            for gpu in gpus:
                tf.config.experimental.set_memory_growth(gpu, True)
            mixed_precision.set_global_policy('mixed_float16')
            print(f"  ✅ GPU : {len(gpus)} GPU(s) detected")
            for g in gpus:
                print(f"       → {g.name}")
            print("  ✅ Mixed precision float16 ENABLED  (2-3x faster)")
            print("="*60)
            return 'GPU', 128
        except RuntimeError as e:
            print(f"  ⚠  GPU error: {e}")

    tf.config.threading.set_inter_op_parallelism_threads(os.cpu_count())
    tf.config.threading.set_intra_op_parallelism_threads(os.cpu_count())
    print(f"  ℹ  No GPU — optimized CPU mode ({os.cpu_count()} cores)")
    print("  💡 Install CUDA + tensorflow-gpu for 10-20x speedup")
    print("="*60)
    return 'CPU', 64


# ══════════════════════════════════════════════════════════════
#  STEP 5 — VERIFY PATHS + DETECT LABELS
# ══════════════════════════════════════════════════════════════
def verify_paths():
    print("\n" + "="*60)
    print("  CHECKING DATASET PATHS")
    print("="*60)
    ok = True
    for lbl, path in [('Base ', BASE_DIR),('Train', TRAIN_DIR),('Test ', TEST_DIR)]:
        exists = os.path.exists(path)
        print(f"  {lbl}: {'✅ Found  ' if exists else '❌ MISSING'} → {path}")
        if not exists: ok = False
    if not ok:
        print("\n  ❌ Fix paths above and re-run.")
        sys.exit(1)
    print("="*60)

def get_labels():
    labels = sorted([d for d in os.listdir(TRAIN_DIR)
                     if os.path.isdir(os.path.join(TRAIN_DIR, d))])
    print(f"\n  Detected {len(labels)} emotions: {labels}")
    return labels

# ══════════════════════════════════════════════════════════════
#  STEP 6 — FAST tf.data PIPELINE
#  Replaces slow ImageDataGenerator:
#    • Parallel image decoding (all CPU cores)
#    • In-memory caching after epoch 1
#    • GPU prefetch — no idle time between batches
# ══════════════════════════════════════════════════════════════
def _load_image(path, label, num_classes):
    img = tf.io.read_file(path)
    img = tf.image.decode_image(img, channels=1, expand_animations=False)
    img = tf.image.resize(img, [IMG_SIZE, IMG_SIZE])
    img = tf.cast(img, tf.float32) / 255.0
    return img, tf.one_hot(label, num_classes)

def _augment(img, label):
    img = tf.image.random_flip_left_right(img)
    img = tf.image.random_brightness(img, max_delta=0.2)
    img = tf.image.random_contrast(img, lower=0.8, upper=1.2)
    img = tf.image.resize_with_crop_or_pad(img, IMG_SIZE+6, IMG_SIZE+6)
    img = tf.image.random_crop(img, [IMG_SIZE, IMG_SIZE, 1])
    img = tf.clip_by_value(img, 0.0, 1.0)
    return img, label

def build_dataset(directory, emotion_labels, batch_size, training=False):
    num_classes = len(emotion_labels)
    all_paths, all_labels = [], []

    for idx, emo in enumerate(emotion_labels):
        folder = os.path.join(directory, emo)
        if not os.path.isdir(folder): continue
        for fname in os.listdir(folder):
            if fname.lower().endswith(('.jpg','.jpeg','.png')):
                all_paths.append(os.path.join(folder, fname))
                all_labels.append(idx)

    split = 'Train' if training else 'Test '
    print(f"  {split} samples : {len(all_paths):,}")

    ds = tf.data.Dataset.from_tensor_slices((all_paths, all_labels))

    if training:
        ds = ds.shuffle(len(all_paths), seed=42, reshuffle_each_iteration=True)

    ds = ds.map(lambda p, l: _load_image(p, l, num_classes),
                num_parallel_calls=AUTOTUNE)

    # Cache: images stay in RAM from epoch 2 onward — huge speedup
    ds = ds.cache()

    if training:
        ds = ds.map(_augment, num_parallel_calls=AUTOTUNE)

    ds = ds.batch(batch_size).prefetch(AUTOTUNE)
    return ds, len(all_paths)


# ══════════════════════════════════════════════════════════════
#  STEP 7 — EFFICIENT MODEL
#  SeparableConv2D = depthwise + pointwise convolution
#  Same accuracy as Conv2D but ~8-9x fewer multiply-ops per layer
# ══════════════════════════════════════════════════════════════
def build_model(num_classes):
    print("\n  Building efficient CNN...")
    model = Sequential([

        # Block 1 — standard conv (first layer needs regular Conv2D)
        Conv2D(32, (3,3), padding='same', activation='relu',
               input_shape=(IMG_SIZE, IMG_SIZE, 1)),
        BatchNormalization(),
        Conv2D(32, (3,3), padding='same', activation='relu'),
        BatchNormalization(),
        MaxPooling2D((2,2)),
        Dropout(0.25),

        # Block 2 — separable conv (faster)
        SeparableConv2D(64, (3,3), padding='same', activation='relu'),
        BatchNormalization(),
        SeparableConv2D(64, (3,3), padding='same', activation='relu'),
        BatchNormalization(),
        MaxPooling2D((2,2)),
        Dropout(0.25),

        # Block 3 — separable conv
        SeparableConv2D(128, (3,3), padding='same', activation='relu'),
        BatchNormalization(),
        SeparableConv2D(128, (3,3), padding='same', activation='relu'),
        BatchNormalization(),
        MaxPooling2D((2,2)),
        Dropout(0.25),

        # Block 4 — separable conv
        SeparableConv2D(256, (3,3), padding='same', activation='relu'),
        BatchNormalization(),
        MaxPooling2D((2,2)),
        Dropout(0.25),

        # Head — GlobalAveragePooling instead of Flatten = fewer params
        GlobalAveragePooling2D(),
        Dense(256, activation='relu'),
        BatchNormalization(),
        Dropout(0.5),
        Dense(128, activation='relu'),
        Dropout(0.4),
        Dense(num_classes, activation='softmax', dtype='float32')

    ], name='EfficientEmotionCNN')

    model.compile(
        optimizer=Adam(learning_rate=LR),
        loss='categorical_crossentropy',
        metrics=['accuracy']
    )

    model.summary()
    total = model.count_params()
    print(f"\n  Parameters : {total:,}  (~{total*4/1024/1024:.1f} MB)")
    return model


# ══════════════════════════════════════════════════════════════
#  STEP 8 — TRAIN
# ══════════════════════════════════════════════════════════════
def train_model(model, train_ds, test_ds, train_size, batch_size):
    print("\n" + "="*60)
    print("  TRAINING  (speed-optimized)")
    print(f"  Max epochs  : {EPOCHS}  (EarlyStopping active)")
    print(f"  Batch size  : {batch_size}")
    print(f"  Steps/epoch : ~{train_size // batch_size}")
    print("="*60)

    os.makedirs(LOG_DIR, exist_ok=True)
    callbacks = [
        EarlyStopping(monitor='val_accuracy', patience=8,
                      restore_best_weights=True, verbose=1),
        ReduceLROnPlateau(monitor='val_loss', factor=0.5,
                          patience=4, min_lr=1e-7, verbose=1),
        ModelCheckpoint(MODEL_PATH, monitor='val_accuracy',
                        save_best_only=True, verbose=1),
        TensorBoard(LOG_DIR, histogram_freq=0, update_freq='epoch')
    ]

    t0 = time.time()
    history = model.fit(train_ds, epochs=EPOCHS,
                        validation_data=test_ds,
                        callbacks=callbacks, verbose=1)
    elapsed  = time.time() - t0
    n_epochs = len(history.history['val_accuracy'])

    print("\n" + "="*60)
    print("  ✅ TRAINING COMPLETE!")
    print(f"  Epochs run       : {n_epochs}")
    print(f"  Total time       : {elapsed/60:.1f} min")
    print(f"  Time per epoch   : {elapsed/n_epochs:.0f} sec")
    print(f"  Best val acc     : {max(history.history['val_accuracy'])*100:.2f}%")
    print("="*60)
    return history


# ══════════════════════════════════════════════════════════════
#  STEP 9 — PLOT HISTORY
# ══════════════════════════════════════════════════════════════
def plot_history(history):
    acc, val_acc = history.history['accuracy'], history.history['val_accuracy']
    loss, val_loss = history.history['loss'], history.history['val_loss']
    ep = range(1, len(acc)+1)

    fig, axes = plt.subplots(1, 2, figsize=(14, 5))
    fig.suptitle('Training History', fontsize=16, fontweight='bold')

    axes[0].plot(ep, acc,     'b-o', label='Train', markersize=4, lw=2)
    axes[0].plot(ep, val_acc, 'r-o', label='Val',   markersize=4, lw=2)
    axes[0].axvline(val_acc.index(max(val_acc))+1, color='green',
                    ls='--', alpha=0.7, label=f'Best {max(val_acc)*100:.1f}%')
    axes[0].set_title('Accuracy'); axes[0].set_ylim([0,1])
    axes[0].set_xlabel('Epoch'); axes[0].legend(); axes[0].grid(alpha=0.3)

    axes[1].plot(ep, loss,     'b-o', label='Train', markersize=4, lw=2)
    axes[1].plot(ep, val_loss, 'r-o', label='Val',   markersize=4, lw=2)
    axes[1].axvline(val_loss.index(min(val_loss))+1, color='green',
                    ls='--', alpha=0.7, label=f'Best {min(val_loss):.4f}')
    axes[1].set_title('Loss')
    axes[1].set_xlabel('Epoch'); axes[1].legend(); axes[1].grid(alpha=0.3)

    plt.tight_layout()
    plt.savefig('3_training_history.png', dpi=100, bbox_inches='tight')
    plt.close()
    print("  ✅ Saved → 3_training_history.png")


# ══════════════════════════════════════════════════════════════
#  STEP 10 — EVALUATE
# ══════════════════════════════════════════════════════════════
def evaluate_model(model, test_ds, emotion_labels):
    print("\n" + "="*60)
    print("  EVALUATION")
    print("="*60)

    loss, acc = model.evaluate(test_ds, verbose=1)
    print(f"\n  Test Accuracy : {acc*100:.2f}%")
    print(f"  Test Loss     : {loss:.4f}")

    y_pred_list, y_true_list = [], []
    for x_b, y_b in test_ds:
        preds = model.predict(x_b, verbose=0)
        y_pred_list.extend(np.argmax(preds, axis=1))
        y_true_list.extend(np.argmax(y_b.numpy(), axis=1))

    y_pred = np.array(y_pred_list)
    y_true = np.array(y_true_list)
    labels = [e.capitalize() for e in emotion_labels]

    print("\n  Classification Report:")
    print(classification_report(y_true, y_pred, target_names=labels))

    cm      = confusion_matrix(y_true, y_pred)
    cm_norm = cm.astype('float') / cm.sum(axis=1)[:, np.newaxis]

    fig, axes = plt.subplots(1, 2, figsize=(18, 7))
    fig.suptitle('Confusion Matrix', fontsize=16, fontweight='bold')
    sns.heatmap(cm,      annot=True, fmt='d',    cmap='Blues',
                xticklabels=labels, yticklabels=labels, ax=axes[0])
    sns.heatmap(cm_norm, annot=True, fmt='.2f',  cmap='Greens',
                xticklabels=labels, yticklabels=labels, ax=axes[1],
                vmin=0, vmax=1)
    for ax, t in zip(axes, ['Count','Normalised']):
        ax.set_title(t); ax.set_xlabel('Predicted'); ax.set_ylabel('Actual')

    plt.tight_layout()
    plt.savefig('4_confusion_matrix.png', dpi=100, bbox_inches='tight')
    plt.close()
    print("  ✅ Saved → 4_confusion_matrix.png")


# ══════════════════════════════════════════════════════════════
#  STEP 11 — EXPLORE DATASET
# ══════════════════════════════════════════════════════════════
def explore_dataset(emotion_labels):
    print("\n" + "="*60)
    print("  DATASET EXPLORATION")
    print("="*60)

    def count(d):
        return {e: len([f for f in os.listdir(os.path.join(d, e))
                        if f.lower().endswith(('.jpg','.png','.jpeg'))])
                for e in emotion_labels if os.path.isdir(os.path.join(d, e))}

    tc = count(TRAIN_DIR); vc = count(TEST_DIR)
    df = pd.DataFrame({'Emotion': emotion_labels,
                       'Train':   [tc.get(e,0) for e in emotion_labels],
                       'Test':    [vc.get(e,0) for e in emotion_labels]})
    print(df.to_string(index=False))
    print(f"\n  Total Train : {df['Train'].sum():,}")
    print(f"  Total Test  : {df['Test'].sum():,}")

    fig, axes = plt.subplots(1, 2, figsize=(14,5))
    fig.suptitle('Dataset Distribution', fontsize=16, fontweight='bold')
    for ax, col, title in zip(axes,['Train','Test'],['Training','Test']):
        bars = ax.bar(df['Emotion'], df[col],
                      color=COLORS[:len(emotion_labels)],
                      edgecolor='white', lw=1.2)
        ax.set_title(title); ax.set_xlabel('Emotion'); ax.set_ylabel('Images')
        ax.tick_params(axis='x', rotation=30); ax.grid(axis='y', alpha=0.3)
        for b in bars:
            ax.text(b.get_x()+b.get_width()/2, b.get_height()+20,
                    str(int(b.get_height())), ha='center', va='bottom', fontsize=9)
    plt.tight_layout()
    plt.savefig('1_dataset_distribution.png', dpi=100, bbox_inches='tight')
    plt.close()
    print("  ✅ Saved → 1_dataset_distribution.png")

    n = len(emotion_labels)
    fig, axes = plt.subplots(2, n, figsize=(n*2.5, 6))
    fig.suptitle('Sample Images', fontsize=14, fontweight='bold')
    for col, emo in enumerate(emotion_labels):
        for row, d in enumerate([TRAIN_DIR, TEST_DIR]):
            folder = os.path.join(d, emo)
            files  = [f for f in os.listdir(folder)
                      if f.lower().endswith(('.jpg','.png','.jpeg'))]
            if files:
                img = cv2.imread(os.path.join(folder, files[0]),
                                 cv2.IMREAD_GRAYSCALE)
                axes[row, col].imshow(img, cmap='gray')
                axes[row, col].set_title(emo.capitalize(), fontsize=10,
                                         color=COLORS[col%len(COLORS)],
                                         fontweight='bold')
            axes[row, col].axis('off')
    plt.tight_layout()
    plt.savefig('2_sample_images.png', dpi=100, bbox_inches='tight')
    plt.close()
    print("  ✅ Saved → 2_sample_images.png")


# ══════════════════════════════════════════════════════════════
#  STEP 12 — PREDICTION GRID
# ══════════════════════════════════════════════════════════════
def prediction_grid(model, emotion_labels, n_per_class=2):
    all_imgs, all_true, all_pred, all_conf = [], [], [], []
    for emo in emotion_labels:
        folder = os.path.join(TEST_DIR, emo)
        files  = [f for f in os.listdir(folder)
                  if f.lower().endswith(('.jpg','.png','.jpeg'))]
        chosen = np.random.choice(files, min(n_per_class, len(files)), replace=False)
        for fname in chosen:
            img   = cv2.imread(os.path.join(folder, fname), cv2.IMREAD_GRAYSCALE)
            img_r = cv2.resize(img, (IMG_SIZE, IMG_SIZE))
            inp   = (img_r/255.0).reshape(1, IMG_SIZE, IMG_SIZE, 1)
            preds = model.predict(inp, verbose=0)[0]
            pidx  = np.argmax(preds)
            all_imgs.append(img_r); all_true.append(emo)
            all_pred.append(emotion_labels[pidx]); all_conf.append(preds[pidx]*100)

    n = len(emotion_labels)
    fig, axes = plt.subplots(n_per_class, n, figsize=(n*2.5, n_per_class*3.2))
    if n_per_class == 1: axes = axes.reshape(1,-1)
    fig.suptitle('Test Predictions  |  ✓ Correct   ✗ Wrong',
                 fontsize=14, fontweight='bold')
    for idx, (img, true, pred, conf) in enumerate(
            zip(all_imgs, all_true, all_pred, all_conf)):
        r, c = divmod(idx, n)
        if r >= n_per_class: break
        axes[r,c].imshow(img, cmap='gray')
        ok = (true == pred)
        axes[r,c].set_title(f'{"✓" if ok else "✗"} T:{true}\nP:{pred} {conf:.0f}%',
                             fontsize=8.5, color='green' if ok else 'red',
                             fontweight='bold')
        axes[r,c].axis('off')
    plt.tight_layout()
    plt.savefig('5_prediction_grid.png', dpi=100, bbox_inches='tight')
    plt.close()
    print("  ✅ Saved → 5_prediction_grid.png")


# ══════════════════════════════════════════════════════════════
#  STEP 13 — PREDICT SINGLE IMAGE
# ══════════════════════════════════════════════════════════════
def predict_image(image_path, model, emotion_labels):
    if not os.path.exists(image_path):
        print(f"  ❌ Not found: {image_path}"); return
    img   = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    img_r = cv2.resize(img, (IMG_SIZE, IMG_SIZE))
    inp   = (img_r/255.0).reshape(1, IMG_SIZE, IMG_SIZE, 1)
    preds = model.predict(inp, verbose=0)[0]
    pidx  = np.argmax(preds)
    emo   = emotion_labels[pidx]
    conf  = preds[pidx]*100

    print(f"\n  🎯 Predicted : {emo.upper()}  ({conf:.1f}%)")
    for e, p in sorted(zip(emotion_labels, preds*100), key=lambda x: -x[1]):
        print(f"    {e:10s}: {'█'*int(p//5):20s} {p:5.1f}%")

    fig, axes = plt.subplots(1, 2, figsize=(12,4))
    axes[0].imshow(img_r, cmap='gray')
    axes[0].set_title(f'{emo.upper()}  {conf:.1f}%',
                      fontsize=13, fontweight='bold', color='green')
    axes[0].axis('off')
    bar_colors = [COLORS[i%len(COLORS)] if i==pidx else '#BDC3C7'
                  for i in range(len(emotion_labels))]
    axes[1].barh([e.capitalize() for e in emotion_labels],
                  preds*100, color=bar_colors, edgecolor='white')
    axes[1].set_xlabel('Confidence (%)'); axes[1].set_xlim(0,100)
    axes[1].set_title('Probabilities')
    plt.tight_layout()
    plt.savefig('6_single_prediction.png', dpi=100, bbox_inches='tight')
    plt.show()
    print("  ✅ Saved → 6_single_prediction.png")


# ══════════════════════════════════════════════════════════════
#  STEP 14 — REAL-TIME WEBCAM
# ══════════════════════════════════════════════════════════════
def run_webcam(model, emotion_labels, camera_index=0):
    face_cascade = cv2.CascadeClassifier(
        cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    cap = cv2.VideoCapture(camera_index)
    if not cap.isOpened():
        print("  ❌ Cannot open webcam."); return
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
    cap.set(cv2.CAP_PROP_FPS, 30)
    print("  ✅ Webcam started — press Q to quit")

    while True:
        ret, frame = cap.read()
        if not ret: break
        gray  = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(
            gray, scaleFactor=1.1, minNeighbors=5, minSize=(40,40))

        for (x, y, w, h) in faces:
            roi   = gray[y:y+h, x:x+w]
            roi_r = cv2.resize(roi, (IMG_SIZE, IMG_SIZE))
            inp   = (roi_r/255.0).reshape(1, IMG_SIZE, IMG_SIZE, 1)
            preds = model.predict(inp, verbose=0)[0]
            eidx  = np.argmax(preds)
            elbl  = emotion_labels[eidx]
            conf  = preds[eidx]*100
            color = EMOTION_BGR.get(elbl, (255,255,255))

            cv2.rectangle(frame, (x,y), (x+w,y+h), color, 2)
            label = f'{elbl.upper()}  {conf:.1f}%'
            (tw, th), _ = cv2.getTextSize(label, cv2.FONT_HERSHEY_DUPLEX, 0.75, 1)
            ly = max(y-10, th+10)
            cv2.rectangle(frame, (x, ly-th-6), (x+tw+6, ly+4), color, -1)
            cv2.putText(frame, label, (x+3, ly),
                        cv2.FONT_HERSHEY_DUPLEX, 0.75, (0,0,0), 1, cv2.LINE_AA)
            for i, (emo, prob) in enumerate(zip(emotion_labels, preds)):
                by = 15 + i*26
                cv2.rectangle(frame, (10,by), (10+int(prob*120), by+16),
                              EMOTION_BGR.get(emo,(200,200,200)), -1)
                cv2.rectangle(frame, (10,by), (130, by+16), (80,80,80), 1)
                cv2.putText(frame, f'{emo[:3]:3s} {prob*100:4.1f}%',
                            (135, by+13), cv2.FONT_HERSHEY_SIMPLEX,
                            0.42, (255,255,255), 1)

        cv2.putText(frame, 'Q = quit', (550,470),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (200,200,200), 1)
        cv2.imshow('Face Emotion Recognition', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
    print("  ✅ Webcam ended.")


# ══════════════════════════════════════════════════════════════
#  STEP 15 — SAVE
# ══════════════════════════════════════════════════════════════
def save_model_files(model):
    model.save(FINAL_PATH)
    print(f"  ✅ Saved → {FINAL_PATH}")
    model.save('emotion_savedmodel/')
    print("  ✅ Saved → emotion_savedmodel/")
    with open('emotion_model_config.json','w') as f:
        f.write(model.to_json())
    print("  ✅ Saved → emotion_model_config.json")


# ══════════════════════════════════════════════════════════════
#  MENU + MAIN
# ══════════════════════════════════════════════════════════════
def main():
    device, batch_size = setup_hardware()

    print(f"""
╔══════════════════════════════════════════════════════╗
║       FACE EMOTION RECOGNITION — FAST MODE          ║
╠══════════════════════════════════════════════════════╣
║  TF Version : {tf.__version__:<37}║
║  Device     : {device:<37}║
║  Batch Size : {str(batch_size):<37}║
╚══════════════════════════════════════════════════════╝""")

    verify_paths()
    emotion_labels = get_labels()
    num_classes    = len(emotion_labels)

    print("""
  ┌──────────────────────────────────────────────┐
  │   CHOOSE AN OPTION                           │
  │                                              │
  │   1  →  Train from scratch  (FAST)           │
  │   2  →  Load saved model + Evaluate          │
  │   3  →  Real-time webcam detection           │
  │   4  →  Predict a single image               │
  │   5  →  Full pipeline  (Train + All)         │
  │   q  →  Quit                                 │
  └──────────────────────────────────────────────┘""")

    choice = input("\n  Enter choice: ").strip().lower()

    def _load_saved():
        path = FINAL_PATH if os.path.exists(FINAL_PATH) else MODEL_PATH
        if not os.path.exists(path):
            print("  ❌ No saved model. Run Option 1 first.")
            sys.exit(1)
        m = load_model(path)
        print(f"  ✅ Loaded: {path}")
        return m

    if choice == '1':
        explore_dataset(emotion_labels)
        print("\n  Building tf.data pipelines...")
        train_ds, train_sz = build_dataset(TRAIN_DIR, emotion_labels, batch_size, training=True)
        test_ds,  test_sz  = build_dataset(TEST_DIR,  emotion_labels, batch_size, training=False)
        model   = build_model(num_classes)
        history = train_model(model, train_ds, test_ds, train_sz, batch_size)
        plot_history(history)
        save_model_files(load_model(MODEL_PATH))

    elif choice == '2':
        model = _load_saved()
        test_ds, _ = build_dataset(TEST_DIR, emotion_labels, batch_size, training=False)
        evaluate_model(model, test_ds, emotion_labels)
        prediction_grid(model, emotion_labels)

    elif choice == '3':
        run_webcam(_load_saved(), emotion_labels)

    elif choice == '4':
        img_path = input("\n  Enter full image path: ").strip().strip('"')
        predict_image(img_path, _load_saved(), emotion_labels)

    elif choice == '5':
        explore_dataset(emotion_labels)
        print("\n  Building tf.data pipelines...")
        train_ds, train_sz = build_dataset(TRAIN_DIR, emotion_labels, batch_size, training=True)
        test_ds,  test_sz  = build_dataset(TEST_DIR,  emotion_labels, batch_size, training=False)
        model   = build_model(num_classes)
        history = train_model(model, train_ds, test_ds, train_sz, batch_size)
        plot_history(history)
        best = load_model(MODEL_PATH)
        evaluate_model(best, test_ds, emotion_labels)
        prediction_grid(best, emotion_labels)
        save_model_files(best)
        if input("\n  Launch webcam? (y/n): ").strip().lower() == 'y':
            run_webcam(best, emotion_labels)

        print("\n" + "="*55)
        print("  ✅ FULL PIPELINE COMPLETE!")
        for f in sorted(os.listdir('.')):
            if f.endswith(('.png','.h5')):
                print(f"     {f:<40} {os.path.getsize(f)/1024:.1f} KB")
        print("="*55)

    elif choice == 'q':
        print("\n  Goodbye! 👋")
    else:
        print("  ❌ Invalid choice.")


if __name__ == '__main__':
    main()
