from pathlib import Path

from PySide6.QtCore import Qt
from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import QFrame, QLabel, QListWidget, QSizePolicy, QVBoxLayout

from core.convert_settings_logic import SettingsLogic
from gui.convert_preview_widgets import PreviewFanWidget


class PreviewUI(QFrame):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName('rightPanel')
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.setMinimumWidth(260)
        layout = QVBoxLayout(self)
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(10)
        self.top_glass = self._create_glass(layout, 1)
        self.mid_glass = self._create_glass(layout, 2)
        self.bottom_glass = self._create_glass(layout, 1)
        self.fan_ui = PreviewFanWidget(); self.fan_ui.hide()
        fan_policy = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Expanding); fan_policy.setRetainSizeWhenHidden(True); self.fan_ui.setSizePolicy(fan_policy)
        self.out_name = QLabel(); self.out_name.setProperty('secondary', True); self.out_name.hide()
        self.file_list = QListWidget(); self.file_list.setObjectName('fileList')
        self.file_list.setStyleSheet('QListWidget { background: transparent; border: none; outline: none; } QListWidget::item { padding: 4px 8px; border-radius: 6px; }')
        self.logo_label = QLabel(); self.logo_label.setAlignment(Qt.AlignmentFlag.AlignCenter); self._load_logo()
        self.top_glass.layout().addWidget(self.fan_ui); self.top_glass.layout().addWidget(self.out_name, 0, Qt.AlignmentFlag.AlignCenter)
        self.mid_glass.layout().addWidget(self.file_list)
        self.bottom_glass.layout().addWidget(self.logo_label, 0, Qt.AlignmentFlag.AlignCenter)

    def _create_glass(self, parent_layout, stretch):
        frame = QFrame(); frame.setStyleSheet('QFrame { background-color: rgba(150,150,150,0.1); border-radius: 12px; border: 1px solid rgba(150,150,150,0.15); }')
        frame.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        layout = QVBoxLayout(frame); layout.setContentsMargins(10, 10, 10, 10)
        parent_layout.addWidget(frame, stretch)
        return frame

    def _load_logo(self):
        path = Path(__file__).resolve().parent.parent / 'assets' / 'AyoCONVERT.png'
        if path.exists():
            pixmap = QPixmap(str(path))
            if not pixmap.isNull():
                self.logo_label.setPixmap(pixmap.scaled(180, 180, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation))

    def update_files(self, paths: list[str]):
        self.file_list.clear(); self.file_list.addItems([Path(path).name for path in paths])
        self.fan_ui.set_images(paths)
        if len(paths) > 1:
            self.out_name.setText(f"{SettingsLogic.tr('lbl_queue_count')} {len(paths)}")
            self.out_name.show()
        else:
            self.out_name.hide()

    def clear_files(self, completed: bool = False):
        self.file_list.clear(); self.fan_ui.set_images([])
        if completed:
            self.out_name.setText(SettingsLogic.tr('lbl_done')); self.out_name.show()
        else:
            self.out_name.clear(); self.out_name.hide()

    def retranslate_ui(self):
        if self.out_name.isVisible() and self.file_list.count() > 1:
            self.out_name.setText(f"{SettingsLogic.tr('lbl_queue_count')} {self.file_list.count()}")
