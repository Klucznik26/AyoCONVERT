import json

from .app_config import (
    DEFAULT_LANGUAGE,
    I18N_DIR,
    I18N_FILE_CODE_MAP,
    LANG_MAP,
    LANGUAGES_DATA,
    THEME_TRANSLATIONS,
)
from .logger import get_logger

logger = get_logger(__name__)

def ensure_translation_files():
    """Automatycznie generuje brakujące pliki językowe przy starcie aplikacji."""
    i18n_path = I18N_DIR
    
    # Upewniamy się, że katalog i18n istnieje
    if not i18n_path.exists():
        try:
            i18n_path.mkdir(parents=True, exist_ok=True)
        except Exception as e:
            logger.error("[i18n] Nie można utworzyć katalogu: %s", e)
            return

    # Sprawdzamy czy mamy wzorzec (angielski)
    template_path = i18n_path / "en.json"
    if not template_path.exists():
        logger.warning("[i18n] Brak pliku wzorcowego en.json - pomijam generowanie.")
        return

    try:
        with open(template_path, "r", encoding="utf-8") as f:
            template = json.load(f)
    except Exception as e:
        logger.error("[i18n] Błąd odczytu en.json: %s", e)
        return

    for _, lang_code, _ in LANGUAGES_DATA:
        if lang_code == "en": continue # Pomijamy wzorzec

        file_code = I18N_FILE_CODE_MAP.get(lang_code, lang_code)
        file_path = i18n_path / f"{file_code}.json"

        if not file_path.exists():
            new_content = template.copy()
            if file_code in THEME_TRANSLATIONS:
                new_content.update(THEME_TRANSLATIONS[file_code])
            
            try:
                with open(file_path, "w", encoding="utf-8") as f:
                    json.dump(new_content, f, indent=4, ensure_ascii=False)
                logger.info("[i18n] Wygenerowano brakujący plik: %s", file_path.name)
            except Exception as e:
                logger.error("[i18n] Błąd zapisu %s: %s", file_path.name, e)

class Translator:
    def __init__(self, config):
        self.config = config
        self.translations = {}
        # Używamy globalnej mapy, ale z obsługą specyficznych nazw plików JSON jeśli są inne niż kody Qt
        # Tutaj zakładamy uproszczenie, że nazwy plików JSON odpowiadają kodom z LANG_MAP
        self.lang_map = LANG_MAP
        self.load_translations()

    def load_translations(self):
        """Ładuje plik JSON odpowiadający wybranemu językowi."""
        lang_name = self.config.get("language", DEFAULT_LANGUAGE)
        lang_code = self.lang_map.get(lang_name, "pl")
        i18n_code = I18N_FILE_CODE_MAP.get(lang_code, lang_code)

        i18n_path = I18N_DIR
        
        # 1. Ładujemy bazowy język (Angielski) jako fallback dla brakujących kluczy
        fallback_path = i18n_path / "en.json"
        self.translations = {}
        
        if fallback_path.exists():
            try:
                with open(fallback_path, "r", encoding="utf-8") as f:
                    self.translations = json.load(f)
            except Exception as e:
                logger.error("[translator] Błąd ładowania fallback en.json: %s", e)

        # 2. Jeśli wybrany język to nie Angielski, nadpisujemy klucze
        if i18n_code != "en":
            file_path = i18n_path / f"{i18n_code}.json"
            logger.debug("[translator] Szukam pliku: %s", file_path)

            if file_path.exists():
                try:
                    with open(file_path, "r", encoding="utf-8") as f:
                        current_trans = json.load(f)
                        self.translations.update(current_trans)
                    logger.info(
                        "[translator] Załadowano %d kluczy dla %s.",
                        len(current_trans),
                        i18n_code,
                    )
                except Exception as e:
                    logger.error("[translator] Błąd ładowania %s: %s", file_path, e)
            else:
                logger.warning(
                    "[translator] Brak pliku %s, pozostaję przy fallbacku.",
                    file_path,
                )

        # 3. Wstrzyknięcie tłumaczeń motywów (jeśli brakuje ich w pliku JSON)
        # Dzięki temu nazwy motywów będą przetłumaczone nawet przy braku pełnego pliku językowego
        if i18n_code in THEME_TRANSLATIONS:
            self.translations.update(THEME_TRANSLATIONS[i18n_code])

    def get(self, key, default=None):
        """Pobiera przetłumaczony tekst dla danego klucza."""
        # Jeśli klucz nie istnieje, zwraca sam klucz (ułatwia szukanie braków w JSON)
        return self.translations.get(key, default if default else key)
