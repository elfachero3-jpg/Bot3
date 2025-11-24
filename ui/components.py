# --- UI Components and Styling ---------------------------------------------
import streamlit as st
from datetime import datetime

# --- Custom CSS Styling ----------------------------------------------------
def inject_custom_css():
    """Inject custom CSS for app styling - with manila folder/browser-style tabs"""
    st.markdown("""
    <style>
    @import url('https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css');
    
    /* Main app background */
    .stApp { 
        background: linear-gradient(135deg, #f5f5f5 0%, #e8e8e8 100%); 
    }
    
    /* Header styling */
    .main-header { 
        text-align: center; 
        color: #2c3e50; 
        padding: 20px 0 20px 0; 
        animation: fadeInDown 0.8s ease; 
    }
    .main-header h1 { 
        font-size: 2.5rem; 
        font-weight: 600; 
        margin-bottom: 10px; 
    }
    .main-header p { 
        font-size: 1.1rem; 
        opacity: 0.85; 
        color: #546e7a; 
    }
    .creator-text { 
        font-size: 0.9rem; 
        margin-top: 5px; 
        opacity: 0.75; 
        color: #607d8b; 
    }
    
    /* MANILA FOLDER / BROWSER-STYLE TAB STYLING */
    .stTabs [data-baseweb="tab-list"] {
        gap: 4px;
        background-color: transparent;
        padding: 0;
        border-bottom: 3px solid #37474f;
        margin-bottom: 0;
    }
    
    .stTabs [data-baseweb="tab"] {
        height: 65px;
        padding: 0 35px;
        background: linear-gradient(to bottom, #d4c5a9 0%, #c9b896 100%);
        border-radius: 12px 12px 0 0;
        font-size: 1.3rem;
        font-weight: 600;
        color: #5d4e37;
        border: 2px solid #a89968;
        border-bottom: none;
        position: relative;
        margin-bottom: -3px;
        transition: all 0.3s ease;
        box-shadow: 
            inset 0 1px 0 rgba(255,255,255,0.3),
            0 2px 5px rgba(0,0,0,0.1);
    }
    
    .stTabs [data-baseweb="tab"]::before {
        content: '';
        position: absolute;
        bottom: 0;
        left: 0;
        right: 0;
        height: 3px;
        background: linear-gradient(to bottom, #d4c5a9 0%, #c9b896 100%);
    }
    
    .stTabs [data-baseweb="tab"]:hover {
        background: linear-gradient(to bottom, #dcd0b8 0%, #d1c4a4 100%);
        color: #4a3d28;
        transform: translateY(-3px);
        box-shadow: 
            inset 0 1px 0 rgba(255,255,255,0.4),
            0 4px 8px rgba(0,0,0,0.15);
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(to bottom, #ffffff 0%, #f8f8f8 100%) !important;
        color: #2c3e50 !important;
        border: 2px solid #37474f;
        border-bottom: none !important;
        height: 70px;
        transform: translateY(-5px);
        z-index: 10;
        box-shadow: 
            0 -2px 8px rgba(0,0,0,0.1),
            inset 0 1px 0 rgba(255,255,255,0.8);
    }
    
    .stTabs [aria-selected="true"]::before {
        background: #ffffff;
        height: 5px;
    }
    
    .stTabs [data-baseweb="tab-panel"] {
        padding-top: 30px;
        background: #ffffff;
        border-radius: 0 0 12px 12px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.1);
        padding: 30px 20px;
        margin-top: -3px;
    }
    
    /* Button styling */
    .stButton > button { 
        background: #37474f; 
        color: white; 
        border: none; 
        padding: 15px 40px; 
        font-size: 1.1rem; 
        font-weight: 600; 
        border-radius: 8px; 
        width: 100%; 
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.15); 
        transition: all 0.3s ease; 
    }
    .stButton > button:hover { 
        background: #455a64; 
        transform: translateY(-2px); 
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2); 
    }
    
    /* Download button styling */
    .stDownloadButton > button { 
        background: #2e7d32 !important; 
        color: white !important; 
        border: none; 
        padding: 15px 40px; 
        font-size: 1.1rem; 
        font-weight: 600; 
        border-radius: 8px; 
        width: 100%; 
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.15); 
    }
    .stDownloadButton > button:hover { 
        background: #388e3c !important; 
        transform: translateY(-2px); 
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2); 
    }
    
    /* Input status box */
    .input-status { 
        background: #ffffff; 
        padding: 15px; 
        border-radius: 8px; 
        box-shadow: 0 2px 4px rgba(0,0,0,0.1); 
        margin: 10px 0; 
    }
    
    /* Chat message styling */
    .chat-message {
        padding: 1rem;
        border-radius: 0.5rem;
        margin-bottom: 1rem;
        display: flex;
        flex-direction: column;
    }
    
    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    
    /* Animation */
    @keyframes fadeInDown { 
        from { opacity: 0; transform: translateY(-30px); } 
        to { opacity: 1; transform: translateY(0); } 
    }
    </style>
    """, unsafe_allow_html=True)

