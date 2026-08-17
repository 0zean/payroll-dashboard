import reflex as rx

from ..backend.auth_state import AuthState
from ..components.icon import icon
from ..components.spline import scene, spline


def _field(label: str, placeholder: str, icon_tag: str, value, on_change, type: str = "text") -> rx.Component:
    """An M3 filled field for the auth form."""
    return rx.vstack(
        rx.text(
            label,
            rx.cond(AuthState.show_signup, rx.text.span(" *", color="var(--md-sys-color-error)")),
            font="var(--md-sys-typescale-body-small)",
            color="var(--md-sys-color-on-surface-variant)",
            width="100%",
        ),
        rx.input(
            rx.input.slot(icon(icon_tag, size=20)),
            placeholder=placeholder,
            type=type,
            size="3",
            width="100%",
            on_change=on_change,
            value=value,
            style={"pointer-events": "auto"},
            required=True,
        ),
        spacing="1",
        width="100%",
    )


def login_view() -> rx.Component:
    return rx.box(
        rx.box(
            spline(scene=scene),
            position="absolute",
            top=0,
            left=0,
            width="100%",
            height="100vh",
            z_index=0,
            style={"transform": "scale(1.25)"},
        ),
        rx.center(
            rx.card(
                rx.vstack(
                    rx.center(
                        icon("badge-dollar-sign", size=32, color="var(--md-sys-color-primary)"),
                        rx.heading(
                            rx.cond(AuthState.show_signup, "Create an account", "Sign in to your account"),
                            size="6",
                            as_="h2",
                            text_align="center",
                            width="100%",
                        ),
                        direction="column",
                        spacing="4",
                        width="100%",
                    ),
                    rx.cond(
                        AuthState.show_signup,
                        _field("Full name", "Enter your full name", "user", AuthState.name, AuthState.set_name),
                    ),
                    _field(
                        "Email address",
                        "user@reflex.dev",
                        "mail",
                        AuthState.email,
                        AuthState.set_email,
                        type="email",
                    ),
                    _field(
                        "Password",
                        "Enter your password",
                        "lock",
                        AuthState.password,
                        AuthState.set_password,
                        type="password",
                    ),
                    rx.cond(
                        AuthState.show_signup,
                        rx.box(
                            rx.checkbox(
                                "Agree to Terms and Conditions",
                                default_checked=True,
                                spacing="2",
                                style={"pointer-events": "auto"},
                            ),
                            width="100%",
                        ),
                    ),
                    rx.button(
                        rx.cond(AuthState.show_signup, "Create account", "Sign in"),
                        size="3",
                        width="100%",
                        on_click=rx.cond(AuthState.show_signup, AuthState.handle_signup, AuthState.handle_login),
                        loading=AuthState.is_loading,
                        style={"pointer-events": "auto"},
                    ),
                    rx.center(
                        rx.text(
                            rx.cond(AuthState.show_signup, "Already have an account?", "New here?"),
                            font="var(--md-sys-typescale-body-medium)",
                            color="var(--md-sys-color-on-surface-variant)",
                        ),
                        rx.link(
                            rx.cond(AuthState.show_signup, "Sign in", "Sign up"),
                            on_click=AuthState.toggle_auth_mode,  # type: ignore
                            style={"pointer-events": "auto"},
                        ),
                        spacing="2",
                        direction="row",
                        style={"pointer-events": "auto"},
                    ),
                    spacing="5",
                    width="100%",
                ),
                max_width="28em",
                size="4",
                width="100%",
                z_index=1,
                style={
                    # Let the 3D scene behind stay interactive; inputs opt back in.
                    "pointer-events": "none",
                    # Tokenised translucency, so the card reads correctly in both themes.
                    "background": "color-mix(in srgb, var(--md-sys-color-surface-container-high) 80%, transparent)",
                    "backdrop-filter": "blur(12px)",
                    "box-shadow": "var(--md-sys-elevation-3)",
                },
            ),
            height="100vh",
            width="100%",
            position="relative",
            style={"pointer-events": "none"},
        ),
        position="relative",
        width="100%",
        height="100vh",
        overflow="hidden",
    )
