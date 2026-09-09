import json
from urllib.parse import urlencode
from urllib.request import Request, urlopen
from urllib.error import HTTPError, URLError

from mobile.config import (
    SUPABASE_URL,
    SUPABASE_ANON_KEY,
    API_TIMEOUT,
)


class ApiError(RuntimeError):
    pass


class _Response:

    def __init__(self, status, body):
        self.status_code = status
        self._body = body or b""

    @property
    def ok(self):
        return 200 <= self.status_code < 300

    def json(self):
        if not self._body:
            return {}

        try:
            return json.loads(
                self._body.decode("utf-8")
            )
        except Exception:
            return {}

    def text(self):
        return self._body.decode(
            "utf-8",
            errors="replace"
        )


def _request(
    method,
    url,
    headers=None,
    payload=None,
    params=None,
    timeout=15,
):

    if params:
        query = urlencode(
            params,
            doseq=True
        )

        url += (
            "&" if "?" in url else "?"
        ) + query

    data = None

    req_headers = dict(
        headers or {}
    )

    if payload is not None:

        data = json.dumps(
            payload,
            ensure_ascii=False
        ).encode("utf-8")

        req_headers["Content-Type"] = (
            "application/json"
        )

    request = Request(
        url,
        data=data,
        headers=req_headers,
        method=method,
    )

    try:

        with urlopen(
            request,
            timeout=timeout
        ) as response:

            return _Response(
                response.status,
                response.read(),
            )

    except HTTPError as exc:

        try:
            body = exc.read()
        except Exception:
            body = b""

        return _Response(
            exc.code,
            body,
        )

    except URLError as exc:

        raise ApiError(
            "خطای اتصال به سرور: "
            + str(exc.reason)
        ) from exc

    except TimeoutError as exc:

        raise ApiError(
            "زمان اتصال به سرور به پایان رسید."
        ) from exc

    except OSError as exc:

        raise ApiError(
            "خطای شبکه: "
            + str(exc)
        ) from exc


