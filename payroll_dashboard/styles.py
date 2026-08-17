"""Styles for the app — cinematic dark "payroll operations cockpit" system."""

import reflex as rx

# Core canvas + accent tokens
canvas_deep = "#020203"
canvas = "#050506"
accent_hex = "#5E6AD2"
accent_soft_hex = "#8B93E8"
accent_bright_hex = "#A5AEFF"

border_radius = "12px"
border = "1px solid rgba(255, 255, 255, 0.08)"
border_strong = "1px solid rgba(255, 255, 255, 0.14)"

text_color = "rgba(233, 234, 240, 0.72)"
text_color_strong = "#F4F5F8"
gray_color = "rgba(233, 234, 240, 0.5)"
gray_bg_color = "rgba(255, 255, 255, 0.06)"

accent_text_color = accent_bright_hex
accent_color = accent_hex
accent_bg_color = "rgba(94, 106, 210, 0.18)"
accent_glow = "rgba(94, 106, 210, 0.45)"

hover_accent_color = {"_hover": {"color": accent_text_color}}
hover_accent_bg = {"_hover": {"background_color": accent_bg_color}}

content_width_vw = "90vw"
sidebar_width = "32em"
sidebar_content_width = "17em"
max_width = "1480px"
color_box_size = ["2.25rem", "2.25rem", "2.5rem"]

transition = "all 240ms cubic-bezier(0.22, 1, 0.36, 1)"

glass_surface = {
    "background": "linear-gradient(180deg, rgba(255,255,255,0.05), rgba(255,255,255,0.018))",
    "backdrop_filter": "blur(20px) saturate(150%)",
    "border": border,
    "border_radius": "16px",
}

template_page_style = {
    "padding_top": ["1em", "1em", "2em"],
    "padding_x": ["1em", "1em", "2em"],
}

template_content_style = {
    "padding": ["0.5em", "0.5em", "1em"],
    "margin_bottom": "2em",
    "min_height": "90vh",
}

link_style = {
    "color": accent_text_color,
    "text_decoration": "none",
    "transition": transition,
    **hover_accent_color,
}

overlapping_button_style = {
    "background_color": "rgba(255, 255, 255, 0.06)",
    "border_radius": border_radius,
}

markdown_style = {
    "code": lambda text: rx.code(text, color_scheme="gray"),
    "codeblock": lambda text, **props: rx.code_block(
        text, **props, margin_y="1em"
    ),
    "a": lambda text, **props: rx.link(
        text,
        **props,
        font_weight="bold",
        text_decoration="underline",
        text_decoration_color=accent_text_color,
    ),
}

notification_badge_style = {
    "width": "1.25rem",
    "height": "1.25rem",
    "display": "flex",
    "align_items": "center",
    "justify_content": "center",
    "position": "absolute",
    "right": "-0.35rem",
    "top": "-0.35rem",
}

ghost_input_style = {
    "--text-field-selection-color": "",
    "--text-field-focus-color": accent_hex,
    "--text-field-border-width": "1px",
    "background_clip": "content-box",
    "background_color": "rgba(255, 255, 255, 0.035)",
    "box_shadow": "inset 0 0 0 var(--text-field-border-width) rgba(255,255,255,0.08)",
    "color": text_color_strong,
    "transition": transition,
    "_hover": {
        "box_shadow": "inset 0 0 0 var(--text-field-border-width) rgba(255,255,255,0.16)",
    },
    "_focus_within": {
        "box_shadow": f"inset 0 0 0 1px {accent_hex}, 0 0 0 4px rgba(94, 106, 210, 0.18)",
    },
}

box_shadow_style = (
    "inset 0 1px 0 rgba(255,255,255,0.06), 0 28px 60px -38px rgba(2,2,3,0.95)"
)

color_picker_style = {
    "border_radius": "max(var(--radius-3), var(--radius-full))",
    "box_shadow": box_shadow_style,
    "cursor": "pointer",
    "display": "flex",
    "align_items": "center",
    "justify_content": "center",
    "transition": "transform 0.2s cubic-bezier(0.22, 1, 0.36, 1)",
    "_hover": {
        "transform": "translateY(-2px) scale(1.04)",
    },
    "_active": {
        "transform": "translateY(2px) scale(0.95)",
    },
}


base_stylesheets = [
    "https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap",
    "/styles.css",
]

base_style = {
    "font_family": (
        "Inter, 'Geist', -apple-system, BlinkMacSystemFont, 'Segoe UI', Helvetica, Arial, sans-serif"
    ),
    "background_color": canvas_deep,
    "color": text_color_strong,
    "letter_spacing": "-0.011em",
}
