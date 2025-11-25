import streamlit as st
from anthropic import Anthropic
import os
import base64
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime

# Helper function to convert image to base64
def get_base64_image(image_path):
    try:
        with open(image_path, "rb") as img_file:
            return base64.b64encode(img_file.read()).decode()
    except:
        return ""

# Format conversation for email
def format_conversation(messages):
    """Format conversation messages for email"""
    if not messages:
        return "No conversation included"
    
    formatted = []
    for i, msg in enumerate(messages, 1):
        role = "USER" if msg["role"] == "user" else "ASSISTANT"
        separator = "-" * 60
        formatted.append(f"\n{separator}\nMessage {i} - {role}\n{separator}\n{msg['content']}\n")
    
    return "\n".join(formatted)

# Gmail SMTP email function
def send_feedback_email(feedback, company, conversation):
    """Send feedback via Gmail SMTP"""
    try:
        # Get credentials from secrets
        sender_email = st.secrets["FEEDBACK_EMAIL"]
        sender_password = st.secrets["FEEDBACK_PASSWORD"]
        receiver_email = st.secrets["DEVELOPER_EMAIL"]
        
        # Create message
        msg = MIMEMultipart()
        msg['From'] = sender_email
        msg['To'] = receiver_email
        msg['Subject'] = f"dataPARC Expressions Feedback - {company if company else 'Anonymous'}"
        
        # Email body
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S UTC')
        body = f"""
New Feedback Received from dataPARC Expressions Assistant
{'='*70}

Time: {timestamp}
Company: {company if company else 'Not provided'}

FEEDBACK:
{'-'*70}
{feedback}

{'='*70}
CONVERSATION CONTEXT:
{'='*70}

{format_conversation(conversation) if conversation else 'Not included'}

{'='*70}
Sent from dataPARC Expressions Chat Assistant
https://dataparc.com
        """
        
        msg.attach(MIMEText(body, 'plain'))
        
        # Send via Gmail SMTP
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(sender_email, sender_password)
        server.send_message(msg)
        server.quit()
        
        return True
        
    except Exception as e:
        st.error(f"Failed to send feedback: {str(e)}")
        return False

# Page config
st.set_page_config(
    page_title="dataPARC Expressions Assistant",
    page_icon="dataparc_rebrand_black.png",
    layout="centered",
    initial_sidebar_state="expanded"
)

