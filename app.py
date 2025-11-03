# --- Main Application File -------------------------------------------------
# Music Teacher Observation Assistant - Modular Version
# Created by Brett Taylor

import streamlit as st

# Import configuration and setup
import config
from ui.components import (
    inject_custom_css,
    render_header,
    render_sidebar_config,
    render_name_inputs,
    render_audio_uploads,
    render_text_inputs,
    render_downloads,
    render_footer
)
from core.transcription import transcribe_audio, align_transcriptions
from core.reports import (
    analyze_lesson_context,
    research_best_practices,
    generate_observation_report
)

# --- App Initialization ----------------------------------------------------
st.set_page_config(**config.PAGE_CONFIG)
inject_custom_css()
config.initialize_session_state()

# Create API client and configs
client = config.create_client()
generation_cfg, transcription_cfg = config.get_generation_configs()

# --- UI Rendering ----------------------------------------------------------
render_header()

# Sidebar configuration
settings = render_sidebar_config()

# Main content area
st.markdown("## 📋 Observation Data")

# Name inputs
teacher_name, observer_name = render_name_inputs()
# Store in session state for download component
st.session_state.teacher_name = teacher_name
st.session_state.observer_name = observer_name

st.markdown("---")

# Audio uploads
teacher_file, observer_file = render_audio_uploads()

st.markdown("---")

# Text inputs
observer_notes, evaluation_criteria = render_text_inputs()

# --- Processing Logic ------------------------------------------------------
st.markdown("---")

if teacher_file:
    if st.button("🎯 Generate Observation Report", use_container_width=True):
        
        # STEP 1: Transcribe Teacher Audio
        with st.spinner("🔄 Step 1/5: Transcribing teacher audio..."):
            try:
                st.session_state.teacher_transcription = transcribe_audio(
                    teacher_file, 
                    is_teacher=True, 
                    client=client, 
                    config=transcription_cfg
                )
                st.success("✅ Teacher audio transcribed!")
            except Exception as e:
                st.error(f"❌ {str(e)}")
                st.error("Please verify the audio file is not corrupted and try again.")
                st.stop()

        # STEP 2: Transcribe Observer Audio (if provided)
        observer_content = ""
        if observer_file:
            with st.spinner("🔄 Step 2/5: Transcribing observer audio..."):
                try:
                    st.session_state.observer_transcription = transcribe_audio(
                        observer_file,
                        is_teacher=False,
                        client=client,
                        config=transcription_cfg
                    )
                    observer_content = st.session_state.observer_transcription
                    st.success("✅ Observer audio transcribed!")
                except Exception as e:
                    st.warning(f"⚠️ Observer audio skipped: {str(e)}")

        # Combine observer notes if provided
        if observer_notes:
            observer_content += f"\n\nOBSERVER WRITTEN NOTES:\n{observer_notes}"
            st.success("✅ Observer notes included!")

        # STEP 3: Align Transcriptions
        with st.spinner("🔄 Step 3/5: Aligning observations chronologically..."):
            try:
                aligned_teacher, aligned_observer = align_transcriptions(
                    st.session_state.teacher_transcription,
                    observer_content,
                    client=client,
                    config=transcription_cfg
                )
                st.session_state.aligned_teacher = aligned_teacher
                st.session_state.aligned_observer = aligned_observer
                st.success("✅ Observations aligned chronologically!")
            except Exception as e:
                st.error(f"❌ Alignment failed: {str(e)}")
                st.stop()

        # STEP 4: Research Best Practices
        with st.spinner("🔄 Step 4/5: Researching music education best practices..."):
            try:
                lesson_analysis = analyze_lesson_context(
                    st.session_state.aligned_teacher,
                    client=client,
                    config=generation_cfg
                )
                st.session_state.lesson_analysis = lesson_analysis

                best_practices = research_best_practices(
                    lesson_analysis,
                    client=client,
                    config=generation_cfg
                )
                st.success("✅ Best practices research completed!")
            except Exception as e:
                st.warning(f"⚠️ Research step encountered an issue. Proceeding with analysis: {str(e)}")
                best_practices = "Using general music education principles."

        # STEP 5: Generate Observation Report
        with st.spinner("🔄 Step 5/5: Generating comprehensive observation report..."):
            try:
                st.session_state.observation_report = generate_observation_report(
                    lesson_analysis=st.session_state.lesson_analysis,
                    best_practices=best_practices,
                    aligned_teacher=st.session_state.aligned_teacher,
                    aligned_observer=st.session_state.aligned_observer,
                    evaluation_criteria=evaluation_criteria,
                    report_sections=settings['report_sections'],
                    report_length=settings['report_length'],
                    client=client,
                    config=generation_cfg
                )
                st.success("✅ Observation report generated!")
            except Exception as e:
                st.error(f"❌ Report generation failed: {str(e)}")
                st.stop()

        # Success message
        st.balloons()
        st.success("🎉 **Analysis Complete!** Your observation report is ready for download.")

# --- Download Section ------------------------------------------------------
if st.session_state.observation_report:
    render_downloads(settings)
else:
    st.info("👆 Upload teacher audio and click 'Generate Observation Report' to begin analysis.")

# --- Footer ----------------------------------------------------------------
render_footer()
