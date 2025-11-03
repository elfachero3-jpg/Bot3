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
        "report_sections": report_sections
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
        teacher_name = st.text_input("👤 Teacher Name", placeholder="Enter teacher's name (optional)")
    with col2:
        observer_name = st.text_input("👤 Observer Name", placeholder="Enter observer's name (optional)")
    
    return teacher_name, observer_name


def render_audio_uploads():
    """
    Render audio file upload components
    
    Returns:
        Tuple of (teacher_file, observer_file)
    """
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 📁 Teacher Audio (Required)")
        teacher_file = st.file_uploader(
            "Upload classroom audio recording",
            type=["mp3", "wav", "m4a", "flac", "ogg", "webm"],
            key="teacher_upload",
            help="Primary classroom recording with teacher and student interactions"
        )
        if teacher_file:
            file_size = teacher_file.size / (1024 * 1024)
            st.success(f"✅ **{teacher_file.name}** ({file_size:.2f} MB)")
            st.audio(teacher_file, format=f'audio/{teacher_file.name.split(".")[-1]}')

    with col2:
        st.markdown("### 📁 Observer Audio (Optional)")
        observer_file = st.file_uploader(
            "Upload observer's verbal notes",
            type=["mp3", "wav", "m4a", "flac", "ogg", "webm"],
            key="observer_upload",
            help="Observer's audio commentary during the observation"
        )
        if observer_file:
            file_size = observer_file.size / (1024 * 1024)
            st.success(f"✅ **{observer_file.name}** ({file_size:.2f} MB)")
            st.audio(observer_file, format=f'audio/{observer_file.name.split(".")[-1]}')
    
    return teacher_file, observer_file


def render_text_inputs():
    """
    Render text input components for observer notes and evaluation criteria
    
    Returns:
        Tuple of (observer_notes, evaluation_criteria)
    """
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 📝 Observer Text Notes (Optional)")
        observer_notes = st.text_area(
            "Written observation notes",
            placeholder="Enter any written notes from the observation...",
            height=200,
            help="Additional written observations or comments"
        )

    with col2:
        st.markdown("### 🎯 Evaluation Criteria (Optional)")
        criteria_method = st.radio(
            "Choose input method:", ["Paste Text", "Upload Document"], horizontal=True
        )
        evaluation_criteria = ""
        if criteria_method == "Paste Text":
            evaluation_criteria = st.text_area(
                "Paste evaluation criteria",
                placeholder="Enter specific criteria to focus the observation...",
                height=200,
                help="Specific teaching aspects or rubric to evaluate"
            )
        else:
            criteria_file = st.file_uploader(
                "Upload criteria document", type=["txt", "pdf", "docx"],
                help="Upload evaluation rubric or criteria document"
            )
            if criteria_file:
                if criteria_file.type == "text/plain":
                    evaluation_criteria = criteria_file.read().decode("utf-8")
                    st.success(f"✅ Loaded: {criteria_file.name}")
                else:
                    st.info("📄 Document uploaded. Text extraction will occur during processing.")
                    evaluation_criteria = f"[Document: {criteria_file.name}]"
    
    return observer_notes, evaluation_criteria


# --- Download Components ---------------------------------------------------
def render_downloads(settings):
    """
    Render download section with PDF/text downloads
    
    Args:
        settings: Dictionary containing include_transcript setting
    """
    from core.reports import (
        create_observation_report_pdf, 
        create_dual_column_pdf,
        create_text_fallback,
        create_transcript_text_fallback
    )
    
    st.markdown("---")
    st.markdown("## 📥 Download Reports")

    # Report preview
    with st.expander("📄 Preview Observation Report", expanded=False):
        st.markdown(st.session_state.observation_report)

    # Generate timestamp
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    date_time_formatted = datetime.now().strftime('%B %d, %Y at %I:%M %p')

    col1, col2 = st.columns(2)

    # Get name inputs from session state or use defaults
    teacher_name = getattr(st.session_state, 'teacher_name', 'Not specified')
    observer_name = getattr(st.session_state, 'observer_name', 'Not specified')

    with col1:
        # Primary download: Observation Report
        try:
            report_pdf_bytes = create_observation_report_pdf(
                report_text=st.session_state.observation_report,
                teacher_name=teacher_name,
                observer_name=observer_name,
                date_time=date_time_formatted,
                report_length=settings['report_length'].lower(),
            )
            st.download_button(
                label="⬇️ Download Observation Report (PDF)",
                data=report_pdf_bytes,
                file_name=f"observation_report_{timestamp}.pdf",
                mime="application/pdf",
                use_container_width=True
            )
        except Exception as e:
            st.error(f"❌ Report PDF generation failed: {str(e)}")
            st.warning("📄 Downloading text version as fallback...")
            
            text_fallback = create_text_fallback(
                st.session_state.observation_report,
                teacher_name,
                observer_name,
                date_time_formatted
            )
            st.download_button(
                label="⬇️ Download Observation Report (TXT - Fallback)",
                data=text_fallback,
                file_name=f"observation_report_{timestamp}.txt",
                mime="text/plain",
                use_container_width=True
            )

    with col2:
        # Secondary download: Full Transcript
        if settings['include_transcript'] and st.session_state.aligned_teacher:
            try:
                if st.session_state.aligned_observer:
                    transcript_pdf_bytes = create_dual_column_pdf(
                        st.session_state.aligned_teacher,
                        st.session_state.aligned_observer
                    )
                else:
                    transcript_pdf_bytes = create_dual_column_pdf(
                        st.session_state.aligned_teacher,
                        "No observer audio or notes provided."
                    )
                st.download_button(
                    label="⬇️ Download Full Transcript (PDF)",
                    data=transcript_pdf_bytes,
                    file_name=f"transcript_{timestamp}.pdf",
                    mime="application/pdf",
                    use_container_width=True
                )
            except Exception as e:
                st.error(f"❌ Transcript PDF generation failed: {str(e)}")
                st.warning("📄 Downloading text version as fallback...")
                
                transcript_text = create_transcript_text_fallback(
                    st.session_state.aligned_teacher,
                    st.session_state.aligned_observer if st.session_state.aligned_observer else "",
                    date_time_formatted
                )
                st.download_button(
                    label="⬇️ Download Full Transcript (TXT - Fallback)",
                    data=transcript_text,
                    file_name=f"transcript_{timestamp}.txt",
                    mime="text/plain",
                    use_container_width=True
                )
        elif settings['include_transcript']:
            st.info("ℹ️ Transcript will be available after processing")


# --- Footer ----------------------------------------------------------------
def render_footer():
    """Render app footer"""
    st.markdown("---")
    st.markdown(
        "<p style='text-align: center; color: #546e7a; opacity: 0.8;'>"
        "Powered by Gemini Flash • Music Teacher Observation Assistant v2.1"
        "</p>",
        unsafe_allow_html=True
    )
