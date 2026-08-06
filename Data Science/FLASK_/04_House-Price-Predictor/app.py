from flask import Flask, render_template, request
import pickle
import traceback
import os

app = Flask(__name__)

# ==========================
# Load Trained Model
# ==========================
try:
    model = pickle.load(open("model.pkl", "rb"))
    print("✅ Model Loaded Successfully")
except Exception as e:
    print("❌ Error Loading Model")
    print(e)
    model = None


# ==========================
# Home Page
# ==========================
@app.route("/")
def home():
    return render_template("index.html")


# ==========================
# Prediction
@app.route('/predict', methods=['POST'])
def predict():
    try:
        # Read input
        features = [float(x) for x in request.form.values()]

        print("Features:", features)

        # Predict
        prediction = model.predict([features])

        print("Prediction:", prediction)
        print("Prediction Type:", type(prediction))

        import numpy as np

        prediction = np.asarray(prediction)

        print("Prediction Shape:", prediction.shape)

        output = prediction.flatten()[0]

        return render_template(
            "index.html",
            prediction_text=f"Predicted House Price: ₹ {output:,.2f}"
        )

    except Exception:
        import traceback
        return f"<pre>{traceback.format_exc()}</pre>"


# ==========================
# Run Flask
# ==========================
if __name__ == "__main__":
    app.run(debug=True)