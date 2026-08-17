"""Styles for the app — Material Design 3 token system.

Color, shape, motion and elevation values mirror the M3 tokens declared in
`assets/m3.css` so Python-side styles stay in sync with the CSS layer.
"""

import reflex as rx

# --- M3 color roles (referenced through CSS custom properties) -------------
surface = "var(--md-sys-color-surface)"
surface_container_low = "var(--md-sys-color-surface-container-low)"
surface_container = "var(--md-sys-color-surface-container)"
surface_container_high = "var(--md-sys-color-surface-container-high)"
surface_container_highest = "var(--md-sys-color-surface-container-highest)"
on_surface = "var(--md-sys-color-on-surface)"
on_surface_variant = "var(--md-sys-color-on-surface-variant)"
outline = "var(--md-sys-color-outline)"
outline_variant = "var(--md-sys-color-outline-variant)"
primary = "var(--md-sys-color-primary)"
on_primary = "var(--md-sys-color-on-primary)"
primary_container = "var(--md-sys-color-primary-container)"
on_primary_container = "var(--md-sys-color-on-primary-container)"
secondary_container = "var(--md-sys-color-secondary-container)"
on_secondary_container = "var(--md-sys-color-on-secondary-container)"
error = "var(--md-sys-color-error)"

# --- M3 shape scale (4px -> 28px) -----------------------------------------
shape_extra_small = "var(--md-sys-shape-corner-extra-small)"
shape_small = "var(--md-sys-shape-corner-small)"
shape_medium = "var(--md-sys-shape-corner-medium)"
shape_large = "var(--md-sys-shape-corner-large)"
shape_extra_large = "var(--md-sys-shape-corner-extra-large)"
shape_full = "var(--md-sys-shape-corner-full)"

# --- M3 elevation ---------------------------------------------------------
elevation_0 = "var(--md-sys-elevation-level0)"
elevation_1 = "var(--md-sys-elevation-level1)"
elevation_2 = "var(--md-sys-elevation-level2)"
elevation_3 = "var(--md-sys-elevation-level3)"

# --- M3 motion ------------------------------------------------------------
easing_standard = "var(--md-sys-motion-easing-standard)"
easing_emphasized = "var(--md-sys-motion-easing-emphasized)"
duration_short = "var(--md-sys-motion-duration-short4)"
duration_medium = "var(--md-sys-motion-duration-medium2)"

# --- Backwards compatible aliases used across views -----------------------
border_radius = shape_medium
border = f"1px solid {outline_variant}"
border_strong = f"1px solid {outline}"

text_color = on_surface_variant
text_color_strong = on_surface
gray_color = on_surface_variant
gray_bg_color = surface_container

accent_text_color = primary
accent_color = primary
accent_bg_color = primary_container

hover_accent_color = {"_hover": {"color": accent_text_color}}
hover_accent_bg = {"_hover": {"background_color": accent_bg_color}}

content_width_vw = "90vw"
sidebar_width = "32em"
sidebar_content_width = "17em"
max_width = "1480px"
color_box_size = ["2.25rem", "2.25rem", "2.5rem"]

transition = f"all {duration_short} {easing_standard}"

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
    "background_color": surface_container,
    "border_radius": shape_full,
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

# M3 filled text field surface treatment.
ghost_input_style = {
    "--text-field-selection-color": "",
    "--text-field-focus-color": primary,
    "--text-field-border-width": "1px",
    "background_clip": "content-box",
    "background_color": surface_container_highest,
    "box_shadow": f"inset 0 0 0 var(--text-field-border-width) {outline_variant}",
    "color": on_surface,
    "transition": transition,
    "_hover": {
        "box_shadow": f"inset 0 0 0 var(--text-field-border-width) {outline}",
    },
    "_focus_within": {
        "box_shadow": f"inset 0 0 0 2px {primary}",
    },
}

box_shadow_style = elevation_1

color_picker_style = {
    "border_radius": shape_full,
    "box_shadow": elevation_1,
    "cursor": "pointer",
    "display": "flex",
    "align_items": "center",
    "justify_content": "center",
    "transition": f"transform {duration_short} {easing_standard}",
    "_hover": {
        "transform": "scale(1.04)",
    },
    "_active": {
        "transform": "scale(0.96)",
    },
}


base_stylesheets = [
    "https://fonts.googleapis.com/css2?family=Roboto:wght@300;400;500;700&display=swap",
    "/m3.css",
]

base_style = {
    "font_family": (
        "Roboto, 'Roboto Flex', system-ui, -apple-system, 'Segoe UI', Helvetica, Arial, sans-serif"
    ),
    "background_color": surface,
    "color": on_surface,
    "letter_spacing": "0",
}
