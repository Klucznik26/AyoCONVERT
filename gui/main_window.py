import os
from PySide6.QtWidgets import (QMainWindow, QWidget, QHBoxLayout, QVBoxLayout, 
                             QLabel, QFileDialog, QApplication)
from PySide6.QtGui import QPixmap
from PySide6.QtCore import Qt
from pathlib import Path

# Importy komponentów AyoCONVERT
from .sidebar import Sidebar
from .drop_area import DropArea
from .styles import get_style
from .settings_window import SettingsWindow
from core.translator import Translator
from core.converter import ImageConverter

class MainWindow(QMainWindow):
    def __init__(self, config, qt_translator, lang_map):
        super().__init__()
        self.config = config
        self.qt_translator = qt_translator
        self.lang_map = lang_map
        self.translator = Translator(self.config)
        
        self.converter = ImageConverter(self.config)
        self.current_files = [] 
        
        # Flaga sesyjna: czy użytkownik potwierdził katalog w tym uruchomieniu?
        self.dir_selected_session = False 
        
        self.setWindowTitle("AyoCONVERT")
        self.setMinimumSize(1000, 700)
        self.apply_theme(self.config.get("theme", "Systemowy"))

        self._init_ui()
        
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
        self.sidebar.btn_open.clicked.connect(self.open_file_dialog)
        self.sidebar.btn_save_dir.clicked.connect(self.select_save_directory)
        self.sidebar.btn_run.clicked.connect(self.start_conversion)
        self.sidebar.btn_settings.clicked.connect(self.show_settings)
        self.sidebar.btn_close.clicked.connect(self.close)
        
        # Panel prawy
        right_panel = QVBoxLayout()
        title = QLabel(self.translator.get("lbl_title"))
        title.setStyleSheet("font-size: 18px; font-weight: bold;")
        title.setAlignment(Qt.AlignCenter)

        content_h = QHBoxLayout()
        self.drop_area = DropArea()
        self.drop_area.setText(self.translator.get("lbl_drop"))
        self.drop_area.files_dropped.connect(self.handle_files)
        
        logo_v = QVBoxLayout()
        logo_v.addStretch(1)
        self.mini_logo = QLabel()
        self.load_logo()
        logo_v.addWidget(self.mini_logo)

        content_h.addWidget(self.drop_area, 1)
        content_h.addLayout(logo_v)

        right_panel.addWidget(title)
        right_panel.addLayout(content_h)

        main_layout.addWidget(self.sidebar, 1)
        main_layout.addLayout(right_panel, 4)

        # Wymuszenie stanu początkowego przy starcie
        self.update_ui_state()

    def update_ui_state(self):
        """
        Gwarantuje sekwencję:
        1. Brak obrazu -> Napis 'Wybierz obraz', Przycisk zablokowany.
        2. Obraz wrzucony, brak katalogu w sesji -> Napis 'Wybierz katalog', Przycisk zablokowany.
        3. Jest obraz i katalog potwierdzony -> Napis znika, Przycisk odblokowany.
        """
        has_files = len(self.current_files) > 0
        
        if not has_files:
            # Stan po starcie lub po udanej konwersji
            self.sidebar.lbl_status.setText(self.translator.get("lbl_status_select_img"))
            self.sidebar.btn_run.setEnabled(False)
        elif not self.dir_selected_session:
            # Plik jest, ale trzeba kliknąć katalog (wymóg sesji)
            self.sidebar.lbl_status.setText(self.translator.get("lbl_status_select_dir"))
            self.sidebar.btn_run.setEnabled(False)
        else:
            # Wszystko gotowe - napisy znikają
            self.sidebar.lbl_status.setText("")
            self.sidebar.btn_run.setEnabled(True)

    def handle_files(self, file_paths):
        """Obsługuje nowe pliki i inteligentnie blokuje format źródłowy."""
        if file_paths:
            self.current_files = file_paths
            self.drop_area.set_preview(file_paths[0])
            
            # Wygaszanie formatu źródłowego
            source_ext = Path(file_paths[0]).suffix[1:].upper()
            if source_ext == "JPEG": source_ext = "JPG"
            
            for i in range(self.sidebar.format_choice.count()):
                format_item = self.sidebar.format_choice.itemText(i)
                if format_item == source_ext:
                    self.sidebar.format_choice.model().item(i).setEnabled(False)
                    if self.sidebar.format_choice.currentIndex() == i:
                        next_idx = (i + 1) % self.sidebar.format_choice.count()
                        self.sidebar.format_choice.setCurrentIndex(next_idx)
                else:
                    self.sidebar.format_choice.model().item(i).setEnabled(True)
            
            self.update_ui_state()

    def select_save_directory(self):
        """Otwiera okno wyboru folderu i odblokowuje flagę sesyjną."""
        title = self.translator.get("btn_save_dir")
        last_dir = self.config.get("last_save_dir", str(Path.home()))
        
        dialog = self._prepare_custom_dialog(title, last_dir)
        dialog.setFileMode(QFileDialog.FileMode.Directory)
        dialog.setOption(QFileDialog.Option.ShowDirsOnly, True)
        dialog.setLabelText(QFileDialog.Accept, self.translator.get("btn_save"))
        
        if dialog.exec():
            selected = dialog.selectedFiles()
            if selected:
                save_path = selected[0]
                self.config.set("last_save_dir", save_path)
                self.sidebar.btn_save_dir.setToolTip(save_path)
                
                # Katalog został potwierdzony w tej sesji
                self.dir_selected_session = True
                self.update_ui_state()

    def _prepare_custom_dialog(self, title, directory, file_filter=None):
        dialog = QFileDialog(self, title, directory)
        dialog.setOption(QFileDialog.Option.DontUseNativeDialog, True)
        if file_filter:
            dialog.setNameFilter(file_filter)
        dialog.setLabelText(QFileDialog.Accept, self.translator.get("btn_open") if file_filter else self.translator.get("btn_save"))
        dialog.setLabelText(QFileDialog.Reject, self.translator.get("btn_cancel"))
        dialog.setLabelText(QFileDialog.FileName, self.translator.get("lbl_file_name"))
        dialog.setLabelText(QFileDialog.FileType, self.translator.get("lbl_file_type"))
        dialog.setLabelText(QFileDialog.LookIn, self.translator.get("lbl_look_in"))
        return dialog

    def open_file_dialog(self):
        title = self.translator.get("btn_open")
        img_label = self.translator.get("dlg_filter_images")
        all_label = self.translator.get("dlg_filter_all")
        file_filter = f"{img_label} (*.png *.jpg *.jpeg *.bmp *.webp *.tiff);;{all_label} (*.*)"
        
        dialog = self._prepare_custom_dialog(title, str(Path.home()), file_filter)
        if dialog.exec():
            files = dialog.selectedFiles()
            if files:
                self.handle_files(files)

    def start_conversion(self):
        """Uruchamia konwersję i czyści interfejs, zachowując pamięć o katalogu."""
        if not self.current_files:
            return
            
        target_format = self.sidebar.format_choice.currentText()
        success, results = self.converter.convert(self.current_files, target_format)
        
        if success:
            # RESET INTERFEJSU PO KONWERSJI
            self.current_files = [] # Obraz znika z pamięci
            self.drop_area.setText(self.translator.get("lbl_drop")) # Reset napisu w polu drop
            
            # Aktualizacja UI - wróci do statusu 'Wybierz obraz', ale flaga sesji zostaje True
            self.update_ui_state()
            print(f"Konwersja zakończona. Pliki w: {self.config.get('last_save_dir')}")

    def show_settings(self):
        dialog = SettingsWindow(self.config, self.translator, self)
        if dialog.exec():
            self.translator.load_translations()
            self._init_ui()

    def apply_theme(self, theme_name):
        style = get_style(theme_name)
        QApplication.instance().setStyleSheet(style)
        self.config.set("theme", theme_name)

    def load_logo(self):
        path = Path(__file__).resolve().parent.parent / "assets" / "AyoCONVERT.png"
        if path.exists():
            pix = QPixmap(str(path))
            self.mini_logo.setPixmap(pix.scaled(180, 180, Qt.KeepAspectRatio, Qt.SmoothTransformation))