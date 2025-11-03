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
    
    Returns:
        Lesson analysis text
    """
    try:
        prompt = prompts.get_lesson_analysis_prompt(transcription)
        response = client.models.generate_content(
            model="gemini-flash-latest",
            contents=[types.Content(parts=[types.Part(text=prompt)])],
            config=config,
        )
        return response.text
    except Exception as e:
        return "General music education class"


# --- Best Practices Research -----------------------------------------------
def research_best_practices(lesson_type: str, client, config) -> str:
    """
    Research music education best practices via Google Search
    
    Args:
        lesson_type: Type of lesson identified
        client: Gemini API client
        config: Generation configuration (with search tool)
    
    Returns:
        Best practices summary
    """
    try:
        prompt = prompts.get_research_prompt(lesson_type)
        response = client.models.generate_content(
            model="gemini-flash-latest",
            contents=[types.Content(parts=[types.Part(text=prompt)])],
            config=config,
        )
        return response.text
    except Exception as e:
        return "Using general music education principles."


# --- Observation Report Generation -----------------------------------------
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
        best_practices: Research findings
        aligned_teacher: Aligned teacher transcription
        aligned_observer: Aligned observer transcription
        evaluation_criteria: Custom criteria (if provided)
        report_sections: Sections to include
        report_length: Brief, Standard, or Comprehensive
        client: Gemini API client
        config: Generation configuration
    
    Returns:
        Observation report text
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
        pdf = FPDF()
        pdf.add_page()
        pdf.set_margins(12, 12, 12)
        pdf.set_auto_page_break(auto=True, margin=15)

        # Sanitize inputs
        report_text = sanitize_text_for_pdf(report_text)
        teacher_name = sanitize_text_for_pdf(teacher_name) if teacher_name else "Not specified"
        observer_name = sanitize_text_for_pdf(observer_name) if observer_name else "Not specified"
        date_time = sanitize_text_for_pdf(date_time)

        usable = pdf.epw  # effective page width

        # Title
        pdf.set_font("Arial", "B", 16)
        pdf.set_x(pdf.l_margin)
        pdf.cell(usable, 10, "Music Teacher Observation Report", ln=True, align="C")
        pdf.ln(3)

        # Date and Time
        pdf.set_font("Arial", "I", 10)
        pdf.set_x(pdf.l_margin)
        pdf.cell(usable, 6, date_time, ln=True, align="C")
        pdf.ln(3)

        # AI Disclaimer at top
        pdf.set_font("Arial", "I", 9)
        pdf.set_text_color(100, 100, 100)
        pdf.set_x(pdf.l_margin)
        pdf.multi_cell(
            usable,
            5,
            "Disclaimer: This observation report was generated by AI and may contain errors. "
            "Please review all content for accuracy and use professional judgment when applying feedback.",
            align="C",
        )
        pdf.set_text_color(0, 0, 0)
        pdf.ln(5)

        # Teacher and Observer names
        pdf.set_font("Arial", "B", 11)
        pdf.set_x(pdf.l_margin)
        if teacher_name and teacher_name != "Not specified":
            pdf.cell(usable, 6, f"Teacher: {teacher_name}", ln=True, align="L")
        pdf.set_x(pdf.l_margin)
        if observer_name and observer_name != "Not specified":
            pdf.cell(usable, 6, f"Observer: {observer_name}", ln=True, align="L")
        pdf.ln(5)

        # Report content
        pdf.set_font("Arial", "", 10)
        line_height = 5

        lines = report_text.split("\n")
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

        # Required note at the bottom
        pdf.ln(4)
        pdf.set_font("Arial", "I", 9)
        pdf.set_text_color(100, 100, 100)
        pdf.set_x(pdf.l_margin)
        pdf.multi_cell(
            usable,
            5,
            "Note: This report was generated by AI and can contain errors.",
            align="L",
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
    
    try:
        pdf = FPDF()
        pdf.add_page()
        pdf.set_auto_page_break(auto=False)
        pdf.set_margins(12, 12, 12)

        # Sanitize inputs
        teacher_text = sanitize_text_for_pdf(teacher_text)
        observer_text = sanitize_text_for_pdf(observer_text)

        # Title
        pdf.set_font("Arial", "B", 16)
        pdf.cell(0, 10, "Aligned Audio Transcription", ln=True, align="C")
        pdf.ln(3)

        # Date
        pdf.set_font("Arial", "I", 10)
        pdf.cell(0, 6, f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", ln=True, align="C")
        pdf.ln(3)

        # AI Disclaimer
        pdf.set_font("Arial", "I", 9)
        pdf.set_text_color(100, 100, 100)
        pdf.multi_cell(0, 5, "Disclaimer: This transcription was created by AI. Please verify all important information for accuracy.", align="C")
        pdf.set_text_color(0, 0, 0)
        pdf.ln(5)

        # Column headers
        pdf.set_font("Arial", "B", 11)
        pdf.cell(95, 6, "Teacher Audio", border=1, align="C")
        pdf.cell(95, 6, "Observer Audio/Notes", border=1, align="C", ln=True)
        pdf.ln(2)

        # Parse segments
        teacher_segments = parse_segments(teacher_text)
        observer_segments = parse_segments(observer_text)
        max_segments = max(len(teacher_segments), len(observer_segments))

        column_width = 92
        left_x = 9
        right_x = 109
        line_height = 4
        page_bottom = 280

        pdf.set_font("Arial", "", 9)
        for i in range(max_segments):
            teacher_seg = teacher_segments[i] if i < len(teacher_segments) else ""
            observer_seg = observer_segments[i] if i < len(observer_segments) else ""

            if pdf.get_y() > page_bottom:
                pdf.add_page()
                pdf.set_font("Arial", "", 9)

            y_start = pdf.get_y()

            # Left column (Teacher)
            pdf.set_xy(left_x, y_start)
            if teacher_seg:
                if teacher_seg.startswith("Teacher:") or teacher_seg.startswith("Student:"):
                    pdf.set_font("Arial", "B", 9)
                    pdf.multi_cell(column_width, line_height, teacher_seg)
                    pdf.set_font("Arial", "", 9)
                elif teacher_seg.startswith("<Music>"):
                    pdf.set_font("Arial", "I", 9)
                    pdf.multi_cell(column_width, line_height, teacher_seg)
                    pdf.set_font("Arial", "", 9)
                else:
                    pdf.multi_cell(column_width, line_height, teacher_seg)
            teacher_y_end = pdf.get_y()

            # Right column (Observer)
            pdf.set_xy(right_x, y_start)
            if observer_seg:
                if observer_seg.startswith("Observer:"):
                    pdf.set_font("Arial", "B", 9)
                    pdf.multi_cell(column_width, line_height, observer_seg)
                    pdf.set_font("Arial", "", 9)
                elif observer_seg.startswith("<Music>"):
                    pdf.set_font("Arial", "I", 9)
                    pdf.multi_cell(column_width, line_height, observer_seg)
                    pdf.set_font("Arial", "", 9)
                else:
                    pdf.multi_cell(column_width, line_height, observer_seg)
            observer_y_end = pdf.get_y()

            pdf.set_y(max(teacher_y_end, observer_y_end))
            pdf.ln(2)

        return bytes(pdf.output())

    except Exception as e:
        error_type = type(e).__name__
        raise Exception(f"PDF Transcript generation error ({error_type}): {str(e)}")


# --- Text Fallback ---------------------------------------------------------
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
This is a plain text version provided as a fallback.
"""


def create_transcript_text_fallback(teacher_text: str, observer_text: str, date_time: str) -> str:
    """Create a plain text transcript as fallback if PDF generation fails"""
    return f"""ALIGNED AUDIO TRANSCRIPTION
Generated: {date_time}

{'='*80}
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
