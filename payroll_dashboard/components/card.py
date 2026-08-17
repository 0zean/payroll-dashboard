import reflex as rx

from payroll_dashboard import styles


def card(*children, **props):
    extra_class = props.pop("class_name", "")
    return rx.card(
        *children,
        box_shadow=styles.box_shadow_style,
        size="3",
        width="100%",
        class_name=f"md-card md-elevate {extra_class}",
        **props,
    )
