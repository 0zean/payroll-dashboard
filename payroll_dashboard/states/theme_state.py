import reflex as rx


class ThemeState(rx.State):
    accent_color: str = "indigo"
    gray_color: str = "slate"
    radius: str = "large"
    scaling: str = "100%"
    appearance: str = "light"

    @rx.var
    def is_dark(self) -> bool:
        return self.appearance == "dark"

    @rx.var
    def shell_class(self) -> str:
        scheme = "md-dark" if self.appearance == "dark" else "md-light"
        return f"md-theme {scheme} md-body min-h-screen w-full"

    @rx.event
    def toggle_appearance(self) -> None:
        self.appearance = "light" if self.appearance == "dark" else "dark"
