import streamlit as st
import pandas as pd
import seaborn as sns

try:
    from sklearn.model_selection import train_test_split
    from sklearn.preprocessing import StandardScaler
    from sklearn.linear_model import LinearRegression
    from sklearn.tree import DecisionTreeRegressor, DecisionTreeClassifier
    from sklearn.ensemble import RandomForestRegressor, RandomForestClassifier
    from sklearn.svm import SVR, SVC
    from sklearn.compose import ColumnTransformer
    from sklearn.pipeline import Pipeline
    from sklearn.impute import SimpleImputer
    from sklearn.preprocessing import OneHotEncoder
    from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score, accuracy_score, precision_score, recall_score, f1_score, confusion_matrix
    SKLEARN_AVAILABLE = True
except ModuleNotFoundError as exc:
    SKLEARN_AVAILABLE = False
    st.set_page_config(page_title="ML App", layout="wide")
    st.error(f"Missing package: {exc.name}. Install it in the current Python environment and restart the app.")
    st.code("C:/Users/2005a/anaconda3/python.exe -m pip install scikit-learn pandas seaborn streamlit matplotlib numpy", language="powershell")
    st.stop()

# Function to preprocess data
def preprocess_data(X, y, problem):
    X = X.copy()
    y = y.copy()

    if X.empty:
        return X, y

    numeric_cols = X.select_dtypes(include=['number']).columns.tolist()
    categorical_cols = X.select_dtypes(exclude=['number']).columns.tolist()

    if problem == "Classification":
        y = y.astype(str)

    transformers = []
    if numeric_cols:
        transformers.append(("num", Pipeline([("imputer", SimpleImputer(strategy="median")), ("scaler", StandardScaler())]), numeric_cols))
    if categorical_cols:
        transformers.append(("cat", Pipeline([("imputer", SimpleImputer(strategy="most_frequent")), ("encoder", OneHotEncoder(handle_unknown="ignore"))]), categorical_cols))

    if not transformers:
        return X.to_numpy(), y

    preprocessor = ColumnTransformer(transformers=transformers, remainder="drop")
    X_processed = preprocessor.fit_transform(X)

    return X_processed, y


# Function to train and evaluate models
def train_and_evaluate(X_train, X_test, y_train, y_test, model):
    model.fit(X_train, y_train)
    predictions = model.predict(X_test)
    return model, predictions


def validate_analysis_inputs(data, features, target, problem_type):
    if not features:
        raise ValueError("Please select at least one feature column.")
    if target in features:
        raise ValueError("The target column cannot also be selected as a feature.")
    if target not in data.columns:
        raise ValueError("The selected target column is not available in the dataset.")
    if data[target].isnull().all():
        raise ValueError("The target column must contain at least one non-missing value.")

    if problem_type == "Regression":
        if not pd.api.types.is_numeric_dtype(data[target]):
            raise ValueError("Regression requires a numeric target column.")
    else:
        if data[target].nunique(dropna=True) < 2:
            raise ValueError("Classification requires at least two classes in the target column.")

