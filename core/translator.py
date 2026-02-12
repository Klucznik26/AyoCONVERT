import json
import os
from pathlib import Path
from PySide6.QtCore import QTranslator

class Translator:
    def __init__(self, config):
        self.config = config
        self.translations = {}
        # Mapowanie nazw z UI na Twoje nazwy plików (ee i ua)
        self.lang_map = {
            "Polski": "pl",
            "English": "en",
            "Українська": "ua",
            "Latviešu": "lv",
            "Lietuvių": "lt",
            "Eesti": "ee",
            "Português": "pt",
            "Čeština": "cz",
            "Slovenščina": "si",
            "ქართული": "ge"
        }
        self.load_translations()

    def load_translations(self):
        """Ładuje plik JSON odpowiadający wybranemu językowi."""
        lang_name = self.config.get("language", "Polski")
        lang_code = self.lang_map.get(lang_name, "pl")
        
        # Ścieżka do folderu i18n względem głównego folderu projektu
        base_path = Path(__file__).resolve().parent.parent
        file_path = base_path / "i18n" / f"{lang_code}.json"

        print(f"[AyoTranslator] Szukam pliku: {file_path}")

        try:
            if file_path.exists():
                with open(file_path, "r", encoding="utf-8") as f:
                    self.translations = json.load(f)
                print(f"[AyoTranslator] Sukces! Załadowano {len(self.translations)} kluczy.")
            else:
                print(f"[AyoTranslator] Błąd: Nie znaleziono pliku {file_path}. Ładuję domyślny plik pl.json.")
                # Fallback do polskiego, jeśli plik nie istnieje
                fallback_path = base_path / "i18n" / "pl.json"
                if fallback_path.exists():
                    with open(fallback_path, "r", encoding="utf-8") as f:
                        self.translations = json.load(f)
        except Exception as e:
            print(f"[AyoTranslator] Krytyczny błąd ładowania: {e}")
            self.translations = {}

    def get(self, key, default=None):
        """Pobiera przetłumaczony tekst dla danego klucza."""
        # Jeśli klucz nie istnieje, zwraca sam klucz (ułatwia szukanie braków w JSON)
        return self.translations.get(key, default if default else key)

class AyoQtTranslator(QTranslator):
    """
    Niestandardowy tłumacz Qt, który przechwytuje systemowe frazy (np. nagłówki kolumn)
    i tłumaczy je używając naszych plików JSON.
    """
    def __init__(self, translations_dict):
        super().__init__()
        self.translations = translations_dict

    def update_translations(self, translations_dict):
        self.translations = translations_dict

    def translate(self, context, source_text, disambiguation=None, n=-1):
        # Mapowanie standardowych tekstów Qt na nasze klucze JSON
        qt_map = {
            "Name": "qt_col_name",
            "Size": "qt_col_size",
            "Type": "qt_col_type",
            "Date Modified": "qt_col_date",
            "Date": "qt_col_date"
        }
        
        if source_text in qt_map:
            key = qt_map[source_text]
            if key in self.translations:
                return self.translations[key]
        
        return super().translate(context, source_text, disambiguation, n)