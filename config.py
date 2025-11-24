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

def create_client():
    """Create and return the Gemini client"""
    return genai.Client(api_key=get_api_key())

def load_developer_prompt():
    """Load system/developer prompt from identity.txt"""
    with open("identity.txt", "r", encoding="utf-8") as f:
        return f.read()

def load_solo_prompt():
    """Load system/developer prompt for solo teaching mode from identity_solo.txt"""
    with open("identity_solo.txt", "r", encoding="utf-8") as f:
        return f.read()

# --- Generation Configs ----------------------------------------------------
def get_generation_configs():
    """Create and return generation configurations for observation mode"""
    system_instructions = load_developer_prompt()
    search_tool = types.Tool(google_search=types.GoogleSearch())

    generation_cfg = types.GenerateContentConfig(
        system_instruction=system_instructions,
        tools=[search_tool],
        temperature=1.0,
        max_output_tokens=8192,
    )

    transcription_cfg = types.GenerateContentConfig(
        system_instruction=system_instructions,
        temperature=1.0,
        max_output_tokens=8192,
    )

    return generation_cfg, transcription_cfg

def get_solo_config():
    """Create and return generation configuration for solo teaching mode"""
    system_instructions = load_solo_prompt()
    
    solo_cfg = types.GenerateContentConfig(
        system_instruction=system_instructions,
        temperature=1.0,
        max_output_tokens=8192,
    )
    
    return solo_cfg

# --- Session State ---------------------------------------------------------
def initialize_session_state():
    """Initialize all session state variables"""
    # Observation mode states
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
    
    # Solo teaching mode states
    if 'solo_transcription' not in st.session_state:
        st.session_state.solo_transcription = None
    if 'solo_chat_history' not in st.session_state:
        st.session_state.solo_chat_history = []
    if 'solo_audio_processed' not in st.session_state:
        st.session_state.solo_audio_processed = False

# --- Constants -------------------------------------------------------------
PAGE_CONFIG = {
    "page_title": "Music Teacher Observation Assistant",
    "page_icon": "🎵",
    "layout": "wide",
    "initial_sidebar_state": "collapsed",
}
