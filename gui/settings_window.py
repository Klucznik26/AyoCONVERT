from PySide6.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QLabel, 
                             QComboBox, QPushButton)
from PySide6.QtCore import Qt
from .info_window import InfoWindow

class SettingsWindow(QDialog):
    def __init__(self, config, translator, parent=None):
        super().__init__(parent)
        self.config = config
        self.tr = translator # Przechowujemy tłumacza przekazanego z MainWindow
        
        # Tytuł okna z tłumacza
        self.setWindowTitle(self.tr.get("settings_title"))
        self.setFixedSize(350, 320)
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 15, 20, 15)
        layout.setSpacing(8)

        # Język
        layout.addWidget(QLabel(self.tr.get("lbl_lang")))
        self.lang_combo = QComboBox()
        self.lang_combo.addItems(["Polski", "English", "Українська", "Latviešu", "Lietuvių", "Eesti"])
        self.lang_combo.setCurrentText(self.config.get("language", "Polski"))
        layout.addWidget(self.lang_combo)

        # Motyw
        layout.addWidget(QLabel(self.tr.get("lbl_theme")))
        self.theme_combo = QComboBox()
        self.theme_combo.addItems(["Systemowy", "Ciemny", "Jasny"])
        self.theme_combo.setCurrentText(self.config.get("theme", "Systemowy"))
        layout.addWidget(self.theme_combo)

        # Przycisk Info
        layout.addSpacing(5)
        self.btn_info = QPushButton("Info")
        self.btn_info.clicked.connect(self.show_info)
        layout.addWidget(self.btn_info)

        layout.addStretch(1)

        btn_layout = QHBoxLayout()
        self.btn_cancel = QPushButton(self.tr.get("btn_cancel"))
        self.btn_cancel.clicked.connect(self.reject)
        
        self.btn_save = QPushButton(self.tr.get("btn_save"))
        self.btn_save.setObjectName("SaveBtn")
        self.btn_save.clicked.connect(self.save_and_close)
        
        btn_layout.addWidget(self.btn_cancel)
        btn_layout.addWidget(self.btn_save)
        layout.addLayout(btn_layout)

    def save_and_close(self):
        self.config.set("language", self.lang_combo.currentText())
        if self.parent() and hasattr(self.parent(), "apply_theme"):
            self.parent().apply_theme(self.theme_combo.currentText())
        self.accept()

    def show_info(self):
        # PRZEKAZUJEMY TŁUMACZA DO OKNA INFO
        info = InfoWindow(self.tr, self)
        info.exec()