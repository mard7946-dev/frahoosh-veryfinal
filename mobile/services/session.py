import json
import os
from pathlib import Path


def _session_file():

    try:
        from kivy.app import App

        app = App.get_running_app()

        if app is not None:
            base = Path(
                app.user_data_dir
            )
        else:
            base = (
                Path.home()
                / ".frahoosh"
            )

    except Exception:
        base = (
            Path.home()
            / ".frahoosh"
        )

    try:
        base.mkdir(
            parents=True,
            exist_ok=True
        )
    except Exception:
        pass

    return base / "session.json"


def _atomic_write(
    path,
    content
):

    temp = path.with_suffix(
        ".tmp"
    )

    try:

        temp.write_text(
            content,
            encoding="utf-8"
        )

        os.replace(
            str(temp),
            str(path)
        )

        return True

    except Exception as exc:

        print(
            "SESSION WRITE ERROR:",
            repr(exc)
        )

        try:
            if temp.exists():
                temp.unlink()
        except Exception:
            pass

        return False


def save_session(data):

    if not isinstance(
        data,
        dict
    ):
        return False

    try:

        content = json.dumps(
            data,
            ensure_ascii=False,
            separators=(
                ",",
                ":"
            )
        )

        return _atomic_write(
            _session_file(),
            content
        )

    except Exception as exc:

        print(
            "SAVE SESSION ERROR:",
            repr(exc)
        )

        return False


def load_session():

    try:

        path = _session_file()

        if not path.exists():
            return None

        raw = path.read_text(
            encoding="utf-8"
        )

        data = json.loads(
            raw
        )

        if not isinstance(
            data,
            dict
        ):
            return None

        if not data.get(
            "access_token"
        ):
            return None

        return data

    except Exception as exc:

        print(
            "LOAD SESSION ERROR:",
            repr(exc)
        )

        return None


def update_session_tokens(
    access_token,
    refresh_token=None,
    expires_in=None,
    expires_at=None,
    token_type=None
):

    session = (
        load_session()
        or {}
    )

    if access_token:
        session[
            "access_token"
        ] = access_token

    if refresh_token:
        session[
            "refresh_token"
        ] = refresh_token

    if expires_in is not None:
        session[
            "expires_in"
        ] = expires_in

    if expires_at is not None:
        session[
            "expires_at"
        ] = expires_at

    if token_type:
        session[
            "token_type"
        ] = token_type

    return save_session(
        session
    )


def clear_session():

    try:

        path = _session_file()

        if path.exists():
            path.unlink()

        return True

    except Exception as exc:

        print(
            "CLEAR SESSION ERROR:",
            repr(exc)
        )

        return False
