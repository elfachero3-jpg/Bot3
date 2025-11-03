# --- Report Generation and PDF Creation ------------------------------------
from datetime import datetime
from fpdf import FPDF
from google.genai import types
from .utils import validate_pdf_inputs, sanitize_text_for_pdf, validate_text_content, parse_segments
import prompts

# --- Lesson Analysis -------------------------------------------------------
def analyze_lesson_context(transcription: str, client, config) -> str:
    """
    Analyze the lesson to identify type, grade level, and focus
    
    Args:
        transcription: Teacher audio transcription
        client: Gemini API client
        config: Generation configuration
...
# --- Report Generation Prompt Call ----------------------------------------
def generate_observation_report(
    lesson_analysis: str,
    best_practices: str,
    aligned_teacher: str,
    aligned_observer: str,
    evaluation_criteria: str,
    report_sections: list,
    report_length: str,
    client,
    config
) -> str:
    """
    Generate comprehensive observation report
    
    Args:
        lesson_analysis: Lesson context analysis
        best_practices: Research summary
        aligned_teacher: Aligned teacher transcription
        aligned_observer: Aligned observer notes
        evaluation_criteria: Optional rubric/criteria
        report_sections: Sections to include
        report_length: Brief/Standard/Comprehensive
        client, config: Gemini client and generation config
    
    Returns:
        The generated report text
    """
    try:
        prompt = prompts.get_report_generation_prompt(
            lesson_analysis,
            best_practices,
            aligned_teacher,
            aligned_observer,
            evaluation_criteria,
            report_sections,
            report_length
        )
        
        response = client.models.generate_content(
            model="gemini-flash-latest",
            contents=[types.Content(parts=[types.Part(text=prompt)])],
            config=config,
        )
        return response.text
    except Exception as e:
        raise Exception(f"Report generation failed: {str(e)}")


# --- PDF Generation: Observation Report ------------------------------------
def create_observation_report_pdf(
    report_text: str,
    teacher_name: str,
    observer_name: str,
    date_time: str,
    report_length: str = "standard",
) -> bytes:
    """Generate a professionally formatted observation report PDF"""
    
    # Validate inputs before processing
    is_valid, error_msg = validate_pdf_inputs(report_text, teacher_name, observer_name, date_time)
    if not is_valid:
        raise ValueError(f"PDF input validation failed: {error_msg}")
    
    try:
        # Initialize PDF
        pdf = FPDF()
        pdf.set_auto_page_break(auto=True, margin=15)
        pdf.add_page()
        
        # Margins and layout
        left_margin = 15
        right_margin = 15
        pdf.set_left_margin(left_margin)
        pdf.set_right_margin(right_margin)
        usable = pdf.w - left_margin - right_margin
        line_height = 6

        # Title
        pdf.set_font("Arial", "B", 14)
        pdf.set_x(pdf.l_margin)
        pdf.cell(usable, 10, "Music Teacher Observation Report", ln=True, align="C")
        pdf.ln(3)

        # Date only (string passed into this function)
        pdf.set_font("Arial", "I", 10)
        pdf.set_x(pdf.l_margin)
        pdf.cell(usable, 6, date_time, ln=True, align="C")
        pdf.ln(3)

        # Teacher and Observer names
        pdf.set_font("Arial", "B", 11)
        pdf.set_x(pdf.l_margin)
        if teacher_name and teacher_name != "Not specified":
            pdf.cell(usable, 6, f"Teacher: {teacher_name}", ln=True, align="L")
        pdf.set_x(pdf.l_margin)
        if observer_name and observer_name != "Not specified":
            pdf.cell(usable, 6, f"Observer: {observer_name}", ln=True, align="L")
        pdf.ln(4)

        # Sanitize and render report text
        safe_text = sanitize_text_for_pdf(report_text or "")
        lines = safe_text.splitlines()
        pdf.set_font("Arial", "", 10)

        # Render content with simple heuristics for headers/bullets
        for raw_line in lines:
            line = raw_line.strip()
            if not line:
                pdf.ln(3)
                continue

            # Headers: trailing colon or short ALL CAPS
            if line.endswith(":") or (line.isupper() and len(line.split()) <= 5):
                pdf.set_font("Arial", "B", 11)
                pdf.set_x(pdf.l_margin)
                pdf.multi_cell(usable, line_height, line)
                pdf.set_font("Arial", "", 10)
                pdf.ln(1)
            # Bulleted lines
            elif line.startswith(("- ", "* ", "• ")):
                pdf.set_x(pdf.l_margin)
                pdf.multi_cell(usable, line_height, line)
            else:
                pdf.set_x(pdf.l_margin)
                pdf.multi_cell(usable, line_height, line)

        # Single footer disclaimer at bottom of final page
        pdf.set_font("Arial", "I", 9)
        pdf.set_text_color(100, 100, 100)
        pdf.set_y(-18)
        pdf.set_x(pdf.l_margin)
        pdf.multi_cell(
            usable,
            5,
            "Disclaimer: This observation report was generated by AI and may contain errors. Please review all content for accuracy and use professional judgment.",
            align="C",
        )
        pdf.set_text_color(0, 0, 0)

        return bytes(pdf.output())

    except Exception as e:
        error_type = type(e).__name__
        raise Exception(f"PDF Report generation error ({error_type}): {str(e)}")


# --- PDF Generation: Dual Column Transcript --------------------------------
def create_dual_column_pdf(teacher_text: str, observer_text: str) -> bytes:
    """Generate a two-column PDF from both transcriptions with synchronized rows"""
    
    # Validate transcription content
    is_valid, error = validate_text_content(teacher_text, "Teacher transcription")
    if not is_valid:
        raise ValueError(f"Teacher transcription validation failed: {error}")
    
    is_valid, error = validate_text_content(observer_text, "Observer transcription")
    if not is_valid:
        # Allow empty observer text as fallback
        if "empty" in error.lower():
            observer_text = "No observer audio or notes provided."
        else:
            raise ValueError(f"Observer transcription validation failed: {error}")

    # ... (unchanged transcript PDF logic, including its own disclaimer)
    # The transcript export remains unchanged by design.

# --- Text Fallbacks --------------------------------------------------------
def create_text_fallback(report_text: str, teacher_name: str, observer_name: str, date_time: str) -> str:
    """Create a plain text version as fallback if PDF generation fails"""
    return f"""MUSIC TEACHER OBSERVATION REPORT
{date_time}

Teacher: {teacher_name if teacher_name else 'Not specified'}
Observer: {observer_name if observer_name else 'Not specified'}

{'='*80}

{report_text}

{'='*80}
Note: This report was generated by AI and can contain errors.
"""

def create_transcript_text_fallback(teacher_text: str, observer_text: str, date_time: str) -> str:
    """Create a text fallback version of the transcript export"""
    return f"""MUSIC TEACHER OBSERVATION - FULL TRANSCRIPT
{date_time}

TEACHER AUDIO:
{'='*80}

{teacher_text}

{'='*80}
OBSERVER AUDIO/NOTES:
{'='*80}

{observer_text if observer_text else "No observer audio or notes provided."}

{'='*80}
Note: This transcription was created by AI. Please verify all important information for accuracy.
"""
