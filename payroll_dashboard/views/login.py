import reflex as rx


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
                        # on_change=State.set_username,
                        # value=State.username,
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
                        # on_change=State.set_password,
                        # value=State.password,
                    ),
                    spacing="2",
                    width="100%",
                ),
                rx.button(
                    "Sign in",
                    size="3",
                    width="100%",
                    # on_click=State.handle_login,
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