# --- Header ----------------------------------------------------------------
def render_header():
    """Render app header matching old design exactly"""
    st.markdown("""
    <div class="main-header">
      <h1><i class="fas fa-music"></i> Music Teacher Observation Assistant</h1>
      <p>AI-Powered Classroom Observation & Feedback Tool</p>
      <p class="creator-text">Created by Brett Taylor</p>
    </div>
    """, unsafe_allow_html=True)

# --- Solo Teaching Interface -----------------------------------------------
def render_solo_interface():
    """Render the Solo Teaching Feedback interface"""
    
    st.markdown("## 💭 Reflect on Your Teaching")
    st.info("📝 **How it works:** Upload your classroom audio, and I'll help you reflect on your teaching through guided conversation.")
    
    # Audio upload section
    st.markdown("### 📁 Upload Classroom Audio")
    solo_audio = st.file_uploader(
        "Upload your classroom recording",
        type=["mp3", "wav", "m4a", "flac", "ogg", "webm"],
        key="solo_audio_upload",
        help="Upload audio from your lesson to begin reflection"
    )
    
    if solo_audio:
        file_size = solo_audio.size / (1024 * 1024)
        st.success(f"✅ **{solo_audio.name}** ({file_size:.2f} MB)")
        st.audio(solo_audio, format=f'audio/{solo_audio.name.split(".")[-1]}')
        
        # Process audio button
        if not st.session_state.solo_audio_processed:
            if st.button("🎯 Process Audio & Start Reflection", use_container_width=True):
                with st.spinner("🔄 Transcribing your classroom audio..."):
                    try:
                        from core.transcription import transcribe_audio
                        import config
                        
                        client = config.create_client()
                        _, transcription_cfg = config.get_generation_configs()
                        
                        # Transcribe audio
                        transcription = transcribe_audio(
                            solo_audio, 
                            is_teacher=True, 
                            client=client, 
                            config=transcription_cfg
                        )
                        
                        st.session_state.solo_transcription = transcription
                        st.session_state.solo_audio_processed = True
                        st.session_state.solo_chat_history = []
                        
                        st.success("✅ Audio transcribed! Let's begin your reflection.")
                        st.rerun()
                        
                    except Exception as e:
                        st.error(f"❌ Transcription failed: {str(e)}")
                        st.error("Please verify the audio file is not corrupted and try again.")
        else:
            st.success("✅ Audio processed! Continue your reflection below.")
    
    # Chat interface (only show if audio is processed)
    if st.session_state.solo_audio_processed and st.session_state.solo_transcription:
        st.markdown("---")
        st.markdown("### 💬 Reflection Conversation")
        
        # Display chat history
        chat_container = st.container()
        with chat_container:
            # If no messages yet, show welcome message
            if len(st.session_state.solo_chat_history) == 0:
                with st.chat_message("assistant"):
                    st.markdown("👋 Hello! I'm here to help you reflect on your teaching. I've reviewed your classroom audio. **What aspects of this lesson are you most curious to explore?**")
            else:
                # Display existing chat history
                for message in st.session_state.solo_chat_history:
                    with st.chat_message(message["role"]):
                        st.markdown(message["content"])
        
        # Chat input
        user_input = st.chat_input("Share your thoughts or ask a question...")
        
        if user_input:
            # Add user message to chat history
            st.session_state.solo_chat_history.append({
                "role": "user",
                "content": user_input
            })
            
            # Display user message
            with st.chat_message("user"):
                st.markdown(user_input)
            
            # Generate AI response
            with st.chat_message("assistant"):
                with st.spinner("Thinking..."):
                    try:
                        from core.reports import solo_feedback_conversation
                        import config
                        
                        client = config.create_client()
                        solo_cfg = config.get_solo_config()
                        
                        # Generate response
                        response = solo_feedback_conversation(
                            transcription=st.session_state.solo_transcription,
                            chat_history=st.session_state.solo_chat_history[:-1],  # Exclude the just-added user message
                            user_message=user_input,
                            client=client,
                            config=solo_cfg
                        )
                        
                        # Add assistant response to chat history
                        st.session_state.solo_chat_history.append({
                            "role": "assistant",
                            "content": response
                        })
                        
                        st.markdown(response)
                        st.rerun()
                        
                    except Exception as e:
                        st.error(f"❌ Response generation failed: {str(e)}")
        
        # Action buttons
        st.markdown("---")
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("🔄 Clear Conversation", use_container_width=True, help="Start a new reflection with the same audio"):
                if st.session_state.solo_chat_history:
                    # Use a confirmation dialog
                    st.session_state.show_clear_confirm = True
        
        with col2:
            if st.button("📥 Download Session", use_container_width=True, help="Export your reflection conversation"):
                render_solo_download()
        
        # Clear confirmation (using a simple approach)
        if hasattr(st.session_state, 'show_clear_confirm') and st.session_state.show_clear_confirm:
            st.warning("⚠️ Are you sure? This will clear your conversation history but keep your audio transcription.")
            confirm_col1, confirm_col2 = st.columns(2)
            with confirm_col1:
                if st.button("Yes, Clear", type="primary", use_container_width=True):
                    st.session_state.solo_chat_history = []
                    st.session_state.show_clear_confirm = False
                    st.rerun()
            with confirm_col2:
                if st.button("Cancel", use_container_width=True):
                    st.session_state.show_clear_confirm = False
                    st.rerun()

