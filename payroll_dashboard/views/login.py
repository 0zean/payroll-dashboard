import reflex as rx

from ..backend.auth_state import AuthState
from ..components.spline import scene, spline

INPUT_STYLE = {
    "pointer-events": "auto",
    "background-color": "rgba(255, 255, 255, 0.04)",
    "box-shadow": "inset 0 0 0 1px rgba(255,255,255,0.1)",
    "color": "#F4F5F8",
    "transition": "box-shadow 220ms cubic-bezier(0.22, 1, 0.36, 1)",
    "--text-field-focus-color": "#5E6AD2",
}


def _field_label(text: str, required: bool) -> rx.Component:
    return rx.text(
        text,
        rx.cond(
            required,
            rx.text.span(" *", color="#F87171"),
        ),
        size="2",
        weight="medium",
        text_align="left",
        width="100%",
        class_name="text-white/60 uppercase tracking-[0.12em] text-[11px]",
    )


def login_view() -> rx.Component:
    return rx.el.div(
        # Cinematic backdrop: spline scene + ambient light + grid/noise scrims
        rx.el.div(
            spline(scene=scene),
            class_name="absolute inset-0 z-0 opacity-70",
            style={"transform": "scale(1.25)"},
        ),
        rx.el.div(
            class_name="absolute inset-0 z-0 bg-[#020203]/72",
        ),
        rx.el.div(
            rx.el.div(class_name="ambient-blob blob-indigo"),
            rx.el.div(class_name="ambient-blob blob-violet"),
            rx.el.div(class_name="grid-overlay"),
            rx.el.div(class_name="noise-overlay"),
            class_name="ambient-layer",
            aria_hidden="true",
        ),
        rx.center(
            rx.el.div(
                rx.card(
                    rx.vstack(
                        rx.center(
                            rx.el.div(
                                rx.icon(
                                    tag="badge-dollar-sign",
                                    size=22,
                                    color="white",
                                ),
                                class_name=(
                                    "brand-mark mb-1 flex h-11 w-11 items-center justify-center rounded-2xl"
                                ),
                            ),
                            rx.el.p(
                                "Payroll operations",
                                class_name=(
                                    "text-[10px] font-semibold uppercase tracking-[0.22em] text-white/40"
                                ),
                            ),
                            rx.heading(
                                rx.cond(
                                    AuthState.show_signup,
                                    "Create an account",
                                    "Sign in to your account",
                                ),
                                size="6",
                                as_="h2",
                                text_align="center",
                                width="100%",
                                class_name="text-white tracking-tight",
                            ),
                            direction="column",
                            spacing="3",
                            width="100%",
                        ),
                        # Name field (only for signup)
                        rx.cond(
                            AuthState.show_signup,
                            rx.vstack(
                                _field_label("Full name", True),
                                rx.input(
                                    rx.input.slot(rx.icon("user")),
                                    placeholder="Enter your full name",
                                    size="3",
                                    width="100%",
                                    on_change=AuthState.set_name,
                                    style=INPUT_STYLE,
                                    required=True,
                                    default_value=AuthState.name,
                                ),
                                spacing="2",
                                width="100%",
                            ),
                        ),
                        rx.vstack(
                            _field_label(
                                "Email address", AuthState.show_signup
                            ),
                            rx.input(
                                rx.input.slot(rx.icon("mail")),
                                placeholder="user@reflex.dev",
                                type="email",
                                size="3",
                                width="100%",
                                on_change=AuthState.set_email,
                                style=INPUT_STYLE,
                                required=True,
                                default_value=AuthState.email,
                            ),
                            spacing="2",
                            width="100%",
                        ),
                        rx.vstack(
                            rx.hstack(
                                _field_label("Password", AuthState.show_signup),
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
                                style=INPUT_STYLE,
                                required=True,
                                default_value=AuthState.password,
                            ),
                            spacing="2",
                            width="100%",
                        ),
                        # Terms checkbox (only for signup)
                        rx.cond(
                            AuthState.show_signup,
                            rx.el.div(
                                rx.checkbox(
                                    "Agree to Terms and Conditions",
                                    default_checked=True,
                                    spacing="2",
                                    style={"pointer-events": "auto"},
                                    class_name="text-white/70",
                                ),
                                class_name="w-full text-sm",
                            ),
                        ),
                        rx.button(
                            rx.cond(
                                AuthState.show_signup,
                                "Create account",
                                "Sign in",
                            ),
                            size="3",
                            width="100%",
                            on_click=rx.cond(
                                AuthState.show_signup,
                                AuthState.handle_signup,
                                AuthState.handle_login,
                            ),
                            is_loading=AuthState.is_loading,
                            class_name="press focus-ring font-semibold",
                            style={
                                "pointer-events": "auto",
                                "background": "linear-gradient(180deg, #6E79DC, #5E6AD2)",
                                "color": "#FFFFFF",
                                "box-shadow": (
                                    "inset 0 1px 0 rgba(255,255,255,0.28), 0 16px 34px -18px rgba(94,106,210,0.75)"
                                ),
                            },
                        ),
                        rx.center(
                            rx.text(
                                rx.cond(
                                    AuthState.show_signup,
                                    "Already have an account?",
                                    "New here?",
                                ),
                                size="2",
                                class_name="text-white/50",
                            ),
                            rx.link(
                                rx.cond(
                                    AuthState.show_signup, "Sign in", "Sign up"
                                ),
                                on_click=AuthState.toggle_auth_mode,  # type: ignore
                                size="2",
                                style={"pointer-events": "auto"},
                                class_name="font-semibold text-[#A5AEFF] transition-colors duration-200 hover:text-white",
                            ),
                            spacing="2",
                            direction="row",
                            style={"pointer-events": "auto"},
                        ),
                        spacing="5",
                        width="100%",
                    ),
                    size="4",
                    width="100%",
                    style={
                        "pointer-events": "none",
                        "background": "linear-gradient(180deg, rgba(255,255,255,0.06), rgba(255,255,255,0.02))",
                        "border": "1px solid rgba(255,255,255,0.1)",
                        "box-shadow": (
                            "inset 0 1px 0 rgba(255,255,255,0.07), 0 40px 90px -50px rgba(2,2,3,0.95)"
                        ),
                        "backdrop-filter": "blur(24px) saturate(150%)",
                    },
                ),
                rx.el.p(
                    "Secure access · approvals managed by your administrator",
                    class_name="mt-4 text-center text-[11px] font-medium text-white/35",
                ),
                class_name="rise-in relative z-10 w-full max-w-[28em] px-4",
            ),
            height="100vh",
            width="100%",
            position="relative",
            style={"pointer-events": "none"},
        ),
        class_name="app-canvas relative h-screen w-full overflow-hidden",
    )
