# --- Main Application File -------------------------------------------------
# Music Teacher Observation Assistant - Modular Version with Solo Teaching
# Created by Brett Taylor

import streamlit as st

# Import configuration and setup
import config
from ui.components import (
    inject_custom_css,
    render_header,
    render_solo_interface,
    render_observation_header,
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
    layout="wide",
)

# Initialize session state
config.initialize_session_state()

# Inject CSS
inject_custom_css()

# Header
render_header()

# --- Tab Navigation --------------------------------------------------------
tab1, tab2 = st.tabs(["💭 Solo Teaching Feedback", "🎯 Observation Assistant"])

# ===========================================================================
# TAB 1: SOLO TEACHING FEEDBACK (Landing Page)
# ===========================================================================
with tab1:
    render_solo_interface()

# ===========================================================================
# TAB 2: OBSERVATION ASSISTANT
# ===========================================================================
with tab2:
    # Info message
    render_observation_header()
    
    # Sidebar config
    settings = render_sidebar_config()

    # Name inputs
    render_name_inputs()

    # Audio uploads
    teacher_file, observer_file = render_audio_uploads()

    # Text inputs
    observer_notes, evaluation_criteria = render_text_inputs()

    # --- Input Validation ------------------------------------------------------
    def validate_inputs(teacher_file, observer_file, observer_notes):
        """
        Validate that at least one input source is provided.
        Returns (is_valid, error_message, input_summary)
        """
        has_teacher = teacher_file is not None
        has_observer_audio = observer_file is not None
        has_observer_notes = observer_notes and observer_notes.strip()
        
        if not any([has_teacher, has_observer_audio, has_observer_notes]):
            return False, "Please provide at least one input: teacher audio, observer audio, or observer notes.", None
        
        # Build input summary
        inputs = []
        if has_teacher:
            inputs.append("teacher classroom audio")
        if has_observer_audio:
            inputs.append("observer audio commentary")
        if has_observer_notes:
            inputs.append("written observer notes")
        
        input_summary = ", ".join(inputs)
        
        return True, "", input_summary

    def calculate_processing_steps(teacher_file, observer_file, observer_notes):
        """
        Calculate total processing steps based on available inputs.
        Returns total_steps count.
        """
        steps = 2  # Always: Research + Report Generation
        
        if teacher_file:
            steps += 1  # Teacher transcription
        
        if observer_file:
            steps += 1  # Observer transcription
        
        # Alignment step only if we have both teacher and observer content
        has_observer_content = observer_file or (observer_notes and observer_notes.strip())
        if teacher_file and has_observer_content:
            steps += 1  # Alignment
        
        return steps

    # --- Processing Button ----------------------------------------------------
    st.markdown("---")

    # Validate inputs before showing button
    is_valid, validation_error, input_summary = validate_inputs(teacher_file, observer_file, observer_notes)

    if is_valid:
        if st.button("🎯 Generate Observation Report", use_container_width=True):
            
            # Calculate total steps
            total_steps = calculate_processing_steps(teacher_file, observer_file, observer_notes)
            current_step = 0
            
            # Setup client/config
            client = config.create_client()
            generation_cfg, transcription_cfg = config.get_generation_configs()

            # STEP 1: Transcribe Teacher Audio (if provided)
            if teacher_file:
                current_step += 1
                with st.spinner(f"🔄 Step {current_step}/{total_steps}: Transcribing teacher audio..."):
                    try:
                        st.session_state.teacher_transcription = transcribe_audio(
                            teacher_file, is_teacher=True, client=client, config=transcription_cfg
                        )
                        st.success("✅ Teacher audio transcribed!")
                    except Exception as e:
                        st.error(f"❌ Teacher transcription failed: {str(e)}")
                        st.error("Please verify the audio file is not corrupted and try again.")
                        st.stop()
            else:
                st.session_state.teacher_transcription = None

            # STEP 2: Transcribe Observer Audio (if provided)
            observer_content = ""
            if observer_file:
                current_step += 1
                with st.spinner(f"🔄 Step {current_step}/{total_steps}: Transcribing observer audio..."):
                    try:
                        st.session_state.observer_transcription = transcribe_audio(
                            observer_file, is_teacher=False, client=client, config=transcription_cfg
                        )
                        observer_content = st.session_state.observer_transcription
                        st.success("✅ Observer audio transcribed!")
                    except Exception as e:
                        st.error(f"❌ Observer transcription failed: {str(e)}")
                        st.stop()
            
            # Combine observer notes if provided
            if observer_notes and observer_notes.strip():
                observer_content += f"\n\nOBSERVER WRITTEN NOTES:\n{observer_notes}"
                st.success("✅ Observer notes included!")

            # STEP 3: Align Transcriptions (only if we have both teacher and observer content)
            if st.session_state.teacher_transcription and observer_content:
                current_step += 1
                with st.spinner(f"🔄 Step {current_step}/{total_steps}: Aligning observations chronologically..."):
                    try:
                        st.session_state.aligned_teacher, st.session_state.aligned_observer = align_transcriptions(
                            st.session_state.teacher_transcription,
                            observer_content,
                            client,
                            generation_cfg
                        )
                        st.success("✅ Observations aligned chronologically!")
                    except Exception as e:
                        # Fallback: just remove timestamps
                        import re
                        st.session_state.aligned_teacher = re.sub(r'\[\d{2}:\d{2}\]\s*', '', st.session_state.teacher_transcription or "")
                        st.session_state.aligned_observer = re.sub(r'\[\d{2}:\d{2}\]\s*', '', observer_content or "")
                        st.success("✅ Observations aligned chronologically!")
            else:
                # Only one source - just clean timestamps
                import re
                if st.session_state.teacher_transcription:
                    st.session_state.aligned_teacher = re.sub(r'\[\d{2}:\d{2}\]\s*', '', st.session_state.teacher_transcription)
                else:
                    st.session_state.aligned_teacher = ""
                
                if observer_content:
                    st.session_state.aligned_observer = re.sub(r'\[\d{2}:\d{2}\]\s*', '', observer_content)
                else:
                    st.session_state.aligned_observer = ""

            # STEP 4: Research Best Practices
            current_step += 1
            with st.spinner(f"🔄 Step {current_step}/{total_steps}: Researching music education best practices..."):
                try:
                    # Use whichever transcription is available for analysis
                    analysis_text = st.session_state.aligned_teacher if st.session_state.aligned_teacher else st.session_state.aligned_observer
                    
                    if analysis_text:
                        lesson_analysis = analyze_lesson_context(
                            transcription=analysis_text,
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
                    else:
                        best_practices = "Using general music education principles."
                        st.session_state.lesson_analysis = "General music education context"
                        st.success("✅ Using general music education principles!")
                        
                except Exception as e:
                    st.warning(f"⚠️ Research step encountered an issue. Proceeding with analysis: {str(e)}")
                    best_practices = "Using general music education principles."
                    st.session_state.lesson_analysis = "General music education context"

            # STEP 5: Generate Observation Report
            current_step += 1
            with st.spinner(f"🔄 Step {current_step}/{total_steps}: Generating comprehensive observation report..."):
                try:
                    # Build scope instruction
                    scope_instruction = ""
                    if st.session_state.aligned_teacher and st.session_state.aligned_observer:
                        scope_instruction = """
SCOPE: Full classroom analysis with both teacher audio and observer notes available.
- Use teacher audio quotes as evidence
- Prioritize observer observations and find supporting evidence in teacher audio
- Provide comprehensive feedback"""
                    elif st.session_state.aligned_teacher:
                        scope_instruction = """
SCOPE: Analysis based on teacher classroom audio only (no observer notes).
- Use teacher audio quotes as evidence
- Base evaluation on best practices research
- Provide objective analysis of observed teaching practices"""
                    else:
                        scope_instruction = """
SCOPE: Analysis based ONLY on observer notes/audio (no teacher classroom audio).
- Focus on documented observer observations
- Acknowledge limited scope - no direct classroom audio evidence available
- Include disclaimer noting report is based on observer perspective only
- Do NOT quote observer audio - paraphrase their observations instead"""
                    
                    criteria_text = ""
                    if evaluation_criteria:
                        criteria_text = f"\n\nEVALUATION CRITERIA PROVIDED:\n{evaluation_criteria}"
                    
                    sections_text = ", ".join(settings['report_sections']) if settings['report_sections'] else "Summary, Strengths, Areas for Growth"
                    
                    length_instruction = {
                        "Brief": "Keep the report concise (1-2 paragraphs per section).",
                        "Standard": "Provide a thorough analysis with appropriate detail (2-3 paragraphs per section).",
                        "Comprehensive": "Provide an extensive, detailed analysis with multiple examples (3-4+ paragraphs per section).",
                    }
                    
                    report_prompt = f"""GENERATE MUSIC TEACHER OBSERVATION REPORT

CRITICAL FORMATTING INSTRUCTIONS - READ CAREFULLY:
1. DO NOT USE MARKDOWN. Do not use asterisks (**) for bold or italics.
2. Use these exact section headers in ALL CAPS with no formatting: LESSON SUMMARY:, STRENGTHS:, AREAS FOR GROWTH:
3. For each item under STRENGTHS and AREAS FOR GROWTH, provide a short descriptive title on its own line (3-7 words, no special formatting, no brackets, no asterisks)
4. Follow each title with explanatory paragraphs in plain text
5. Never use brackets [ ] or asterisks ** in your output
6. Use plain text only - the PDF formatting will be applied automatically
7. Use quotations ONLY from teacher audio as evidence (if available)
8. Be generous with praise but clear with constructive criticism
9. Maintain professional, neutral language throughout
10. Do NOT include any 'Note:' or 'Disclaimer:' lines in your output. The application adds a single disclaimer in the PDF footer.

OUTPUT FORMAT EXAMPLE (follow this exact style):
LESSON SUMMARY:
[Your paragraph here in plain text]

STRENGTHS:
Positive Classroom Environment
[Paragraph explaining this strength]

Effective Use of Feedback
[Paragraph explaining this strength]

AREAS FOR GROWTH:
Differentiation Strategies
[Paragraph with constructive feedback]

Time Management
[Paragraph with constructive feedback]

{scope_instruction}
{criteria_text}

SECTION REQUIREMENTS:
Include these sections: {sections_text}
{length_instruction[settings['report_length']]}

AVAILABLE DATA:
- Teacher Audio: {'YES' if st.session_state.aligned_teacher else 'NO'}
- Observer Audio/Notes: {'YES' if st.session_state.aligned_observer else 'NO'}
- Input Summary: {input_summary}

LESSON ANALYSIS:
{st.session_state.lesson_analysis}

BEST PRACTICES RESEARCH:
{best_practices}

TEACHER AUDIO TRANSCRIPTION:
{st.session_state.aligned_teacher if st.session_state.aligned_teacher else "Not available - no teacher audio provided."}

OBSERVER OBSERVATIONS:
{st.session_state.aligned_observer if st.session_state.aligned_observer else "No observer notes provided."}

REMEMBER: Output plain text only. No markdown. No asterisks. No brackets. The formatting will be applied during PDF generation. Do NOT include any 'Note:' or 'Disclaimer:' text."""
                    
                    response = client.models.generate_content(
                        model="gemini-flash-latest",
                        contents=[{"role": "user", "parts": [{"text": report_prompt}]}],
                        config=generation_cfg,
                    )
                    
                    st.session_state.observation_report = response.text
                    st.success("✅ Observation report generated!")
                    
                except Exception as e:
                    st.error(f"❌ Report generation failed: {str(e)}")
                    st.stop()

            # Success message
            st.balloons()
            st.success("🎉 **Analysis Complete!** Your observation report is ready for download.")

    else:
        # Show disabled button with error message
        st.button("🎯 Generate Observation Report", disabled=True, use_container_width=True)
        st.error(f"❌ {validation_error}")

    # --- Download Section ------------------------------------------------------
    if st.session_state.observation_report:
        render_downloads(settings)

# --- Footer ----------------------------------------------------------------
render_footer()
