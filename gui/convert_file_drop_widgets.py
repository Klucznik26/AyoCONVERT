from PySide6.QtCore import Property, QEasingCurve, QPropertyAnimation, Qt, Signal
from PySide6.QtGui import QColor, QDragEnterEvent, QDropEvent, QLinearGradient, QPainter, QPainterPath, QPixmap
from PySide6.QtWidgets import QLabel, QSizePolicy

from core.convert_theme_selector_logic import ThemeSelectorLogic
from core.convert_settings_logic import SUPPORTED_IMAGE_EXTENSIONS, SettingsLogic


class FileDropLabel(QLabel):
    files_dropped = Signal(list)

    def __init__(self, parent=None):
        super().__init__(parent)
        self._animating = False
        self._rotation = 0.0
        self.error_loading_text = SettingsLogic.tr('err_image_load', 'Image loading error')
        self.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.setAcceptDrops(True)
        self.setScaledContents(False)
        self.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        self.setWordWrap(True)
        self.retranslate_ui()

    def get_rotation(self) -> float:
        return self._rotation

    def set_rotation(self, angle: float):
        self._rotation = angle
        self.update()

    rotation = Property(float, get_rotation, set_rotation)

    def retranslate_ui(self):
        self.error_loading_text = SettingsLogic.tr('err_image_load', 'Image loading error')
        if self.text() and not self.pixmap():
            self.setText(SettingsLogic.tr('lbl_drop'))

    def set_preview(self, file_path: str):
        self.setStyleSheet('')
        pixmap = QPixmap(file_path)
        if pixmap.isNull():
            self.setText(self.error_loading_text)
            return
        self.setPixmap(pixmap.scaled(self.size() * 0.9, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation))

    def animate_success(self, on_finished_callback):
        self._animating = True
        self.animation = QPropertyAnimation(self, b'rotation')
        self.animation.setDuration(400)
        self.animation.setStartValue(0.0)
        self.animation.setEndValue(-90.0)
        self.animation.setEasingCurve(QEasingCurve.Type.InBack)
        self.animation.finished.connect(lambda: self._finish_animation(on_finished_callback))
        self.animation.start()

    def _finish_animation(self, callback):
        self._animating = False
        self._rotation = 0.0
        self.clear()
        if callback:
            callback()

    def show_success(self, text: str):
        self.setText(text)
        theme = ThemeSelectorLogic.get_theme()
        accent = theme.get('accent', '#04E38A')
        if accent.startswith('#') and len(accent) == 7:
            bg_color = f'rgba({int(accent[1:3], 16)}, {int(accent[3:5], 16)}, {int(accent[5:7], 16)}, 0.1)'
        else:
            bg_color = 'rgba(4, 227, 138, 0.1)'
        self.setStyleSheet(f'font-size: 32px; font-weight: bold; color: {accent}; border: 3px solid {accent}; background-color: {bg_color};')

    def reset(self):
        self.setPixmap(QPixmap())
        self.setStyleSheet('')
        self.setText(SettingsLogic.tr('lbl_drop'))

    def paintEvent(self, event):
        painter_bg = QPainter(self)
        painter_bg.setRenderHint(QPainter.RenderHint.Antialiasing)
        theme_color = self.palette().color(self.backgroundRole())
        gradient = QLinearGradient(0, 0, 0, self.height())
        gradient.setColorAt(0.0, QColor(255, 255, 255, 30))
        gradient.setColorAt(0.1, QColor(theme_color.red(), theme_color.green(), theme_color.blue(), 180))
        gradient.setColorAt(0.5, QColor(theme_color.red(), theme_color.green(), theme_color.blue(), 70))
        gradient.setColorAt(0.9, QColor(theme_color.red(), theme_color.green(), theme_color.blue(), 180))
        gradient.setColorAt(1.0, QColor(0, 0, 0, 40))
        path = QPainterPath(); path.addRoundedRect(self.rect(), 12.0, 12.0)
        painter_bg.setClipPath(path)
        painter_bg.fillRect(self.rect(), gradient)
        painter_bg.setPen(QColor(255, 255, 255, 35))
        painter_bg.drawRoundedRect(self.rect(), 12.0, 12.0)
        painter_bg.end()
        if self._animating and self.pixmap() and not self.pixmap().isNull():
            painter = QPainter(self)
            painter.setRenderHint(QPainter.RenderHint.Antialiasing)
            painter.setRenderHint(QPainter.RenderHint.SmoothPixmapTransform)
            pixmap = self.pixmap()
            x = (self.width() - pixmap.width()) / 2
            y = (self.height() - pixmap.height()) / 2
            painter.save()
            if self._rotation < 0:
                opacity = 1.0 - (abs(self._rotation) / 90.0)
                painter.setOpacity(max(0.0, min(1.0, opacity)))
            painter.translate(x, y + pixmap.height())
            painter.rotate(self._rotation)
            painter.translate(-x, -(y + pixmap.height()))
            painter.drawPixmap(int(x), int(y), pixmap)
            painter.restore()
        else:
            super().paintEvent(event)

    def dragEnterEvent(self, event: QDragEnterEvent):
        if event.mimeData().hasUrls():
            event.acceptProposedAction()
            theme = ThemeSelectorLogic.get_theme()
            accent = theme.get('accent', '#04E38A')
            if accent.startswith('#') and len(accent) == 7:
                bg_color = f'rgba({int(accent[1:3], 16)}, {int(accent[3:5], 16)}, {int(accent[5:7], 16)}, 0.08)'
            else:
                bg_color = 'rgba(4, 227, 138, 0.08)'
            self.setStyleSheet(f'border: 2px dashed {accent}; background-color: {bg_color};')

    def dragLeaveEvent(self, event):
        self.setStyleSheet('')

    def dropEvent(self, event: QDropEvent):
        self.setStyleSheet('')
        paths = []
        for url in event.mimeData().urls():
            local_path = url.toLocalFile()
            if local_path:
                paths.append(local_path)
        if paths:
            self.files_dropped.emit(paths)
            event.acceptProposedAction()
