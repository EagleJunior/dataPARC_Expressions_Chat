import streamlit as st
from anthropic import Anthropic

st.set_page_config(
    page_title="dataPARC Expressions Assistant",
    page_icon="💬",
    layout="centered"
)

st.title("💬 dataPARC Expressions Assistant")
st.caption("Ask me anything about dataPARC expressions and functions")

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
    st.error("⚠️ Claude API key not configured. Please add it in Streamlit secrets.")
    st.stop()

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

user_input = st.chat_input("Ask about dataPARC expressions...")

if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)
    
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
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
    st.header("ℹ️ About")
    st.write("AI assistant for dataPARC expressions and functions")
    
    if st.button("Clear Chat"):
        st.session_state.messages = []
        st.rerun()