# CSS styling
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
        
        .stChatMessage {
            background-color: #2d2d2d !important;
            border-left-color: var(--dataparc-teal) !important;
            color: #ffffff !important;
        }
        
        [data-testid="stChatMessage"]:has([data-testid="chatAvatarIcon-user"]) {
            background: linear-gradient(to right, #252525 0%, #2d2d2d 100%) !important;
            border-left-color: var(--dataparc-teal) !important;
        }
        
        h1, h2, h3, p, div {
            color: #ffffff !important;
        }
        
        strong {
            color: #ffffff !important;
        }
        
        .stMarkdown, .stCaption {
            color: #b0b0b0 !important;
        }
        
        .stChatInputContainer {
            background-color: #2d2d2d !important;
            border-top-color: var(--dataparc-teal) !important;
        }
        
        hr {
            border-color: #404040 !important;
        }
        
        a {
            color: var(--dataparc-teal) !important;
        }
    }
    
    /* Light mode styles */
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
    
    .stChatMessage img {
        border-radius: 50%;
        box-shadow: 0 2px 4px rgba(0,0,0,0.2);
    }
    
    /* Feedback button styling - Extra prominent */
    div[data-testid="stSidebar"] button[key="feedback_button"] {
        background: linear-gradient(135deg, #FF6B6B 0%, #FF8E53 100%) !important;
        color: white !important;
        border: 2px solid #FF8E53 !important;
        font-weight: 700 !important;
        font-size: 16px !important;
    }
    
    div[data-testid="stSidebar"] button[key="feedback_button"]:hover {
        background: linear-gradient(135deg, #FF8E53 0%, #FFA07A 100%) !important;
        border: 2px solid #FFA07A !important;
        box-shadow: 0 4px 12px rgba(255, 107, 107, 0.4) !important;
        transform: translateY(-2px) !important;
    }
    
    /* Alternative selector for feedback button */
    .feedback-button button {
        background: linear-gradient(135deg, #FF6B6B 0%, #FF8E53 100%) !important;
        color: white !important;
        border: 2px solid #FF8E53 !important;
    }
    
    .feedback-button button:hover {
        background: linear-gradient(135deg, #FF8E53 0%, #FFA07A 100%) !important;
    }
    </style>
""", unsafe_allow_html=True)

# Check for logo and avatar files
logo_black_exists = os.path.exists("dataparc_rebrand_black.png")
logo_white_exists = os.path.exists("dataparc_rebrand_white.png")
avatar_exists = os.path.exists("dataparc_rebrand_social_blue.png")

# Set assistant avatar
assistant_avatar = "dataparc_rebrand_social_blue.png" if avatar_exists else "🔷"

# Header with adaptive logo
if logo_black_exists and logo_white_exists:
    col1, col2 = st.columns([1, 5])
    with col1:
        st.markdown(f"""
            <style>
            .adaptive-logo-black {{
                display: block;
                width: 100px;
            }}
            .adaptive-logo-white {{
                display: none;
                width: 100px;
            }}
            @media (prefers-color-scheme: dark) {{
                .adaptive-logo-black {{
                    display: none !important;
                }}
                .adaptive-logo-white {{
                    display: block !important;
                }}
            }}
            </style>
            <img src="data:image/png;base64,{get_base64_image('dataparc_rebrand_black.png')}" class="adaptive-logo-black" alt="dataPARC">
            <img src="data:image/png;base64,{get_base64_image('dataparc_rebrand_white.png')}" class="adaptive-logo-white" alt="dataPARC">
        """, unsafe_allow_html=True)
    with col2:
        st.title("Expressions Assistant")
        st.markdown("**Powered by AI - Industrial Analytics Intelligence**")
        st.caption("Get instant help with expressions, functions, and best practices")
elif logo_black_exists:
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

# Load knowledge base
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

# Build knowledge base
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

# Initialize feedback modal state
if "show_feedback" not in st.session_state:
    st.session_state.show_feedback = False

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

# Feedback Modal
if st.session_state.show_feedback:
    st.markdown("---")
    st.markdown("### 📝 Send Feedback")
    st.write("Help us improve the dataPARC Expressions Assistant!")
    
    with st.form("feedback_form", clear_on_submit=False):
        feedback_text = st.text_area(
            "Your Feedback *",
            placeholder="Tell us what you think, report issues, or suggest improvements...",
            height=150,
            key="feedback_text"
        )
        
        company_name = st.text_input(
            "Company Name (optional)",
            placeholder="Your company or organization",
            key="company_name"
        )
        
        include_conversation = st.checkbox(
            "📎 Include current conversation in feedback",
            value=False,
            help="This helps us understand the context of your feedback",
            key="include_conv"
        )
        
        if include_conversation and st.session_state.messages:
            with st.expander("Preview conversation to be included"):
                st.caption(f"{len(st.session_state.messages)} messages will be included")
                for msg in st.session_state.messages[-3:]:  # Show last 3 messages as preview
                    role = "You" if msg["role"] == "user" else "Assistant"
                    st.text(f"{role}: {msg['content'][:100]}...")
        
        col1, col2 = st.columns(2)
        with col1:
            cancel = st.form_submit_button("Cancel", use_container_width=True)
        with col2:
            submit = st.form_submit_button("Send Feedback", type="primary", use_container_width=True)
        
        if submit:
            if feedback_text.strip():
                with st.spinner("Sending feedback..."):
                    success = send_feedback_email(
                        feedback=feedback_text,
                        company=company_name if company_name.strip() else None,
                        conversation=st.session_state.messages if include_conversation else None
                    )
                
                if success:
                    st.success("✅ Feedback sent successfully! Thank you for helping us improve.")
                    st.balloons()
                    st.session_state.show_feedback = False
                    # Clear form
                    st.session_state.pop("feedback_text", None)
                    st.session_state.pop("company_name", None)
                    st.session_state.pop("include_conv", None)
                    st.rerun()
                else:
                    st.error("❌ Failed to send feedback. Please try again or contact support.")
            else:
                st.error("Please enter your feedback before submitting.")
        
        if cancel:
            st.session_state.show_feedback = False
            st.rerun()

# Sidebar
with st.sidebar:
    if logo_white_exists:
        st.image("dataparc_rebrand_white.png", width=150)
    elif logo_black_exists:
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
    
    st.caption("🔒 Secure and Private")
    st.caption("Powered by Claude AI")

# Action buttons above footer
st.divider()

col1, col2 = st.columns(2)

with col1:
    if st.button("🗑️ Clear Chat History", use_container_width=True, key="clear_history"):
        st.session_state.messages = []
        st.session_state.welcomed = False
        st.rerun()

with col2:
    if st.button("📝 Send Feedback", use_container_width=True, key="feedback_button", type="primary"):
        st.session_state.show_feedback = True
        st.rerun()

# Custom CSS for orange feedback button
st.markdown("""
    <style>
    /* Force orange color on feedback button */
    button[kind="primary"] {
        background: linear-gradient(135deg, #FF6B6B 0%, #FF8E53 100%) !important;
        border-color: #FF8E53 !important;
        color: white !important;
    }
    button[kind="primary"]:hover {
        background: linear-gradient(135deg, #FF8E53 0%, #FFA07A 100%) !important;
        box-shadow: 0 4px 12px rgba(255, 107, 107, 0.4) !important;
    }
    </style>
""", unsafe_allow_html=True)

# Footer
st.divider()
st.markdown(
    "Need more help? Contact [dataPARC Support](https://www.dataparc.com/support)",
    unsafe_allow_html=True
)
