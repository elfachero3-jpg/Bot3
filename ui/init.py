# UI module initialization
from .styling import inject_custom_css
from .solo_components import (
    render_solo_interface,
    render_solo_download
)
from .observation_components import (
    render_header,
    render_observation_header,
    render_name_inputs,
    render_audio_uploads,
    render_text_inputs,
    render_downloads,
    render_footer
)

__all__ = [
    'inject_custom_css',
    'render_header',
    'render_solo_interface',
    'render_observation_header',
    'render_name_inputs',
    'render_audio_uploads',
    'render_text_inputs',
    'render_downloads',
    'render_footer'
]
