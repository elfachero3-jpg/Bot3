# --- All Prompt Templates --------------------------------------------------

# --- Transcription Prompts -------------------------------------------------
TEACHER_TRANSCRIPTION_PROMPT = """CRITICAL INSTRUCTIONS:
1. Transcribe this entire audio file accurately with timestamps [MM:SS]
2. Label speech: "Teacher:" for teacher, "Student:" for students, "<Music>" for music
3. NEVER include student names - only use "Student:" label
4. Use voice recognition to distinguish teacher from other voices
5. Provide clear formatting with line breaks between segments
6. Do not make up content - transcribe only what you hear

Example format:
[00:15] Teacher: Welcome to class today.
[00:22] Student: Thank you for having us.
[00:30] <Music>"""

...
# --- Alignment Prompt ------------------------------------------------------
def get_alignment_prompt(teacher_transcription: str, observer_content: str) -> str:
    """Generate alignment prompt for chronological synchronization"""
    return f"""CRITICAL INSTRUCTIONS FOR ALIGNMENT:
You have two transcriptions with timestamps.
Your task:
1. Align them chronologically based on timestamps
2. Remove ALL timestamps from the output
3. Present clean transcriptions side by side
4. For Teacher Audio: Keep "Teacher:" and "Student:" labels and "<Music>"
5. For Observer Audio: Keep ONLY "Observer:" labels and "<Music>"
6. Ensure matching moments appear at similar positions
7. Do NOT include any introductory text or explanations
...
[00:45] <Music>"""

# --- Report Generation Prompt ----------------------------------------------
def get_report_generation_prompt(
    lesson_analysis: str,
    best_practices: str,
    aligned_teacher: str,
    aligned_observer: str,
    evaluation_criteria: str,
    report_sections: list,
    report_length: str
) -> str:
    """Generate comprehensive observation report prompt"""
    
    criteria_text = ""
    if evaluation_criteria:
        criteria_text = f"\n\nEVALUATION CRITERIA PROVIDED:\n{evaluation_criteria}"
    
    sections_text = ", ".join(report_sections) if report_sections else "Summary, Strengths, Areas for Growth"
    
    length_instruction = {
        "Brief": "Keep the report concise (1-2 paragraphs per section).",
        "Standard": "Provide a thorough analysis with appropriate detail (2-3 paragraphs per section).",
        "Comprehensive": "Provide an extensive, detailed analysis with multiple examples (3-4+ paragraphs per section).",
    }
    
    return f"""GENERATE MUSIC TEACHER OBSERVATION REPORT

CRITICAL INSTRUCTIONS:
1. Use quotations ONLY from teacher audio as evidence - NEVER quote observer
2. Be generous with praise but clear with constructive criticism
3. Maintain professional, neutral language throughout
4. If observer notes are provided, PRIORITIZE their observations and find evidence
5. Base evaluation on provided criteria, or use best practices research
6. Include these sections: {sections_text}
7. {length_instruction[report_length]}
8. VERIFY all quoted evidence comes from teacher audio, not observer
9. Do NOT include any 'Note:' or 'Disclaimer:' lines in your output. The application appends a single disclaimer at the bottom of the exported PDF.
{criteria_text}

LESSON ANALYSIS:
{lesson_analysis}

BEST PRACTICES:
{best_practices}

ALIGNED TEACHER TRANSCRIPTION (EVIDENCE SOURCE):
{aligned_teacher}

ALIGNED OBSERVER NOTES (CONTEXT ONLY):
{aligned_observer if aligned_observer else "No observer notes provided."}

Generate a professional observation report following the format:

LESSON SUMMARY:
[Brief overview of what occurred during the lesson]

STRENGTHS:
[Bullet points highlighting effective teaching practices with evidence]

AREAS FOR GROWTH:
[Bullet points with constructive feedback and specific suggestions]

Do not include any meta-commentary or explanations - just the report content."""
