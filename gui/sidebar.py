from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QPushButton, 
                             QComboBox, QLabel, QMenu)
from PySide6.QtCore import Qt

class Sidebar(QWidget):
    def __init__(self, translator):
        super().__init__()
        self.translator = translator
        self.setFixedWidth(250) # Stała szerokość panelu niezależnie od języka
        self._init_ui()

    def _init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(10, 0, 10, 0)
        layout.setSpacing(15)

        # 1. Przycisk wyboru źródła (Menu rozwijane)
        self.btn_source = QPushButton(self.translator.get("btn_select_source"))
        self.btn_source.setMinimumHeight(40)
        
        self.menu_source = QMenu(self)
        self.action_open_file = self.menu_source.addAction(self.translator.get("btn_open"))
        self.action_open_dir = self.menu_source.addAction(self.translator.get("btn_open_dir"))
        self.btn_source.setMenu(self.menu_source)

        # 2. Przycisk Katalog zapisu
        self.btn_save_dir = QPushButton(self.translator.get("btn_save_dir"))
        self.btn_save_dir.setMinimumHeight(40)

        # 3. Etykieta statusu (dynamiczne podpowiedzi)
        self.lbl_status = QLabel("")
        self.lbl_status.setAlignment(Qt.AlignCenter)
        self.lbl_status.setWordWrap(True)
        # Złoty kolor Ayo dla lepszej widoczności statusu
        self.lbl_status.setStyleSheet("font-size: 11px; color: #d4a373; font-weight: bold;")

        layout.addWidget(self.btn_source)
        layout.addWidget(self.btn_save_dir)
        layout.addWidget(self.lbl_status)

        layout.addStretch(1)

        # 4. Wybór formatu
        lbl_format = QLabel(self.translator.get("lbl_format"))
        self.format_choice = QComboBox()
        self.format_choice.addItems(["PNG", "JPG", "WEBP", "BMP", "TIFF"])
        self.format_choice.setMinimumHeight(35)

        layout.addWidget(lbl_format)
        layout.addWidget(self.format_choice)

        # 5. Przycisk Wykonaj (Główna akcja)
        self.btn_run = QPushButton(self.translator.get("btn_run"))
        self.btn_run.setMinimumHeight(50)
        self.btn_run.setEnabled(False) # Blokada sesyjna
        self.btn_run.setStyleSheet("font-weight: bold; font-size: 14px;")

        layout.addWidget(self.btn_run)
        
        # 6. Przyciski dolne w układzie POZIOMYM
        # Tworzymy QHBoxLayout, aby przyciski były obok siebie
        bottom_buttons_layout = QHBoxLayout()
        bottom_buttons_layout.setSpacing(10) # Odstęp między przyciskami

        self.btn_settings = QPushButton(self.translator.get("btn_settings"))
        self.btn_settings.setMinimumHeight(35)
        
        self.btn_close = QPushButton(self.translator.get("btn_close"))
        self.btn_close.setMinimumHeight(35)
        
        # Dodajemy do układu poziomego: Ustawienia po lewej, Zamknij po prawej
        bottom_buttons_layout.addWidget(self.btn_settings)
        bottom_buttons_layout.addWidget(self.btn_close)
        
        # Dodajemy cały poziomy rząd do głównego pionowego układu Sidebaru
        layout.addLayout(bottom_buttons_layout)

        # Podniesienie dolnej sekcji o 5px od dolnej krawędzi
        layout.addSpacing(5)