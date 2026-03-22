from pathlib import Path

from PySide6.QtCore import Qt
from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import QDialog, QLabel, QPushButton, QVBoxLayout, QWidget

from core.convert_settings_logic import SettingsLogic


class SettingsInfoUI(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle(SettingsLogic.tr('info_title'))
        self.setFixedSize(450, 680)
        layout = QVBoxLayout(self); layout.setContentsMargins(0, 0, 0, 20)
        banner = QLabel(); self._load_banner(banner); layout.addWidget(banner)
        content = QWidget(); content_layout = QVBoxLayout(content); content_layout.setContentsMargins(25, 10, 25, 10)
        for title_key, desc_key, secondary in [('info_name_conv', 'info_desc_conv', False), ('info_name_up', 'info_desc_up', True)]:
            if secondary:
                note = QLabel(SettingsLogic.tr('info_also_available')); note.setStyleSheet('color: #bb9af7; font-size: 11px; margin-top: 10px;'); content_layout.addWidget(note)
            title = QLabel(SettingsLogic.tr(title_key)); title.setObjectName('Section'); content_layout.addWidget(title)
            desc = QLabel(SettingsLogic.tr(desc_key)); desc.setObjectName('Text'); desc.setWordWrap(True); content_layout.addWidget(desc)
        layout.addWidget(content); layout.addStretch()
        button = QPushButton(SettingsLogic.tr('info_btn_close')); button.clicked.connect(self.accept)
        button_layout = QVBoxLayout(); button_layout.setContentsMargins(25, 0, 25, 0); button_layout.addWidget(button)
        layout.addLayout(button_layout)
        self.setStyleSheet("QLabel#Section { font-size: 15px; font-weight: bold; margin-top: 15px; } QLabel#Text { font-size: 12px; } QPushButton { padding: 10px; font-weight: bold; }")

    def _load_banner(self, label: QLabel):
        path = Path(__file__).resolve().parent.parent / 'assets' / 'Ayo.png'
        if path.exists():
            pixmap = QPixmap(str(path))
            label.setPixmap(pixmap.scaled(450, 250, Qt.AspectRatioMode.KeepAspectRatioByExpanding, Qt.TransformationMode.SmoothTransformation))
