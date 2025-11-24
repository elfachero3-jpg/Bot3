# --- PDF Generation Functions ----------------------------------------------
from datetime import datetime
from fpdf import FPDF
from .utils import validate_pdf_inputs, sanitize_text_for_pdf, validate_text_content, parse_segments

# --- PDF Generation: Observation Report ------------------------------------
def create_observation_report_pdf(
    report_text: str,
    teacher_name: str,
    observer_name: str,
    date_str: str,
    report_length: str = "standard",
    has_teacher_audio: bool = True,
) -> bytes:
    """Generate a professionally formatted observation report PDF"""
    
    # Validate inputs before processing
    is_valid, error_msg = validate_pdf_inputs(report_text, teacher_name, observer_name, date_str)
    if not is_valid:
        raise ValueError(f"PDF input validation failed: {error_msg}")
    
    try:
        pdf = FPDF()
        pdf.add_page()
        pdf.set_margins(12, 12, 12)
        pdf.set_auto_page_break(auto=True, margin=12)

        # Sanitize inputs
        report_text = sanitize_text_for_pdf(report_text)
        teacher_name = sanitize_text_for_pdf(teacher_name) if teacher_name else "Not specified"
        observer_name = sanitize_text_for_pdf(observer_name) if observer_name else "Not specified"
        date_str = sanitize_text_for_pdf(date_str)

        # CRITICAL: Remove markdown formatting from report text
        import re
        # Remove bold markers
        report_text = re.sub(r'\*\*(.+?)\*\*', r'\1', report_text)
        # Remove italic markers  
        report_text = re.sub(r'\*(.+?)\*', r'\1', report_text)

        usable = pdf.epw

        # Title
        pdf.set_font("Arial", "B", 16)
        pdf.set_x(pdf.l_margin)
        pdf.cell(usable, 10, "Music Teacher Observation Report", ln=True, align="C")
        pdf.ln(3)

        # Date only (no time)
        pdf.set_font("Arial", "I", 10)
        pdf.set_x(pdf.l_margin)
        pdf.cell(usable, 6, date_str, ln=True, align="C")
        pdf.ln(5)

        # Scope disclaimer if no teacher audio
        if not has_teacher_audio:
            pdf.set_font("Arial", "I", 9)
            pdf.set_text_color(100, 100, 100)
            pdf.set_x(pdf.l_margin)
            pdf.multi_cell(
                usable,
                5,
                "Note: This report is based on observer notes/audio without teacher classroom audio evidence.",
                align="L",
            )
            pdf.set_text_color(0, 0, 0)
            pdf.ln(3)

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

            # Check if line is an ALL CAPS section header (main sections)
            # Must be all uppercase and end with colon
            if line.isupper() and line.endswith(":") and len(line.split()) <= 5:
                pdf.set_font("Arial", "B", 11)
                pdf.set_x(pdf.l_margin)
                pdf.multi_cell(usable, line_height, line)
                pdf.set_font("Arial", "", 10)
                pdf.ln(2)
            # Check if line is a subsection header (short descriptive title)
            # Characteristics: 2-12 words, starts with capital, doesn't end with sentence punctuation
            # Not a bullet, not part of a sentence (doesn't start with common sentence words)
            elif (len(line.split()) >= 2 and len(line.split()) <= 12 and 
                  not line.startswith(("- ", "* ", "• ", "The ", "This ", "When ", "After ", "Before ", "During ", "To ", "In ", "As ", "For ", "With ")) and
                  not line.endswith((".","!","?",",",";")) and
                  line[0].isupper() and
                  not line.startswith(("Teacher:", "Student:", "Observer:"))):
                pdf.set_font("Arial", "B", 10)
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

        # Add disclaimer immediately after content (not at bottom of page)
        pdf.ln(8)  # Small space before disclaimer
        pdf.set_font("Arial", "I", 9)
        pdf.set_text_color(100, 100, 100)
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


