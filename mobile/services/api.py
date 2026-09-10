import json
from urllib.parse import quote
from urllib.request import Request, urlopen
from urllib.error import HTTPError, URLError

from mobile.config import SUPABASE_URL, SUPABASE_ANON_KEY, API_TIMEOUT


class SupabaseClient:
    """Minimal Supabase Auth + REST client using Python stdlib only."""

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

    def _headers(self, authenticated=False, extra=None):
        headers = {
            "apikey": self.supabase_key,
            "Content-Type": "application/json",
            "Accept": "application/json",
        }
        if authenticated and self.access_token:
            headers["Authorization"] = f"Bearer {self.access_token}"
        else:
            headers["Authorization"] = f"Bearer {self.supabase_key}"
        if extra:
            headers.update(extra)
        return headers

    def _request(self, method, path, payload=None, authenticated=False, extra_headers=None):
        if not self.configured:
            raise RuntimeError("تنظیمات اتصال به سرور فراهوش کامل نشده است.")

        url = f"{self.supabase_url}/{path.lstrip('/')}"
        body = None if payload is None else json.dumps(payload, ensure_ascii=False).encode("utf-8")
        request = Request(
            url,
            data=body,
            headers=self._headers(authenticated, extra_headers),
            method=method.upper(),
        )
        try:
            with urlopen(request, timeout=API_TIMEOUT) as response:
                raw = response.read().decode("utf-8")
                return response.status, raw
        except HTTPError as exc:
            raw = exc.read().decode("utf-8", errors="replace")
            return exc.code, raw
        except URLError as exc:
            raise RuntimeError(f"خطای شبکه: {exc.reason}") from exc
        except TimeoutError as exc:
            raise RuntimeError("مهلت اتصال به سرور تمام شد.") from exc

    @staticmethod
    def _json(raw):
        try:
            return json.loads(raw) if raw else None
        except Exception:
            return None

    def login(self, national_code, password):
        email = self.get_user_email(national_code)
        if not email:
            return None

        status, raw = self._request(
            "POST",
            "/auth/v1/token?grant_type=password",
            payload={"email": email, "password": password},
        )
        result = self._json(raw) or {}
        if status != 200 or not result.get("access_token"):
            print("LOGIN STATUS:", status, raw)
            return None

        self.access_token = result.get("access_token", "")
        self.refresh_token = result.get("refresh_token", "")
        self.expires_in = result.get("expires_in")
        self.expires_at = result.get("expires_at")
        self.token_type = result.get("token_type") or "bearer"

        user = result.get("user") or {}
        profile = self.get_profile(national_code, user)
        return {
            "access_token": self.access_token,
            "refresh_token": self.refresh_token,
            "expires_in": self.expires_in,
            "expires_at": self.expires_at,
            "token_type": self.token_type,
            "user": user,
            "profile": profile,
        }

    def get_user_email(self, national_code):
        value = quote(str(national_code).strip(), safe="")
        status, raw = self._request(
            "GET",
            f"/rest/v1/users?select=email&national_code=eq.{value}&limit=1",
        )
        if status != 200:
            print("USER LOOKUP STATUS:", status, raw)
            return None
        rows = self._json(raw)
        if not isinstance(rows, list) or not rows:
            return None
        return rows[0].get("email")

    def get_profile(self, national_code, user=None):
        value = quote(str(national_code).strip(), safe="")
        status, raw = self._request(
            "GET",
            f"/rest/v1/users?select=*&national_code=eq.{value}&limit=1",
            authenticated=True,
        )
        if status == 200:
            rows = self._json(raw)
            if isinstance(rows, list) and rows:
                return rows[0]
        return user or {}

    def health_check(self):
        try:
            status, _ = self._request("GET", "/auth/v1/settings")
            return (status == 200, "اتصال به سرور برقرار است." if status == 200 else f"سرور پاسخ {status} برگرداند.")
        except Exception as exc:
            return False, str(exc)

    def validate_session(self):
        if not self.access_token:
            return False
        try:
            status, _ = self._request("GET", "/auth/v1/user", authenticated=True)
            return status == 200
        except Exception as exc:
            print("SESSION VALIDATION ERROR:", repr(exc))
            return False

    def refresh_access_token(self):
        if not self.refresh_token:
            return False
        status, raw = self._request(
            "POST",
            "/auth/v1/token?grant_type=refresh_token",
            payload={"refresh_token": self.refresh_token},
        )
        result = self._json(raw) or {}
        if status != 200 or not result.get("access_token"):
            print("REFRESH STATUS:", status, raw)
            return False
        self.access_token = result.get("access_token", "")
        self.refresh_token = result.get("refresh_token") or self.refresh_token
        self.expires_in = result.get("expires_in")
        self.expires_at = result.get("expires_at")
        self.token_type = result.get("token_type") or "bearer"
        return True

    def sign_out(self):
        if not self.access_token:
            return True
        try:
            status, _ = self._request("POST", "/auth/v1/logout", authenticated=True)
            return status in (200, 204)
        except Exception as exc:
            print("SIGN OUT ERROR:", repr(exc))
            return False

    def table_select(self, table, select="*"):
        table_q = quote(str(table), safe="_")
        select_q = quote(str(select), safe="*,()")
        status, raw = self._request(
            "GET",
            f"/rest/v1/{table_q}?select={select_q}",
            authenticated=bool(self.access_token),
        )
        if status not in (200, 206):
            print("TABLE SELECT STATUS:", table, status, raw)
            return []
        data = self._json(raw)
        return data if isinstance(data, list) else []

    def table_insert(self, table, payload):
        table_q = quote(str(table), safe="_")
        status, raw = self._request(
            "POST",
            f"/rest/v1/{table_q}",
            payload=payload,
            authenticated=True,
            extra_headers={"Prefer": "return=representation"},
        )
        if status not in (200, 201):
            print("TABLE INSERT STATUS:", table, status, raw)
            return None
        return self._json(raw)


class APIService(SupabaseClient):
    pass
