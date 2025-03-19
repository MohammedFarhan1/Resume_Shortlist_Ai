import streamlit as st
import requests
import time
from datetime import datetime

# Page Configuration with custom theme
st.set_page_config(
    page_title="Resume Shortlist AI",
    page_icon="📄",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS with dark theme and better visibility
st.markdown("""
    <style>
    /* Main theme colors */
    :root {
        --primary-color: #4CAF50;
        --secondary-color: #2E7D32;
        --background-color: #1E1E1E;
        --surface-color: #2D2D2D;
        --text-color: #FFFFFF;
        --error-color: #CF6679;
        --success-color: #4CAF50;
    }

    /* Global styles */
    .main {
        background-color: var(--background-color);
        color: var(--text-color);
        padding: 2rem;
    }

    /* Button styles */
    .stButton>button {
        width: 100%;
        border-radius: 8px;
        height: 3em;
        background-color: var(--primary-color);
        color: white;
        font-weight: bold;
        border: none;
        transition: all 0.3s ease;
    }
    .stButton>button:hover {
        background-color: var(--secondary-color);
        transform: translateY(-2px);
        box-shadow: 0 4px 8px rgba(0,0,0,0.2);
    }

    /* Message boxes */
    .success-message {
        padding: 1em;
        border-radius: 8px;
        background-color: rgba(76, 175, 80, 0.1);
        border-left: 5px solid var(--success-color);
        color: #FFFFFF;
        margin: 1em 0;
    }
    .error-message {
        padding: 1em;
        border-radius: 8px;
        background-color: rgba(207, 102, 121, 0.1);
        border-left: 5px solid var(--error-color);
        color: #FFFFFF;
        margin: 1em 0;
    }
    .info-box {
        padding: 1.5em;
        background-color: var(--surface-color);
        border-radius: 8px;
        margin: 1em 0;
        color: #FFFFFF;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }

    /* Header styles */
    .header-container {
        display: flex;
        align-items: center;
        justify-content: space-between;
        padding: 1em 0;
        border-bottom: 2px solid var(--primary-color);
        margin-bottom: 2em;
        background-color: var(--surface-color);
        border-radius: 8px;
        padding: 1.5em;
    }
    .header-container h1 {
        color: #FFFFFF;
        margin: 0;
        font-size: 2em;
    }

    /* Status indicator */
    .status-indicator {
        font-size: 0.9em;
        padding: 0.5em 1em;
        border-radius: 20px;
        display: inline-block;
        margin: 0.5em 0;
    }
    .status-online {
        background-color: rgba(76, 175, 80, 0.2);
        color: #4CAF50;
    }
    .status-offline {
        background-color: rgba(207, 102, 121, 0.2);
        color: #CF6679;
    }

    /* Footer */
    .footer {
        position: fixed;
        bottom: 0;
        left: 0;
        width: 100%;
        background-color: var(--surface-color);
        padding: 1em;
        text-align: center;
        border-top: 1px solid rgba(255,255,255,0.1);
        color: #FFFFFF;
    }

    /* Upload area */
    .upload-area {
        border: 2px dashed var(--primary-color);
        border-radius: 8px;
        padding: 2em;
        text-align: center;
        margin: 1em 0;
        background-color: var(--surface-color);
        transition: all 0.3s ease;
    }
    .upload-area:hover {
        border-color: var(--secondary-color);
        background-color: rgba(76, 175, 80, 0.1);
    }

    /* Progress bar */
    .stProgress > div > div {
        background-color: var(--primary-color);
    }

    /* Text area */
    .stTextArea textarea {
        background-color: var(--surface-color);
        color: #FFFFFF;
        border: 1px solid rgba(255,255,255,0.1);
        border-radius: 8px;
    }

    /* Sidebar */
    .css-1d391kg {
        background-color: var(--surface-color);
    }
    .sidebar .sidebar-content {
        background-color: var(--surface-color);
    }
    
    /* Make text more visible */
    p, h1, h2, h3, h4, h5, h6 {
        color: #FFFFFF !important;
    }
    .stMarkdown {
        color: #FFFFFF !important;
    }
    </style>
    """, unsafe_allow_html=True)

# Backend URL
BACKEND_URL = "http://127.0.0.1:5000"

# Sidebar
with st.sidebar:
    st.image("https://img.icons8.com/color/96/000000/artificial-intelligence.png")
    st.title("About")
    st.markdown("""
    <div class="info-box">
        📌 <b>This AI-powered tool helps you:</b>
        <ul>
            <li>Remove personal information from resumes</li>
            <li>Maintain document formatting</li>
            <li>Ensure privacy compliance</li>
        </ul>
        <b>🛡️Your data is processed securely and not stored.</b>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    st.markdown("""
    <div class="info-box">
        <h3>How to use</h3>
        <ol>
            <li>Upload your PDF resume</li>
            <li>Wait for AI processing</li>
            <li>Review the cleaned content</li>
            <li>Download the result</li>
        </ol>
    </div>
    """, unsafe_allow_html=True)

# Main Content
col1, col2, col3 = st.columns([1,3,1])
with col2:
    st.markdown("""
        <div class="header-container">
            <h1>📄 Resume Shortlist AI</h1>
        </div>
    """, unsafe_allow_html=True)

# Test backend connection
def test_backend_connection():
    try:
        response = requests.get(BACKEND_URL)
        if response.status_code == 200:
            data = response.json()
            if data.get("status") == "success":
                return True
        return False
    except requests.exceptions.ConnectionError:
        return False

# Connection Status
if test_backend_connection():
    st.markdown("""
        <div class="success-message">
            <span class="status-indicator status-online">●</span>
            System Status: Online and Ready
        </div>
    """, unsafe_allow_html=True)
else:
    st.markdown("""
        <div class="error-message">
            <span class="status-indicator status-offline">●</span>
            System Status: Offline - Please check server connection
        </div>
    """, unsafe_allow_html=True)
    st.info("Please make sure the Flask server is running (python app.py)")
    st.stop()

# Main Upload Section
st.markdown("""
    <div class="info-box">
        <h3>📤 Upload Your Resume</h3>
        <p>Supported format: PDF (Max size: 10MB)</p>
    </div>
""", unsafe_allow_html=True)

uploaded_file = st.file_uploader("", type=["pdf"])

if uploaded_file is not None:
    # File info display
    st.markdown("""
        <div class="info-box">
            <div style="display: flex; justify-content: space-between;">
                <div><strong>File Name:</strong> {}</div>
                <div><strong>Upload Time:</strong> {}</div>
            </div>
        </div>
    """.format(uploaded_file.name, datetime.now().strftime('%Y-%m-%d %H:%M:%S')), unsafe_allow_html=True)
    
    # Processing
    with st.spinner("🔄 Processing your resume..."):
        progress_bar = st.progress(0)
        for i in range(100):
            time.sleep(0.01)
            progress_bar.progress(i + 1)
        
        files = {"file": (uploaded_file.name, uploaded_file, "application/pdf")}
        try:
            response = requests.post(f"{BACKEND_URL}/process-pdf", files=files)
            
            if response.status_code == 200:
                cleaned_text = response.json().get("cleaned_text", "")

                # Success Section
                st.markdown("""
                    <div class="success-message">
                        ✅ Processing Complete!
                    </div>
                """, unsafe_allow_html=True)

                # Results Section
                st.markdown("""
                    <div class="info-box">
                        <h3>📑 Processed Content</h3>
                        <p>Review the cleaned content below:</p>
                    </div>
                """, unsafe_allow_html=True)
                st.text_area("", cleaned_text, height=400)

                # Download Section
                col1, col2, col3 = st.columns([1,2,1])
                with col2:
                    st.download_button(
                        label="📥 Download Processed Resume",
                        data=cleaned_text,
                        file_name=f"processed_{uploaded_file.name.split('.')[0]}.txt",
                        mime="text/plain",
                    )

            else:
                error_message = response.json().get("error", "Unknown error occurred")
                st.markdown(f"""
                    <div class="error-message">
                        ⚠️ Error: {error_message}
                    </div>
                """, unsafe_allow_html=True)

        except requests.exceptions.ConnectionError:
            st.markdown("""
                <div class="error-message">
                    ❌ Connection Error: Unable to reach the server
                </div>
            """, unsafe_allow_html=True)
        except Exception as e:
            st.markdown(f"""
                <div class="error-message">
                    ❌ Unexpected Error: {str(e)}
                </div>
            """, unsafe_allow_html=True)

# Footer
st.markdown("""
    <div class="footer">
        <p>© 2024 Resume Shortlist AI | Powered by Groq AI</p>
    </div>
""", unsafe_allow_html=True)
