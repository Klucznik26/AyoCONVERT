from core.convert_settings_logic import SettingsLogic
from core.convert_theme_selector_theme_arctic import THEME as ARCTIC_THEME
from core.convert_theme_selector_theme_creative import THEME as CREATIVE_THEME
from core.convert_theme_selector_theme_dark import THEME as DARK_THEME
from core.convert_theme_selector_theme_light import THEME as LIGHT_THEME
from core.convert_theme_selector_theme_relax import THEME as RELAX_THEME
from core.convert_theme_selector_theme_system import THEME as SYSTEM_THEME


_THEME_MAP = {'dark': DARK_THEME, 'light': LIGHT_THEME, 'creative': CREATIVE_THEME, 'relax': RELAX_THEME, 'arctic': ARCTIC_THEME, 'system': SYSTEM_THEME}


class ThemeSelectorLogic:
    @staticmethod
    def get_theme_codes() -> list[str]:
        return SettingsLogic.get_theme_codes()

    @staticmethod
    def get_theme(theme_name: str | None = None) -> dict:
        return _THEME_MAP.get(theme_name or SettingsLogic.get_theme(), SYSTEM_THEME)

    @staticmethod
    def get_preview_palette(theme_name: str | None = None) -> dict:
        theme = ThemeSelectorLogic.get_theme(theme_name)
        return {'bg': theme['bg_panel'], 'text': theme['text'], 'glow': theme['accent']}

    @staticmethod
    def get_stylesheet(theme_name: str | None = None) -> str:
        t = ThemeSelectorLogic.get_theme(theme_name)
        narrow_bg = t.get('narrow_bg', t['bg_panel'])
        narrow_border = t.get('narrow_border', t['border'])
        panel_border = t.get('panel_border', t['border'])
        drop_bg = t.get('drop_bg', t['bg_panel_alt'])
        drop_border = t.get('drop_border', f"2px dashed {t['border']}")
        drop_radius = t.get('drop_radius', '10px')
        drop_color = t.get('drop_color', t['text_muted'])
        btn_hover_border = t.get('button_hover_border', f"1px solid {t['border']}")
        btn_hover_text = t.get('button_hover_text', t['text'])
        btn_pressed_text = t.get('button_pressed_text', t['text'])
        btn_disabled_border = t.get('button_disabled_border', 'none')
        item_hover_bg = t.get('item_hover_bg', t.get('button_hover', 'transparent'))
        item_hover_text = t.get('item_hover_text', t['text'])
        scroll_handle = t.get('scrollbar_handle', t['accent'])
        scroll_hover = t.get('scrollbar_handle_hover', t['accent_hover'])
        icon_color = t.get('icon_color', t['text'])
        list_text = t.get('list_text', t['text'])
        run_btn_bg = t.get('run_btn_bg', t['accent'])
        run_btn_color = t.get('run_btn_color', t['selection_text'])
        run_btn_border = t.get('run_btn_border', 'none')
        run_btn_hover_bg = t.get('run_btn_hover_bg', t['accent_hover'])
        run_btn_hover_color = t.get('run_btn_hover_color', t['selection_text'])
        run_btn_hover_border = t.get('run_btn_hover_border', 'none')
        run_btn_pressed_bg = t.get('run_btn_pressed_bg', t['accent_pressed'])
        slider_sub = t.get('run_btn_bg', t['button_hover'])

        return f"""
        QWidget {{ color: {t['text']}; font-size: 11px; font-family: 'Segoe UI', 'Noto Sans', 'Ubuntu', 'DejaVu Sans', sans-serif; }}
        QWidget#main_widget, QMainWindow {{ background-color: {t['bg_main']}; }}
        QFrame#leftPanel, QFrame#rightPanel {{ background-color: {t['bg_panel']}; border: 1px solid {panel_border}; border-radius: 14px; }}
        QFrame#narrowPanel {{ background: {narrow_bg}; border: 1px solid {narrow_border}; border-radius: 14px; }}
        QLabel {{ color: {t['text']}; }}
        QLabel[secondary='true'] {{ color: {t['text_muted']}; }}
        QLabel#dropArea {{ background: {drop_bg}; color: {drop_color}; font-size: 16px; border: {drop_border}; border-radius: {drop_radius}; padding: 15px; }}
        QLabel#cornerLogo {{ min-width: 150px; min-height: 150px; padding: 0; background-color: {t['corner_bg']}; border: 1px solid {t['border']}; border-radius: 10px; }}
        QPushButton {{ background-color: {t['button_bg']}; color: {t['text']}; border: 1px solid {t['border']}; border-radius: 8px; padding: 8px 12px; }}
        QPushButton:hover {{ background-color: {t['button_hover']}; border: {btn_hover_border}; color: {btn_hover_text}; }}
        QPushButton:pressed {{ background-color: {t['button_pressed']}; color: {btn_pressed_text}; }}
        QPushButton:disabled {{ background-color: {t['button_disabled_bg']}; color: {t['button_disabled_text']}; border: {btn_disabled_border}; }}
        QPushButton#runButton {{ background-color: {run_btn_bg}; color: {run_btn_color}; border: {run_btn_border}; font-weight: bold; }}
        QPushButton#runButton:hover {{ background-color: {run_btn_hover_bg}; color: {run_btn_hover_color}; border: {run_btn_hover_border}; }}
        QPushButton#runButton:pressed {{ background-color: {run_btn_pressed_bg}; }}
        QPushButton#iconButton {{ background-color: transparent; border: none; color: {icon_color}; font-size: 20px; border-radius: 10px; padding: 0; }}
        QPushButton#iconButton:hover {{ background-color: {t['hover']}; color: {t['title']}; }}
        QPushButton#iconButton[danger='true']:hover {{ background-color: {t['danger_hover']}; color: {t['danger']}; }}
        QToolButton {{ background-color: transparent; border: none; border-radius: 4px; color: {icon_color}; padding: 4px; }}
        QToolButton:hover {{ background-color: {t['hover']}; color: {t['title']}; }}
        QToolButton:pressed {{ background-color: {t['accent']}; color: {t['selection_text']}; }}
        QDialog {{ background-color: {t['bg_main']}; color: {t['text']}; }}
        QComboBox, QLineEdit {{ background-color: {t['field_bg']}; color: {t['text']}; border: 1px solid {t['border']}; border-radius: 6px; padding: 5px; }}
        QComboBox:focus, QLineEdit:focus {{ border: 1px solid {t['accent']}; background-color: {t['bg_panel']}; }}
        QComboBox::drop-down {{ border: none; }}
        QComboBox QAbstractItemView, QListWidget, QListView, QTreeView, QTableWidget {{ background-color: {t['field_alt_bg']}; color: {list_text}; border: 1px solid {t['border']}; outline: none; selection-background-color: {t['selection_bg']}; selection-color: {t['selection_text']}; border-radius: 6px; }}
        QListWidget::item:hover, QListView::item:hover, QTreeView::item:hover, QTableWidget::item:hover {{ background-color: {item_hover_bg}; color: {item_hover_text}; }}
        QListWidget::item:selected, QListView::item:selected, QTreeView::item:selected, QTableWidget::item:selected {{ background-color: {t['selection_bg']}; color: {t['selection_text']}; }}
        QHeaderView::section {{ background-color: {t['button_bg']}; color: {t['text']}; border: none; border-right: 1px solid {t['border']}; border-bottom: 1px solid {t['border']}; padding: 4px; }}
        QScrollBar:vertical {{ background: {t['field_alt_bg']}; width: 12px; margin: 2px; border-radius: 6px; }}
        QScrollBar::handle:vertical {{ background: {scroll_handle}; min-height: 24px; border-radius: 6px; }}
        QScrollBar::handle:vertical:hover {{ background: {scroll_hover}; }}
        QScrollBar:horizontal {{ background: {t['field_alt_bg']}; height: 12px; margin: 2px; border-radius: 6px; }}
        QScrollBar::handle:horizontal {{ background: {scroll_handle}; min-width: 24px; border-radius: 6px; }}
        QScrollBar::handle:horizontal:hover {{ background: {scroll_hover}; }}
        QScrollBar::add-line, QScrollBar::sub-line, QScrollBar::add-page, QScrollBar::sub-page {{ background: transparent; border: none; }}
        QProgressBar {{ background-color: {t['field_bg']}; border: 1px solid {t['border']}; border-radius: 6px; text-align: center; color: {t['text']}; }}
        QProgressBar::chunk {{ background-color: {t['accent']}; border-radius: 5px; }}
        QSlider::groove:horizontal {{ height: 6px; background: {t['field_bg']}; border-radius: 3px; }}
        QSlider::handle:horizontal {{ background: {t['accent']}; width: 16px; margin: -5px 0; border-radius: 8px; }}
        QSlider::sub-page:horizontal {{ background: {slider_sub}; border-radius: 3px; }}
        QSlider::add-page:horizontal {{ background: {t['field_bg']}; border-radius: 3px; }}
        """
