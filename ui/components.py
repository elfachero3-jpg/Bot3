# --- UI Components and Styling ---------------------------------------------
import streamlit as st
from datetime import datetime

# --- Custom CSS Styling ----------------------------------------------------
def inject_custom_css():
    """Inject custom CSS for app styling (light/dark)"""
    dark = st.session_state.get("dark_mode", False)
    if dark:
        st.markdown(
            """<style>
/* Dark mode overrides */
@import url('https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css');
.stApp { background: linear-gradient(135deg, #0f172a 0%, #111827 100%); }
.main-header { text-align: center; color: #e5e7eb; padding: 20px 0 30px 0; animation: fadeInDown 0.8s ease; }
.main-header h1 { font-size: 2.5rem; font-weight: 600; margin-bottom: 10px; color: #f1f5f9; }
.main-header p { font-size: 1.1rem; opacity: 0.9; color: #cbd5e1; }
.creator-text { font-size: 0.9rem; margin-top: 5px; opacity: 0.8; color: #94a3b8; }

/* Buttons */
.stButton > button { background: #1f2937; color: #e5e7eb; border: none; border-radius: 10px; padding: 0.6rem 1.2rem; box-shadow: 0 2px 8px rgba(0, 0, 0, 0.35); transition: all 0.3s ease; }
.stButton > button:hover { background: #374151; transform: translateY(-2px); box-shadow: 0 4px 12px rgba(0, 0, 0, 0.45); }

/* Inputs */
.stTextInput > div > div > input { background: #0b1220; color: #e5e7eb; border: 1px solid #334155; border-radius: 8px; }
.stTextArea > div > textarea { background: #0b1220; color: #e5e7eb; border: 1px solid #334155; border-radius: 8px; }

/* File uploader */
.stFileUploader > div > div { background: #0b1220; color: #cbd5e1; border: 1px dashed #334155; border-radius: 10px; }
.stFileUploader label { color: #cbd5e1 !important; }

/* Panels & sections */
.container, .section, .panel { background: rgba(255,255,255,0.03); border-radius: 14px; padding: 18px; box-shadow: 0 2px 10px rgba(0,0,0,0.25); border: 1px solid rgba(148,163,184,0.18); }
.divider { height: 1px; background: linear-gradient(90deg, rgba(148,163,184,0.2), rgba(148,163,184,0.05), rgba(148,163,184,0.2)); margin: 24px 0; }

/* Typography */
h1, h2, h3, h4, h5, h6, label, p, li, span { color: #e5e7eb; }
.subtle { color: #94a3b8; }

/* Blockquote / evidence */
blockquote { border-left: 4px solid #475569; background: rgba(71,85,105,0.15); padding: 12px 16px; color: #e2e8f0; border-radius: 6px; }

/* Metric cards */
.metric-card { background: rgba(255,255,255,0.04); border-radius: 12px; padding: 12px; text-align: center; box-shadow: 0 1px 6px rgba(0,0,0,0.25); border: 1px solid rgba(148,163,184,0.18); }
.metric-card h3 { margin: 0; font-size: 0.9rem; color: #cbd5e1; }
.metric-card p { margin: 8px 0 0 0; font-size: 1.6rem; font-weight: 600; color: #f1f5f9; }

/* Icons & tags */
.icon { color: #93c5fd; }
.tag { background: rgba(99,102,241,0.2); color: #e0e7ff; border-radius: 8px; padding: 2px 8px; font-size: 0.85rem; }
</style>""",
            unsafe_allow_html=True
        )
    else:
        st.markdown(
            """<style>
    @import url('https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css');
    .stApp { background: linear-gradient(135deg, #f5f5f5 0%, #e8e8e8 100%); }
    .main-header { text-align: center; color: #2c3e50; padding: 20px 0 30px 0; animation: fadeInDown 0.8s ease; }
    .main-header h1 { font-size: 2.5rem; font-weight: 600; margin-bottom: 10px; }
    .main-header p { font-size: 1.1rem; opacity: 0.85; color: #546e7a; }
    .creator-text { font-size: 0.9rem; margin-top: 5px; opacity: 0.75; color: #607d8b; }
    .stButton > button { background: #37474f; color: white; border: none; border-radius: 10px; padding: 0.6rem 1.2rem; box-shadow: 0 2px 8px rgba(0, 0, 0, 0.15); transition: all 0.3s ease; }
    .stButton > button:hover { background: #455a64; transform: translateY(-2px); box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2); }
    .stTextInput > div > div > input { background: #ffffff; color: #2c3e50; border: 1px solid #cfd8dc; border-radius: 8px; }
    .stTextArea > div > textarea { background: #ffffff; color: #2c3e50; border: 1px solid #cfd8dc; border-radius: 8px; }
    .stFileUploader > div > div { background: #fafafa; border: 1px dashed #b0bec5; border-radius: 10px; }
    .container, .section, .panel { background: #ffffff; border-radius: 14px; padding: 18px; box-shadow: 0 2px 10px rgba(0, 0, 0, 0.08); border: 1px solid rgba(0, 0, 0, 0.04); }
    blockquote { border-left: 4px solid #90a4ae; background: #eceff1; padding: 12px 16px; color: #37474f; border-radius: 6px; }
    .metric-card { background: #ffffff; border-radius: 12px; padding: 12px; text-align: center; box-shadow: 0 1px 6px rgba(0, 0, 0, 0.08); border: 1px solid rgba(0, 0, 0, 0.05); }
    .metric-card h3 { margin: 0; font-size: 0.9rem; color: #546e7a; }
    .metric-card p { margin: 8px 0 0 0; font-size: 1.6rem; font-weight: 600; color: #263238; }
    h3, h4, h5 { color: #37474f; }
    .divider { height: 1px; background: linear-gradient(90deg, rgba(84,110,122,0.15), rgba(84,110,122,0.05), rgba(84,110,122,0.15)); margin: 24px 0; }
    .icon { color: #546e7a; }
    .tag { background: #eef2ff; color: #4338ca; border-radius: 8px; padding: 2px 8px; font-size: 0.85rem; }
    .subtle { color: #607d8b; }
    @keyframes fadeInDown { from { opacity: 0; transform: translateY(-8px);} to { opacity: 1; transform: translateY(0);} }
</style>""",
            unsafe_allow_html=True
        )

