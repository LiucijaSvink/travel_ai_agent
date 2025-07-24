import os
from datetime import date, timedelta

import streamlit as st

# Utils and agent functions (adjust import paths if needed)
from utils.utils import get_api_key
from agents.supervisor import run_supervisor_graph  # assumed main entrypoint

# Set environment variables for API keys and endpoints
os.environ["OPENAI_API_KEY"] = get_api_key("OPENAI_API_KEY")
os.environ["TAVILY_API_KEY"] = get_api_key("TAVILY_API_KEY")
os.environ["LANGSMITH_API_KEY"] = get_api_key("LANGSMITH_API_KEY")
os.environ["LANGCHAIN_ENDPOINT"] = "https://api.smith.langchain.com"
os.environ["LANGSMITH_PROJECT"] = "AI_travel_planning_agent"
os.environ["LANGCHAIN_TRACING_V2"] = "true"

# Default travel dates
today = date.today()
default_start = today
default_end = today + timedelta(days=5)

# Initialize Streamlit session state variables
if "state" not in st.session_state:
    st.session_state.state = None
if "messages" not in st.session_state:
    st.session_state.messages = []
if "show_chat" not in st.session_state:
    st.session_state.show_chat = False
if "prior_msgs" not in st.session_state:
    st.session_state.prior_msgs = []

# App Title and Description
st.title("✈️ AI-Powered Travel Planning Agent")

st.markdown("""
### Agent Purpose
The Travel Assistant helps users efficiently plan personalized trips by supporting early-stage travel preference extraction and personalized planning.

---

### Capabilities
- Understand natural language and extract travel preferences (origin, destination, travel dates).  
- Find top tourist attractions and experiences.  
- Recommend accommodations based on location and travel time.  
- Generate personalized day-by-day itineraries.  
- Answer general travel questions (packing, visa, customs).

Ideal for travelers who want curated suggestions without planning stress.

---

### Get Started
Please fill in your travel preferences below.
""")

# --- Travel Preferences Form ---
with st.form("travel_form"):
    origin = st.text_input("From")
    destination = st.text_input("To")
    start_date = st.date_input("Start Date", value=default_start)
    end_date = st.date_input("End Date", value=default_end)
    submit = st.form_submit_button("Submit Preferences")

if submit:
    combined_input = f"I want to travel from {origin} to {destination}, starting on {start_date} and returning by {end_date}."
    st.session_state.messages.append(("user", combined_input))
    st.session_state.prior_msgs = []  # reset prior messages for new session

    with st.spinner("Analyzing your preferences..."):
        response = run_supervisor_graph(
            user_message=combined_input,
            thread_id="0",
            prior_messages=st.session_state.prior_msgs,
        )
        st.session_state.prior_msgs = response["messages"]

    st.session_state.messages.append(("agent", response["messages"][-1].content))
    st.session_state.show_chat = True

# --- Chat Window ---
if st.session_state.show_chat:
    for sender, msg in st.session_state.messages:
        if sender == "user":
            st.markdown(f"**You:** {msg}")
        else:
            st.markdown(f"**Agent:** {msg}")

    user_input = st.text_input("Send a message", key="chat_input")
    if st.button("Send", key="send_button"):
        if user_input.strip():
            st.session_state.messages.append(("user", user_input))

            with st.spinner("Assistant is thinking..."):
                response = run_supervisor_graph(
                    user_message=user_input,
                    thread_id="0",
                    prior_messages=st.session_state.prior_msgs,
                )
                st.session_state.prior_msgs = response["messages"]

            st.session_state.messages.append(("agent", response["messages"][-1].content))
            st.rerun()
