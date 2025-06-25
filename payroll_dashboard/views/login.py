import reflex as rx

from ..backend.auth_state import AuthState


def login_view() -> rx.Component:
    return rx.center(
        rx.card(
            rx.vstack(
                rx.center(
                    rx.icon(tag="badge-dollar-sign", size=28),
                    rx.heading(
                        "Sign in to your account",
                        size="6",
                        as_="h2",
                        text_align="center",
                        width="100%",
                    ),
                    direction="column",
                    spacing="5",
                    width="100%",
                ),
                rx.vstack(
                    rx.text(
                        "Email address",
                        size="3",
                        weight="medium",
                        text_align="left",
                        width="100%",
                    ),
                    rx.input(
                        rx.input.slot(rx.icon("user")),
                        placeholder="user@reflex.dev",
                        type="email",
                        size="3",
                        width="100%",
                        on_change=AuthState.set_email,
                        value=AuthState.email,
                    ),
                    spacing="2",
                    width="100%",
                ),
                rx.vstack(
                    rx.hstack(
                        rx.text(
                            "Password",
                            size="3",
                            weight="medium",
                        ),
                        justify="between",
                        width="100%",
                    ),
                    rx.input(
                        rx.input.slot(rx.icon("lock")),
                        placeholder="Enter your password",
                        type="password",
                        size="3",
                        width="100%",
                        on_change=AuthState.set_password,
                        value=AuthState.password,
                    ),
                    spacing="2",
                    width="100%",
                ),
                rx.button(
                    "Sign in",
                    size="3",
                    width="100%",
                    on_click=AuthState.handle_login,
                    is_loading=AuthState.is_loading,
                ),
                rx.center(
                    rx.text("New here?", size="3"),
                    rx.link("Sign up", href="#", size="3"),
                    opacity="0.8",
                    spacing="2",
                    direction="row",
                ),
                spacing="6",
                width="100%",
            ),
            max_width="28em",
            size="4",
            width="100%",
        ),
        height="100vh",
        width="100%",
    )
