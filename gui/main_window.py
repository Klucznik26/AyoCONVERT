from pathlib import Path

from PySide6.QtCore import Qt, Signal, QTimer, QStringListModel
from PySide6.QtGui import QColor, QPainter, QPixmap
from PySide6.QtWidgets import QApplication, QGraphicsDropShadowEffect, QHBoxLayout, QMainWindow, QPushButton, QWidget

from core.translator import Translator
from . import dialogs
from .info_window import InfoWindow
from .language_window import LanguageWindow
from .main_window_layout import build_ui_panels
from .qt_i18n import AyoQtTranslator
from .settings_window import SettingsWindow
from .styles import get_style
from .theme_window import ThemeSelectionDialog


class ProgressButton(QPushButton):
    """Przycisk z możliwością wyświetlania paska postępu w tle."""

    def __init__(self, text, parent=None):
        super().__init__(text, parent)
        self._progress = 0.0

    def set_progress(self, value):
        self._progress = value
        self.update()

    def paintEvent(self, event):
        super().paintEvent(event)
        if self._progress > 0:
            painter = QPainter(self)
            painter.fillRect(0, 0, int(self.width() * self._progress), self.height(), QColor(158, 206, 106, 100))


class MainWindow(QMainWindow):
    files_dropped_signal = Signal(list)
    dir_selected_signal = Signal(str)
    conversion_requested_signal = Signal(str)

    progress_button_cls = ProgressButton
    string_list_model_cls = QStringListModel

    def __init__(self, config, qt_translator):
        super().__init__()
        self.config = config
        self.qt_translator = qt_translator
        self.translator = Translator(self.config)
        self._status_message_key = ""

        self.custom_qt_translator = AyoQtTranslator(self.translator.translations)
        QApplication.instance().installTranslator(self.custom_qt_translator)

        self.setWindowTitle("AyoConvert v 1.5.0")
        self.setMinimumSize(1000, 700)
        self.resize(1000, 700)

        self._init_ui()

        last_dir = self.config.get("last_save_dir")
        if last_dir and hasattr(self, "btn_save_dir"):
            self.btn_save_dir.setToolTip(f"Ostatni zapis: {last_dir}")

        self.progress_timer = QTimer()
        self.progress_timer.timeout.connect(self._update_button_progress)

        self.apply_theme(self.config.get("theme", "creative"))

    def _init_ui(self):
        if self.centralWidget():
            self.centralWidget().setParent(None)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        main_layout = QHBoxLayout(central_widget)
        main_layout.setContentsMargins(10, 10, 10, 10)
        main_layout.setSpacing(10)

        def add_shadow(widget):
            shadow = QGraphicsDropShadowEffect()
            shadow.setBlurRadius(30)
            shadow.setOffset(0, 6)
            shadow.setColor(QColor(0, 0, 0, 60))
            widget.setGraphicsEffect(shadow)

        build_ui_panels(self, main_layout, add_shadow)

        if self._status_message_key:
            self.lbl_status.setText(self.translator.get(self._status_message_key))
        else:
            self.lbl_status.setText("")

    def bind_on_files_dropped(self, handler):
        self.files_dropped_signal.connect(handler)

    def bind_on_dir_selected(self, handler):
        self.dir_selected_signal.connect(handler)

    def bind_on_conversion_requested(self, handler):
        self.conversion_requested_signal.connect(handler)

    def show_preview(self, file_path):
        self.drop_area.set_preview(file_path)

    def update_fan(self, file_paths):
        self.image_fan.set_images(file_paths)
        if len(file_paths) > 1:
            self.file_list_model.setStringList([Path(p).name for p in file_paths])
            self.lbl_files.setVisible(True)
            self.file_list.setVisible(True)
        else:
            self.file_list_model.setStringList([])
            self.lbl_files.setVisible(False)
            self.file_list.setVisible(False)

    def update_save_dir_tooltip(self, path):
        self.btn_save_dir.setToolTip(path)

    def set_status_message(self, key_msg):
        self._status_message_key = key_msg or ""
        self.lbl_status.setText("" if not key_msg else self.translator.get(key_msg))

    def set_run_enabled(self, enabled):
        self.btn_run.setEnabled(enabled)

    def show_success_message(self):
        self.progress_timer.stop()
        self.btn_run.set_progress(1.0)

        def on_anim_finished():
            self.drop_area.show_success(self.translator.get("lbl_done", "WYKONANO"))
            QTimer.singleShot(1000, lambda: self.btn_run.set_progress(0.0))

        self.drop_area.animate_success(on_anim_finished)

    def reset_after_conversion(self):
        self.image_fan.set_images([])
        self.file_list_model.setStringList([])
        self.lbl_files.setVisible(False)
        self.file_list.setVisible(False)

    def update_format_availability(self, source_ext):
        for i in range(self.format_choice.count()):
            format_item = self.format_choice.itemText(i)
            self.format_choice.model().item(i).setEnabled(format_item != source_ext)

    def handle_files(self, file_paths):
        if file_paths:
            self.files_dropped_signal.emit(file_paths)

    def select_save_directory(self):
        last_dir = self.config.get("last_save_dir", str(Path.home()))
        save_path = dialogs.select_save_directory(self, self.translator, last_dir)
        if save_path:
            self.dir_selected_signal.emit(save_path)

    def open_file_dialog(self):
        files = dialogs.open_files_dialog(self, self.translator, str(Path.home()))
        if files:
            self.handle_files(files)

    def open_source_directory(self):
        files = dialogs.open_directory_scan(self, self.translator, str(Path.home()))
        if files:
            self.handle_files(files)

    def start_conversion(self):
        self.btn_run.set_progress(0.0)
        self.progress_timer.start(50)
        self.conversion_requested_signal.emit(self.format_choice.currentText())

    def _update_button_progress(self):
        current = self.btn_run._progress
        if current < 0.85:
            self.btn_run.set_progress(current + 0.02)

    def show_settings(self):
        dialog = SettingsWindow(self.config, self.translator, self)
        if dialog.exec():
            self.translator.load_translations()
            self.custom_qt_translator.update_translations(self.translator.translations)
            self._init_ui()

    def show_language_window(self):
        dialog = LanguageWindow(self.config, self.translator, self)
        if dialog.exec():
            self.translator.load_translations()
            self.custom_qt_translator.update_translations(self.translator.translations)
            self._init_ui()

    def show_theme_window(self):
        dialog = ThemeSelectionDialog(self.translator, self)
        dialog.setStyleSheet(self.styleSheet())
        dialog.theme_selected.connect(self.apply_theme)
        dialog.exec()

    def show_info_window(self):
        dialog = InfoWindow(self.translator, self)
        dialog.setStyleSheet(self.styleSheet())
        dialog.exec()

    def apply_theme(self, theme_name):
        QApplication.instance().setStyleSheet(get_style(theme_name))
        self.config.set("theme", theme_name)

    def load_logo(self):
        path = Path(__file__).resolve().parent.parent / "assets" / "AyoCONVERT.png"
        if path.exists():
            pix = QPixmap(str(path))
            self.mini_logo.setPixmap(pix.scaled(180, 180, Qt.KeepAspectRatio, Qt.SmoothTransformation))
