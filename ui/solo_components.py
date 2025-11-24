# --- Solo Teaching Interface Components -----------------------------------
import streamlit as st
from datetime import datetime

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
            # Display existing chat history (AI generates its own first message now)
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
                        from core.analysis import solo_feedback_conversation
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
        
        # If chat history is empty (just transcribed), generate first AI message automatically
        elif len(st.session_state.solo_chat_history) == 0:
            with st.chat_message("assistant"):
                with st.spinner("Analyzing your lesson..."):
                    try:
                        from core.analysis import solo_feedback_conversation
                        import config
                        
                        client = config.create_client()
                        solo_cfg = config.get_solo_config()
                        
                        # Generate initial response with empty user message (triggers first message format)
                        response = solo_feedback_conversation(
                            transcription=st.session_state.solo_transcription,
                            chat_history=[],
                            user_message="",  # Empty message triggers first message format
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
                        st.error(f"❌ Initial response generation failed: {str(e)}")
        
        # Action buttons
        st.markdown("---")
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("🔄 Clear Conversation", use_container_width=True, help="Start a new reflection with the same audio"):
                if st.session_state.solo_chat_history:
                    st.session_state.show_clear_confirm = True
        
        with col2:
            if st.button("📥 Download Session", use_container_width=True, help="Export your reflection conversation"):
                render_solo_download()
        
        # Clear confirmation
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
    from core.pdf_generation import create_solo_session_pdf
    from core.text_exports import create_solo_session_text_fallback
    
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
