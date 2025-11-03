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
from core.transcription import (
    transcribe_audio_file,
    align_speakers
)
from core.reports import (
    analyze_lesson_context,
    research_best_practices,
    generate_observation_report
)

# --- App Initialization ----------------------------------------------------
st.set_page_config(**config.PAGE_CONFIG)
# moved earlier so CSS can read the choice on first load
config.initialize_session_state()
inject_custom_css()

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
if st.button("🚀 Generate Observation Report", type="primary", use_container_width=True):
    if not teacher_file and not observer_notes and not evaluation_criteria:
        st.warning("Please provide at least a teacher audio file, observer notes, or evaluation criteria.")
        st.stop()

    with st.spinner("🔄 Processing inputs..."):
        # STEP 1: Transcribe Teacher Audio
        teacher_content = ""
        if teacher_file:
            with st.spinner("🔄 Step 1/5: Transcribing teacher audio..."):
                try:
                    teacher_content = transcribe_audio_file(
                        file_obj=teacher_file,
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
                    observer_content = transcribe_audio_file(
                        file_obj=observer_file,
                        client=client,
                        config=transcription_cfg
                    )
                    st.success("✅ Observer audio transcribed!")
                except Exception as e:
                    st.error(f"❌ {str(e)}")
                    st.stop()

        # STEP 3: Align Speakers (if teacher audio exists)
        if teacher_content:
            with st.spinner("🔄 Step 3/5: Aligning speakers..."):
                try:
                    aligned_teacher, aligned_observer = align_speakers(teacher_content, observer_content)
                    st.session_state.aligned_teacher = aligned_teacher
                    st.session_state.aligned_observer = aligned_observer
                    st.success("✅ Speaker alignment complete!")
                except Exception as e:
                    st.error(f"❌ {str(e)}")
                    st.stop()

        # STEP 4: Analyze Lesson Context
        with st.spinner("🔄 Step 4/5: Analyzing lesson context..."):
            try:
                lesson_analysis = analyze_lesson_context(
                    teacher_content=teacher_content,
                    observer_notes=observer_notes,
                    evaluation_criteria=evaluation_criteria,
                    settings=settings,
                    client=client,
                    generation_cfg=generation_cfg
                )
                st.session_state.lesson_analysis = lesson_analysis
                st.success("✅ Lesson context analyzed!")
            except Exception as e:
                st.error(f"❌ {str(e)}")
                st.stop()

        # STEP 5: Generate Observation Report
        with st.spinner("📝 Step 5/5: Generating observation report..."):
            try:
                report_pdf = generate_observation_report(
                    teacher_name=teacher_name,
                    observer_name=observer_name,
                    include_transcript=settings["include_transcript"],
                    report_sections=settings["report_sections"],
                    report_length=settings["report_length"],
                    lesson_analysis=st.session_state.lesson_analysis,
                    aligned_teacher=st.session_state.aligned_teacher,
                    aligned_observer=st.session_state.aligned_observer
                )
                st.session_state.observation_report = report_pdf
            except Exception as e:
                st.error(f"❌ {str(e)}")
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
