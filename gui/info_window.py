from PySide6.QtWidgets import QDialog, QVBoxLayout, QLabel, QPushButton, QWidget
from PySide6.QtGui import QPixmap
from PySide6.QtCore import Qt
from pathlib import Path

class InfoWindow(QDialog):
    def __init__(self, translator, parent=None):
        super().__init__(parent)
        self.tr = translator
        
        # Pobieramy przetłumaczony tytuł zamiast technicznego klucza
        self.setWindowTitle(self.tr.get("info_title"))
        self.setFixedSize(450, 680)
        
        # Twoja złota stylistyka Ayo
        self.setStyleSheet("""
            QDialog { background-color: #1a1b26; }
            QLabel { color: #e0af68; font-family: 'Segoe UI'; }
            QLabel#Section { font-size: 15px; font-weight: bold; margin-top: 15px; }
            QLabel#Text { font-size: 12px; }
            QPushButton { 
                background-color: #24283b; color: #e0af68; 
                border: 1px solid #e0af68; padding: 10px; border-radius: 4px;
                font-weight: bold;
            }
        """)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 20)

        # Baner z Twoimi kartami
        self.banner = QLabel()
        self.load_banner()
        layout.addWidget(self.banner)

        content = QWidget()
        c_layout = QVBoxLayout(content)
        c_layout.setContentsMargins(25, 10, 25, 10)

        # Funkcja pomocnicza zamieniająca klucze na tekst
        def add_info(title_text, desc_key, is_sub=False):
            if is_sub:
                sub = QLabel(self.tr.get("info_also_available"))
                sub.setStyleSheet("color: #bb9af7; font-size: 11px; margin-top: 10px;")
                c_layout.addWidget(sub)
            
            t_lbl = QLabel(title_text)
            t_lbl.setObjectName("Section")
            c_layout.addWidget(t_lbl)
            
            d_lbl = QLabel(self.tr.get(desc_key))
            d_lbl.setObjectName("Text")
            d_lbl.setWordWrap(True)
            c_layout.addWidget(d_lbl)

        add_info("Ayo CONVERT v 1.0", "info_desc_conv")
        add_info("Ayo Up v 1.0", "info_desc_up", is_sub=True)

        layout.addWidget(content)
        layout.addStretch()

        # Przycisk zamknięcia z tłumaczeniem
        self.btn_close = QPushButton(self.tr.get("info_btn_close"))
        self.btn_close.clicked.connect(self.accept)
        
        btn_container = QVBoxLayout()
        btn_container.setContentsMargins(25, 0, 25, 0)
        btn_container.addWidget(self.btn_close)
        layout.addLayout(btn_container)

    def load_banner(self):
        path = Path(__file__).resolve().parent.parent / "assets" / "Ayo.png"
        if path.exists():
            pix = QPixmap(str(path))
            self.banner.setPixmap(pix.scaled(450, 250, Qt.KeepAspectRatioByExpanding, Qt.SmoothTransformation))