# Main application function
def main():
    st.title("Machine Learning Application")
    st.write("Welcome to the machine learning application. This app allows you to train and evaluate different machine learning models on your dataset.")
    
    # Data upload or example data selection
    data_source = st.sidebar.selectbox("Do you want to upload data or use example data?", ["Upload", "Example"])
    data = None
    available_datasets = ["titanic", "tips", "iris", "diamonds", "penguins"]

    if data_source == "Upload":
        uploaded_file = st.sidebar.file_uploader("Choose a file", type=['csv', 'xlsx', 'tsv'])
        if uploaded_file is not None:
            file_name = uploaded_file.name.lower()
            if file_name.endswith('.csv'):
                data = pd.read_csv(uploaded_file)
            elif file_name.endswith('.xlsx'):
                data = pd.read_excel(uploaded_file)
            elif file_name.endswith('.tsv'):
                data = pd.read_csv(uploaded_file, sep='\t')
            else:
                st.error("Unsupported file type.")
                st.stop()
        else:
            st.info("Upload a file to preview it, or choose one of the built-in datasets below.")
            dataset_name = st.sidebar.selectbox("Select an example dataset", available_datasets, key="example_dataset_upload")
            try:
                data = sns.load_dataset(dataset_name)
            except Exception as exc:
                st.error(f"Could not load dataset '{dataset_name}': {exc}")
                st.stop()
    else:
        dataset_name = st.sidebar.selectbox("Select an example dataset", available_datasets, key="example_dataset")
        try:
            data = sns.load_dataset(dataset_name)
        except Exception as exc:
            st.error(f"Could not load dataset '{dataset_name}': {exc}")
            st.stop()

    if data is not None and not data.empty:
        st.subheader("Dataset Preview")
        st.dataframe(data.head(10))
        st.write("Data Shape:", data.shape)
        st.write("Column Names:", data.columns.tolist())
        with st.expander("More dataset details"):
            st.write("Data Description:", data.describe())
            st.write("Data Info:", data.info())
        
        # Select features and target
        features = st.multiselect("Select features columns", data.columns.tolist())
        target = st.selectbox("Select target column", data.columns.tolist())
        problem_type = st.selectbox("Problem Type", ["Classification", "Regression"])
        
        if features and target and problem_type:
            try:
                validate_analysis_inputs(data, features, target, problem_type)
            except ValueError as exc:
                st.error(str(exc))
                st.stop()

            X = data[features]
            y = data[target]
            
            st.write(f"You have selected a {problem_type} problem.")
            
            # Button to start analysis
            if st.button("Run Analysis"):
                try:
                    # Pre-process data
                    X_processed, y_processed = preprocess_data(X, y, problem_type)
                    
                    # Train-test split
                    test_size = st.slider(
                        "Select test split size",
                        min_value=0.1,
                        max_value=0.5,
                        value=0.2,
                        step=0.1,
                    )
                    X_train, X_test, y_train, y_test = train_test_split(X_processed, y_processed, test_size=test_size, random_state=42)
                    
                    # Model selection based on problem type
                    model_options = ['Linear Regression', 'Decision Tree', 'Random Forest', 'SVM'] if problem_type == 'Regression' else ['Decision Tree', 'Random Forest', 'SVM']
                    selected_model = st.sidebar.selectbox("Select model", model_options)
                    
                    # Initialize model
                    if selected_model == 'Linear Regression':
                        model = LinearRegression()
                    elif selected_model == 'Decision Tree':
                        model = DecisionTreeRegressor() if problem_type == 'Regression' else DecisionTreeClassifier()
                    elif selected_model == 'Random Forest':
                        model = RandomForestRegressor() if problem_type == 'Regression' else RandomForestClassifier()
                    elif selected_model == 'SVM':
                        model = SVR() if problem_type == 'Regression' else SVC()
                        
                    # Train and evaluate model
                    model, predictions = train_and_evaluate(X_train, X_test, y_train, y_test, model)

                    if problem_type == "Regression":
                        st.write("MSE:", mean_squared_error(y_test, predictions))
                        st.write("MAE:", mean_absolute_error(y_test, predictions))
                        st.write("R2 Score:", r2_score(y_test, predictions))
                    else:
                        st.write("Accuracy:", accuracy_score(y_test, predictions))
                        st.write("Precision:", precision_score(y_test, predictions, average="weighted", zero_division=0))
                        st.write("Recall:", recall_score(y_test, predictions, average="weighted", zero_division=0))
                        st.write("F1 Score:", f1_score(y_test, predictions, average="weighted", zero_division=0))
                        st.write("Confusion Matrix:")
                        st.write(confusion_matrix(y_test, predictions))

                    st.write("Model training and evaluation complete.")

                    results = pd.DataFrame({
                        "Actual": pd.Series(y_test).reset_index(drop=True),
                        "Predicted": pd.Series(predictions).reset_index(drop=True)
                    })
                    st.subheader("Prediction Results")
                    st.dataframe(results.head(20))
                except Exception as exc:
                    st.error(f"Analysis failed: {exc}")
                    st.stop()
                
                # Download model, make predictions, and show results
                # Further implementation needed based on application requirements.
                
if __name__ == "__main__":
    main()