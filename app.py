import streamlit as st
import requests
import openai
from dotenv import load_dotenv
import os
import base64
from pathlib import Path

# Configuration
BASE_URL = os.getenv("BACKEND_URL", "http://127.0.0.1:8000")
if os.getenv("PORT"):  # Cloud environment
    BASE_URL = "http://localhost:8000"

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

# Initialize session state
def initialize_session_state():
    """Initialize all session state variables with default values."""
    default_states = {
        "candidate_id": None,
        "chat_history": [],
        "page": "login",
        "candidate_name": "",
        "candidate_email": "",
        "temp_stack": [],
        "experience": {"years": 0, "months": 0},
        "interested_roles": [],
        "interview_started": False,
        "input_counter": 0,
        "history_loaded": False,
        "is_returning_user": False
    }
    
    for key, value in default_states.items():
        if key not in st.session_state:
            st.session_state[key] = value

# Common CSS styles
def load_common_styles():
    """Load common CSS styles used across all pages."""
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;500;700&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Space Grotesk', sans-serif;
        color: white;
        background-color: #0f0f0f;
    }
    
    .stTextInput > div > div > input,
    .stTextArea > div > div > textarea {
        background-color: rgba(255, 255, 255, 0.1) !important;
        border: 1px solid rgba(255, 255, 255, 0.4) !important;
        border-radius: 8px !important;
        color: white !important;
        font-family: 'Space Grotesk', sans-serif !important;
    }
    
    .stTextArea > div > div > textarea:focus,
    .stTextInput > div > div > input:focus {
        border: 1px solid #ff4c4c !important;
        box-shadow: 0 0 10px rgba(255, 76, 76, 0.3) !important;
    }
    
    .stTextArea > div > div > textarea {
        resize: vertical !important;
        min-height: 150px !important;
        background-image: 
            linear-gradient(135deg, transparent 0%, transparent 30%, #ff4c4c 30%, #ff4c4c 32%, transparent 32%, transparent 35%, #ff4c4c 35%, #ff4c4c 37%, transparent 37%, transparent 40%, #ff4c4c 40%, #ff4c4c 42%, transparent 42%) !important;
        background-size: 20px 20px !important;
        background-repeat: no-repeat !important;
        background-position: bottom right !important;
    }
    
    .stButton > button {
        background-color: #ff4c4c !important;
        border: none !important;
        color: white !important;
        padding: 12px 24px !important;
        border-radius: 8px !important;
        font-weight: 600 !important;
        font-family: 'Space Grotesk', sans-serif !important;
        box-shadow: 0 0 15px rgba(255, 76, 76, 0.4) !important;
        transition: all 0.3s ease !important;
    }
    
    .stButton > button:hover {
        background-color: #ff1a1a !important;
        box-shadow: 0 0 25px rgba(255, 76, 76, 0.6) !important;
        transform: translateY(-2px) !important;
    }
    
    .logo-header {
        display: flex;
        justify-content: center;
        align-items: baseline;
        font-size: 2.5em;
        font-weight: 700;
        margin-bottom: 30px;
        gap: 12px;
        flex-wrap: wrap;
        text-align: center;
        max-width: 100%;
        overflow-wrap: break-word;
    }
    
    .brand-text {
        white-space: nowrap;
    }
    
    @media (max-width: 768px) {
        .logo-header {
            font-size: 1.8em !important;
            gap: 6px;
            margin-bottom: 10px !important;
            flex-direction: column;
            align-items: center;
            text-align: center;
            padding: 5px 0 !important;
            position: relative !important;
            z-index: 10;
        }
        .welcome-text {
            display: block;
            margin-bottom: -10px;
        }

        .brand-text {
            display: inline-flex;
            align-items: center;
            justify-content: center;
            gap: 6px;
            flex-wrap: wrap;
        }
        .brand-text img {
            vertical-align: middle;
            transform: none;
            width: 60px !important;
            height: auto !important;
        }
        
        .block-container {
            margin-top: 0px !important;
            padding-top: 2.5rem !important;
        }
        
        .title {
            font-size: 1.8em !important;
        }
                
        .logo-container img {
            width: 108px !important;
        }
    }
    
    @media (max-width: 400px) {
        .logo-header {
            font-size: 1.35em !important;
            margin-bottom: -5px !important;
        }
        
        .title {
            font-size: 1.35em !important;
        }
        
        .brand-text img {
            width: 45px !important;
        }
    }
    
    @media (max-width: 416px) {
        h2 {
            font-size: 1.7em !important;
        }
    }

    @media (max-width: 355px) {
        h3 {
            font-size: 1.5em !important;
        }
        
        div[data-testid="stExpander"] img {
            width: 220px !important;
            height: 120px !important;
        }
    }
    
    .logo-header img {
        height: 80px;
        width: auto;
        box-shadow: none;
        margin-left: 5px;
        border-radius: 0px !important;
        vertical-align: bottom;
    }
    
    .info-container {
        background: rgba(255, 255, 255, 0.1);
        border: 1px solid rgba(255, 255, 255, 0.2);
        padding: 15px;
        border-radius: 8px;
        margin-bottom: 20px;
        font-family: 'Space Grotesk', sans-serif;
    }

    </style>
    """, unsafe_allow_html=True)

# API helper functions
def make_api_request(endpoint, method="GET", json_data=None):
    """Make API request with error handling."""
    try:
        url = f"{BASE_URL}/{endpoint}"
        print(f"🔗 Making {method} request to: {url}")
        
        # Increased timeout for LLM operations and added connection timeout
        if method == "GET":
            response = requests.get(url, timeout=(5, 60))  # (connection_timeout, read_timeout)
        else:
            response = requests.post(url, json=json_data, timeout=(5, 60))
        
        print(f"📊 Response status: {response.status_code}")
        
        if response.status_code == 200:
            return response.json(), None
        else:
            error_msg = response.json().get('detail', 'Unknown error') if response.content else f"HTTP {response.status_code}"
            print(f"❌ API Error: {error_msg}")
            return None, error_msg
    except requests.exceptions.Timeout as e:
        error_msg = f"Request timed out: {str(e)}"
        print(f"⏰ Timeout Error: {error_msg}")
        return None, error_msg
    except requests.exceptions.ConnectionError as e:
        error_msg = f"Connection failed: {str(e)}"
        print(f"🔌 Connection Error: {error_msg}")
        return None, error_msg
    except Exception as e:
        error_msg = str(e)
        print(f"❌ Request Exception: {error_msg}")
        return None, error_msg

def add_to_chat_history(user_message=None, bot_message=None):
    """Add messages to chat history."""
    if user_message:
        st.session_state.chat_history.append(("You", user_message))
    if bot_message:
        st.session_state.chat_history.append(("Rick", bot_message))

# Technology extraction function
def extract_technologies(text):
    """Extract technologies from text using OpenAI."""
    if not text.strip():
        return []
    
    prompt = f"""
    Extract a list of technologies, tools, and frameworks from the following input. Only return a clean Python list. No explanation, no extra text.

    Input: "{text}"

    Output (as a Python list, convert all tech names to standardized full names in title case):
    """

    try:
        response = openai.chat.completions.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}],
            temperature=0,
        )
        answer = response.choices[0].message.content
        tech_list = eval(answer.strip()) if answer.strip().startswith("[") else []
        return sorted(set(tech_list))
    except Exception as e:
        st.error(f"Error extracting technologies: {e}")
        return []

# Audio helper function
def play_audio(audio_file_path):
    """Play audio using HTML5 audio element with base64 encoding for local files."""
    try:
        # Read the audio file and encode to base64
        audio_path = Path(audio_file_path)
        if audio_path.exists():
            audio_bytes = audio_path.read_bytes()
            audio_base64 = base64.b64encode(audio_bytes).decode()
            
            audio_html = f"""
            <audio autoplay style="display: none;">
                <source src="data:audio/mpeg;base64,{audio_base64}" type="audio/mpeg">
                Your browser does not support the audio element.
            </audio>
            <script>
                setTimeout(function() {{
                    var audio = document.querySelector('audio');
                    if (audio) {{
                        audio.play().catch(function(error) {{
                            console.log('Audio play failed:', error);
                        }});
                    }}
                }}, 100);
            </script>
            """
            st.markdown(audio_html, unsafe_allow_html=True)
        else:
            print(f"Audio file not found: {audio_file_path}")
    except Exception as e:
        print(f"Error playing audio: {e}")

# Header component
def render_header():
    """Render common header with logo."""
    try:
        logo_path = Path("techrickal.png")
        if logo_path.exists():
            encoded_logo = base64.b64encode(logo_path.read_bytes()).decode()
            st.markdown(f"""
            <div class='logo-header'>
                <span class="welcome-text">Welcome to </span><span class="brand-text">TechRickal Interviews  <img src="data:image/png;base64,{encoded_logo}" alt="TechRicka Logo"></span>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown("<div class='logo-header'>🤖 TechRickal Interviews</div>", unsafe_allow_html=True)
    except Exception:
        st.markdown("<div class='logo-header'>🤖 TechRickal Interviews</div>", unsafe_allow_html=True)

def login_page():
    """Login/Registration page."""
    load_common_styles()
    
    # Add Rick and Morty theme with Rick's photo
    st.markdown("""
    <style>
    .logo-container {
        display: flex;
        justify-content: center;
        margin-bottom: 20px;
    }

    .logo-container img {
        width: 150px;
    }

    .title {
        text-align: center;
        font-size: 40px;
        margin-top: -10px;
        color: red;
        text-shadow: 2px 2px 4px #000;
    }
    </style>

    <div class="logo-container">
        <img src="https://static.wikia.nocookie.net/rickandmorty/images/d/df/Robot_Rick.png" alt="Rick Logo">
    </div>

    <div class="title">🤖 Interview Chatbot</div>
    """, unsafe_allow_html=True)
    
    render_header()
    name = st.text_input("Name", placeholder="Full Name")
    email = st.text_input("Email", placeholder="you@example.com")
    password = st.text_input("Password", type="password", placeholder="Minimum 6 characters")

    if st.button("Submit"):
        if not all([name, email, password]):
            st.error("Please fill in all fields.")
            return
        
        # Play audio when login button is clicked
        play_audio("woo_vu_luvub_dub_dub.mp3")
        
        # Add a small delay to let audio play
        import time
        time.sleep(1.2)
            
        with st.spinner("Authenticating..."):
            # Try login first
            login_data, login_error = make_api_request("login", "POST", {
                "name": name, "email": email, "password": password
            })
            
            if login_data:
                st.session_state.candidate_id = login_data["candidate_id"]
                st.session_state.candidate_name = login_data["name"]
                st.session_state.candidate_email = login_data["email"]
                
                # Check if tech stack exists
                stack_data, _ = make_api_request(f"tech_stack/{login_data['candidate_id']}")
                if stack_data and stack_data.get("tech_stack"):
                    st.session_state.page = "chat"
                else:
                    st.session_state.page = "tech_stack"
                st.rerun()
            elif login_error == "Invalid Credentials." or "password" in login_error.lower():
                st.error("Invalid credentials.")
            else:
                # Try registration
                reg_data, reg_error = make_api_request("register", "POST", {
                    "name": name, "email": email, "password": password
                })
                
                if reg_data:
                    st.session_state.candidate_id = reg_data["candidate_id"]
                    st.session_state.candidate_name = name
                    st.session_state.candidate_email = email
                    st.session_state.page = "tech_stack"
                    st.success("Registered successfully!")
                    st.rerun()
                else:
                    st.error(f"Registration failed: {reg_error}")

def tech_stack_page():
    """Tech stack input page."""
    load_common_styles()
    st.subheader("🛸 Enter Your Tech Stack")

    stack_input = st.text_input("Describe your tech stack (e.g., I've worked with Python, some React, and a little AWS)")
    st.caption("📌 Press Enter after typing to detect your tech stack.")
    
    extracted_stack = extract_technologies(stack_input) if stack_input else []

    if stack_input: 
        if extracted_stack:
            st.markdown("🔍 **Detected Technologies:**")
            st.write(extracted_stack)
        else:
            st.warning("⚠️ Couldn't detect any technologies. Please revise your input.")

    col1, col2 = st.columns(2)
    with col1:
        years_exp = st.selectbox("Years of Experience", list(range(0, 21)))
    with col2:
        months_exp = st.selectbox("Months of Experience", list(range(0, 12)))

    roles = [
        "Frontend Developer", "Backend Developer", "Full Stack Developer",
        "DevOps Engineer", "Machine Learning Engineer"
    ]
    selected_roles = st.multiselect("What roles are you interested in?", roles)
    
    if st.button("Submit Tech Stack"):
        if not extracted_stack:
            st.warning("🚫 Please enter a valid tech stack.")
        elif not selected_roles:
            st.warning("🚫 Please select at least one role.")
        else:
            st.session_state.temp_stack = extracted_stack
            st.session_state.experience = {"years": years_exp, "months": months_exp}
            st.session_state.interested_roles = selected_roles
            st.session_state.page = "confirm_stack"
            st.rerun()

def confirm_stack_page():
    """Tech stack confirmation page."""
    load_common_styles()
    st.markdown("## ✅ Review Your Details")
    st.caption("Make sure everything looks good before you start the interview.")

    with st.container():
        st.markdown("### 💻 Tech Stack")
        if st.session_state.temp_stack:
            st.markdown(f"`{', '.join(st.session_state.temp_stack)}`")
        else:
            st.info("No tech stack detected.")

        st.markdown("### 📅 Experience")
        exp = st.session_state.experience
        exp_str = f"{exp['years']} year{'s' if exp['years'] != 1 else ''}"
        if exp["months"]:
            exp_str += f" and {exp['months']} month{'s' if exp['months'] != 1 else ''}"
        st.markdown(f"**{exp_str}**")

        st.markdown("### 🎯 Interested Roles")
        roles = st.session_state.interested_roles
        if roles:
            st.markdown("🔹 " + "<br>🔹 ".join(roles), unsafe_allow_html=True)
        else:
            st.warning("No roles selected.")

    st.divider()

    col1, col2 = st.columns(2)
    with col1:
        if st.button("🔁 Re-enter Tech Stack"):
            st.session_state.page = "tech_stack"
            st.rerun()
    with col2:
        if st.button("🤖 Start Interview"):
            payload = {
                "tech_stack": st.session_state.temp_stack,
                "experience": st.session_state.experience,
                "interested_roles": st.session_state.interested_roles
            }
            
            data, error = make_api_request(f"update_full_details/{st.session_state.candidate_id}", "POST", payload)
            if data:
                st.session_state.page = "chat"
                st.rerun()
            else:
                st.error(f"Failed to save details: {error}")

def render_chat_message(sender, message):
    """Render a single chat message."""
    if sender == "You":
        st.markdown(f"""
        <div class="message-container user-message">
            <div class="message-sender user-sender">
                <img src="https://raw.githubusercontent.com/PrakharPandey2729/interview-chatbot/main/morty.png" alt="User" class="morty-icon">
                You
            </div>
            <div class="message-bubble user-bubble">{message}</div>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown(f"""
        <div class="message-container rick-message">
            <div class="message-sender rick-sender">
                <img src="https://raw.githubusercontent.com/PrakharPandey2729/interview-chatbot/main/Robot_Rick.png" alt="Rick" class="rick-icon">
                Rick
            </div>
            <div class="message-bubble rick-bubble">{message}</div>
        </div>
        """, unsafe_allow_html=True)

def chat_page():
    """Main chat interface."""
    load_common_styles()
    
    # Load chat-specific styles
    st.markdown("""
    <style>
    .chat-container {
        max-height: 65vh;
        overflow-y: auto;
        position: relative;
        overflow-x: hidden;
    }
    
    .chat-container::-webkit-scrollbar {
        width: 8px;
    }
    
    .chat-container::-webkit-scrollbar-track {
        background: rgba(255, 255, 255, 0.1);
        border-radius: 10px;
    }
    
    .chat-container::-webkit-scrollbar-thumb {
        background: #ff4c4c;
        border-radius: 10px;
    }
    
    .message-container {
        margin-bottom: 20px;
        display: flex;
        flex-direction: column;
        width: 100%;
    }
    
    .user-message {
        align-items: flex-end;
        text-align: right;
    }
    
    .rick-message {
        align-items: flex-start;
        text-align: left;
    }
    
    .message-bubble {
        padding: 15px 20px;
        border-radius: 15px;
        margin: 8px 0;
        word-wrap: break-word;
        width: fit-content;
        min-width: 80px;
        max-width: 75%;
        text-align: left;
        display: inline-block;
        font-family: 'Space Grotesk', sans-serif;
        font-weight: 500;
        transition: all 0.2s ease;
    }
    
    .message-bubble:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3);
    }
    
    .user-bubble {
        background: rgba(255, 255, 255, 0.1);
        color: white;
        border: 1px solid rgba(255, 255, 255, 0.2);
        margin-left: auto;
    }
    
    .rick-bubble {
        background: #ff4c4c;
        color: white;
        margin-right: auto;
        box-shadow: 0 0 15px rgba(255, 76, 76, 0.3);
    }
    
    .message-sender {
        font-size: 0.9em;
        opacity: 0.8;
        margin-bottom: 5px;
        width: fit-content;
        font-family: 'Space Grotesk', sans-serif;
        font-weight: 600;
        display: flex;
        align-items: center;
        gap: 8px;
    }
    
    .user-sender {
        margin-left: auto;
        text-align: right;
        color: rgba(255, 255, 255, 0.7);
    }
    
    .rick-sender {
        margin-right: auto;
        text-align: left;
        color: #ff4c4c;
    }
    
    .rick-icon {
        width: 50px;
        height: 55px;
        border-radius: 0%;
    }
    
    .morty-icon {
        width: 50px;
        height: 45px;
        border-radius: 0%;
    }
    
    .interview-header {
        text-align: center;
        font-family: 'Space Grotesk', sans-serif;
        font-weight: 700;
        font-size: 2.2em;
        color: #ff4c4c;
        margin-bottom: 20px;
        text-shadow: 0 0 20px rgba(255, 76, 76, 0.5);
        max-width: 100%;
        overflow-wrap: break-word;
    }
    
    @media (max-width: 768px) {
        .interview-header {
            font-size: 1.6em;
        }
        .interview-header img {
            width: 80px !important;
            height: 44px !important;
        }
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Load existing chat history if not already loaded
    if not st.session_state.history_loaded:
        data, error = make_api_request(f"history/{st.session_state.candidate_id}")
        if data:
            db_history = data["chat_history"]
            st.session_state.chat_history = []
            
            for entry in db_history:
                if entry['user'] != "START_INTERVIEW":
                    st.session_state.chat_history.append(("You", entry['user']))
                st.session_state.chat_history.append(("Rick", entry['bot']))
            
            if db_history:
                st.session_state.interview_started = True
                st.session_state.is_returning_user = len(db_history) > 1
            else:
                st.session_state.is_returning_user = False
        
        st.session_state.history_loaded = True
    
    # Header
    st.markdown("""
    <div class="interview-header" style="display: flex; align-items: center; justify-content: center; gap: 20px;">
        <img src="https://media2.giphy.com/media/v1.Y2lkPTc5MGI3NjExMnlmejhvbGprdzFxMTZpa3h3bzF0c3draXB0ZjQ1MGoyOXRwajZ1bCZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/YmuBikckdIDXC5jPFf/giphy.gif" style="width: 120px; height: 66px; border-radius: 8px;">
        <span>Tech<span style="color: #a8c8ec;">Rick</span>al Interview</span>
        <img src="https://media2.giphy.com/media/v1.Y2lkPTc5MGI3NjExMnlmejhvbGprdzFxMTZpa3h3bzF0c3draXB0ZjQ1MGoyOXRwajZ1bCZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/YmuBikckdIDXC5jPFf/giphy.gif" style="width: 120px; height: 66px; border-radius: 8px;">
    </div>
    """, unsafe_allow_html=True)
    
    # User info
    st.markdown(f"""
    <div class="info-container">
        <strong>Candidate:</strong> {st.session_state.candidate_name}<br>
        <strong>Email:</strong> {st.session_state.candidate_email}
    </div>
    """, unsafe_allow_html=True)
    
    # Welcome message for returning users
    if st.session_state.interview_started and st.session_state.is_returning_user:
        st.markdown("""
        <div class="info-container" style="background: rgba(168, 200, 236, 0.1); border: 1px solid rgba(168, 200, 236, 0.3); text-align: center;">
           🏁 Welcome back! 🏁 <br> Your previous conversation with Rick has been loaded. <br>Continue where you left off...
        </div>
        """, unsafe_allow_html=True)
    elif not st.session_state.interview_started:
        st.markdown("""
        <div class="info-container" style="background: rgba(255, 76, 76, 0.1); border: 1px solid rgba(255, 76, 76, 0.3); text-align: center;">
            ⚡ Prepare for a technical interview with Rick Sanchez! ⚡<br>Answer his questions to showcase your skills. 
        </div>
        """, unsafe_allow_html=True)
    
    # Start interview button
    if not st.session_state.interview_started:
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if st.button("🤖 Start Interview", key="start_interview_btn", use_container_width=True):
                # Play audio when start interview button is clicked
                play_audio("woo_vu_luvub_dub_dub.mp3")
                
                # Add a small delay to let audio play
                import time
                time.sleep(1)
                
                data, error = make_api_request(f"start_interview/{st.session_state.candidate_id}", "POST")
                if data:
                    add_to_chat_history(bot_message=data["response"])
                    st.session_state.interview_started = True
                    st.rerun()
                else:
                    st.error(f"❌ Error: {error}")
        return
    
    # Display chat history
    st.markdown('<div class="chat-container">', unsafe_allow_html=True)
    for sender, message in st.session_state.chat_history:
        render_chat_message(sender, message)
    st.markdown('</div>', unsafe_allow_html=True)

    # Chat input
    user_message = st.text_area(
        "💬 Your response", 
        key=f"chat_input_{st.session_state.input_counter}",
        placeholder="Type your response here...",
        height=100,
        help="Press Ctrl+Enter to send or use the button below"
    )

    # Send button
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        send_clicked = st.button("🚀 Send Response", key="send_btn", use_container_width=True)
    
    # Handle message sending
    if send_clicked and user_message.strip():
        data, error = make_api_request(f"chat/{st.session_state.candidate_id}", "POST", {"message": user_message})
        if data:
            add_to_chat_history(user_message, data["response"])
            if data.get("interview_started"):
                st.session_state.interview_started = True
            st.session_state.input_counter += 1
            st.rerun()
        else:
            st.error(f"❌ Error: {error}")

    # Interview controls
    with st.expander("⚙️ Interview Controls", expanded=False):
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("""
            <div style="text-align: center; margin-bottom: 10px;">
                <img src="https://media3.giphy.com/media/v1.Y2lkPTc5MGI3NjExNTczaXFkZGhvbGlrcjJra21tcDluMzRtdWNvZHo2MmpyZ2s1eXUwYiZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/vhhRM3XldbbQA/giphy.gif" 
                     style="width: 300px; height: 160px; border-radius: 8px;">
            </div>
            """, unsafe_allow_html=True)
            
            if st.button("Log Out", use_container_width=True, type="primary", key="logout_btn"):
                st.session_state.clear()
                st.rerun()
        
        with col2:
            st.markdown("""
            <div style="text-align: center; margin-bottom: 10px;">
                <img src="https://media4.giphy.com/media/v1.Y2lkPTc5MGI3NjExYmpxZWN4MndnN3kxdWhxMnBwYXF6MmR3YXJ5cXNyYnRnYXpzZ244ayZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/3oEhmVQaCjPOJJQgG4/giphy.gif" 
                     style="width: 300px; height: 160px; border-radius: 8px;">
            </div>
            """, unsafe_allow_html=True)
            
            if st.button("🛑 End Interview", use_container_width=True, type="primary"):
                data, error = make_api_request(f"end_interview/{st.session_state.candidate_id}", "POST")
                if data:
                    # Clear all session state to completely reset the app
                    st.session_state.clear()
                    # Initialize with login page
                    st.session_state.page = "login"
                    st.success("Interview ended successfully! You have been logged out.")
                    st.rerun()
                else:
                    st.error(f"Could not end interview: {error}")

# Main application logic
def main():
    """Main application entry point."""
    initialize_session_state()
    
    # Page routing
    page_functions = {
        "login": login_page,
        "tech_stack": tech_stack_page,
        "confirm_stack": confirm_stack_page,
        "chat": chat_page
    }
    
    current_page = st.session_state.get("page", "login")
    page_function = page_functions.get(current_page, login_page)
    page_function()

if __name__ == "__main__":
    main() 