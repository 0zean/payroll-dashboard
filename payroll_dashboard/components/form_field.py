import reflex as rx

from .icon import icon


def form_field(
    label: str,
    placeholder: str,
    type: str,
    name: str,
    icon_tag: str,
    default_value: str = "",
    on: rx.event.EventType | None = None,
    required: bool = False,
    error_message: str = "",
    helper: str = "",
) -> rx.Component:
    """An M3 filled text field with a leading icon label and supporting text."""
    input_props = {
        "placeholder": placeholder,
        "type": type,
        "default_value": default_value,
        "on_change": on,
        "name": name,
        "size": "3",
    }

    if type == "number":
        input_props["step"] = "0.1"

    if required:
        input_props["required"] = True

    return rx.form.field(
        rx.flex(
            rx.hstack(
                icon(icon_tag, size=18, color="var(--md-sys-color-on-surface-variant)"),
                rx.form.label(label),
                rx.cond(required, rx.text("*", color="var(--md-sys-color-error)")),
                align="center",
                spacing="2",
            ),
            rx.form.control(
                rx.input(**input_props),
                as_child=True,
            ),
            # M3 supporting text sits under the field, in the same slot as the error.
            rx.cond(
                error_message != "",
                rx.form.message(error_message),
                rx.cond(
                    helper != "",
                    rx.text(
                        helper,
                        font="var(--md-sys-typescale-body-small)",
                        color="var(--md-sys-color-on-surface-variant)",
                    ),
                    "",
                ),
            ),
            direction="column",
            spacing="1",
        ),
        name=name,
        width="100%",
    )
