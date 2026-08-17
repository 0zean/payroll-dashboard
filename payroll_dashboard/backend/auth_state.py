import reflex as rx
from starlette.config import Config
from supabase import AuthApiError, Client, create_client
from supabase_auth.types import Session, User

from ..backend.schemas import PayrollUser

config = Config(".env")

url: str = config.get("SUPABASE_URL")
key: str = config.get("SUPABASE_KEY")

supabase: Client = create_client(url, key)


class AuthState(rx.State):
    user: PayrollUser | None = None
    is_authenticated: bool = False
    is_loading: bool = False
    session: Session | None = None
    first_name: str = ""

    # Auth form state
    show_signup: bool = False
    email: str = ""
    password: str = ""
    name: str = ""

    @rx.event
    def handle_user_session(self, supabase_user: User):
        try:
            response = (
                supabase.table("profiles")
                .select("status, email", "full_name")
                .eq("id", supabase_user.id)
                .single()
                .execute()
            )
            data = response.data
            if not data or data.get("status") != "approved":
                rx.toast.warning(
                    "Your account is pending approval by an administrator."
                )
                supabase.auth.sign_out()
                self.user = None
                self.is_authenticated = False
                return
            self.user = PayrollUser(
                id=supabase_user.id,
                email=data.get("email") or supabase_user.email,
                name=data.get("full_name"),
            )
            self.is_authenticated = True
        except Exception as e:
            print("Error in handle_user_session:", e)
            self.user = None
            self.is_authenticated = False
            rx.toast.error("Error getting user info")

    @rx.event
    def login(self, email: str, password: str):
        self.is_loading = True
        try:
            result = supabase.auth.sign_in_with_password(
                {"email": email, "password": password}
            )
            user = result.user
            if not user:
                raise Exception("User not found")
            self.handle_user_session(user)
        except AuthApiError as e:
            return print("Login error:", e)
        except Exception as e:
            return print("Login failed:", e)
        finally:
            self.is_loading = False

    @rx.event
    def handle_login(self):
        self.login(self.email, self.password)
        if self.is_authenticated:
            self.email = ""
            self.password = ""
            return rx.toast.success("Login successful! 🎉")
        else:
            return rx.toast.error(
                "Login failed, please check your credentials."
            )

    @rx.event
    def handle_signup(self):
        self.signup(self.email, self.password, self.name)
        if not self.is_authenticated:
            self.email = ""
            self.password = ""
            self.name = ""
            self.show_signup = False
            return rx.toast.info(
                "Your account has been created and is pending approval by an administrator."
            )
        else:
            return rx.toast.error("Signup failed, please try again.")

    @rx.event
    def signup(self, email: str, password: str, name: str):
        self.is_loading = True
        try:
            trimmed_name = name.strip()
            if not trimmed_name:
                raise Exception("Full name is required")
            print("Full name for signup:", trimmed_name)
            result = supabase.auth.sign_up(
                {
                    "email": email,
                    "password": password,
                    "options": {"data": {"name": trimmed_name}},
                }
            )
            user = result.user
            if not user:
                raise Exception("Failed to create user")
            profile_response = (
                supabase.table("profiles")
                .select("*")
                .eq("id", user.id)
                .single()
                .execute()
            )
            if not profile_response.data:
                try:
                    supabase.table("profiles").insert(
                        {
                            "id": user.id,
                            "email": email,
                            "full_name": trimmed_name,
                            "status": "pending",
                        }
                    ).execute()
                except Exception as e:
                    print("Error creating profile manually:", e)
                    raise Exception("Error creating user profile")
            rx.toast.info(
                "Your account has been created and is pending approval by an administrator."
            )
            supabase.auth.sign_out()
            self.user = None
            self.is_authenticated = False
        except Exception as e:
            print("Signup failed:", e)
            rx.toast.error(e)
            raise
        finally:
            self.is_loading = False

    @rx.event
    def logout(self):
        try:
            supabase.auth.sign_out()
            self.user = None
            self.is_authenticated = False
            return rx.redirect("/")
        except Exception as e:
            print("Logout failed:", e)
            return rx.toast.error(e)

    @rx.event
    def set_email(self, value: str):
        try:
            self.email = value
        except ValueError:
            self.email = ""

    @rx.event
    def set_password(self, value: str):
        try:
            self.password = value
        except ValueError:
            self.password = ""

    @rx.event
    def set_name(self, value: str):
        try:
            self.name = value
        except ValueError:
            self.name = ""

    @rx.event
    def toggle_auth_mode(self):
        """Toggle between login and signup modes."""
        self.show_signup = not self.show_signup
        self.email = ""
        self.password = ""
        self.name = ""
