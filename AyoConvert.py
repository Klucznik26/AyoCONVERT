import sys
from PySide6.QtWidgets import QApplication
from PySide6.QtCore import QTranslator, QLibraryInfo
from pathlib import Path

from core.manager import ConfigManager
from gui.main_window import MainWindow

def update_qt_translator(app, translator, lang_code):
    """Oficjalny i dynamiczny sposób ładowania tłumaczeń systemowych Qt."""
    # Najpierw usuwamy stary translator, jeśli istnieje
    app.removeTranslator(translator)
    
    # Znajdujemy ścieżkę do plików .qm w Twoim venv
    qt_translations_path = QLibraryInfo.path(QLibraryInfo.TranslationsPath)
    
    # Próbujemy załadować odpowiedni plik (np. qtbase_lt.qm)
    if translator.load(f"qtbase_{lang_code}.qm", qt_translations_path):
        app.installTranslator(translator)
        print(f"[Qt] Załadowano tłumaczenie systemowe dla: {lang_code}")
    else:
        # Fallback na ogólny plik qt_*.qm
        if translator.load(f"qt_{lang_code}.qm", qt_translations_path):
            app.installTranslator(translator)
            print(f"[Qt] Załadowano zbiorcze tłumaczenie: {lang_code}")
        else:
            print(f"[Qt] Brak systemowego pliku .qm dla: {lang_code}")

def main():
    app = QApplication(sys.argv)
    config = ConfigManager()

    # Twoja mapa języków
    lang_map = {
        "Polski": "pl",
        "English": "en",
        "Українська": "uk",
        "Latviešu": "lv",
        "Lietuvių": "lt",
        "Eesti": "et"
    }

    # Tworzymy jeden globalny obiekt translatora dla Qt
    qt_translator = QTranslator(app)
    
    # Pobieramy obecny język z config.json
    lang_name = config.get("language", "Polski")
    lang_code = lang_map.get(lang_name, "pl")

    # Pierwsze ładowanie przy starcie
    update_qt_translator(app, qt_translator, lang_code)

    # Uruchamiamy MainWindow i przekazujemy mu dostęp do aplikacji i translatora
    window = MainWindow(config, qt_translator, lang_map)
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()