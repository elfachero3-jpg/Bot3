# --- Observation Assistant Interface Components ---------------------------
import streamlit as st
from datetime import datetime
import re

def render_header():
    """Render app header"""
    st.markdown("""
    <div class="main-header">
      <h1><i class="fas fa-music"></i> Music Teacher Observation Assistant</h1>
      <p>AI-Powered Classroom Observation & Feedback Tool</p>
      <p class="creator-text">Created by Brett Taylor</p>
    </div>
    """, unsafe_allow_html=True)


def render_observation_header():
    """Render header for observation assistant tab"""
    st.info("💡 **Getting Started:** Provide at least one input source (teacher audio, observer audio, or observer notes) to generate an observation report.")


def render_name_inputs():
    """Render observation data section with name inputs"""
    st.markdown("## 📋 Observation Data")
    
    col_name1, col_name2 = st.columns(2)
    with col_name1:
        st.text_input(
            "👤 Teacher Name", 
            key="teacher_name", 
            placeholder="Enter teacher's name (optional)"
        )
    with col_name2:
        st.text_input(
            "👤 Observer Name", 
            key="observer_name", 
            placeholder="Enter observer's name (optional)"
        )
    
    st.markdown("---")


def render_audio_uploads():
    """Render audio upload widgets"""
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 📁 Teacher Audio (Optional)")
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
    
    st.markdown("---")
    
    return teacher_file, observer_file


def render_text_inputs():
    """Render observer notes and evaluation criteria inputs"""
    col3, col4 = st.columns(2)
    
    with col3:
        st.markdown("### 📝 Observer Text Notes (Optional)")
        observer_notes = st.text_area(
            "Written observation notes",
            placeholder="Enter any written notes from the observation...",
            height=200,
            help="Additional written observations or comments"
        )
    
    with col4:
        st.markdown("### 🎯 Evaluation Criteria (Optional)")
        criteria_method = st.radio(
            "Choose input method:", 
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


def render_downloads():
    """
    Render download section with PDF/text downloads
    Uses hardcoded settings: report_length="Standard", include_transcript=True
    """
    from core.pdf_generation import (
        create_observation_report_pdf, 
        create_dual_column_pdf,
    )
    from core.text_exports import (
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
    date_formatted = datetime.now().strftime('%B %d, %Y')

    col_dl1, col_dl2 = st.columns(2)

    # Get name inputs from session state or use defaults
    teacher_name = getattr(st.session_state, 'teacher_name', 'Not specified')
    observer_name = getattr(st.session_state, 'observer_name', 'Not specified')

    with col_dl1:
        # Primary download: Observation Report
        try:
            # Clean any duplicate header text from AI output
            cleaned_report = st.session_state.observation_report
            
            # Remove any AI-generated headers that duplicate what we add in PDF
            cleaned_report = re.sub(
                r'^\*{0,2}Music Teacher Observation Report\*{0,2}\s*\n',
                '',
                cleaned_report,
                flags=re.IGNORECASE | re.MULTILINE
            )
            
            # Remove date lines that match our format
            cleaned_report = re.sub(
                r'^[A-Z][a-z]+ \d{1,2},? \d{4}\s*\n',
                '',
                cleaned_report,
                flags=re.MULTILINE
            )
            
            # Remove Teacher: and Observer: lines if at the start
            cleaned_report = re.sub(
                r'^Teacher:\s*.+?\n',
                '',
                cleaned_report,
                flags=re.IGNORECASE | re.MULTILINE,
                count=1
            )
            cleaned_report = re.sub(
                r'^Observer:\s*.+?\n',
                '',
                cleaned_report,
                flags=re.IGNORECASE | re.MULTILINE,
                count=1
            )
            
            # Remove any leading whitespace
            cleaned_report = cleaned_report.lstrip()
            
            # Determine if we have teacher audio
            has_teacher_audio = hasattr(st.session_state, 'teacher_transcription') and st.session_state.teacher_transcription
            
            report_pdf_bytes = create_observation_report_pdf(
                report_text=cleaned_report,
                teacher_name=teacher_name if teacher_name else "Not specified",
                observer_name=observer_name if observer_name else "Not specified",
                date_str=date_formatted,
                report_length="standard",  # Hardcoded default
                has_teacher_audio=has_teacher_audio,
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
                date_formatted
            )
            st.download_button(
                label="⬇️ Download Observation Report (TXT - Fallback)",
                data=text_fallback,
                file_name=f"observation_report_{timestamp}.txt",
                mime="text/plain",
                use_container_width=True
            )

    with col_dl2:
        # Secondary download: Full Transcript (always included)
        if st.session_state.aligned_teacher or st.session_state.aligned_observer:
            try:
                # Determine which PDF format to use
                if st.session_state.aligned_teacher and st.session_state.aligned_observer:
                    # Both sources: dual column
                    transcript_pdf_bytes = create_dual_column_pdf(
                        st.session_state.aligned_teacher,
                        st.session_state.aligned_observer
                    )
                else:
                    # Single source: use dual column with empty for missing side
                    transcript_pdf_bytes = create_dual_column_pdf(
                        st.session_state.aligned_teacher if st.session_state.aligned_teacher else "",
                        st.session_state.aligned_observer if st.session_state.aligned_observer else ""
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
                
                # Text fallback for transcript
                transcript_text = create_transcript_text_fallback(
                    st.session_state.aligned_teacher if st.session_state.aligned_teacher else "",
                    st.session_state.aligned_observer if st.session_state.aligned_observer else "",
                    date_formatted
                )
                st.download_button(
                    label="⬇️ Download Full Transcript (TXT - Fallback)",
                    data=transcript_text,
                    file_name=f"transcript_{timestamp}.txt",
                    mime="text/plain",
                    use_container_width=True
                )
        else:
            st.info("ℹ️ Transcript will be available after processing")


def render_footer():
    """Render app footer"""
    st.markdown("---")
    st.markdown(
        "<p style='text-align: center; color: #546e7a; opacity: 0.8;'>"
        "Powered by Gemini Flash • Music Teacher Observation Assistant v2.4"
        "</p>",
        unsafe_allow_html=True
    )
