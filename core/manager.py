import json
import os
from pathlib import Path

class ConfigManager:
    def __init__(self):
        # Ścieżka do pliku ustawień (cross-platform)
        self.config_dir = Path(__file__).resolve().parent.parent / "config"
        self.config_path = self.config_dir / "config.json"
        
        # Upewnij się, że katalog 'config' istnieje
        if not self.config_dir.exists():
            self.config_dir.mkdir(parents=True, exist_ok=True)
        
        # Domyślne ustawienia (zgodnie z Ayo-UP)
        self.defaults = {
            "language": "Polski",
            "theme": "Systemowy",
            "last_format": "png",
            "output_suffix": "_AOC" # Ayo Convert
        }
        self.settings = self.load_config()

    def load_config(self):
        """Wczytuje ustawienia z pliku JSON."""
        if self.config_path.exists():
            try:
                with open(self.config_path, 'r', encoding='utf-8') as f:
                    return {**self.defaults, **json.load(f)}
            except Exception:
                return self.defaults
        return self.defaults

    def save_config(self):
        """Zapisuje aktualne ustawienia."""
        with open(self.config_path, 'w', encoding='utf-8') as f:
            json.dump(self.settings, f, indent=4, ensure_ascii=False)

    def get(self, key, default=None):
        """
        Naprawiony getter - teraz przyjmuje argument 'default', 
        co rozwiązuje problem TypeError w MainWindow.
        """
        # Jeśli klucz jest w aktualnych ustawieniach, zwróć go
        if key in self.settings:
            return self.settings[key]
        # Jeśli nie, zwróć przekazany 'default' lub wartość z domyślnych
        return default if default is not None else self.defaults.get(key)

    def set(self, key, value):
        self.settings[key] = value
        self.save_config()