# --- PDF Generation: Solo Teaching Session Export -------------------------
def create_solo_session_pdf(
    transcription: str,
    chat_history: list,
    date_str: str
) -> bytes:
    """Generate a PDF export of solo teaching reflection session"""
    
    try:
        pdf = FPDF()
        pdf.add_page()
        pdf.set_margins(12, 12, 12)
        pdf.set_auto_page_break(auto=True, margin=12)

        # Sanitize inputs
        transcription = sanitize_text_for_pdf(transcription)
        date_str = sanitize_text_for_pdf(date_str)

        usable = pdf.epw

        # Title
        pdf.set_font("Arial", "B", 16)
        pdf.set_x(pdf.l_margin)
        pdf.cell(usable, 10, "Solo Teaching Reflection Session", ln=True, align="C")
        pdf.ln(3)

        # Date
        pdf.set_font("Arial", "I", 10)
        pdf.set_x(pdf.l_margin)
        pdf.cell(usable, 6, date_str, ln=True, align="C")
        pdf.ln(5)

        # Conversation Section
        pdf.set_font("Arial", "B", 12)
        pdf.set_x(pdf.l_margin)
        pdf.cell(usable, 6, "REFLECTION CONVERSATION:", ln=True)
        pdf.ln(3)

        # Chat history
        pdf.set_font("Arial", "", 10)
        line_height = 5

        for msg in chat_history:
            role_label = "You: " if msg["role"] == "user" else "Coach: "
            content = sanitize_text_for_pdf(msg["content"])
            
            # Role label in bold
            pdf.set_font("Arial", "B", 10)
            pdf.set_x(pdf.l_margin)
            pdf.cell(usable, line_height, role_label, ln=True)
            
            # Message content
            pdf.set_font("Arial", "", 10)
            pdf.set_x(pdf.l_margin)
            pdf.multi_cell(usable, line_height, content)
            pdf.ln(3)

        # Transcription section
        pdf.ln(5)
        pdf.set_font("Arial", "B", 12)
        pdf.set_x(pdf.l_margin)
        pdf.cell(usable, 6, "CLASSROOM AUDIO TRANSCRIPTION:", ln=True)
        pdf.ln(3)

        pdf.set_font("Arial", "", 9)
        pdf.set_x(pdf.l_margin)
        pdf.multi_cell(usable, 4, transcription)

        # Add disclaimer
        pdf.ln(8)
        pdf.set_font("Arial", "I", 9)
        pdf.set_text_color(100, 100, 100)
        pdf.set_x(pdf.l_margin)
        pdf.multi_cell(
            usable,
            5,
            "Disclaimer: This reflection session and transcription were generated by AI and may contain errors. Please review all content for accuracy and use professional judgment.",
            align="C",
        )
        pdf.set_text_color(0, 0, 0)

        return bytes(pdf.output())

    except Exception as e:
        error_type = type(e).__name__
        raise Exception(f"PDF Solo Session generation error ({error_type}): {str(e)}")


# --- PDF Generation: Dual Column Transcript --------------------------------
def create_dual_column_pdf(teacher_text: str, observer_text: str) -> bytes:
    """Generate a two-column PDF from both transcriptions with synchronized rows"""
    
    is_valid, error = validate_text_content(teacher_text, "Teacher transcription")
    if not is_valid:
        raise ValueError(f"Teacher transcription validation failed: {error}")
    
    is_valid, error = validate_text_content(observer_text, "Observer transcription")
    if not is_valid:
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
        pdf.cell(0, 6, f"Generated: {datetime.now().strftime('%B %d, %Y')}", ln=True, align="C")
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

        # Add disclaimer immediately after content
        pdf.ln(5)
        pdf.set_font("Arial", "I", 8)
        pdf.set_text_color(100, 100, 100)
        pdf.set_x(12)
        usable_width = pdf.w - 24
        pdf.multi_cell(
            usable_width,
            4,
            "Note: This transcription was created by AI. Please verify all important information for accuracy.",
            align="C",
        )
        pdf.set_text_color(0, 0, 0)

        return bytes(pdf.output())

    except Exception as e:
        error_type = type(e).__name__
        raise Exception(f"PDF Transcript generation error ({error_type}): {str(e)}")
