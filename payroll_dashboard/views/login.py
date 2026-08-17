"""Material 3 authentication view."""

import reflex as rx

from ..backend.auth_state import AuthState

INPUT_STYLE = {
    "background_color": "var(--md-sys-color-surface-container-highest)",
    "box_shadow": "inset 0 0 0 1px var(--md-sys-color-outline-variant)",
    "color": "var(--md-sys-color-on-surface)",
    "transition": (
        "box-shadow var(--md-sys-motion-duration-short4)"
        " var(--md-sys-motion-easing-standard)"
    ),
    "--text-field-focus-color": "var(--md-sys-color-primary)",
    "_focus_within": {
        "box_shadow": "inset 0 0 0 2px var(--md-sys-color-primary)",
    },
}

FILLED_BUTTON_STYLE = {
    "background_color": "var(--md-sys-color-primary)",
    "color": "var(--md-sys-color-on-primary)",
    "border_radius": "var(--md-sys-shape-corner-full)",
    "box_shadow": "none",
}


def _field_label(text: str, required: bool) -> rx.Component:
    return rx.el.label(
        text,
        rx.cond(
            required,
            rx.el.span(" *", class_name="md-field-required"),
            rx.fragment(),
        ),
        class_name="md-field-label w-full text-left",
    )


def login_header() -> rx.Component:
    """Monogram, eyebrow and headline for the auth card."""
    return rx.el.div(
        rx.el.div(
            rx.icon("badge-dollar-sign", size=24),
            class_name=(
                "md-brand-mark mb-1 flex h-14 w-14 items-center justify-center rounded-full"
            ),
        ),
        rx.el.p(
            "Payroll operations",
            class_name="md-label-medium md-on-surface-variant",
        ),
        rx.el.h1(
            rx.cond(
                AuthState.show_signup,
                "Create an account",
                "Sign in to your account",
            ),
            class_name="md-headline-small md-on-surface text-center",
        ),
        class_name="flex w-full flex-col items-center gap-2",
    )


def login_view() -> rx.Component:
    """The M3 sign-in / sign-up screen."""
    return rx.el.div(
        rx.el.div(
            rx.el.div(
                login_header(),
                rx.cond(
                    AuthState.show_signup,
                    rx.el.div(
                        _field_label("Full name", True),
                        rx.input(
                            rx.input.slot(rx.icon("user", size=16)),
                            placeholder="Enter your full name",
                            size="3",
                            width="100%",
                            radius="small",
                            on_change=AuthState.set_name,
                            style=INPUT_STYLE,
                            required=True,
                            default_value=AuthState.name,
                        ),
                        class_name="flex w-full flex-col gap-1.5",
                    ),
                    rx.fragment(),
                ),
                rx.el.div(
                    _field_label("Email address", AuthState.show_signup),
                    rx.input(
                        rx.input.slot(rx.icon("mail", size=16)),
                        placeholder="user@reflex.dev",
                        type="email",
                        size="3",
                        width="100%",
                        radius="small",
                        on_change=AuthState.set_email,
                        style=INPUT_STYLE,
                        required=True,
                        default_value=AuthState.email,
                    ),
                    class_name="flex w-full flex-col gap-1.5",
                ),
                rx.el.div(
                    _field_label("Password", AuthState.show_signup),
                    rx.input(
                        rx.input.slot(rx.icon("lock", size=16)),
                        placeholder="Enter your password",
                        type="password",
                        size="3",
                        width="100%",
                        radius="small",
                        on_change=AuthState.set_password,
                        style=INPUT_STYLE,
                        required=True,
                        default_value=AuthState.password,
                    ),
                    rx.cond(
                        AuthState.show_signup,
                        rx.el.p(
                            "Use at least 8 characters.",
                            class_name="md-supporting-text",
                        ),
                        rx.fragment(),
                    ),
                    class_name="flex w-full flex-col gap-1.5",
                ),
                rx.cond(
                    AuthState.show_signup,
                    rx.el.div(
                        rx.checkbox(
                            "Agree to Terms and Conditions",
                            default_checked=True,
                            spacing="2",
                            class_name="md-body-medium md-on-surface-variant",
                        ),
                        class_name="w-full",
                    ),
                    rx.fragment(),
                ),
                rx.button(
                    rx.cond(AuthState.show_signup, "Create account", "Sign in"),
                    size="3",
                    width="100%",
                    on_click=rx.cond(
                        AuthState.show_signup,
                        AuthState.handle_signup,
                        AuthState.handle_login,
                    ),
                    loading=AuthState.is_loading,
                    class_name="md-press focus-ring md-label-large",
                    style=FILLED_BUTTON_STYLE,
                ),
                rx.el.div(
                    rx.el.span(
                        rx.cond(
                            AuthState.show_signup,
                            "Already have an account?",
                            "New here?",
                        ),
                        class_name="md-body-medium md-on-surface-variant",
                    ),
                    rx.link(
                        rx.cond(AuthState.show_signup, "Sign in", "Sign up"),
                        on_click=AuthState.toggle_auth_mode,  # type: ignore
                        underline="none",
                        class_name="md-button-text focus-ring",
                    ),
                    class_name="flex w-full items-center justify-center gap-2",
                ),
                class_name=(
                    "md-card md-enter flex w-full flex-col items-center gap-5 "
                    "rounded-[var(--md-sys-shape-corner-extra-large)] p-6 sm:p-8"
                ),
            ),
            rx.el.p(
                "Secure access · approvals managed by your administrator",
                class_name="md-body-small md-on-surface-variant mt-4 text-center",
            ),
            class_name="w-full max-w-[28em] px-4",
        ),
        class_name=(
            "md-app-canvas flex min-h-screen w-full items-center justify-center py-10"
        ),
    )
