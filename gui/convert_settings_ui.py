from pathlib import Path

from PySide6.QtCore import QRect, QSize, Qt, Signal
from PySide6.QtGui import QColor, QIcon, QImage, QPainter, QPixmap
from PySide6.QtWidgets import QFrame, QGraphicsDropShadowEffect, QPushButton, QVBoxLayout

from core.convert_settings_logic import SettingsLogic
from gui.convert_settings_info_ui import SettingsInfoUI
from gui.convert_settings_language_ui import SettingsLanguageUI
from gui.convert_theme_selector_ui import ThemeSelectorUI


class PanelIconButton(QPushButton):
    def __init__(self, icon_name: str, is_danger: bool = False, parent=None):
        super().__init__('', parent)
        self.setFixedSize(44, 44)
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.setObjectName('iconButton')
        self.setProperty('danger', is_danger)

        path = Path(__file__).resolve().parent.parent / 'assets' / 'icons' / icon_name
        self.pixmap = QPixmap()
        if path.exists():
            self.pixmap = self._crop(QPixmap(str(path)))

        self.shadow = QGraphicsDropShadowEffect()
        self.shadow.setBlurRadius(0)
        self.shadow.setOffset(0, 0)
        self.shadow.setColor(QColor(0, 0, 0, 0))
        self.setGraphicsEffect(self.shadow)

    def _crop(self, pixmap):
        if pixmap.isNull():
            return pixmap
        image = pixmap.toImage().convertToFormat(QImage.Format.Format_ARGB32)
        w, h = image.width(), image.height()
        points = [(x, y) for y in range(h) for x in range(w) if (image.pixel(x, y) >> 24) & 0xFF > 5]
        if not points:
            return pixmap
        xs, ys = zip(*points)
        return pixmap.copy(QRect(min(xs), min(ys), max(xs) - min(xs) + 1, max(ys) - min(ys) + 1))

    def enterEvent(self, event):
        self.shadow.setBlurRadius(16)
        self.shadow.setColor(QColor(2, 115, 70, 220))  # Ciemny szmaragd
        super().enterEvent(event)

    def leaveEvent(self, event):
        self.shadow.setBlurRadius(0)
        self.shadow.setColor(QColor(0, 0, 0, 0))
        super().leaveEvent(event)

    def paintEvent(self, event):
        super().paintEvent(event)
        if not self.pixmap.isNull():
            painter = QPainter(self)
            painter.setRenderHint(QPainter.RenderHint.SmoothPixmapTransform)
            target_size = 38  # Powiększone o dodatkowe 10 pikseli
            scaled_pix = self.pixmap.scaled(target_size, target_size, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
            x = (self.width() - scaled_pix.width()) // 2
            y = (self.height() - scaled_pix.height()) // 2
            painter.drawPixmap(x, y, scaled_pix)


class SettingsUI(QFrame):
    close_requested = Signal()
    language_changed = Signal(str)
    theme_changed = Signal(str)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName('narrowPanel')
        self.setFixedWidth(60)
        layout = QVBoxLayout(self); layout.setContentsMargins(0, 20, 0, 20); layout.setSpacing(20)
        self.btn_logo = self._create_button(); self._set_logo_icon(self.btn_logo); self.btn_logo.clicked.connect(self.show_info_dialog)
        self.btn_lang = self._create_button('languages.png'); self.btn_lang.clicked.connect(self.show_language_dialog)
        self.btn_theme = self._create_button('settings.png'); self.btn_theme.clicked.connect(self.show_theme_dialog)
        self.btn_close = self._create_button('exit.png', is_danger=True); self.btn_close.clicked.connect(self.close_requested.emit)
        layout.addWidget(self.btn_logo, 0, Qt.AlignmentFlag.AlignHCenter)
        layout.addStretch()
        layout.addWidget(self.btn_lang, 0, Qt.AlignmentFlag.AlignHCenter)
        layout.addWidget(self.btn_theme, 0, Qt.AlignmentFlag.AlignHCenter)
        layout.addWidget(self.btn_close, 0, Qt.AlignmentFlag.AlignHCenter)
        self.retranslate_ui()

    def _create_button(self, icon_name: str = '', is_danger: bool = False) -> QPushButton:
        if icon_name.endswith('.png'):
            return PanelIconButton(icon_name, is_danger, self)
        button = QPushButton(icon_name); button.setObjectName('iconButton'); button.setFixedSize(44, 44); button.setCursor(Qt.CursorShape.PointingHandCursor); return button

    def _set_logo_icon(self, button: QPushButton):
        path = Path(__file__).resolve().parent.parent / 'assets' / 'ACONVERT.png'
        if path.exists():
            pixmap = QPixmap(str(path))
            if not pixmap.isNull():
                button.setIcon(QIcon(pixmap)); button.setIconSize(QSize(39, 39)); return
        button.setText('A')

    def retranslate_ui(self):
        self.btn_logo.setToolTip(SettingsLogic.tr('btn_info'))
        self.btn_lang.setToolTip(SettingsLogic.tr('lbl_lang'))
        self.btn_theme.setToolTip(SettingsLogic.tr('lbl_theme'))
        self.btn_close.setToolTip(SettingsLogic.tr('btn_close'))

    def show_info_dialog(self):
        dialog = SettingsInfoUI(self); dialog.setStyleSheet(self.window().styleSheet()); dialog.exec()

    def show_language_dialog(self):
        dialog = SettingsLanguageUI(self); dialog.setStyleSheet(self.window().styleSheet()); dialog.language_selected.connect(self._apply_language); dialog.exec()

    def show_theme_dialog(self):
        dialog = ThemeSelectorUI(self); dialog.setStyleSheet(self.window().styleSheet()); dialog.theme_selected.connect(self._apply_theme); dialog.exec()

    def _apply_language(self, code: str):
        SettingsLogic.set_language_code(code); self.language_changed.emit(code)

    def _apply_theme(self, code: str):
        SettingsLogic.set_theme(code); self.theme_changed.emit(code)