class SupabaseClient:

    def __init__(self):

        self.url = (
            SUPABASE_URL or ""
        ).rstrip("/")

        self.key = (
            SUPABASE_ANON_KEY or ""
        )

        self.access_token = ""
        self.refresh_token = ""
        self.expires_in = None
        self.expires_at = None
        self.token_type = "bearer"


    @property
    def configured(self):

        return bool(
            self.url
            and self.key
        )


    def _headers(
        self,
        authenticated=False
    ):

        headers = {
            "apikey": self.key,
            "Content-Type": (
                "application/json"
            ),
        }

        if (
            authenticated
            and self.access_token
        ):

            headers["Authorization"] = (
                f"Bearer {self.access_token}"
            )

        return headers

    # -------------------------------------------------
    # SERVER HEALTH / SESSION VALIDATION
    # -------------------------------------------------

    def health_check(self):
        """Check that the configured Supabase Auth service is reachable."""
        if not self.configured:
            return False, "تنظیمات سرور وارد نشده است."
        try:
            response = _request(
                "GET",
                f"{self.url}/auth/v1/settings",
                headers={"apikey": self.key},
                timeout=API_TIMEOUT,
            )
            if response.ok:
                return True, "اتصال به سرور برقرار است."
            return False, self._error(response, "سرور پاسخ معتبر نداد.")
        except Exception as exc:
            return False, str(exc)

    def validate_session(self):
        """Validate the current access token against Supabase Auth."""
        if not self.configured or not self.access_token:
            return False
        try:
            response = _request(
                "GET",
                f"{self.url}/auth/v1/user",
                headers=self._headers(True),
                timeout=API_TIMEOUT,
            )
            if response.ok:
                user = response.json() or {}
                return bool(user.get("id"))
            return False
        except Exception as exc:
            print("SESSION VALIDATION ERROR:", repr(exc))
            return False

    # -------------------------------------------------
    # AUTHENTICATION
    # -------------------------------------------------

    def sign_in(
        self,
        identifier,
        password
    ):

        identifier = (
            identifier or ""
        ).strip()

        password = (
            password or ""
        )


        # =============================================
        # ورود واقعی Supabase
        # =============================================


        if not self.configured:

            raise ApiError(
                "اتصال سرور در این نسخه تنظیم نشده است."
            )


        if not identifier:

            raise ApiError(
                "کد ملی را وارد کنید."
            )


        if not password:

            raise ApiError(
                "رمز عبور را وارد کنید."
            )


        if "@" in identifier:

            email = identifier


        else:

            if not identifier.isdigit():

                raise ApiError(
                    "کد ملی باید فقط شامل اعداد باشد."
                )


            if len(identifier) != 10:

                raise ApiError(
                    "کد ملی باید ۱۰ رقم باشد."
                )


            email = (
                self.resolve_email_by_national_code(
                    identifier
                )
            )


            if not email:

                raise ApiError(
                    "کاربری با این کد ملی پیدا نشد."
                )


        response = _request(

            "POST",

            f"{self.url}/auth/v1/token"
            "?grant_type=password",

            headers=self._headers(),

            payload={

                "email":
                    email,

                "password":
                    password,

            },

            timeout=API_TIMEOUT,
        )


        if not response.ok:

            raise ApiError(

                self._error(

                    response,

                    "کد ملی یا رمز عبور صحیح نیست."

                )

            )


        data = (
            response.json()
            or {}
        )


        self.access_token = (

            data.get(
                "access_token"
            )
            or ""

        )


        self.refresh_token = (

            data.get(
                "refresh_token"
            )
            or ""

        )


        self.expires_in = (

            data.get(
                "expires_in"
            )

        )


        self.expires_at = (

            data.get(
                "expires_at"
            )

        )


        self.token_type = (

            data.get(
                "token_type"
            )
            or "bearer"

        )


        if not self.access_token:

            raise ApiError(
                "سرور نشست معتبر ایجاد نکرد."
            )


        user = (

            data.get(
                "user"
            )
            or {}

        )


        profile = (
            self._profile(user)
        )


        profile.setdefault(

            "email",

            user.get(
                "email",
                email
            )

        )


        return {

            "user":
                user,

            "profile":
                profile,

            "access_token":
                self.access_token,

            "refresh_token":
                self.refresh_token,

            "expires_in":
                self.expires_in,

            "expires_at":
                self.expires_at,

            "token_type":
                self.token_type,

        }

    def resolve_email_by_national_code(
        self,
        national_code
    ):

        if not self.configured:

            raise ApiError(
                "اتصال سرور فعال نیست."
            )


        national_code = str(
            national_code or ""
        ).strip()


        response = _request(

            "GET",

            f"{self.url}/rest/v1/account_settings",

            headers=self._headers(),

            params={

                "national_code":
                    f"eq.{national_code}",

                "select":
                    "email",

                "limit":
                    "1",

            },

            timeout=API_TIMEOUT,

        )


        if response.ok:

            rows = (
                response.json()
                or []
            )


            if (

                isinstance(
                    rows,
                    list
                )

                and rows

                and isinstance(
                    rows[0],
                    dict
                )

            ):

                return (
                    rows[0].get(
                        "email"
                    )
                )


        return None



    # -------------------------------------------------
    # PROFILE
    # -------------------------------------------------

    def _profile(
        self,
        user
    ):

        user = (
            user
            if isinstance(
                user,
                dict
            )
            else {}
        )


        metadata = (

            user.get(
                "user_metadata"
            )

            or {}

        )


        profile = {}


        for key in (

            "role",

            "display_name",

            "full_name",

            "username",

            "national_code",

            "first_name",

            "last_name",

        ):

            if key in metadata:

                profile[key] = (
                    metadata[key]
                )



        email = (

            user.get(
                "email"
            )

            or ""

        )


        try:

            response = _request(

                "GET",

                f"{self.url}/rest/v1/account_settings",

                headers=self._headers(True),

                params={

                    "email":
                        f"eq.{email}",

                    "limit":
                        "1",

                },

                timeout=API_TIMEOUT,

            )


            if response.ok:

                rows = (

                    response.json()

                    or []

                )


                if rows and isinstance(

                    rows[0],

                    dict

                ):

                    profile.update(
                        rows[0]
                    )


        except Exception:

            pass


        profile.setdefault(
            "email",
            email
        )


        profile.setdefault(
            "username",
            email
        )


        profile.setdefault(
            "display_name",
            email
        )


        return profile



    # -------------------------------------------------
    # TOKEN
    # -------------------------------------------------

    def refresh_access_token(
        self
    ):

        if (

            not self.configured

            or not self.refresh_token

        ):

            return False



        response = _request(

            "POST",

            f"{self.url}/auth/v1/token"
            "?grant_type=refresh_token",

            headers=self._headers(),

            payload={

                "refresh_token":
                    self.refresh_token

            },

            timeout=API_TIMEOUT,

        )


        if not response.ok:

            self.access_token = ""

            self.refresh_token = ""

            return False



        data = (

            response.json()

            or {}

        )


        token = (

            data.get(
                "access_token"
            )

            or ""

        )


        if not token:

            return False


        self.access_token = token


        if data.get(
            "refresh_token"
        ):

            self.refresh_token = (
                data.get(
                    "refresh_token"
                )
            )


        return True



    # -------------------------------------------------
    # TABLE METHODS
    # -------------------------------------------------

    def table_select(
        self,
        table,
        params=None
    ):

        if not self.access_token:

            raise ApiError(
                "نشست معتبر وجود ندارد."
            )


        response = _request(

            "GET",

            f"{self.url}/rest/v1/{table}",

            headers=self._headers(True),

            params=params or {
                "select": "*"
            },

            timeout=API_TIMEOUT,

        )


        if not response.ok:

            raise ApiError(
                self._error(response)
            )


        return response.json()



    def table_insert(
        self,
        table,
        payload
    ):

        if not self.access_token:

            raise ApiError(
                "نشست معتبر وجود ندارد."
            )


        response = _request(

            "POST",

            f"{self.url}/rest/v1/{table}",

            headers=self._headers(True),

            payload=payload,

            timeout=API_TIMEOUT,

        )


        if not response.ok:

            raise ApiError(
                self._error(response)
            )


        return response.json()



    def sign_out(
        self
    ):

        self.access_token = ""

        self.refresh_token = ""

        self.expires_in = None

        self.expires_at = None



    def _error(
        self,
        response,
        default="خطای سرور"
    ):

        try:

            data = response.json()

            if isinstance(
                data,
                dict
            ):

                return (

                    data.get(
                        "message"
                    )

                    or default

                )

        except Exception:

            pass


        return (
            f"{default} "
            f"({response.status_code})"
        )
