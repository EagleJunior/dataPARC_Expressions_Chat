import streamlit as st
from anthropic import Anthropic

st.set_page_config(
    page_title="dataPARC Expressions Assistant",
    page_icon="dataparc_rebrand_black.png",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Custom CSS matching dataPARC branding
st.markdown("""
    <style>
    /* dataPARC Brand Colors */
    :root {
        --dataparc-teal: #5DD9D1;
        --dataparc-dark: #1E3A5F;
        --dataparc-light-bg: #F7F9FC;
        --dataparc-white: #FFFFFF;
    }
    
    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    header {visibility: hidden;}
    footer {visibility: hidden;}
    
    /* Main container background */
    .main {
        background-color: var(--dataparc-light-bg);
    }
    
    /* Header container */
    .header-container {
        background: white;
        padding: 25px;
        border-radius: 12px;
        margin-bottom: 30px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.08);
        border-bottom: 4px solid var(--dataparc-teal);
    }
    
    /* Chat messages */
    .stChatMessage {
        background-color: white;
        border-radius: 12px;
        padding: 20px;
        margin: 15px 0;
        box-shadow: 0 2px 8px rgba(0,0,0,0.08);
        border-left: 4px solid var(--dataparc-teal);
    }
    
    /* User message special styling */
    [data-testid="stChatMessage"]:has([data-testid="chatAvatarIcon-user"]) {
        border-left-color: var(--dataparc-dark);
        background: linear-gradient(to right, #f8f9fa 0%, white 100%);
    }
    
    /* Chat input area */
    .stChatInputContainer {
        border-top: 3px solid var(--dataparc-teal);
        padding-top: 20px;
        background-color: white;
    }
    
    /* Buttons */
    .stButton button {
        background: linear-gradient(135deg, var(--dataparc-teal) 0%, #4ECDC4 100%);
        color: var(--dataparc-dark);
        border-radius: 8px;
        border: none;
        padding: 12px 28px;
        font-weight: 600;
        font-size: 15px;
        transition: all 0.3s ease;
        box-shadow: 0 2px 4px rgba(93,217,209,0.3);
    }
    
    .stButton button:hover {
        background: linear-gradient(135deg, #4ECDC4 0%, #45C4BC 100%);
        box-shadow: 0 4px 8px rgba(93,217,209,0.4);
        transform: translateY(-2px);
    }
    
    /* Sidebar styling */
    [data-testid="stSidebar"] {
        background-color: var(--dataparc-dark);
    }
    
    [data-testid="stSidebar"] h1, 
    [data-testid="stSidebar"] h2, 
    [data-testid="stSidebar"] h3 {
        color: white;
    }
    
    [data-testid="stSidebar"] p {
        color: rgba(255,255,255,0.85);
    }
    
    /* Loading spinner */
    .stSpinner > div {
        border-top-color: var(--dataparc-teal) !important;
    }
    
    /* Column alignment */
    [data-testid="column"] {
        display: flex;
        align-items: center;
    }
    </style>
""", unsafe_allow_html=True)

# Header container wrapper
st.markdown('<div class="header-container">', unsafe_allow_html=True)

# Branded header with logo
col1, col2 = st.columns([1, 4])
with col1:
    st.image("dataparc_rebrand_black.png", width=120)
with col2:
    st.markdown("""
        <div style='padding-top: 10px;'>
            <h1 style='color: #1E3A5F; margin: 0; font-size: 32px; font-weight: 700;'>
                Expressions Assistant
            </h1>
            <p style='color: #5DD9D1; margin: 5px 0 0 0; font-size: 16px; font-weight: 500;'>
                Powered by AI • Industrial Analytics Intelligence
            </p>
            <p style='color: #666; margin: 5px 0 0 0; font-size: 14px;'>
                Get instant help with expressions, functions, and best practices
            </p>
        </div>
    """, unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

# Welcome message (only show on first load)
if "welcomed" not in st.session_state:
    with st.chat_message("assistant", avatar="🔷"):
        st.markdown("""
        👋 **Welcome to the dataPARC Expressions Assistant!**
        
        I'm here to help you with:
        - ✅ **Expression syntax** and best practices
        - ✅ **Function references** and examples  
        - ✅ **Troubleshooting** expression errors
        - ✅ **Performance optimization** tips
        
        **Ask me anything about dataPARC expressions!**
        """)
    st.session_state.welcomed = True

# Load knowledge base
@st.cache_data
def load_knowledge():
    try:
        with open('Expressions RAG.txt', 'r', encoding='utf-8') as f:
            expressions_rag = f.read()
        with open('Expressions_Manual.txt', 'r', encoding='utf-8') as f:
            expressions_manual = f.read()
        with open('Function List.txt', 'r', encoding='utf-8') as f:
            function_list = f.read()
        with open('SuperPrompt_2.txt', 'r', encoding='utf-8') as f:
            system_prompt = f.read()
        return expressions_rag, expressions_manual, function_list, system_prompt
    except FileNotFoundError as e:
        st.error(f"Missing file: {e.filename}")
        st.stop()

expressions_rag, expressions_manual, function_list, system_prompt = load_knowledge()

knowledge_base = f"""
EXPRESSIONS RAG:
{expressions_rag}

EXPRESSIONS MANUAL:
{expressions_manual}

FUNCTION LIST:
{function_list}
"""

# Initialize Claude
try:
    client = Anthropic(api_key=st.secrets["CLAUDE_API_KEY"])
except KeyError:
    st.error("⚠️ Claude API key not configured.")
    st.stop()

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat history
for message in st.session_state.messages:
    avatar = "🔷" if message["role"] == "assistant" else "👤"
    with st.chat_message(message["role"], avatar=avatar):
        st.markdown(message["content"])

# Chat input
user_input = st.chat_input("Ask about dataPARC expressions...")

if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user", avatar="👤"):
        st.markdown(user_input)
    
    with st.chat_message("assistant", avatar="🔷"):
        with st.spinner("Analyzing..."):
            try:
                claude_messages = []
                for msg in st.session_state.messages:
                    claude_messages.append({
                        "role": msg["role"],
                        "content": msg["content"]
                    })
                
                response = client.messages.create(
                    model="claude-sonnet-4-5-20250929",
                    max_tokens=2048,
                    system=[
                        {
                            "type": "text",
                            "text": system_prompt,
                            "cache_control": {"type": "ephemeral"}
                        },
                        {
                            "type": "te
