from pathlib import Path

from .logger import get_logger
from .view_contract import MainViewContract


logger = get_logger(__name__)


class MainController:
    def __init__(self, view: MainViewContract, config, converter):
        self.view = view
        self.config = config
        self.converter = converter
        self.current_files = []

        # Podłączenie callbacków z Widoku do metod Kontrolera
        self.view.bind_on_files_dropped(self.handle_files)
        self.view.bind_on_dir_selected(self.handle_save_dir)
        self.view.bind_on_conversion_requested(self.run_conversion)

        # Inicjalny stan UI
        self.check_readiness()

    def handle_files(self, file_paths):
        """Logika po wybraniu/upuszczeniu plików."""
        if not file_paths:
            return

        self.current_files = file_paths
        
        # 1. Zleć widokowi wyświetlenie podglądu
        self.view.show_preview(file_paths[0])
        self.view.update_fan(file_paths)

        # 2. Logika blokowania formatów (np. nie konwertuj JPG na JPG)
        source_ext = Path(file_paths[0]).suffix[1:].upper()
        if source_ext == "JPEG": source_ext = "JPG"
        self.view.update_format_availability(source_ext)

        # 3. Sprawdź czy można uruchomić
        self.check_readiness()

    def handle_save_dir(self, path):
        """Logika po zmianie katalogu zapisu."""
        self.config.set("last_save_dir", path)
        self.view.update_save_dir_tooltip(path)
        self.check_readiness()

    def check_readiness(self):
        """Decyduje, czy przycisk 'Wykonaj' ma być aktywny."""
        has_files = len(self.current_files) > 0
        save_dir = self.config.get("last_save_dir")
        dir_valid = save_dir and Path(save_dir).exists()

        if not has_files:
            self.view.set_status_message("lbl_status_select_img")
            self.view.set_run_enabled(False)
        elif not dir_valid:
            self.view.set_status_message("lbl_status_select_dir")
            self.view.set_run_enabled(False)
        else:
            self.view.set_status_message("") # Pusto = OK
            self.view.set_run_enabled(True)

    def run_conversion(self, target_format):
        """Uruchamia proces konwersji."""
        if not self.current_files:
            return

        success, _results = self.converter.convert(self.current_files, target_format)

        if success:
            # Reset stanu po sukcesie
            self.current_files = []
            self.view.reset_after_conversion()
            self.view.show_success_message()
            self.check_readiness()
            logger.info(
                "Konwersja zakończona. Pliki w: %s",
                self.config.get("last_save_dir"),
            )
