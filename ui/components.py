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
    .stButton > button { background: #37474f; color: white; border-radius: 10px; border: none; padding: 0.6rem 1rem; box-shadow: 0 2px 8px rgba(0, 0, 0, 0.15); transition: all 0.3s ease; }
    .stButton > button:hover { background: #263238; transform: translateY(-1px); box-shadow: 0 4px 12px rgba(0,0,0,0.2); }
    .stDownloadButton > button { width: 100%; }
    .expander > div { padding: 0.5rem 0.75rem; }
    .stTextArea textarea { font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, "Liberation Mono", "Courier New", monospace; }
    </style>
    """, unsafe_allow_html=True)

# --- Header ----------------------------------------------------------------
def render_header():
    """Render app header"""
    st.markdown("""
    <div class="main-header">
        <h1>🎵 Music Teacher Observation Assistant</h1>
        <p>Create clear, professional observations with aligned evidence and targeted feedback.</p>
        <div class="creator-text">Created by Brett Taylor</div>
    </div>
    """, unsafe_allow_html=True)

# --- Sidebar Config ---------------------------------------------------------
def render_sidebar_config():
    """
    Render configuration controls in the sidebar
    
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

# --- Name Inputs ------------------------------------------------------------
def render_name_inputs():
    """Render inputs for teacher and observer names"""
    c1, c2 = st.columns(2)
    with c1:
        st.text_input("Teacher Name", key="teacher_name", placeholder="Enter teacher's full name")
    with c2:
        st.text_input("Observer Name", key="observer_name", placeholder="Enter observer's full name")

# --- Audio Uploads ----------------------------------------------------------
def render_audio_uploads():
    """Render audio upload widgets"""
    c1, c2 = st.columns(2)
    
    with c1:
        teacher_file = st.file_uploader(
            "Upload Teacher Audio (MP3/WAV/M4A)",
            type=["mp3", "wav", "m4a"],
            key="teacher_audio"
        )
    with c2:
        observer_file = st.file_uploader(
            "Upload Observer Audio (optional)",
            type=["mp3", "wav", "m4a"],
            key="observer_audio"
        )
    return teacher_file, observer_file

# --- Text Inputs ------------------------------------------------------------
def render_text_inputs():
    """Render observer notes and evaluation criteria inputs"""
    with st.expander("Observer Notes / Evaluation Criteria", expanded=False):
        st.markdown("You can paste observer notes, upload audio, and/or provide evaluation criteria.")
        
        notes_method = st.radio(
            "Observer notes source",
            ["Paste Text", "Upload Audio"],
            horizontal=True
        )
        
        observer_notes = ""
        if notes_method == "Paste Text":
            observer_notes = st.text_area(
                "Paste observer notes (optional)",
                placeholder="Enter your notes here...",
                height=200,
            )
        else:
            st.info("Upload the observer audio in the 'Upload Observer Audio' section above.")
        
        st.markdown("---")
        criteria_method = st.radio(
            "Evaluation criteria source",
            ["Paste Text", "Upload Document"],
            horizontal=True
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
    report_date_formatted = datetime.now().strftime('%B %d, %Y')

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
                date_time=report_date_formatted,
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
                report_date_formatted
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
                        ""
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
