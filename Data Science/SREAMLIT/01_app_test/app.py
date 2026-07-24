import streamlit as st
import numpy as np
import pandas as pd
# (numpy and pandas not required in this simple app)

# Adding Title and Text
st.title("Hello Streamlit!")
st.write("Welcome to Streamlit in VS Code.")

# take user input
my_class = st.text_input("Enter your Class name")

number = st.number_input("Enter your number", min_value=0, max_value=100, step=1)

slider = st.slider("select your value", min_value=0, max_value=100, step=1)

# Adding button to submit the input
if st.button("Submit"):
    st.write('You entered Class name:', my_class)
    st.write('You entered number:', number)
    st.write('You selected value:', slider)
else:
    st.write("Please enter your details and click Submit.")

# Add a radio button to select an option
option = st.radio("Select an option", ("Option 1", "Option 2", "Option 3")) 

# Add a checkbox to select multiple options
checkbox1 = st.checkbox("Checkbox 1")
checkbox2 = st.checkbox("Checkbox 2")

# Add dropdown menu to select an option
dropdown = st.selectbox("Select an option from dropdown", ("Dropdown Option 1", "Dropdown Option 2", "Dropdown Option 3"))  

# Adding sidebar with a slider
st.sidebar.title("Sidebar") 
sidebar_slider = st.sidebar.slider("Adjust the slider", min_value=0, max_value=100, step=1)

# Adding chhose file uploader
uploaded_file = st.file_uploader("Choose a file")  


# Create a line plot
# Plotting
data = pd.DataFrame({
    'first column': list(range(1, 11)),
    'second column': np.arange(number, number + 10)
})

st.line_chart(data)