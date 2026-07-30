import streamlit as st
from langchain_openai import OpenAI
from openai import RateLimitError

st.title('🦜🔗 Quickstart App')
openai_api_key = st.sidebar.text_input('OpenAI API Key')


def generate_response(input_text):
    if not openai_api_key.startswith('sk-'):
        st.warning('Please enter your OpenAI API key!', icon='⚠')
        return

    try:
        llm = OpenAI(temperature=0.7, api_key=openai_api_key)
        response = llm.invoke(input_text)
        st.info(response)
    except RateLimitError:
        st.error('OpenAI quota exceeded or rate limited. Please check your billing plan and try again later.')
    except Exception as e:
        st.error(f'Something went wrong: {e}')


with st.form('my_form'):
    text = st.text_area('Enter text:', '...')
    submitted = st.form_submit_button('Submit')

    if submitted:
        generate_response(text)