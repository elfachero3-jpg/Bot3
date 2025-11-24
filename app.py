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
    render_footer,
)
from core.transcription import (
    transcribe_audio,
    align_transcriptions,
)
from core.reports import (
    analyze_lesson_context,
    research_best_practices,
    generate_observation_report,
)

# --- Page Setup ------------------------------------------------------------
st.set_page_config(
    page_title="Music Teacher Observation Assistant",
    page_icon="🎵",
    layout="centered",
)

# Initialize session state
config.initialize_session_state()

# Inject CSS
inject_custom_css()

# Header
render_header()

# Sidebar config
settings = render_sidebar_config()

# Name inputs
render_name_inputs()

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

    with st.spinner("🔄 Processing..."):
        # Setup client/config
        client = config.create_client()
        generation_cfg, transcription_cfg = config.get_generation_configs()

        # STEP 1: Transcribe Teacher
        if teacher_file:
            with st.spinner("🎙️ Step 1/5: Transcribing teacher audio..."):
                st.session_state.teacher_transcription = transcribe_audio(
                    teacher_file, is_teacher=True, client=client, config=transcription_cfg
                )
        else:
            st.session_state.teacher_transcription = ""

        # STEP 2: Transcribe or load Observer Notes
        with st.spinner("📝 Step 2/5: Processing observer notes..."):
            if observer_file:
                st.session_state.observer_transcription = transcribe_audio(
                    observer_file, is_teacher=False, client=client, config=transcription_cfg
                )
            else:
                st.session_state.observer_transcription = observer_notes or ""

        # STEP 3: Align Transcriptions
        with st.spinner("🧭 Step 3/5: Aligning transcriptions..."):
            st.session_state.aligned_teacher, st.session_state.aligned_observer = align_transcriptions(
                st.session_state.teacher_transcription,
                st.session_state.observer_transcription,
                client,
                generation_cfg
            )

        # STEP 4: Lesson Analysis + (optional) Best Practices
        with st.spinner("🔬 Step 4/5: Analyzing lesson context..."):
            lesson_analysis = analyze_lesson_context(
                transcription=st.session_state.teacher_transcription,
                client=client,
                config=generation_cfg
            )
            st.session_state.lesson_analysis = lesson_analysis

            try:
                best_practices = research_best_practices(
                    lesson_analysis,
                    client=client,
                    config=generation_cfg
                )
                st.success("✅ Best practices research completed!")
            except Exception as e:
                st.warning(f"⚠️ Research step encountered an issue. Proceeding with analysis: {str(e)}")
                st.session_state.lesson_analysis = st.session_state.get("lesson_analysis") or ""
                best_practices = "Using general music education principles."

        # STEP 5: Generate Observation Report
        with st.spinner("📝 Step 5/5: Generating comprehensive observation report..."):
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
