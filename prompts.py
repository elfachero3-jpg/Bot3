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

OBSERVER_TRANSCRIPTION_PROMPT = """CRITICAL INSTRUCTIONS:
1. Transcribe this entire audio file accurately with timestamps [MM:SS]
2. Label ALL speech as "Observer:" - this is the observer's verbal notes
3. Include "<Music>" tags for any background music or classroom audio
4. NEVER include student names - only use generic references
5. Provide clear formatting with line breaks between segments
6. Do not make up content - transcribe only what you hear
7. This is observer commentary, not classroom audio

Example format:
[00:15] Observer: The teacher is greeting students at the door.
[00:30] Observer: Students are settling into their seats quietly.
[00:45] <Music>
[01:00] Observer: The teacher begins the lesson with a clear objective."""

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
8. Output ONLY in this exact format:

ALIGNED_TEACHER:
[Clean teacher transcription without timestamps]

ALIGNED_OBSERVER:
[Clean observer transcription without timestamps]

TEACHER TRANSCRIPTION WITH TIMESTAMPS:
{teacher_transcription}

OBSERVER CONTENT WITH TIMESTAMPS:
{observer_content}

Remember: Output must start with "ALIGNED_TEACHER:" and include "ALIGNED_OBSERVER:" section. No other text."""

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

SCOPE INSTRUCTION:
{_get_scope_instruction(aligned_teacher, aligned_observer)}
{criteria_text}

SECTION REQUIREMENTS:
Include these sections: {sections_text}
{length_instruction[report_length]}

AVAILABLE DATA:
- Teacher Audio: {'YES' if aligned_teacher else 'NO'}
- Observer Audio/Notes: {'YES' if aligned_observer else 'NO'}

LESSON ANALYSIS:
{lesson_analysis}

BEST PRACTICES RESEARCH:
{best_practices}

TEACHER AUDIO TRANSCRIPTION:
{aligned_teacher if aligned_teacher else "Not available - no teacher audio provided."}

OBSERVER OBSERVATIONS:
{aligned_observer if aligned_observer else "No observer notes provided."}

REMEMBER: Output plain text only. No markdown. No asterisks. No brackets. The formatting will be applied during PDF generation. Do NOT include any 'Note:' or 'Disclaimer:' text."""

def _get_scope_instruction(aligned_teacher: str, aligned_observer: str) -> str:
    """Helper function to determine scope instruction based on available inputs"""
    if aligned_teacher and aligned_observer:
        return """
SCOPE: Full classroom analysis with both teacher audio and observer notes available.
- Use teacher audio quotes as evidence
- Prioritize observer observations and find supporting evidence in teacher audio
- Provide comprehensive feedback"""
    elif aligned_teacher:
        return """
SCOPE: Analysis based on teacher classroom audio only (no observer notes).
- Use teacher audio quotes as evidence
- Base evaluation on best practices research
- Provide objective analysis of observed teaching practices"""
    else:
        return """
SCOPE: Analysis based ONLY on observer notes/audio (no teacher classroom audio).
- Focus on documented observer observations
- Acknowledge limited scope - no direct classroom audio evidence available
- Include disclaimer noting report is based on observer perspective only
- Do NOT quote observer audio - paraphrase their observations instead"""
