#!/usr/bin/env python3
import logging
import sys

from PySide6.QtCore import QTranslator, qInstallMessageHandler
from PySide6.QtWidgets import QApplication

from core.app_config import DEFAULT_LANGUAGE, LANG_MAP
from core.controller import MainController
from core.converter import ImageConverter
from core.manager import ConfigManager
from core.translator import ensure_translation_files
from ui_main import MainWindow
from gui.qt_i18n import update_qt_translator


def _qt_message_filter(_msg_type, _context, message):
    # Wyciszenie znanego ostrzeżenia Qt, które nie wpływa na działanie aplikacji.
    if "QString::arg: 2 argument(s) missing in" in message:
        return
    print(message)

def main():
    logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
    qInstallMessageHandler(_qt_message_filter)
    
    # Sprawdzenie i ewentualne utworzenie brakujących plików językowych
    ensure_translation_files()
    
    app = QApplication(sys.argv)
    config = ConfigManager()

    # Tworzymy jeden globalny obiekt translatora dla Qt
    qt_translator = QTranslator(app)
    
    # Pobieramy obecny język z config.json
    lang_name = config.get("language", DEFAULT_LANGUAGE)
    lang_code = LANG_MAP.get(lang_name, "pl")

    # Pierwsze ładowanie przy starcie
    update_qt_translator(app, qt_translator, lang_code)

    # Inicjalizacja logiki biznesowej
    converter = ImageConverter(config)

    # Uruchamiamy MainWindow i przekazujemy mu dostęp do aplikacji i translatora
    window = MainWindow(config, qt_translator)
    
    # Spinamy Widok z Logiką za pomocą Kontrolera
    _controller = MainController(window, config, converter)
    
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