def render_solo_download():
    """Render download options for solo teaching session"""
    from core.reports import create_solo_session_pdf, create_solo_session_text_fallback
    
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    date_formatted = datetime.now().strftime('%B %d, %Y at %I:%M %p')
    
    try:
        # Generate PDF
        session_pdf = create_solo_session_pdf(
            transcription=st.session_state.solo_transcription,
            chat_history=st.session_state.solo_chat_history,
            date_str=date_formatted
        )
        
        st.download_button(
            label="⬇️ Download Session (PDF)",
            data=session_pdf,
            file_name=f"reflection_session_{timestamp}.pdf",
            mime="application/pdf",
            use_container_width=True
        )
    except Exception as e:
        st.error(f"❌ PDF generation failed: {str(e)}")
        st.warning("📄 Downloading text version as fallback...")
        
        # Text fallback
        text_fallback = create_solo_session_text_fallback(
            transcription=st.session_state.solo_transcription,
            chat_history=st.session_state.solo_chat_history,
            date_str=date_formatted
        )
        
        st.download_button(
            label="⬇️ Download Session (TXT - Fallback)",
            data=text_fallback,
            file_name=f"reflection_session_{timestamp}.txt",
            mime="text/plain",
            use_container_width=True
        )

# --- Observation Assistant Header ------------------------------------------
def render_observation_header():
    """Render header for observation assistant tab"""
    st.info("💡 **Getting Started:** Provide at least one input source (teacher audio, observer audio, or observer notes) to generate an observation report.")

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

# --- Audio Uploads ----------------------------------------------------------
def render_audio_uploads():
    """Render audio upload widgets matching old layout exactly"""
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

# --- Text Inputs ------------------------------------------------------------
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
    import re
    
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
            # CRITICAL: Clean any duplicate header text from AI output
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
            
            # Determine if we have teacher audio (check session state)
            has_teacher_audio = hasattr(st.session_state, 'teacher_transcription') and st.session_state.teacher_transcription
            
            report_pdf_bytes = create_observation_report_pdf(
                report_text=cleaned_report,
                teacher_name=teacher_name if teacher_name else "Not specified",
                observer_name=observer_name if observer_name else "Not specified",
                date_str=date_formatted,
                report_length=settings['report_length'].lower(),
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
        # Secondary download: Full Transcript
        if settings['include_transcript'] and (st.session_state.aligned_teacher or st.session_state.aligned_observer):
            try:
                # Determine which PDF format to use based on old logic
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
                transcript_text = f"""TRANSCRIPTION
Generated: {date_formatted}
{'='*80}
"""
                if st.session_state.aligned_teacher:
                    transcript_text += f"""TEACHER AUDIO:
{'='*80}
{st.session_state.aligned_teacher}
"""
                if st.session_state.aligned_observer:
                    transcript_text += f"""{'='*80}
OBSERVER AUDIO/NOTES:
{'='*80}
{st.session_state.aligned_observer}
"""
                transcript_text += f"""{'='*80}
Note: This transcription was created by AI. Please verify all important information for accuracy.
"""
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
        "Powered by Gemini Flash • Music Teacher Observation Assistant v2.4"
        "</p>",
        unsafe_allow_html=True
    )
