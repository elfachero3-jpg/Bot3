# --- Utility Functions: Text Validation & Sanitization --------------------
import re

# --- Text Validation -------------------------------------------------------
def validate_text_content(text: str, field_name: str = "content") -> tuple[bool, str]:
    """
    Validate text content before PDF generation.
    Returns (is_valid, error_message)
    """
    if not text:
        return False, f"{field_name} is empty or None"
    
    if not isinstance(text, str):
        return False, f"{field_name} must be a string, got {type(text)}"
    
    if len(text.strip()) == 0:
        return False, f"{field_name} contains only whitespace"
    
    # Check for reasonable length (prevent memory issues)
    if len(text) > 500000:  # ~500KB of text
        return False, f"{field_name} is too long ({len(text)} chars). Maximum is 500,000 characters."
    
    return True, ""


def validate_pdf_inputs(report_text: str, teacher_name: str, observer_name: str, date_time: str) -> tuple[bool, str]:
    """
    Validate all inputs before PDF generation.
    Returns (is_valid, error_message)
    """
    # Validate report text
    is_valid, error = validate_text_content(report_text, "Report text")
    if not is_valid:
        return False, f"Report validation failed: {error}"
    
    # Validate names (can be empty, but must be strings)
    if teacher_name is not None and not isinstance(teacher_name, str):
        return False, "Teacher name must be a string"
    
    if observer_name is not None and not isinstance(observer_name, str):
        return False, "Observer name must be a string"
    
    # Validate date/time
    if not date_time or not isinstance(date_time, str):
        return False, "Date/time must be a non-empty string"
    
    # Test encoding cycle
    try:
        sanitized = sanitize_text_for_pdf(report_text[:1000])  # Test first 1000 chars
        if not sanitized:
            return False, "Text sanitization produced empty result"
    except Exception as e:
        return False, f"Text sanitization failed: {str(e)}"
    
    return True, ""


# --- Text Sanitization -----------------------------------------------------
def sanitize_text_for_pdf(text: str) -> str:
    """
    Replace/strip characters not supported by core PDF fonts (Latin-1)
    and add soft break opportunities to very long tokens so MultiCell can wrap.
    """
    if not text:
        return ""

    # Comprehensive Unicode to ASCII/Latin-1 replacement map
    replacements = {
        # Dashes
        "\u2014": "-",   # em dash —
        "\u2013": "-",   # en dash –
        "\u2012": "-",   # figure dash ‒
        "\u2011": "-",   # non-breaking hyphen ‑
        
        # Quotes
        "\u2018": "'",   # left single quote '
        "\u2019": "'",   # right single quote '
        "\u201A": "'",   # single low-9 quote ‚
        "\u201B": "'",   # single high-reversed-9 quote ‛
        "\u201C": '"',   # left double quote "
        "\u201D": '"',   # right double quote "
        "\u201E": '"',   # double low-9 quote „
        "\u201F": '"',   # double high-reversed-9 quote ‟
        "\u2039": "'",   # single left-pointing angle quote ‹
        "\u203A": "'",   # single right-pointing angle quote ›
        
        # Special punctuation
        "\u2026": "...", # ellipsis …
        "\u2022": "-",   # bullet •
        "\u2023": "-",   # triangular bullet ‣
        "\u2043": "-",   # hyphen bullet ⁃
        "\u00B7": "-",   # middle dot ·
        "\u00A0": " ",   # non-breaking space
        "\u202F": " ",   # narrow no-break space
        "\u2002": " ",   # en space
        "\u2003": " ",   # em space
        "\u2009": " ",   # thin space
        
        # Mathematical and special symbols
        "\u00D7": "x",   # multiplication sign ×
        "\u00F7": "/",   # division sign ÷
        "\u2212": "-",   # minus sign −
        "\u2260": "!=",  # not equal to ≠
        "\u2264": "<=",  # less than or equal to ≤
        "\u2265": ">=",  # greater than or equal to ≥
        
        # Currency (keep common ones)
        "\u20AC": "EUR", # euro sign €
        "\u00A3": "GBP", # pound sign £
        "\u00A5": "YEN", # yen sign ¥
    }
    
    # Apply replacements
    for src, dst in replacements.items():
        text = text.replace(src, dst)

    # Insert break opportunities for very long unbroken tokens (e.g., URLs)
    # This ensures MultiCell has a place to wrap lines.
    text = re.sub(r"(\S{60})(?=\S)", r"\1 ", text)

    # Latin-1 encode/decode to drop remaining unsupported chars safely.
    try:
        text = text.encode("latin-1", "ignore").decode("latin-1")
    except Exception as e:
        # If encoding fails completely, try aggressive cleaning
        text = ''.join(char for char in text if ord(char) < 256)

    # Normalize line endings
    text = text.replace("\r\n", "\n").replace("\r", "\n")
    
    return text


# --- Transcription Cleaning ------------------------------------------------
def clean_transcription(text: str) -> str:
    """Remove AI preamble from transcription"""
    if not text:
        return ""
    
    text = re.sub(r'Thank you for providing.*?file:', '', text, flags=re.IGNORECASE | re.DOTALL)
    text = re.sub(r'I will transcribe.*?file:', '', text, flags=re.IGNORECASE | re.DOTALL)
    text = re.sub(r'Here is the transcription.*?:', '', text, flags=re.IGNORECASE | re.DOTALL)
    return text.strip()


def remove_timestamps(text: str) -> str:
    """Remove timestamp markers from transcription"""
    if not text:
        return ""
    return re.sub(r'\[\d{2}:\d{2}\]\s*', '', text)


# --- Segment Parsing for PDF -----------------------------------------------
def parse_segments(text: str) -> list:
    """Parse transcription into segments for dual-column PDF"""
    if not text or not text.strip():
        return ["No content available."]
    
    segments = []
    current_segment = []
    
    for line in text.split('\n'):
        line = line.strip()
        if not line:
            continue
        
        if line.startswith(('Teacher:', 'Student:', 'Observer:', '<Music>')):
            if current_segment:
                segments.append(' '.join(current_segment))
            current_segment = [line]
        else:
            current_segment.append(line)
    
    if current_segment:
        segments.append(' '.join(current_segment))
    
    return segments if segments else ["No content available."]
