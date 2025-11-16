# streamlit_app.py
import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="Medibot (External Chatbot)", layout="wide")

# Sidebar (keeps your existing content / branding)
st.sidebar.markdown("<h2 style='color: #ffffff;'>📌 Description</h2>", unsafe_allow_html=True)
st.sidebar.image("utils/ph2.png", use_container_width=True)
st.sidebar.markdown(
    "<p class='sidebar-text'>The LLM Medical Chatbot is an AI-powered assistant designed to provide instant, accurate, and reliable healthcare insights.</p>",
    unsafe_allow_html=True,
)
st.sidebar.markdown("""
### 🔍 About Medibot:
- Uses an external chatbot widget
- Fast integration — no local LLM required
- Data will go to the external agent provider (see note below)
""")

# Option to toggle between external widget and your original code (useful for testing)
use_external = st.sidebar.checkbox("Use external chatbot widget (recommended)", value=True)

if use_external:
    st.title("💬 Medibot — External Chatbot")
    st.markdown("Ask medical-related questions — powered by the external agent widget.")

    # The HTML/JS snippet you supplied. Place it inside a small HTML wrapper.
    widget_html = f"""
    <div id="do-ai-widget-root"></div>
    <script async
      src="https://wsi66hsa4eiamko53x74lvzk.agents.do-ai.run/static/chatbot/widget.js"
      data-agent-id="73fa428f-78c3-11f0-b074-4e013e2ddde4"
      data-chatbot-id="D3PM7drc5b_6KUHsyOCtsJNr_pvjKfe_"
      data-name="Medibot"
    #   data-primary-color="#e0e0e0"
      data-primary-color="#0d1b2a"
    #   data-secondary-color="#0d1b2a"
      data-secondary-color="#e0e0e0"
      data-button-background-color="#0061EB"
      data-starting-message="Hello! How can I help you today?"
      data-logo="/static/chatbot/icons/default-agent.svg">
    </script>
    """

    # Embed the widget. Adjust height as needed.
    components.html(widget_html, height=700, scrolling=True)

    st.caption("If the widget fails to load, check that your host allows external scripts and that the `src` URL is reachable.")
else:
    st.title("💬 Medibot — Local (placeholder)")
    st.info("You chose to run the local chatbot. Re-enable your original Streamlit + LLM code here.")
    st.markdown(
        "To restore your custom bot: paste your previous Streamlit logic (vectorstore, LLM loading, RetrievalQA call, etc.) in this branch."
    )

# ---- Important notes ----
st.markdown("---")
st.markdown(
    "**Privacy & Security — READ:** The embedded widget loads and executes an external script from a third-party host. "
    "User messages may be routed to that provider. Make sure this is acceptable for your use-case and complies with your org's data policy."
)
