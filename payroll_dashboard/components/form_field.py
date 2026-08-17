"""Material 3 filled text field with supporting / error states."""

import reflex as rx

from payroll_dashboard import styles


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
    supporting_text: str = "",
) -> rx.Component:
    """An M3 filled text field.

    Args:
        label: The field label.
        placeholder: Placeholder text inside the field.
        type: The HTML input type.
        name: The submitted field name (unchanged payload key).
        icon: The leading label icon.
        default_value: Initial value of the field.
        on: The on_change event handler.
        required: Whether the field is required.
        error_message: Error text; when set, the field renders the error role.
        supporting_text: Helper text shown when there is no error.

    Returns:
        The form field component.
    """
    input_props = {
        "placeholder": placeholder,
        "type": type,
        "default_value": default_value,
        "on_change": on,
        "name": name,
        "size": "3",
        "radius": "small",
        "width": "100%",
        "style": styles.ghost_input_style,
    }

    if type == "number":
        input_props["step"] = "0.1"

    if required:
        input_props["required"] = True

    return rx.form.field(
        rx.el.div(
            rx.el.label(
                rx.icon(icon, size=15, stroke_width=1.5),
                rx.el.span(label),
                rx.cond(
                    required,
                    rx.el.span("*", class_name="md-field-required"),
                    rx.fragment(),
                ),
                class_name="md-field-label flex items-center gap-2",
            ),
            rx.form.control(
                rx.input(**input_props),
                as_child=True,
            ),
            rx.cond(
                error_message != "",
                rx.el.p(
                    rx.icon("circle-alert", size=13),
                    rx.el.span(error_message),
                    role="alert",
                    class_name="md-error-text",
                ),
                rx.cond(
                    supporting_text != "",
                    rx.el.p(supporting_text, class_name="md-supporting-text"),
                    rx.fragment(),
                ),
            ),
            class_name=rx.cond(
                error_message != "",
                "md-field md-field-invalid",
                "md-field",
            ),
        ),
        name=name,
        width="100%",
    )
