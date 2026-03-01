from PySide6.QtWidgets import (QMainWindow, QWidget, QHBoxLayout, QVBoxLayout, 
                             QLabel, QApplication)
from PySide6.QtGui import QPixmap
from PySide6.QtCore import Qt, Signal
from pathlib import Path

# Importy komponentów AyoCONVERT
from .sidebar import Sidebar
from .drop_area import DropArea
from .image_fan import ImageFan
from .styles import get_style
from .settings_window import SettingsWindow
from core.translator import Translator
from .qt_i18n import AyoQtTranslator
from . import dialogs

class MainWindow(QMainWindow):
    # Sygnały do komunikacji z Kontrolerem
    files_dropped_signal = Signal(list)
    dir_selected_signal = Signal(str)
    conversion_requested_signal = Signal(str)

    def __init__(self, config, qt_translator):
        super().__init__()
        self.config = config
        self.qt_translator = qt_translator
        self.translator = Translator(self.config)
        self._status_message_key = ""
        
        # Instalacja naszego tłumacza dla kolumn tabel Qt
        self.custom_qt_translator = AyoQtTranslator(self.translator.translations)
        QApplication.instance().installTranslator(self.custom_qt_translator)
        
        self.setWindowTitle("AyoConvert v 1.3.0")
        self.setMinimumSize(1000, 520)
        self.resize(1000, 520)
        self.apply_theme(self.config.get("theme", "system"))

        self._init_ui()
        
        # Jeśli mamy zapamiętany katalog, ustawiamy tooltip od razu
        last_dir = self.config.get("last_save_dir")
        if last_dir:
            self.sidebar.btn_save_dir.setToolTip(last_dir)
        
    def _init_ui(self):
        """Buduje interfejs i ustawia rygorystyczną sekwencję blokad."""
        if self.centralWidget():
            self.centralWidget().setParent(None)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QHBoxLayout(central_widget)
        main_layout.setContentsMargins(30, 30, 30, 30)
        main_layout.setSpacing(30)

        # Sidebar - lewy panel sterowania
        self.sidebar = Sidebar(self.translator)
        self.sidebar.lbl_status.setObjectName("statusLabel")
        self.sidebar.action_open_file.triggered.connect(self.open_file_dialog)
        self.sidebar.action_open_dir.triggered.connect(self.open_source_directory)
        self.sidebar.btn_save_dir.clicked.connect(self.select_save_directory)
        self.sidebar.btn_run.clicked.connect(self.start_conversion)
        self.sidebar.btn_settings.clicked.connect(self.show_settings)
        self.sidebar.btn_close.clicked.connect(self.close)
        
        # Panel prawy
        right_panel = QVBoxLayout()
        right_panel.setContentsMargins(0, 0, 0, 0)
        right_panel.setSpacing(15) # Zgodność z odstępami w Sidebarze (15px)
        
        # Górny pasek: Tytuł + Wachlarz (Top Right)
        top_bar = QHBoxLayout()
        top_bar.setContentsMargins(0, 0, 0, 0)
        
        title = QLabel(self.translator.get("lbl_title"))
        title.setStyleSheet("font-size: 18px; font-weight: bold;")
        title.setAlignment(Qt.AlignCenter)
        title.setFixedHeight(40) # Wysokość zgodna z przyciskiem w Sidebarze
        
        self.image_fan = ImageFan(self.translator)
        
        # Układ: Stretch | Tytuł | Stretch | Wachlarz
        # Dzięki temu tytuł jest na środku, a wachlarz po prawej, nie spychając tytułu
        top_bar.addStretch(1)
        top_bar.addWidget(title)
        top_bar.addSpacing(240) # Przesunięcie tytułu o 120px w lewo (balansując środek)
        top_bar.addStretch(1)

        content_h = QHBoxLayout()
        content_h.setContentsMargins(0, 0, 0, 0)
        self.drop_area = DropArea()
        self.drop_area.setObjectName("dropArea") # ID dla stylów CSS
        self.drop_area.setText(self.translator.get("lbl_drop"))
        self.drop_area.files_dropped.connect(self.handle_files)
        
        logo_v = QVBoxLayout()
        self.logo_v_layout = logo_v # Zapisujemy referencję do layoutu
        
        # Wachlarz przeniesiony tutaj, aby nie spychał DropArea w dół
        logo_v.addWidget(self.image_fan, 0, Qt.AlignRight | Qt.AlignTop)
        
        logo_v.addStretch(1)
        self.mini_logo = QLabel()
        self.load_logo()
        # Wymuszenie pozycji w prawym dolnym rogu kontenera
        logo_v.addWidget(self.mini_logo, 0, Qt.AlignRight | Qt.AlignBottom)

        content_h.addWidget(self.drop_area, 1, Qt.AlignTop)
        content_h.addLayout(logo_v)

        right_panel.addLayout(top_bar)
        right_panel.addLayout(content_h)

        main_layout.addWidget(self.sidebar, 1)
        main_layout.addLayout(right_panel, 4)

        # Po przebudowie UI (np. po zmianie języka) odtwarzamy aktualny status.
        if self._status_message_key:
            self.sidebar.lbl_status.setText(self.translator.get(self._status_message_key))
        else:
            self.sidebar.lbl_status.setText("")

    # --- Rejestracja callbacków dla warstwy logiki (bez zależności od Qt) ---

    def bind_on_files_dropped(self, handler):
        self.files_dropped_signal.connect(handler)

    def bind_on_dir_selected(self, handler):
        self.dir_selected_signal.connect(handler)

    def bind_on_conversion_requested(self, handler):
        self.conversion_requested_signal.connect(handler)

    # --- Metody wywoływane przez Kontroler (API Widoku) ---

    def show_preview(self, file_path):
        self.drop_area.set_preview(file_path)

    def update_fan(self, file_paths):
        self.image_fan.set_images(file_paths)
        self.logo_v_layout.activate()

    def update_save_dir_tooltip(self, path):
        self.sidebar.btn_save_dir.setToolTip(path)

    def set_status_message(self, key_msg):
        """Ustawia tekst statusu na podstawie klucza tłumaczenia lub czyści."""
        self._status_message_key = key_msg or ""
        if not key_msg:
            self.sidebar.lbl_status.setText("")
        else:
            self.sidebar.lbl_status.setText(self.translator.get(key_msg))

    def set_run_enabled(self, enabled):
        self.sidebar.btn_run.setEnabled(enabled)

    def show_success_message(self):
        self.drop_area.show_success(self.translator.get("lbl_done", "WYKONANO"))

    def reset_after_conversion(self):
        self.image_fan.set_images([])

    def update_format_availability(self, source_ext):
        """Blokuje format źródłowy na liście wyboru."""
        for i in range(self.sidebar.format_choice.count()):
            format_item = self.sidebar.format_choice.itemText(i)
            if format_item == source_ext:
                self.sidebar.format_choice.model().item(i).setEnabled(False)
                if self.sidebar.format_choice.currentIndex() == i:
                    next_idx = (i + 1) % self.sidebar.format_choice.count()
                    self.sidebar.format_choice.setCurrentIndex(next_idx)
            else:
                self.sidebar.format_choice.model().item(i).setEnabled(True)

    # --- Obsługa zdarzeń UI (Emitowanie sygnałów) ---

    def handle_files(self, file_paths):
        """Przekazuje pliki do kontrolera."""
        if file_paths:
            self.files_dropped_signal.emit(file_paths)

    def select_save_directory(self):
        """Używa helpera dialogs do wyboru katalogu."""
        last_dir = self.config.get("last_save_dir", str(Path.home()))
        save_path = dialogs.select_save_directory(self, self.translator, last_dir)
        if save_path:
            self.dir_selected_signal.emit(save_path)

    def open_file_dialog(self):
        """Używa helpera dialogs do wyboru plików."""
        files = dialogs.open_files_dialog(self, self.translator, str(Path.home()))
        if files:
            self.handle_files(files)

    def open_source_directory(self):
        """Używa helpera dialogs do skanowania folderu."""
        files = dialogs.open_directory_scan(self, self.translator, str(Path.home()))
        if files:
            self.handle_files(files)

    def start_conversion(self):
        """Zgłasza chęć konwersji."""
        target_format = self.sidebar.format_choice.currentText()
        self.conversion_requested_signal.emit(target_format)

    def show_settings(self):
        dialog = SettingsWindow(self.config, self.translator, self)
        if dialog.exec():
            self.translator.load_translations()
            # Aktualizacja tłumaczeń kolumn Qt
            self.custom_qt_translator.update_translations(self.translator.translations)
            self._init_ui()

    def apply_theme(self, theme_name):
        style = get_style(theme_name)
        QApplication.instance().setStyleSheet(style)
        self.config.set("theme", theme_name)

    def load_logo(self):
        root_path = Path(__file__).resolve().parent.parent
        path = root_path / "assets" / "AyoCONVERT.png"
        if path.exists():
            pix = QPixmap(str(path))
            self.mini_logo.setPixmap(pix.scaled(180, 180, Qt.KeepAspectRatio, Qt.SmoothTransformation))