# --- Header ----------------------------------------------------------------
def render_header():
    st.markdown(
        "<div class='main-header'>"
        "<h1>🎵 Music Teacher Observation Assistant</h1>"
        "<p class='subtle'>Generate anonymized, evidence-based observation reports</p>"
        "<p class='creator-text'>Created by Brett Taylor</p>"
        "</div>",
        unsafe_allow_html=True
    )

# --- Configuration -------------------------------------------------
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

        # NEW: Visual Settings (requested)
        with st.expander("Visual Settings", expanded=False):
            dark_mode_val = st.toggle(
                "🌗 Dark mode",
                value=st.session_state.get("dark_mode", False),
                help="Switch the app’s visuals between light and dark."
            )
            st.session_state.dark_mode = dark_mode_val
    
    return {
        "report_length": report_length,
        "include_transcript": include_transcript,
        "report_sections": report_sections,
        # expose current mode to callers (non-breaking)
        "dark_mode": st.session_state.get("dark_mode", False)
    }

# --- Input Components ------------------------------------------------------
def render_name_inputs():
    """
    Render teacher and observer name input fields
    
    Returns:
        Tuple of (teacher_name, observer_name)
    """
    col1, col2 = st.columns(2)
    with col1:
        teacher_name = st.text_input("👤 Teacher Name", placeholder="Enter the teacher's name")
    with col2:
        observer_name = st.text_input("🕵️ Observer Name", placeholder="Enter your name")
    return teacher_name, observer_name

# (… the rest of your components file remains unchanged …)
# render_audio_uploads(), render_text_inputs(), render_downloads(), render_footer()
