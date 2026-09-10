import requests
from urllib.parse import quote

from mobile.config import SUPABASE_URL, SUPABASE_ANON_KEY, API_TIMEOUT


class SupabaseClient:
    """Small, dependency-light Supabase REST/Auth client for the mobile app."""

    def __init__(self):
        self.supabase_url = (SUPABASE_URL or "").rstrip("/")
        self.supabase_key = SUPABASE_ANON_KEY or ""
        self.access_token = ""
        self.refresh_token = ""
        self.expires_in = None
        self.expires_at = None
        self.token_type = "bearer"

    @property
    def configured(self):
        return bool(self.supabase_url and self.supabase_key)

    def _headers(self, authenticated=False):
        headers = {
            "apikey": self.supabase_key,
            "Content-Type": "application/json",
        }
        if authenticated and self.access_token:
            headers["Authorization"] = f"Bearer {self.access_token}"
        else:
            headers["Authorization"] = f"Bearer {self.supabase_key}"
        return headers

    def _request(self, method, path, **kwargs):
        if not self.configured:
            raise RuntimeError("تنظیمات اتصال به سرور فراهوش کامل نشده است.")
        url = f"{self.supabase_url}/{path.lstrip('/')}"
        headers = kwargs.pop("headers", None) or self._headers(
            authenticated=kwargs.pop("authenticated", False)
        )
        response = requests.request(
            method,
            url,
            headers=headers,
            timeout=API_TIMEOUT,
            **kwargs,
        )
        return response

    def login(self, national_code, password):
        """Login with national code by resolving it to the user's Auth email."""
        email = self.get_user_email(national_code)
        if not email:
            return None

        response = self._request(
            "POST",
            "/auth/v1/token?grant_type=password",
            json={"email": email, "password": password},
        )
        if response.status_code != 200:
            print("LOGIN STATUS:", response.status_code, response.text)
            return None

        result = response.json()
        self.access_token = result.get("access_token") or ""
        self.refresh_token = result.get("refresh_token") or ""
        self.expires_in = result.get("expires_in")
        self.token_type = result.get("token_type") or "bearer"
        return self._build_session(result, national_code)

    def _build_session(self, result, national_code):
        user = result.get("user") or {}
        profile = self.get_profile(national_code, user)
        return {
            "access_token": self.access_token,
            "refresh_token": self.refresh_token,
            "expires_in": self.expires_in,
            "token_type": self.token_type,
            "user": user,
            "profile": profile,
        }

    def get_user_email(self, national_code):
        value = quote(str(national_code).strip(), safe="")
        # The application data model uses the users table for the national-code lookup.
        response = self._request(
            "GET",
            f"/rest/v1/users?select=*&national_code=eq.{value}&limit=1",
        )
        if response.status_code != 200:
            print("USER LOOKUP STATUS:", response.status_code, response.text)
            return None
        rows = response.json()
        if not isinstance(rows, list) or not rows:
            return None
        return rows[0].get("email")

    def get_profile(self, national_code, user=None):
        value = quote(str(national_code).strip(), safe="")
        response = self._request(
            "GET",
            f"/rest/v1/users?select=*&national_code=eq.{value}&limit=1",
        )
        if response.status_code == 200:
            rows = response.json()
            if isinstance(rows, list) and rows:
                return rows[0]
        return user or {}

    def health_check(self):
        try:
            response = self._request("GET", "/auth/v1/settings")
            if response.status_code == 200:
                return True, "اتصال به سرور برقرار است."
            return False, f"سرور پاسخ {response.status_code} برگرداند."
        except Exception as exc:
            return False, str(exc)

    def validate_session(self):
        if not self.access_token:
            return False
        try:
            response = self._request("GET", "/auth/v1/user", authenticated=True)
            return response.status_code == 200
        except Exception as exc:
            print("SESSION VALIDATION ERROR:", repr(exc))
            return False

    def refresh_access_token(self):
        if not self.refresh_token:
            return False
        response = self._request(
            "POST",
            "/auth/v1/token?grant_type=refresh_token",
            json={"refresh_token": self.refresh_token},
        )
        if response.status_code != 200:
            print("REFRESH STATUS:", response.status_code, response.text)
            return False
        result = response.json()
        self.access_token = result.get("access_token") or ""
        self.refresh_token = result.get("refresh_token") or self.refresh_token
        self.expires_in = result.get("expires_in")
        self.token_type = result.get("token_type") or "bearer"
        return bool(self.access_token)

    def sign_out(self):
        if not self.access_token:
            return True
        try:
            response = self._request("POST", "/auth/v1/logout", authenticated=True)
            return response.status_code in (200, 204)
        except Exception as exc:
            print("SIGN OUT ERROR:", repr(exc))
            return False

    def table_select(self, table, select="*"):
        table_q = quote(str(table), safe="_")
        select_q = quote(str(select), safe="*,()")
        response = self._request(
            "GET",
            f"/rest/v1/{table_q}?select={select_q}",
            authenticated=bool(self.access_token),
        )
        if response.status_code not in (200, 206):
            print("TABLE SELECT STATUS:", table, response.status_code, response.text)
            return []
        data = response.json()
        return data if isinstance(data, list) else []

    def table_insert(self, table, payload):
        table_q = quote(str(table), safe="_")
        response = self._request(
            "POST",
            f"/rest/v1/{table_q}",
            json=payload,
            authenticated=True,
            headers={**self._headers(True), "Prefer": "return=representation"},
        )
        if response.status_code not in (200, 201):
            print("TABLE INSERT STATUS:", table, response.status_code, response.text)
            return None
        return response.json()


class APIService(SupabaseClient):
    """Backward-compatible name used by the login screen."""
    pass
