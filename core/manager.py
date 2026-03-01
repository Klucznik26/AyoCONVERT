import json
from typing import Any, Dict, Optional

from .app_config import CONFIG_DIR, CONFIG_PATH, DEFAULT_SETTINGS
from .logger import get_logger


logger = get_logger(__name__)


class ConfigManager:
    def __init__(self):
        self.config_dir = CONFIG_DIR
        self.config_path = CONFIG_PATH
        
        # Upewnij się, że katalog 'config' istnieje
        if not self.config_dir.exists():
            self.config_dir.mkdir(parents=True, exist_ok=True)
        
        # Domyślne ustawienia (zgodnie z Ayo-UP)
        self.defaults = DEFAULT_SETTINGS.copy()
        self.settings = self.load_config()

    def load_config(self) -> Dict[str, Any]:
        """Wczytuje ustawienia z pliku JSON."""
        if self.config_path.exists():
            try:
                with open(self.config_path, 'r', encoding='utf-8') as f:
                    return {**self.defaults, **json.load(f)}
            except (json.JSONDecodeError, OSError) as e:
                logger.error("[config] Błąd ładowania pliku konfiguracyjnego: %s", e)
                return self.defaults
        return self.defaults

    def save_config(self):
        """Zapisuje aktualne ustawienia."""
        with open(self.config_path, 'w', encoding='utf-8') as f:
            json.dump(self.settings, f, indent=4, ensure_ascii=False)

    def get(self, key: str, default: Optional[Any] = None) -> Any:
        """
        Naprawiony getter - teraz przyjmuje argument 'default', 
        co rozwiązuje problem TypeError w MainWindow.
        """
        # Jeśli klucz jest w aktualnych ustawieniach, zwróć go
        if key in self.settings:
            return self.settings[key]
        # Jeśli nie, zwróć przekazany 'default' lub wartość z domyślnych
        return default if default is not None else self.defaults.get(key)

    def set(self, key: str, value: Any):
        self.settings[key] = value
        self.save_config()
