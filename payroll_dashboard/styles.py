"""Styles for the app.

Design tokens live in CSS (assets/m3.css + the generated assets/m3-theme.css).
The names below are thin Python aliases for the M3 tokens that Python-side code
still needs to reference inline.
"""

border_radius = "var(--md-sys-shape-corner-medium)"
border = "1px solid var(--md-sys-color-outline-variant)"

text_color = "var(--md-sys-color-on-surface-variant)"
gray_color = "var(--md-sys-color-on-surface-variant)"
gray_bg_color = "var(--md-sys-color-surface-container)"
accent_text_color = "var(--md-sys-color-primary)"
accent_color = "var(--md-sys-color-on-secondary-container)"
accent_bg_color = "var(--md-sys-color-secondary-container)"

box_shadow_style = "var(--md-sys-elevation-1)"

sidebar_width = "32em"
sidebar_content_width = "18em"
max_width = "1480px"

template_page_style = {
    "padding_top": ["1em", "1em", "2em"],
    "padding_x": ["auto", "auto", "2em"],
}

template_content_style = {
    "padding": "1em",
    "margin_bottom": "2em",
    "min_height": "90vh",
}

ghost_input_style = {
    "--text-field-selection-color": "",
    "--text-field-focus-color": "transparent",
    "--text-field-border-width": "1px",
    "background_clip": "content-box",
    "background_color": "transparent",
    "box_shadow": "inset 0 0 0 var(--text-field-border-width) transparent",
    "color": "",
}

base_stylesheets = [
    "https://fonts.googleapis.com/css2?family=Roboto+Flex:opsz,wght@8..144,300..700&display=swap",
    "https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined:opsz,wght,FILL,GRAD@24,400,0..1,0&display=swap",
    "m3-theme.css",
    "m3.css",
    "m3-components.css",
    "styles.css",
]

base_style = {
    "font_family": '"Roboto Flex", "Roboto", system-ui, sans-serif',
}
