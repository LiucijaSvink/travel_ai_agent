import streamlit as st

def get_api_key(key_name: str = "OPEN_API_KEY") -> str:
    """
    Retrieve an API key from Streamlit secrets.
    """
    api_key = st.secrets[key_name]
    return api_key