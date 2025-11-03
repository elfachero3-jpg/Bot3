# --- Configuration and Setup -----------------------------------------------
import os
import streamlit as st
from google import genai
from google.genai import types

# --- API Configuration -----------------------------------------------------
def get_api_key():
    """Get API key from Streamlit secrets"""
    API_KEY = st.secrets.get("GEMINI_API_KEY", "")
    if not API_KEY:
        st.warning("⚠️ 'GEMINI_API_KEY' is not set in st.secrets. Add it before deploying.")
        st.stop()
    return API_KEY

# --- Client ----------------------------------------------------------------
def create_client():
    """Create and return the Gemini client"""
    return genai.Client(api_key=get_api_key())

# --- Generation Configs ----------------------------------------------------
def get_generation_configs():
    """Return generation and transcription config objects"""
    generation_cfg = types.GenerateContentConfig(
        temperature=0.4,
        top_p=0.9,
        top_k=40
    )
    transcription_cfg = types.TranscriptionConfig(
        language_code="en-US"
    )
    return generation_cfg, transcription_cfg

# --- Session State ---------------------------------------------------------
def initialize_session_state():
    """Initialize all session state variables"""
    if 'teacher_transcription' not in st.session_state:
        st.session_state.teacher_transcription = None
    if 'observer_transcription' not in st.session_state:
        st.session_state.observer_transcription = None
    if 'aligned_teacher' not in st.session_state:
        st.session_state.aligned_teacher = None
    if 'aligned_observer' not in st.session_state:
        st.session_state.aligned_observer = None
    if 'observation_report' not in st.session_state:
        st.session_state.observation_report = None
    if 'lesson_analysis' not in st.session_state:
        st.session_state.lesson_analysis = None
    # NEW: per-session visual preference
    if 'dark_mode' not in st.session_state:
        st.session_state.dark_mode = False

# --- Constants -------------------------------------------------------------
PAGE_CONFIG = {
    "page_title": "Music Teacher Observation Assistant",
    "page_icon": "🎵",
    "layout": "wide",
    # NEW: requested behavior — sidebar starts collapsed
    "initial_sidebar_state": "collapsed"
}
