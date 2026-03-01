from PySide6.QtWidgets import (
    QComboBox,
    QDialog,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QVBoxLayout,
)

from core.app_config import (
    DEFAULT_LANGUAGE,
    DEFAULT_THEME,
    LANGUAGES_DATA,
    LEGACY_THEME_MAP,
    THEME_OPTIONS,
)
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
        
        current_lang = self.config.get("language", DEFAULT_LANGUAGE)
        # Generowanie listy dynamicznie z jednego źródła prawdy
        for lang_name, _code, flag in LANGUAGES_DATA:
            # Wyświetlamy flagę i nazwę, ale w 'userData' trzymamy czystą nazwę dla configu
            self.lang_combo.addItem(f"{flag}  {lang_name}", userData=lang_name)
            
        index = self.lang_combo.findData(current_lang)
        if index >= 0:
            self.lang_combo.setCurrentIndex(index)
            
        layout.addWidget(self.lang_combo)

        # Motyw
        layout.addWidget(QLabel(self.tr.get("lbl_theme")))
        self.theme_combo = QComboBox()
        
        for theme_code, theme_key in THEME_OPTIONS:
            self.theme_combo.addItem(self.tr.get(theme_key), userData=theme_code)

        # Pobieramy obecny motyw i mapujemy stare nazwy na nowe kody (kompatybilność)
        current_theme = self.config.get("theme", DEFAULT_THEME)
        current_theme = LEGACY_THEME_MAP.get(current_theme, current_theme)

        index = self.theme_combo.findData(current_theme)
        if index >= 0:
            self.theme_combo.setCurrentIndex(index)
            
        layout.addWidget(self.theme_combo)

        # Przycisk Info
        layout.addSpacing(5)
        self.btn_info = QPushButton(self.tr.get("btn_info"))
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
        self.config.set("language", self.lang_combo.currentData())
        if self.parent() and hasattr(self.parent(), "apply_theme"):
            self.parent().apply_theme(self.theme_combo.currentData())
        self.accept()

    def show_info(self):
        # PRZEKAZUJEMY TŁUMACZA DO OKNA INFO
        info = InfoWindow(self.tr, self)
        info.exec()
