from themes.dark import DARK_THEME
from themes.light import LIGHT_THEME
from themes.creative import CREATIVE_THEME as CREATIVE_THEME_BASE
from themes.relax import RELAX_THEME as RELAX_THEME_BASE
from themes.arctic import ARCTIC_THEME as ARCTIC_THEME_BASE
from themes.system import SYSTEM_THEME as SYSTEM_THEME_BASE

# Styl paneli i przycisków ikon jak w AyoARCHI
SIDEBAR_STYLE = """
    QFrame#leftPanel, QFrame#rightPanel {
        background: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 rgba(255, 255, 255, 0.20), stop:1 rgba(255, 255, 255, 0.08));
        border-radius: 14px;
        border: 1px solid rgba(255,255,255,0.40);
    }
    QFrame#narrowPanel {
        background: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 rgba(0, 0, 0, 0.25), stop:1 rgba(0, 0, 0, 0.15));
        border-radius: 14px;
        border: 1px solid rgba(255,255,255,0.1);
    }
    QPushButton#iconButton {
        background-color: transparent;
        border: none;
        font-size: 24px;
        padding: 8px;
        color: rgba(255, 255, 255, 0.85);
    }
    QPushButton#iconButton:hover {
        background-color: rgba(255, 255, 255, 0.15);
        border-radius: 10px;
    }
    QPushButton#iconButton[danger="true"] {
        color: #ff5a5a;
    }
    QPushButton#iconButton[danger="true"]:hover {
        color: #ff7a7a;
        background-color: rgba(255, 90, 90, 0.18);
        border-radius: 10px;
    }
"""

ARCTIC_SIDEBAR_STYLE = """
    QFrame#leftPanel, QFrame#rightPanel {
        background: qlineargradient(
            x1:0, y1:0, x2:1, y2:1,
            stop:0 rgba(220, 245, 255, 0.26),
            stop:1 rgba(120, 210, 255, 0.10)
        );
        border-radius: 14px;
        border: 1px solid rgba(140, 225, 255, 0.45);
    }
    QFrame#narrowPanel {
        background: qlineargradient(
            x1:0, y1:0, x2:0, y2:1,
            stop:0 rgba(120, 220, 255, 0.30),
            stop:0.55 rgba(80, 170, 220, 0.22),
            stop:1 rgba(40, 120, 175, 0.32)
        );
        border-radius: 14px;
        border: 1px solid rgba(165, 236, 255, 0.55);
    }
    QPushButton#iconButton {
        background-color: transparent;
        border: none;
        font-size: 24px;
        padding: 8px;
        color: #E7FBFF;
    }
    QPushButton#iconButton:hover {
        background-color: rgba(165, 236, 255, 0.24);
        border-radius: 10px;
    }
    QPushButton#iconButton[danger="true"] {
        color: #ff5a5a;
    }
    QPushButton#iconButton[danger="true"]:hover {
        color: #ff7a7a;
        background-color: rgba(255, 90, 90, 0.18);
        border-radius: 10px;
    }
"""


def get_style(theme_name):
    """Zwraca styl 1:1 jak w AyoARCHI dla wskazanego motywu."""
    theme_map = {
        "dark": DARK_THEME + SIDEBAR_STYLE,
        "light": LIGHT_THEME + SIDEBAR_STYLE,
        "relax": RELAX_THEME_BASE + SIDEBAR_STYLE,
        "creative": CREATIVE_THEME_BASE + SIDEBAR_STYLE,
        "arctic": ARCTIC_THEME_BASE + ARCTIC_SIDEBAR_STYLE,
        "system": SYSTEM_THEME_BASE + SIDEBAR_STYLE,
    }
    return theme_map.get(theme_name, theme_map["dark"])
