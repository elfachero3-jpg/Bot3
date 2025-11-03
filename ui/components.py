# --- UI Components and Styling ---------------------------------------------
import streamlit as st
from datetime import datetime

# --- Custom CSS Styling ----------------------------------------------------
def inject_custom_css():
    """Inject custom CSS for app styling"""
    st.markdown("""
    <style>
    @import url('https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css');
    .stApp { background: linear-gradient(135deg, #f5f5f5 0%, #e8e8e8 100%); }
    .main-header { text-align: center; color: #2c3e50; padding: 20px 0 30px 0; animation: fadeInDown 0.8s ease; }
    .main-header h1 { font-size: 2.5rem; font-weight: 600; margin-bottom: 10px; }
    .main-header p { font-size: 1.1rem; opacity: 0.85; color: #546e7a; }
    .creator-text { font-size: 0.9rem; margin-top: 5px; opacity: 0.75; color: #607d8b; }
    .stButton > button { background: #37474f; color: white; border: none; padding: 15px 40px; font-size: 1.1rem; font-weight: 600; border-radius: 8px; width: 100%; box-shadow: 0 2px 8px rgba(0, 0, 0, 0.15); transition: all 0.3s ease; }
    .stButton > button:hover { background: #455a64; transform: translateY(-2px); box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2); }
    .stDownloadButton > button { background: #2e7d32 !important; color: white !important; border: none; padding: 15px 40px; font-size: 1.1rem; font-weight: 600; border-radius: 8px; width: 100%; box-shadow: 0 2px 8px rgba(0, 0, 0, 0.15); }
    .stDownloadButton > button:hover { background: #388e3c !important; transform: translateY(-2px); box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2); }
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    @keyframes fadeInDown { from { opacity: 0; transform: translateY(-30px); } to { opacity: 1; transform: translateY(0); } }
    </style>
    """, unsafe_allow_html=True)


# --- Header ----------------------------------------------------------------
def render_header():
    """Render app header with title and description"""
    st.markdown("""
    <div class="main-header">
      <h1><i class="fas fa-music"></i> Music Teacher Observation Assistant</h1>
      <p>AI-Powered Classroom Observation & Feedback Tool</p>
      <p class="creator-text">Created by Brett Taylor</p>
    </div>
    """, unsafe_allow_html=True)


# --- Sidebar Configuration -------------------------------------------------
def render_sidebar_config():
    """
    Render sidebar configuration options
    
    Returns:
        Dictionary with settings: report_length, include_transcript, report_sections
    """
    with st.sidebar:
        st.markdown("## ⚙️ Configuration")
        
        with st.expander("Report Settings", expanded=False):
            report_length = st.selectbox(
                "Report Length", 
                ["Brief", "Standard", "Comprehensive"], 
                index=1,
                help="Choose the level of detail in the observation report"
            )
            
            include_transcript = st.checkbox(
                "Generate Full Transcript", 
                value=True,
                help="Include downloadable aligned transcription PDF"
            )
            
            report_sections = st.multiselect(
                "Include Sections",
                ["Summary", "Strengths", "Areas for Growth", "Specific Evidence"],
                default=["Summary", "Strengths", "Areas for Growth"],
                help="Customize which sections appear in the report"
            )
    
    return {
        "report_length": report_length,
        "include_transcript": include_transcript,
        "report_
