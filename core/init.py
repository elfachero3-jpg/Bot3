# Core module initialization
from .transcription import transcribe_audio, align_transcriptions
from .reports import (
    analyze_lesson_context,
    research_best_practices,
    generate_observation_report,
    create_observation_report_pdf,
    create_dual_column_pdf,
    create_text_fallback,
    create_transcript_text_fallback
)
from .utils import (
    validate_text_content,
    validate_pdf_inputs,
    sanitize_text_for_pdf,
    clean_transcription,
    remove_timestamps,
    parse_segments
)

__all__ = [
    'transcribe_audio',
    'align_transcriptions',
    'analyze_lesson_context',
    'research_best_practices',
    'generate_observation_report',
    'create_observation_report_pdf',
    'create_dual_column_pdf',
    'create_text_fallback',
    'create_transcript_text_fallback',
    'validate_text_content',
    'validate_pdf_inputs',
    'sanitize_text_for_pdf',
    'clean_transcription',
    'remove_timestamps',
    'parse_segments'
]
