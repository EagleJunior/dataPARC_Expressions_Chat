import streamlit as st
from anthropic import Anthropic
import os

st.set_page_config(
    page_title="dataPARC Expressions Assistant",
    page_icon="dataparc_rebrand_black.png",
    layout="centered",
    initial_sidebar_state="collapsed"
)

st.markdown("""
    <style>
    :root {
        --dataparc-teal: #5DD9D1;
        --dataparc-dark: #1E3A5F;
        --dataparc-light-bg: #F7F9FC;
    }
    
    #MainMenu {visibility: hidden;}
    header {visibility: hidden;}
    footer {visibility: hidden;}
    
    .main {
        background-color: var(--dataparc-light-bg);
    }
    
    /* Dark mode adjustments */
    @media (prefers-color-scheme: dark) {
        .main {
            background-color: #1a1a1a;
        }
        
        /* Make chat messages visible in dark mode */
        .stChatMessage {
            background-color: #2d2d2d !important;
            border-left-color: var(--dataparc-teal) !important;
            color: #ffffff !important;
        }
        
        /* User messages slightly different shade */
        [data-testid="stChatMessage"]:has([data-testid="chatAvatarIcon-user"]) {
            background: linear-gradient(to right, #252525 0%, #2d2d2d 100%) !important;
            border-left-color: var(--dataparc-teal) !important;
        }
        
        /* Avatar images - add white background circle for visibility */
        .stChatMessage img {
            background-color: white !important;
            padding: 4px !important;
            border: 2px solid var(--dataparc-teal) !important;
        }
        
        /* Title and text */
        h1, h2, h3, p, div {
            color: #ffffff !important;
        }
        
        /* Caption text */
        .stCaption {
            color: #b0b0b0 !important;
        }
        
        /* Input area */
        .stChatInputContainer {
            background-color: #2d2d2d !important;
            border-top-color: var(--dataparc-teal) !important;
        }
        
        /* Dividers */
        hr {
            border-color: #404040 !important;
        }
        
        /* Footer links */
        a {
            color: var(--dataparc-teal) !important;
        }
    }
    
    /* Light mode (existing styles) */
    .stChatMessage {
        background-color: white;
        border-radius: 12px;
        padding: 20px;
        margin: 15px 0;
        box-shadow: 0 2px 8px rgba(0,0,0,0.08);
        border-left: 4px solid var(--dataparc-teal);
    }
    
    [data-testid="stChatMessage"]:has([data-testid="chatAvatarIcon-user"]) {
        border-left-color: var(--dataparc-dark);
        background: linear-gradient(to right, #f8f9fa 0%, white 100%);
    }
    
    .stChatInputContainer {
        border-top: 3px solid var(--dataparc-teal);
        padding-top: 20px;
        background-color: white;
    }
    
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
    
    .stSpinner > div {
        border-top-color: var(--dataparc-teal) !important;
    }
    
    /* Avatar styling - works in both modes */
    .stChatMessage img {
        border-radius: 50%;
        box-shadow: 0 2px 4px rgba(0,0,0,0.2);
    }
    </style>
""", unsafe_allow_html=True)

# Check for logo and avatar files
logo_exists = os.path.exists("dataparc_rebrand_black.png")
avatar_exists = os.path.exists("dataparc_rebrand_social_blue.png")

# Set assistant avatar
assistant_avatar = "dataparc_rebrand_social_blue.png" if avatar_exists else "🔷"

# Simple header with logo
if logo_exists:
    col1, col2 = st.columns([1, 5])
    with col1:
        st.image("dataparc_rebrand_black.png", width=100)
    with col2:
        st.title("Expressions Assistant")
        st.markdown("**Powered by AI - Industrial Analytics Intelligence**")
        st.caption("Get instant help with expressions, functions, and best practices")
else:
    st.title("dataPARC Expressions Assistant")
    st.markdown("**Powered by AI - Industrial Analytics Intelligence**")
    st.caption("Get instant help with expressions, functions, and best practices")

st.divider()

# Welcome message
if "welcomed" not in st.session_state:
    with st.chat_message("assistant", avatar=assistant_avatar):
        st.markdown("""
        Welcome to the dataPARC Expressions Assistant!
        
        I can help you with:
        - Expression syntax and best practices
        - Function references and examples  
        - Troubleshooting expression errors
        - Performance optimization tips
        
        Ask me anything about dataPARC expressions!
        """)
    st.session_state.welcomed = True

# Load knowledge base - UPDATED WITH COMMON PITFALLS
@st.cache_data
def load_knowledge():
    try:
        with open('Expressions_Complete.txt', 'r', encoding='utf-8') as f:
            expressions_complete = f.read()
        with open('Function List.txt', 'r', encoding='utf-8') as f:
            function_list = f.read()
        with open('SuperPrompt_2.txt', 'r', encoding='utf-8') as f:
            system_prompt = f.read()
        with open('Common_pitfalls.txt', 'r', encoding='utf-8') as f:
            common_pitfalls = f.read()
        return expressions_complete, function_list, system_prompt, common_pitfalls
    except FileNotFoundError as e:
        st.error(f"Missing file: {e.filename}")
        st.stop()

expressions_complete, function_list, system_prompt, common_pitfalls = load_knowledge()

# Build knowledge base with all documents
knowledge_base = f"""
COMPLETE EXPRESSIONS REFERENCE:
{expressions_complete}

FUNCTION LIST:
{function_list}

COMMON PITFALLS TO AVOID:
{common_pitfalls}
"""

# Initialize Claude
try:
    client = Anthropic(api_key=st.secrets["CLAUDE_API_KEY"])
except KeyError:
    st.error("Claude API key not configured.")
    st.stop()

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat history
for message in st.session_state.messages:
    avatar = assistant_avatar if message["role"] == "assistant" else "👤"
    with st.chat_message(message["role"], avatar=avatar):
        st.markdown(message["content"])

# Chat input
user_input = st.chat_input("Ask about dataPARC expressions...")

if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user", avatar="👤"):
        st.markdown(user_input)
    
    with st.chat_message("assistant", avatar=assistant_avatar):
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
                            "type": "text",
                            "text": knowledge_base,
                            "cache_control": {"type": "ephemeral"}
                        }
                    ],
                    messages=claude_messages
                )
                
                answer = response.content[0].text
                st.markdown(answer)
                st.session_state.messages.append({"role": "assistant", "content": answer})
                
            except Exception as e:
                st.error(f"Error: {str(e)}")

# Sidebar
with st.sidebar:
    if logo_exists:
        st.image("dataparc_rebrand_black.png", width=150)
        st.divider()
    
    st.subheader("About")
    st.markdown("""
    This AI assistant helps dataPARC users with:
    - Expression syntax
    - Function documentation
    - Troubleshooting
    - Best practices
    """)
    
    st.divider()
    
    if st.button("Clear Chat History"):
        st.session_state.messages = []
        st.session_state.welcomed = False
        st.rerun()
    
    st.divider()
    
    st.caption("🔒 Secure and Private")
    st.caption("Powered by Claude AI")

# Footer
st.divider()
st.markdown(
    "Need more help? Contact [dataPARC Support](https://www.dataparc.com/support)",
    unsafe_allow_html=True
)
