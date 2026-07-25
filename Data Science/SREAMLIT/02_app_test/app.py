import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Title and Text
st.title("Data Analysis App")
st.subheader("This is a simple data analysis app using Streamlit.")

# Dataset selection
available_datasets = {
    "Tips": "tips",
    "Iris": "iris",
    "Titanic": "titanic",
}

selected_dataset = st.selectbox(
    "Choose a built-in dataset",
    options=list(available_datasets.keys()),
    index=0,
)

use_uploaded_file = st.button("Upload your own data")

if use_uploaded_file:
    uploaded_file = st.file_uploader("Choose a CSV file", type=["csv"])
    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file)
        st.success("Loaded your uploaded file successfully.")
    else:
        st.info("Please upload a CSV file to continue.")
        st.stop()
else:
    df = sns.load_dataset(available_datasets[selected_dataset])

st.subheader("Dataset Preview")
st.dataframe(df)

# Display basic statistics
st.subheader("Basic Statistics")
st.write("Shape of the dataset:", df.shape)
st.write("Number of missing values in each column:")
st.write(df.isnull().sum())
st.write("Columns in the dataset:", df.columns.tolist())
st.write("Data types of each column:", df.dtypes.tolist())
st.write("Summary statistics of the dataset:")
st.write(df.describe())

# Display plotting options with specific columns X and Y
st.subheader("Plotting Options")

numeric_columns = df.select_dtypes(include=["number"]).columns.tolist()
cat_columns = df.select_dtypes(exclude=["number"]).columns.tolist()

x_axis = st.selectbox("Select X-axis column", options=numeric_columns + cat_columns)
y_axis = st.selectbox("Select Y-axis column", options=numeric_columns)
plot_type = st.selectbox("Choose plot type", ["Scatter", "Line", "Bar", "Histogram"])

if plot_type == "Scatter":
    fig, ax = plt.subplots()
    sns.scatterplot(data=df, x=x_axis, y=y_axis, ax=ax)
    st.pyplot(fig)
elif plot_type == "Line":
    fig, ax = plt.subplots()
    sns.lineplot(data=df, x=x_axis, y=y_axis, ax=ax)
    st.pyplot(fig)
elif plot_type == "Bar":
    fig, ax = plt.subplots()
    sns.barplot(data=df, x=x_axis, y=y_axis, ax=ax)
    st.pyplot(fig)
elif plot_type == "Histogram":
    fig, ax = plt.subplots()
    sns.histplot(data=df, x=y_axis, ax=ax)
    st.pyplot(fig)



# Display correlation matrix
st.subheader("Correlation Matrix")

numeric_df = df.select_dtypes(include=["number"])
if numeric_df.shape[1] > 1:
    correlation_matrix = numeric_df.corr()
    st.dataframe(correlation_matrix)
else:
    st.info("Not enough numeric columns to display a correlation matrix.")



