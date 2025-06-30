import reflex as rx


def form_field(
    label: str,
    placeholder: str,
    type: str,
    name: str,
    icon: str,
    default_value: str = "",
    on: rx.event.EventType | None = None,
    required: bool = False,
    error_message: str = "",
) -> rx.Component:
    input_props = {
        "placeholder": placeholder,
        "type": type,
        "default_value": default_value,
        "on_change": on,
        "name": name,
    }

    if type == "number":
        input_props["step"] = "0.1"

    if required:
        input_props["required"] = True

    return rx.form.field(
        rx.flex(
            rx.hstack(
                rx.icon(icon, size=16, stroke_width=1.5),
                rx.form.label(label),
                align="center",
                spacing="2",
            ),
            rx.form.control(
                rx.input(**input_props),
                as_child=True,
            ),
            rx.cond(
                error_message != "",
                rx.form.message(error_message, color="tomato"),
                "",
            ),
            direction="column",
            spacing="1",
        ),
        name=name,
        width="100%",
    )
