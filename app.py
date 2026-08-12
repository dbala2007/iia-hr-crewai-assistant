import os
import streamlit as st
from dotenv import load_dotenv
from crew_workflow import run_hr_crew

load_dotenv()

st.set_page_config(page_title="IIA HR Policy Assistant", layout="wide")

# Retrieve app password from environment variables
APP_PASSWORD = os.getenv("APP_PASSWORD", "defaultpass")

# --- Simple Password Authentication Gate ---
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

if not st.session_state.authenticated:
    st.title("🔒 Security Access Required")
    user_input_pass = st.text_input("Enter Password:", type="password")
    if st.button("Login"):
        if user_input_pass == APP_PASSWORD:
            st.session_state.authenticated = True
            st.rerun()
        else:
            st.error("Incorrect password. Access denied.")
    st.stop()

# --- Main Streamlit Application ---
st.title("🤖 IIA HR Policy & Web Search Multi-Agent Crew")
st.markdown("Query the **IIA HR Policy Document** alongside real-time **Web Search results**.")

# User Query Input Box
user_query = st.text_input("Enter your query:", placeholder="e.g., What are the rules regarding probation period and leave policy?")

if st.button("Submit Query") and user_query:
    with st.spinner("CrewAI Agents are working on your query..."):
        # Execute the multi-agent workflow
        results = run_hr_crew(user_query)
        
        # Display side-by-side responses
        col1, col2 = st.columns(2)
        
        with col1:
            st.header("📄 HR Assistant (RAG Output)")
            st.write(results["hr_response"])
            
        with col2:
            st.header("🌐 Web Search Assistant Output")
            st.write(results["web_response"])
            
        # Log notification
        st.success(f"Status: {results['sheet_status']}")

# Sidebar Info
st.sidebar.title("App Guardrails & Config")
st.sidebar.info(f"""
- **Max RPM:** {os.getenv('MAX_RPM', '10')}
- **Max Iterations:** {os.getenv('MAX_ITER', '3')}
- **Execution Timeout:** {os.getenv('MAX_EXECUTION_TIME', '120')}s
""")

if st.sidebar.button("Logout"):
    st.session_state.authenticated = False
    st.rerun()