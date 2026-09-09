from mobile.services.api import (
    SupabaseClient
)

from mobile.services.session import (
    load_session,
    save_session,
    clear_session,
)


class AppState:

    def __init__(self):

        self.session = {}
        self.api = None

        try:

            self.api = SupabaseClient()

        except Exception as exc:

            print(
                "API INIT ERROR:",
                repr(exc)
            )

            self.api = None

        try:

            self.session = (
                load_session()
                or {}
            )

        except Exception:

            self.session = {}

        self._load_tokens()

    # -----------------------------------------
    # TOKEN
    # -----------------------------------------

    def _load_tokens(self):

        if self.api is None:
            return

        session = (
            self.session
            if isinstance(
                self.session,
                dict
            )
            else {}
        )

        self.api.access_token = (
            session.get(
                "access_token",
                ""
            )
            or ""
        )

        self.api.refresh_token = (
            session.get(
                "refresh_token",
                ""
            )
            or ""
        )

        self.api.expires_in = (
            session.get(
                "expires_in"
            )
        )

        self.api.expires_at = (
            session.get(
                "expires_at"
            )
        )

        self.api.token_type = (
            session.get(
                "token_type",
                "bearer"
            )
            or "bearer"
        )

    # -----------------------------------------
    # USER
    # -----------------------------------------

    @property
    def user(self):

        if not isinstance(
            self.session,
            dict
        ):
            return {}

        value = (
            self.session.get(
                "user"
            )
            or {}
        )

        return (
            value
            if isinstance(
                value,
                dict
            )
            else {}
        )

    @property
    def profile(self):

        if not isinstance(
            self.session,
            dict
        ):
            return {}

        value = (
            self.session.get(
                "profile"
            )
            or {}
        )

        return (
            value
            if isinstance(
                value,
                dict
            )
            else {}
        )

    @property
    def role(self):

        profile = self.profile
        user = self.user

        role = (
            profile.get("role")
            or user.get("role")
        )

        metadata = user.get(
            "user_metadata"
        )

        if (
            not role
            and isinstance(
                metadata,
                dict
            )
        ):
            role = metadata.get(
                "role"
            )

        return str(
            role
            or "student"
        ).strip().lower()

    @property
    def national_code(self):

        profile = self.profile

        return str(
            profile.get(
                "national_code"
            )
            or profile.get(
                "nationalcode"
            )
            or profile.get(
                "national_id"
            )
            or ""
        ).strip()

    @property
    def display_name(self):

        profile = self.profile

        for key in (
            "display_name",
            "full_name",
            "name",
        ):

            value = profile.get(key)

            if value:
                return str(value)

        user = self.user

        metadata = user.get(
            "user_metadata"
        )

        if isinstance(
            metadata,
            dict
        ):

            for key in (
                "display_name",
                "full_name",
                "name",
            ):

                value = metadata.get(
                    key
                )

                if value:
                    return str(value)

        for key in (
            "display_name",
            "full_name",
            "name",
        ):

            value = user.get(key)

            if value:
                return str(value)

        return (
            user.get("email")
            or "کاربر فراهوش"
        )

    @property
    def server_configured(self):
        return bool(self.api and self.api.configured)

    def check_server(self):
        if not self.api:
            return False, "سرویس شبکه آماده نیست."
        return self.api.health_check()

    def validate_server_session(self):
        if not self.api or not self.api.validate_session():
            return False
        return True

    @property
    def logged_in(self):

        return bool(
            self.api is not None
            and self.api.access_token
            and isinstance(
                self.session,
                dict
            )
        )

    # -----------------------------------------
    # SESSION
    # -----------------------------------------

    def set_session(
        self,
        payload
    ):

        if not isinstance(
            payload,
            dict
        ):
            return False

        access_token = (
            payload.get(
                "access_token"
            )
            or ""
        )

        if not access_token:
            self.logout()
            return False

        self.session = dict(
            payload
        )

        self._load_tokens()

        return save_session(
            self.session
        )

    def persist_refreshed_token(self):

        if (
            self.api is None
            or not self.api.access_token
        ):
            return False

        if not isinstance(
            self.session,
            dict
        ):
            self.session = {}

        self.session[
            "access_token"
        ] = self.api.access_token

        if self.api.refresh_token:
            self.session[
                "refresh_token"
            ] = self.api.refresh_token

        if self.api.expires_in is not None:
            self.session[
                "expires_in"
            ] = self.api.expires_in

        if self.api.expires_at is not None:
            self.session[
                "expires_at"
            ] = self.api.expires_at

        if self.api.token_type:
            self.session[
                "token_type"
            ] = self.api.token_type

        return save_session(
            self.session
        )

    def refresh_session(self):

        if (
            self.api is None
            or not self.api.refresh_token
        ):
            return False

        try:

            if self.api.refresh_access_token():

                return (
                    self.persist_refreshed_token()
                )

        except Exception as exc:

            print(
                "REFRESH ERROR:",
                repr(exc)
            )

        return False

    def logout(self):

        try:

            if self.api is not None:
                self.api.sign_out()

        except Exception:
            pass

        clear_session()

        self.session = {}

        if self.api is not None:

            self.api.access_token = ""
            self.api.refresh_token = ""
            self.api.expires_in = None
            self.api.expires_at = None
            self.api.token_type = "bearer"

        return True
