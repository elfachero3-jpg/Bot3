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
1. This is OBSERVER audio - transcribe with timestamps [MM:SS]
2. Label ALL observer speech with "Observer:"
3. IGNORE and DO NOT TRANSCRIBE background voices or conversations
4. Only transcribe the primary observer's voice
5. When music is present, label with "<Music>"
6. Do not make up content - transcribe only what you hear

Example format:
[00:15] Observer: I'm noticing the classroom environment.
[00:30] Observer: The teacher is now engaging with students.
[00:45] <Music>"""

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
8. ONLY output the transcriptions in the specified format
9. VERIFY no student names appear in either transcription

TEACHER AUDIO TRANSCRIPTION:
{teacher_transcription}

OBSERVER CONTENT:
{observer_content}

Format your response exactly as:
ALIGNED_TEACHER:
[transcription here]

ALIGNED_OBSERVER:
[transcription here]"""

# --- Lesson Analysis Prompt ------------------------------------------------
def get_lesson_analysis_prompt(transcription: str) -> str:
    """Generate prompt for analyzing lesson context"""
    return f"""Based on this classroom transcription, identify:
1. Type of music class (choir, band, orchestra, general music, etc.)
2. Grade level (estimate if not obvious)
3. Key teaching focus or musical concepts being taught

TRANSCRIPTION:
{transcription[:2000]}

Provide a brief analysis (2-3 sentences)."""

# --- Best Practices Research Prompt ----------------------------------------
def get_research_prompt(lesson_type: str) -> str:
    """Generate prompt for researching best practices"""
    return f"""You are analyzing a music education classroom observation.

LESSON CONTEXT:
{lesson_type}

Use Google Search to find current best practices, pedagogical approaches, and teaching strategies relevant to this type of music class. Focus on evidence-based teaching methods.
Summarize key best practices in 4-5 bullet points that will inform the observation report."""

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
{criteria_text}

LESSON ANALYSIS:
{lesson_analysis}

BEST PRACTICES RESEARCH:
{best_practices}

TEACHER AUDIO TRANSCRIPTION:
{aligned_teacher}

OBSERVER OBSERVATIONS:
{aligned_observer if aligned_observer else "No observer notes provided."}

Generate a professional observation report following the format:

LESSON SUMMARY:
[Brief overview of what occurred during the lesson]

STRENGTHS:
[Bullet points highlighting effective teaching practices with evidence]

AREAS FOR GROWTH:
[Bullet points with constructive feedback and specific suggestions]

Do not include any meta-commentary or explanations - just the report content."""
