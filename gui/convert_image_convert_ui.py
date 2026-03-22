from pathlib import Path

from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QColor, QPainter
from PySide6.QtWidgets import QComboBox, QFrame, QLabel, QMenu, QPushButton, QVBoxLayout

from core.convert_settings_logic import SettingsLogic


class ProgressButton(QPushButton):
    def __init__(self, text, parent=None):
        super().__init__(text, parent)
        self._progress = 0.0

    def set_progress(self, value: float):
        self._progress = value
        self.update()

    def paintEvent(self, event):
        super().paintEvent(event)
        if self._progress > 0:
            painter = QPainter(self)
            painter.fillRect(0, 0, int(self.width() * self._progress), self.height(), QColor(158, 206, 106, 100))


class ImageConvertUI(QFrame):
    open_files_requested = Signal()
    open_dir_requested = Signal()
    save_dir_requested = Signal()
    run_requested = Signal(str)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName('leftPanel')
        self.setFixedWidth(200)
        layout = QVBoxLayout(self)
        layout.setContentsMargins(15, 20, 15, 20)
        layout.setSpacing(10)
        self.btn_open = QPushButton(); self.btn_open.setObjectName('runButton'); self.btn_open.setMinimumHeight(60)
        self.menu_source = QMenu(self)
        self.action_open_file = self.menu_source.addAction('')
        self.action_open_dir = self.menu_source.addAction('')
        self.btn_open.setMenu(self.menu_source)
        self.action_open_file.triggered.connect(self.open_files_requested.emit)
        self.action_open_dir.triggered.connect(self.open_dir_requested.emit)
        self.lbl_status = QLabel(''); self.lbl_status.setWordWrap(True)
        self.btn_save_dir = QPushButton(); self.btn_save_dir.setMinimumHeight(60); self.btn_save_dir.clicked.connect(self.save_dir_requested.emit)
        self.lbl_target_format = QLabel()
        self.format_choice = QComboBox(); self.format_choice.setMinimumHeight(35)
        self.btn_run = ProgressButton(''); self.btn_run.setObjectName('runButton'); self.btn_run.setMinimumHeight(80)
        self.btn_run.clicked.connect(lambda: self.run_requested.emit(self.format_choice.currentText()))
        layout.addWidget(self.btn_open); layout.addWidget(self.lbl_status); layout.addWidget(self.btn_save_dir); layout.addStretch(1)
        layout.addWidget(self.lbl_target_format); layout.addWidget(self.format_choice); layout.addWidget(self.btn_run)
        self._fill_formats(); self.retranslate_ui(); self.set_ready_state(False)

    def _fill_formats(self):
        current = SettingsLogic.get_last_format()
        self.format_choice.clear(); self.format_choice.addItems(SettingsLogic.get_available_target_formats())
        index = self.format_choice.findText(current)
        if index >= 0:
            self.format_choice.setCurrentIndex(index)

    def retranslate_ui(self):
        self.btn_open.setText(SettingsLogic.tr('btn_select_source'))
        self.action_open_file.setText(SettingsLogic.tr('btn_open'))
        self.action_open_dir.setText(SettingsLogic.tr('btn_open_dir'))
        self.btn_save_dir.setText(SettingsLogic.tr('btn_save_dir'))
        self.lbl_target_format.setText(SettingsLogic.tr('lbl_format'))
        self.btn_run.setText(SettingsLogic.tr('btn_run'))

    def set_status_message(self, key_or_text: str):
        self.lbl_status.setText(SettingsLogic.tr(key_or_text) if key_or_text and key_or_text.startswith('lbl_') else key_or_text)

    def set_ready_state(self, enabled: bool):
        self.btn_run.setEnabled(enabled)

    def update_output_dir_tooltip(self, path: str):
        self.btn_save_dir.setToolTip(path)

    def update_format_availability(self, source_ext: str):
        for index in range(self.format_choice.count()):
            item = self.format_choice.model().item(index)
            item.setEnabled(self.format_choice.itemText(index) != source_ext)

    def reset_progress(self):
        self.btn_run.set_progress(0.0)
