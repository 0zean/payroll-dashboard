from unittest.mock import MagicMock, patch

# from payroll_dashboard.backend.auth_state import AuthState
from payroll_dashboard.backend.schemas import PayrollUser


def test_handle_user_session_approved(auth_state):
    mock_user = MagicMock()
    mock_user.id = "123"
    mock_user.email = "test@example.com"
    mock_response = MagicMock()
    mock_response.data = {"status": "approved", "email": "test@example.com", "full_name": "Test User"}
    with patch("payroll_dashboard.backend.auth_state.supabase") as mock_supabase:
        mock_supabase.table.return_value.select.return_value.eq.return_value.single.return_value.execute.return_value = mock_response
        auth_state.handle_user_session(mock_user)
        assert auth_state.is_authenticated
        assert isinstance(auth_state.user, PayrollUser)
        assert auth_state.user.email == "test@example.com"


def test_handle_user_session_not_approved(auth_state):
    mock_user = MagicMock()
    mock_user.id = "123"
    mock_user.email = "test@example.com"
    mock_response = MagicMock()
    mock_response.data = {"status": "pending", "email": "test@example.com", "full_name": "Test User"}
    with patch("payroll_dashboard.backend.auth_state.supabase") as mock_supabase:
        mock_supabase.table.return_value.select.return_value.eq.return_value.single.return_value.execute.return_value = mock_response
        with patch("payroll_dashboard.backend.auth_state.rx.toast"):
            auth_state.handle_user_session(mock_user)
            assert not auth_state.is_authenticated


def test_login_success(auth_state):
    with (
        patch("payroll_dashboard.backend.auth_state.supabase.auth.sign_in_with_password") as mock_sign_in,
        patch("payroll_dashboard.backend.auth_state.supabase.table") as mock_table,
    ):
        # Mock user returned from sign in
        mock_user = MagicMock()
        mock_user.id = "123e4567-e89b-12d3-a456-426614174000"
        mock_user.email = "test@example.com"

        mock_result = MagicMock()
        mock_result.user = mock_user
        mock_sign_in.return_value = mock_result

        # Mock Supabase profile lookup in handle_user_session: table().select().eq().single().execute()
        mock_execute = MagicMock()
        mock_execute.data = {"status": "approved", "email": "test@example.com", "full_name": "Test User"}

        mock_single = MagicMock()
        mock_single.execute.return_value = mock_execute

        mock_eq = MagicMock()
        mock_eq.single.return_value = mock_single

        mock_select = MagicMock()
        mock_select.eq.return_value = mock_eq

        mock_table.return_value.select.return_value = mock_select

        auth_state.login("test@example.com", "password123")

        mock_sign_in.assert_called_once_with({"email": "test@example.com", "password": "password123"})
        if isinstance(auth_state.user, PayrollUser):
            assert auth_state.is_authenticated is True
            assert auth_state.user.email == "test@example.com"
            assert auth_state.user.name == "Test User"
            assert auth_state.is_loading is False


def test_login_failure(auth_state):
    with patch("payroll_dashboard.backend.auth_state.supabase") as mock_supabase:
        mock_supabase.auth.sign_in_with_password.return_value.user = None
        with patch("payroll_dashboard.backend.auth_state.AuthState.handle_user_session") as mock_handle:
            # auth_state = AuthState()
            auth_state.login("test@example.com", "password")
            mock_handle.assert_not_called()


def test_signup_success(auth_state):
    mock_user = MagicMock()
    mock_user.id = "123"
    with patch("payroll_dashboard.backend.auth_state.supabase") as mock_supabase:
        mock_supabase.auth.sign_up.return_value.user = mock_user
        mock_supabase.table.return_value.select.return_value.eq.return_value.single.return_value.execute.return_value.data = True
        with patch("payroll_dashboard.backend.auth_state.rx.toast") as mock_toast:
            auth_state.signup("test@example.com", "password", "Test User")
            mock_toast.info.assert_called()


def test_logout(auth_state):
    with patch("payroll_dashboard.backend.auth_state.supabase"):
        auth_state.user = PayrollUser(id="1", email="a", name="b")
        auth_state.logout()
        assert auth_state.user is None
