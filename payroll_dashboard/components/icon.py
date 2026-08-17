"""Material Symbols icons, drop-in replacement for rx.icon."""

import reflex as rx

# Lucide tag -> Material Symbols ligature, for the icons this app actually uses.
_SYMBOLS = {
    "add": "add",
    "align-justify": "menu",
    "arrow-down-a-z": "sort_by_alpha",
    "arrow-down-z-a": "sort_by_alpha",
    "badge-dollar-sign": "paid",
    "blend": "contrast",
    "brush-cleaning": "mop",
    "calendar-days": "calendar_month",
    "check": "check",
    "chevron-left": "chevron_left",
    "chevron-right": "chevron_right",
    "chevrons-left": "keyboard_double_arrow_left",
    "chevrons-right": "keyboard_double_arrow_right",
    "clock": "schedule",
    "clock-arrow-up": "more_time",
    "cog": "settings",
    "dollar-sign": "attach_money",
    "download": "download",
    "home": "home",
    "hourglass": "hourglass_top",
    "id-card": "badge",
    "layout-dashboard": "dashboard",
    "lock": "lock",
    "log-out": "logout",
    "mail": "mail",
    "notebook-pen": "edit_note",
    "palette": "palette",
    "plus": "add",
    "search": "search",
    "settings": "settings",
    "sheet": "table_view",
    "square-pen": "edit",
    "table-2": "table",
    "trash-2": "delete",
    "user": "person",
    "user-plus": "person_add",
    "users": "group",
    "x": "close",
}


def icon(tag: str, size: int = 24, fill: bool = False, **props) -> rx.Component:
    """A Material Symbols icon.

    Args:
        tag: Lucide-style name (mapped to its Material Symbols equivalent) or a
            Material Symbols ligature directly.
        size: Optical size in px.
        fill: Use the filled variant (M3 uses this for active navigation items).
        **props: Passed through to the underlying span.

    Returns:
        The icon component.

    """
    style = props.pop("style", {})
    return rx.el.span(
        _SYMBOLS.get(tag, tag),
        class_name="m3-icon",
        style={
            "font-size": f"{size}px",
            "width": f"{size}px",
            "height": f"{size}px",
            "--m3-icon-fill": rx.cond(fill, 1, 0) if isinstance(fill, rx.Var) else int(fill),
            **style,
        },
        aria_hidden="true",
        **props,
    )
