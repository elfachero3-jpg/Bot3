# --- UI Components and Styling ---------------------------------------------
import streamlit as st
from datetime import datetime

# --- Custom CSS Styling ----------------------------------------------------
def inject_custom_css():
    """Inject custom CSS for app styling"""
    st.markdown("""
    <style>
    @import url('https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css');
    
    /* Main app background */
    .stApp { 
        background: linear-gradient(135deg, #f5f7fa 0%, #e8eef5 100%); 
    }
    
    /* Header styling */
    .main-header { 
        text-align: center; 
        color: #1f2937; 
        padding: 20px 0 10px 0; 
        animation: fadeInDown 0.8s ease; 
    }
    .main-header h1 { 
        font-size: 2.5rem; 
        font-weight: 600; 
        margin-bottom: 10px;
        color: #1f2937;
    }
    .main-header .subtitle { 
        font-size: 1.1rem; 
        color: #6b7280; 
        margin-bottom: 5px;
    }
    .main-header .creator { 
        font-size: 0.95rem; 
        color: #9ca3af; 
        margin-top: 8px;
    }
    
    /* Info banner styling */
    .info-banner {
        background: linear-gradient(135deg, #dbeafe 0%, #bfdbfe 100%);
        border-left: 4px solid #3b82f6;
        padding: 16px 20px;
        border-radius: 8px;
        margin: 20px 0 30px 0;
        color: #1e40af;
        font-size: 1rem;
        box-shadow: 0 2px 8px rgba(59, 130, 246, 0.1);
    }
    .info-banner strong {
        color: #1e3a8a;
        font-weight: 600;
    }
    
    /* Section headers with icons */
    .section-header {
        display: flex;
        align-items: center;
        font-size: 1.5rem;
        font-weight: 600;
        color: #374151;
        margin: 30px 0 20px 0;
        padding-bottom: 10px;
        border-bottom: 2px solid #e5e7eb;
    }
    .section-header .icon {
        margin-right: 12px;
        font-size: 1.6rem;
    }
    
    /* Audio section styling */
    .audio-section-title {
        display: flex;
        align-items: center;
        font-size: 1.25rem;
        font-weight: 600;
        color: #4b5563;
        margin-bottom: 8px;
    }
    .audio-section-title .icon {
        margin-right: 10px;
        font-size: 1.3rem;
    }
    .audio-description {
        color: #6b7280;
        font-size: 0.95rem;
        margin-bottom: 12px;
    }
    
    /* Button styling */
    .stButton > button { 
        background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%);
        color: white; 
        border-radius: 10px; 
        border: none; 
        padding: 0.7rem 1.2rem;
        font-weight: 600;
        font-size: 1.05rem;
        box-shadow: 0 4px 12px rgba(59, 130, 246, 0.3);
        transition: all 0.3s ease; 
    }
    .stButton > button:hover { 
        background: linear-gradient(135deg, #2563eb 0%, #1d4ed8 100%);
        transform: translateY(-2px); 
        box-shadow: 0 6px 16px rgba(59, 130, 246, 0.4); 
    }
    
    /* Download buttons */
    .stDownloadButton > button { 
        width: 100%;
        background: linear-gradient(135deg, #10b981 0%, #059669 100%);
        box-shadow: 0 3px 10px rgba(16, 185, 129, 0.3);
    }
    .stDownloadButton > button:hover {
        background: linear-gradient(135deg, #059669 0%, #047857 100%);
        box-shadow: 0 5px 14px rgba(16, 185, 129, 0.4);
    }
    
    /* Text input styling */
    .stTextInput > div > div > input {
        border-radius: 8px;
        border: 2px solid #e5e7eb;
        padding: 0.6rem 0.8rem;
    }
    .stTextInput > div > div > input:focus {
        border-color: #3b82f6;
        box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1);
    }
    
    /* File uploader styling */
    .stFileUploader {
        border-radius: 10px;
    }
    
    /* Text area styling */
    .stTextArea textarea { 
        font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, "Liberation Mono", "Courier New", monospace;
        border-radius: 8px;
        border: 2px solid #e5e7eb;
    }
    .stTextArea textarea:focus {
        border-color: #3b82f6;
        box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1);
    }
    
    /* Expander styling */
    .streamlit-expanderHeader {
        background-color: #f9fafb;
        border-radius: 8px;
        font-weight: 600;
    }
    
    /* Divider styling */
    hr {
        margin: 30px 0;
        border: none;
        border-top: 2px solid #e5e7eb;
    }
    </style>
    """, unsafe_allow_html=True)

# --- Header ----------------------------------------------------------------
def render_header():
    """Render app header matching old design"""
    st.markdown("""
    <div class="main-header">
        <h1>🎵 Music Teacher Observation Assistant</h1>
        <div class="subtitle">AI-Powered Classroom Observation & Feedback Tool</div>
        <div class="creator">Created by Brett Taylor</div>
    </div>
    """, unsafe_allow_html=True)
    
    # Info banner
    st.markdown("""
    <div class="info-banner">
        💡 <strong>Getting Started:</strong> Provide at least one input source (teacher audio, observer audio, or observer notes) to generate an observation report.
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
    """Render observation data section with name inputs"""
    st.markdown("""
    <div class="section-header">
        <span class="icon">📋</span>
        <span>Observation Data</span>
    </div>
    """, unsafe_allow_html=True)
    
    c1, c2 = st.columns(2)
    with c1:
        st.text_input(
            "👤 Teacher Name", 
            key="teacher_name", 
            placeholder="Enter teacher's name (optional)"
        )
    with c2:
        st.text_input(
            "👤 Observer Name", 
            key="observer_name", 
            placeholder="Enter observer's name (optional)"
        )

# --- Audio Uploads ----------------------------------------------------------
def render_audio_uploads():
    """Render audio upload widgets with styled headers"""
    st.markdown("<br>", unsafe_allow_html=True)
    
    c1, c2 = st.columns(2)
    
    with c1:
        st.markdown("""
        <div class="audio-section-title">
            <span class="icon">🎙️</span>
            <span>Teacher Audio (Optional)</span>
        </div>
        <div class="audio-description">Upload classroom audio recording</div>
        """, unsafe_allow_html=True)
        
        teacher_file = st.file_uploader(
            "teacher_audio_uploader",
            type=["mp3", "wav", "m4a", "flac", "ogg", "webm"],
            key="teacher_audio",
            label_visibility="collapsed"
        )
    
    with c2:
        st.markdown("""
        <div class="audio-section-title">
            <span class="icon">🎙️</span>
            <span>Observer Audio (Optional)</span>
        </div>
        <div class="audio-description">Upload observer's verbal notes</div>
        """, unsafe_allow_html=True)
        
        observer_file = st.file_uploader(
            "observer_audio_uploader",
            type=["mp3", "wav", "m4a", "flac", "ogg", "webm"],
            key="observer_audio",
            label_visibility="collapsed"
        )
    
    return teacher_file, observer_file

# --- Text Inputs ------------------------------------------------------------
def render_text_inputs():
    """Render observer notes and evaluation criteria inputs"""
    st.markdown("<br>", unsafe_allow_html=True)
    
    with st.expander("📝 Observer Notes / Evaluation Criteria", expanded=False):
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
            st.info("👆 Upload the observer audio in the 'Observer Audio' section above.")
        
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
                "Upload criteria document", 
                type=["txt", "pdf", "docx"],
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
        "<p style='text-align: center; color: #6b7280; font-size: 0.9rem;'>"
        "Powered by Gemini Flash • Music Teacher Observation Assistant v2.1"
        "</p>",
        unsafe_allow_html=True
    )
