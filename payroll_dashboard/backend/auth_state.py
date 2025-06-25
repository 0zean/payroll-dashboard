import os

import reflex as rx
from dotenv import load_dotenv
from gotrue import Session, User
from supabase import AuthApiError, Client, create_client

from ..backend.schemas import PayrollUser

load_dotenv()

url: str = os.environ.get("SUPABASE_URL")  # type: ignore
key: str = os.environ.get("SUPABASE_KEY")  # type: ignore

supabase: Client = create_client(url, key)


class AuthState(rx.State):
    user: PayrollUser | None = None
    is_authenticated: bool = False
    is_loading: bool = False
    session: Session | None = None
    
    email: str = ""
    password: str = ""

    def handle_user_session(self, supabase_user: User):
        try:
            response = (
                supabase.table("profiles").select("status, email").eq("id", supabase_user.id).single().execute()
            )
            data = response.data
            if not data or data.get("status") != "approved":
                rx.toast.error("Your account is pending approval by an administrator.")
                supabase.auth.sign_out()
                self.user = None
                self.is_authenticated = False
                return
            self.user = PayrollUser(
                id=supabase_user.id,
                email=data.get("email") or supabase_user.email, # type: ignore
                name=supabase_user.user_metadata.get("name"),
            )
            self.is_authenticated = True
        except Exception as e:
            print("Error in handle_user_session:", e)
            self.user = None
            self.is_authenticated = False

    def login(self, email: str, password: str):
        self.is_loading = True
        try:
            result = supabase.auth.sign_in_with_password({"email": email, "password": password})
            user = result.user
            if not user:
                raise Exception("User not found")
            self.handle_user_session(user)
        except AuthApiError as e:
            print("Login error:", e)
            rx.toast.error(str(e))
            raise
        except Exception as e:
            print("Login failed:", e)
            rx.toast.error(str(e))
            raise
        finally:
            self.is_loading = False
    
    def handle_login(self):
        self.login(self.email, self.password)
        if self.is_authenticated:
            rx.toast.success("Login Successfull!")

    def signup(self, email: str, password: str, name: str):
        self.is_loading = True
        try:
            trimmed_name = name.strip()
            if not trimmed_name:
                raise Exception("Full name is required")
            print("Full name for signup:", trimmed_name)
            result = supabase.auth.sign_up(
                {"email": email, "password": password, "options": {"data": {"name": trimmed_name}}}
            )
            user = result.user
            if not user:
                raise Exception("Failed to create user")
            # Check if profile exists
            profile_response = supabase.table("profiles").select("*").eq("id", user.id).single().execute()
            if not profile_response.data:
                # Create profile manually
                try:
                    supabase.table("profiles").insert(
                        {"id": user.id, "email": email, "full_name": trimmed_name, "status": "pending"}
                    ).execute()
                except Exception as e:
                    print("Error creating profile manually:", str(e))
                    raise Exception("Error creating user profile")
            rx.toast.info("Your account has been created and is pending approval by an administrator.")
            supabase.auth.sign_out()
            self.user = None
            self.is_authenticated = False
        except Exception as e:
            print("Signup failed:", e)
            rx.toast.error(str(e))
            raise
        finally:
            self.is_loading = False

    def logout(self):
        try:
            supabase.auth.sign_out()
            self.user = None
            self.is_authenticated = False
        except Exception as e:
            print("Logout failed:", e)
            rx.toast.error(str(e))
            raise

    def load_session(self):
        self.is_loading = True
        try:
            session = supabase.auth.get_session()
            self.session = session
            if session and hasattr(session, "user"):
                self.handle_user_session(session.user)
            else:
                self.user = None
                self.is_authenticated = False
        except Exception as e:
            print("Error loading session:", e)
            self.user = None
            self.is_authenticated = False
        finally:
            self.is_loading = False

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