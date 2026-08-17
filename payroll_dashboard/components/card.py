import reflex as rx

from payroll_dashboard import styles


def card(*children, **props):
    extra_class = props.pop("class_name", "")
    return rx.card(
        *children,
        box_shadow=styles.box_shadow_style,
        size="3",
        width="100%",
        class_name=f"glass-card spotlight rounded-2xl {extra_class}",
        **props,
    )
