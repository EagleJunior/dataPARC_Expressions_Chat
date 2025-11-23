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
        --dataparc-white: #FFFFFF;
    }
    
    #MainMenu {visibility: hidden;}
    header {visibility: hidden;}
    footer {visibility: hidden;}
    
    .main {
        background-color: var(--dataparc-light-bg);
    }
    
    .header-container {
        background: white;
        padding: 25px;
        border-radius: 12px;
        margin-bottom: 30px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.08);
        border-bottom: 4px solid var(--dataparc-teal);
    }
    
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
    
    [data-testid="column"] {
        display: flex;
        align-items: center;
    }
    </style>
""", unsafe_allow_html=True)

st.markdown('<div class="header-container">', unsafe_allow_html=True)

# Branded header with logo
logo_exists = os.path.exists("dataparc_rebrand_black.png")

if logo_exists:
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
                    Powered by AI - Industrial Analytics Intelligence
                </p>
                <p style='color: #666; margin: 5px 0 0 0; font-size: 14px;'>
                    Get instant help with expressions, functions, and best practices
                </p>
            </div>
        """, unsafe_allow_html=True)
else:
    st.markdown("""
        <div style='padding-top: 10px;'>
            <h1 style='color: #1E3A5F; margin: 0; font-size: 36px; font-weight: 700;'>
                dataPARC Expressions Assistant
            </h1>
            <p style='color: #5DD9D1; margin: 8px 0 0 0; font-size: 16px; font-weight: 500;'>
                Powered by AI - Industrial Analytics Intelligence
            </p>
            <p style='color: #666; margin: 5px 0 0 0; font-size: 14px;'>
                Get instant help with expressions, functions, and best practices
            </p>
        </div>
    """, unsafe_allow_html=True)

st.markdown("<hr style='margin: 20px 0; border: none; border-top: 2px solid #5DD9D1;'>", unsafe_allow_html=True)

if "welcomed" not in st.session_state:
    with st.chat_message("assistant", avatar="🔷"):
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

try:
    client = Anthropic(api_key=st.secrets["CLAUDE_API_KEY"])
except KeyError:
    st.error("Claude API key not configured.")
    st.stop()

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    avatar = "🔷" if message["role"] == "assistant" else "👤"
    with st.chat_message(message["role"], avatar=avatar):
        st.markdown(message["content"])

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

with st.sidebar:
    if logo_exists:
        st.image("dataparc_rebrand_black.png", width=150)
        st.markdown("---")
    
    st.markdown("### About")
    st.markdown("""
    This AI assistant helps dataPARC users with:
    - Expression syntax
    - Function documentation
    - Troubleshooting
    - Best practices
    """)
    
    st.markdown("---")
    
    if st.button("Clear Chat History"):
        st.session_state.messages = []
        st.session_state.welcomed = False
        st.rerun()
    
    st.markdown("---")
    
    st.markdown("""
    <div style='text-align: center; padding: 20px 0;'>
        <p style='color: rgba(255,255,255,0.6); font-size: 12px; margin: 0;'>
            Secure and Private
        </p>
        <p style='color: rgba(255,255,255,0.6); font-size: 12px; margin: 5px 0 0 0;'>
            Powered by Claude AI
        </p>
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")
st.markdown("""
    <div style='text-align: center; color: #666; font-size: 13px; padding: 10px 0;'>
        <p style='margin: 0;'>
            Need more help? Contact 
            <a href='https://www.dataparc.com/support' target='_blank' style='color: #5DD9D1;'>dataPARC Support</a>
        </p>
    </div>
""", unsafe_allow_html=True)
