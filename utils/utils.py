import os
import streamlit as st

def get_api_key(key_name: str = "OPEN_API_KEY") -> str:
    """
    Try to retrieve an API key from environment variables.
    Fallback to Streamlit secrets.
    """
    api_key = os.getenv(key_name)
    if not api_key:
        try:
            api_key = st.secrets[key_name]
        except Exception:
            raise ValueError(f"Missing {key_name} in both environment and st.secrets.")
    return api_key