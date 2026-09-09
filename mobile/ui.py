from pathlib import Path

from kivy.core.text import LabelBase
from kivy.graphics import Color, RoundedRectangle, Line
from kivy.uix.widget import Widget
from kivy.uix.textinput import TextInput

from mobile.config import (
    FONT_REGULAR,
    FONT_BOLD,
    CARD,
    BORDER,
)


# ============================================================
# Font state
# ============================================================

_FONT_REGISTERED = False
_FONT_NAME = "Frahoosh"


# ============================================================
# Font registration
# ============================================================

def register_fonts():
    """
    Register the Persian/Arabic fonts used by Frahoosh.

    Returns:
        str: Registered font name when successful,
             otherwise an empty string.
    """

    global _FONT_REGISTERED

    if _FONT_REGISTERED:
        return _FONT_NAME

    regular = Path(FONT_REGULAR)
    bold = Path(FONT_BOLD)

    if not regular.is_file():
        print("FONT FILE NOT FOUND:", str(regular))
        return ""

    try:
        bold_path = (
            bold
            if bold.is_file()
            else regular
        )

        LabelBase.register(
            name=_FONT_NAME,
            fn_regular=str(regular),
            fn_bold=str(bold_path),
            fn_italic=str(regular),
            fn_bolditalic=str(bold_path),
        )

        _FONT_REGISTERED = True

        print(
            "FRAHOOSH FONT REGISTERED:",
            str(regular)
        )

        return _FONT_NAME

    except Exception as exc:
        print(
            "FONT REGISTER ERROR:",
            repr(exc)
        )
        return ""


# ============================================================
# Font helper
# ============================================================

def font_name():
    """
    Return the Frahoosh font if available.
    Falls back to Roboto so the application never crashes
    because of a missing font.
    """

    registered = register_fonts()

    if registered:
        return registered

    return "Roboto"


# ============================================================
# Persian / RTL text normalization
# ============================================================

def rtl_text(value):
    """
    Normalize and reshape Persian/Arabic text for Kivy.

    The application stores normal Persian text, while this
    function prepares it for visual RTL rendering.
    """

    text = str(value or "")

    # --------------------------------------------------------
    # Arabic -> Persian character normalization
    # --------------------------------------------------------

    replacements = {
        "ي": "ی",
        "ى": "ی",
        "ك": "ک",
        "ۀ": "هٔ",
        "ة": "ه",
    }

    for old, new in replacements.items():
        text = text.replace(old, new)

    # --------------------------------------------------------
    # Arabic shaping + bidi
    # --------------------------------------------------------

    try:
        import arabic_reshaper
        from bidi.algorithm import get_display

        reshaped = arabic_reshaper.reshape(text)

        return get_display(reshaped)

    except Exception as exc:
        # Never allow a missing RTL package to crash the app.
        print(
            "RTL RENDER ERROR:",
            repr(exc)
        )

        return text


# ============================================================
# Persian TextInput
# ============================================================

class PersianTextInput(TextInput):
    """
    TextInput optimized for Persian/Farsi UI.
    """

    def __init__(self, **kwargs):

        register_fonts()

        kwargs.setdefault(
            "font_name",
            font_name()
        )

        kwargs.setdefault(
            "halign",
            "right"
        )

        kwargs.setdefault(
            "multiline",
            False
        )

        kwargs.setdefault(
            "cursor_width",
            2
        )

        # Better Persian input defaults.
        kwargs.setdefault(
            "padding",
            [12, 10, 12, 10]
        )

        kwargs.setdefault(
            "write_tab",
            False
        )

        super().__init__(
            **kwargs
        )


# ============================================================
# Card widget
# ============================================================

class Card(Widget):
    """
    Simple rounded card used throughout Frahoosh mobile UI.
    """

    def __init__(
        self,
        radius=18,
        **kwargs
    ):

        super().__init__(
            **kwargs
        )

        self.radius = radius

        # ----------------------------------------------------
        # Background
        # ----------------------------------------------------

        with self.canvas.before:

            self._color = Color(
                *CARD
            )

            self._rect = RoundedRectangle(
                pos=self.pos,
                size=self.size,
                radius=[
                    radius
                ],
            )

            # ------------------------------------------------
            # Border
            # ------------------------------------------------

            self._line_color = Color(
                *BORDER
            )

            self._line = Line(
                rounded_rectangle=(
                    self.x,
                    self.y,
                    self.width,
                    self.height,
                    radius,
                ),
                width=0.8,
            )

        self.bind(
            pos=self._sync,
            size=self._sync,
        )

    # --------------------------------------------------------
    # Synchronize canvas
    # --------------------------------------------------------

    def _sync(self, *_):

        self._rect.pos = self.pos
        self._rect.size = self.size

        self._line.rounded_rectangle = (
            self.x,
            self.y,
            self.width,
            self.height,
            self.radius,
        )

    # --------------------------------------------------------
    # Runtime color update
    # --------------------------------------------------------

    def set_background(self, color):

        try:
            self._color.rgba = color
        except Exception as exc:
            print(
                "CARD COLOR ERROR:",
                repr(exc)
            )

    def set_border(self, color):

        try:
            self._line_color.rgba = color
        except Exception as exc:
            print(
                "CARD BORDER ERROR:",
                repr(exc)
            )
