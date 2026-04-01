# streamlit_app.py
import streamlit as st
import requests

# ==========================================
# CONFIGURATION & THEME
# ==========================================
st.set_page_config(page_title="Medibot", layout="wide")

# Injecting custom CSS to match your requested theme colors
st.markdown("""
<style>
    /* Main App Background (Primary Color) */
    .stApp {
        background-color: #0d1b2a;
    }
    
    /* Sidebar Background (Slightly darker for contrast) */
    [data-testid="stSidebar"] {
        background-color: #08111a;
    }
    
    /* Base Text Color (Secondary Color) */
    .stApp, p, h1, h2, h3, h4, h5, h6, li {
        color: #e0e0e0 !important;
    }
    
    /* Chat Input Focus Ring (Button/Accent Color) */
    .stChatInputContainer:focus-within {
        border-color: #0061EB !important;
        box-shadow: 0 0 0 1px #0061EB !important;
    }
    
    /* Hide the default top header bar */
    [data-testid="stHeader"] {
        background-color: transparent;
    }
</style>
""", unsafe_allow_html=True)

# ==========================================
# DIGITAL OCEAN AGENT API SETTINGS
# ==========================================
API_KEY = st.secrets["API_KEY"]
AGENT_URL = st.secrets["AGENT_URL"]
API_ENDPOINT = f"{AGENT_URL}/api/v1/chat/completions"

# ==========================================
# SIDEBAR
# ==========================================
st.sidebar.markdown("<h2>📌 Description</h2>", unsafe_allow_html=True)
# st.sidebar.image("utils/ph2.png", use_container_width=True) # Uncomment if you have the image
st.sidebar.markdown(
    "<p>The Medibot Assistant is an AI-powered clinical assistant designed to systematically gather your symptoms and provide a preliminary diagnostic assessment.</p>",
    unsafe_allow_html=True,
)
st.sidebar.markdown("""
### 🔍 About Medibot:
- Fast, secure native chat interface
- Powered by DigitalOcean AI
- Strictly focused on medical triage
""")

st.sidebar.markdown("---")
st.sidebar.markdown(
    "**Privacy & Security:** User messages are processed securely. Please do not share sensitive personally identifiable information (PII) beyond your medical symptoms."
)

# ==========================================
# MAIN CHAT INTERFACE
# ==========================================
st.title("💬 Medibot — Diagnostic Assistant")

# Initialize chat history with the required first message
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Please state your symptoms."}
    ]

# Render previous chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# React to user input
if prompt := st.chat_input("E.g., I have a sharp headache that started 2 days ago..."):
    
    # 1. Display user's message
    st.chat_message("user").markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    # 2. Display assistant's response container with a loading state
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        message_placeholder.markdown("Analyzing symptoms...")
        
        # Format the conversation history for the OpenAI-compatible DO endpoint
        # Exclude the very first hardcoded prompt if you only want to send user data, 
        # or send the whole array to maintain context.
        api_messages = [{"role": m["role"], "content": m["content"]} for m in st.session_state.messages]
        
        headers = {
            "Authorization": f"Bearer {API_KEY}", 
            "Content-Type": "application/json"
        }
        
        payload = {
            "messages": api_messages
        }
        
        try:
            # Hit the DigitalOcean Agent API
            response = requests.post(API_ENDPOINT, json=payload, headers=headers)
            response.raise_for_status() # Raise an error for bad status codes
            
            # Parse the response (OpenAI chat completion format)
            data = response.json()
            bot_reply = data["choices"][0]["message"]["content"]
            
        except requests.exceptions.RequestException as e:
            bot_reply = f"**Connection Error:** Could not reach the DigitalOcean Agent. Please check your API key or network connection. \n\n`{e}`"
        except KeyError:
            bot_reply = "**Data Error:** The agent returned an unexpected data format."

        # Update the placeholder with the final response
        message_placeholder.markdown(bot_reply)
    
    # 3. Save assistant message to history
    st.session_state.messages.append({"role": "assistant", "content": bot_reply})