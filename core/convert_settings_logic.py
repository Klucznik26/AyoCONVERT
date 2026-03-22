import json
from pathlib import Path

try:
    from PIL import Image
except Exception:
    Image = None


PROJECT_ROOT = Path(__file__).resolve().parent.parent
CONFIG_PATH = PROJECT_ROOT / 'config' / 'config.json'
LEGACY_CONFIG_PATH = PROJECT_ROOT / 'config.json'
I18N_DIR = PROJECT_ROOT / 'i18n'
DEFAULT_SETTINGS = {'language': 'pl', 'theme': 'system', 'last_format': 'PNG', 'output_suffix': '_AC', 'last_save_dir': ''}
LANGUAGES = [
    ('Polski', 'pl', '🇵🇱'), ('English', 'en', '🇬🇧'), ('Български', 'bg', '🇧🇬'), ('Čeština', 'cs', '🇨🇿'),
    ('Dansk', 'da', '🇩🇰'), ('Deutsch', 'de', '🇩🇪'), ('Español', 'es', '🇪🇸'), ('Eesti', 'et', '🇪🇪'),
    ('Suomi', 'fi', '🇫🇮'), ('Français', 'fr', '🇫🇷'), ('Magyar', 'hu', '🇭🇺'), ('Íslenska', 'is', '🇮🇸'),
    ('Italiano', 'it', '🇮🇹'), ('Lietuvių', 'lt', '🇱🇹'), ('Latviešu', 'lv', '🇱🇻'), ('Nederlands', 'nl', '🇳🇱'),
    ('Norsk', 'no', '🇳🇴'), ('Português', 'pt', '🇵🇹'), ('Română', 'ro', '🇷🇴'), ('Slovenčina', 'sk', '🇸🇰'),
    ('Svenska', 'sv', '🇸🇪'), ('Українська', 'uk', '🇺🇦'), ('Ελληνικά', 'el', '🇬🇷'), ('ქართული', 'ka', '🇬🇪'),
    ('Türkçe', 'tr', '🇹🇷'), ('Српски', 'sr', '🇷🇸'), ('Slovenščina', 'sl', '🇸🇮'), ('Català', 'ca', '🇪🇸'),
    ('Hrvatski', 'hr', '🇭🇷'), ('Shqip', 'sq', '🇦🇱'), ('Malti', 'mt', '🇲🇹'),
    ('Azərbaycan', 'az', '🇦🇿'), ('Euskara', 'eu', '🇪🇸'), ('Bosanski', 'bs', '🇧🇦'),
    ('Galego', 'gl', '🇪🇸'), ('Gaeilge', 'ga', '🇮🇪'), ('日本語', 'ja', '🇯🇵'),
    ('Қазақ тілі', 'kk', '🇰🇿'), ('Corsu', 'co', '🇫🇷'), ('Lëtzebuergesch', 'lb', '🇱🇺'),
    ('Македонски', 'mk', '🇲🇰'), ('Հայերեն', 'hy', '🇦🇲'), ('Kiswahili', 'sw', '🇰🇪'),
]
LANG_NAME_TO_CODE = {name: code for name, code, _ in LANGUAGES}
SUPPORTED_IMAGE_EXTENSIONS = {'.png', '.jpg', '.jpeg', '.bmp', '.webp', '.tiff', '.gif', '.avif', '.heic', '.heif', '.svg', '.ico'}
TARGET_FORMATS = ['PNG', 'JPG', 'WEBP', 'BMP', 'TIFF', 'GIF', 'AVIF', 'HEIC', 'ICO']
FORMAT_MAP_FOR_SAVE = {'JPG': 'JPEG', 'HEIC': 'HEIF'}
_TRANSLATION_CACHE = {}


class SettingsLogic:
    @staticmethod
    def ensure_translation_files() -> None:
        I18N_DIR.mkdir(parents=True, exist_ok=True)
        template = I18N_DIR / 'en.json'
        if not template.exists():
            return
        try:
            base = json.loads(template.read_text(encoding='utf-8'))
        except Exception:
            return
        for _name, code, _flag in LANGUAGES:
            path = I18N_DIR / f'{code}.json'
            if not path.exists():
                path.write_text(json.dumps(base, indent=4, ensure_ascii=False), encoding='utf-8')

    @staticmethod
    def load() -> dict:
        source = CONFIG_PATH if CONFIG_PATH.exists() else LEGACY_CONFIG_PATH
        data = dict(DEFAULT_SETTINGS)
        if source.exists():
            try:
                data.update(json.loads(source.read_text(encoding='utf-8')))
            except Exception:
                pass
        SettingsLogic.save(data)
        return data

    @staticmethod
    def save(settings: dict) -> None:
        CONFIG_PATH.parent.mkdir(parents=True, exist_ok=True)
        data = dict(DEFAULT_SETTINGS)
        data.update(settings)
        CONFIG_PATH.write_text(json.dumps(data, indent=4, ensure_ascii=False), encoding='utf-8')

    @staticmethod
    def get_language_code() -> str:
        value = SettingsLogic.load().get('language', 'pl')
        if value in LANG_NAME_TO_CODE:
            return LANG_NAME_TO_CODE[value]
        return value if value in {code for _name, code, _flag in LANGUAGES} else 'pl'

    @staticmethod
    def set_language_code(code: str) -> None:
        settings = SettingsLogic.load()
        settings['language'] = code
        SettingsLogic.save(settings)

    @staticmethod
    def get_theme() -> str:
        return SettingsLogic.load().get('theme', 'system')

    @staticmethod
    def set_theme(code: str) -> None:
        settings = SettingsLogic.load(); settings['theme'] = code; SettingsLogic.save(settings)

    @staticmethod
    def get_output_dir() -> str:
        return SettingsLogic.load().get('last_save_dir', '')

    @staticmethod
    def set_output_dir(path: str) -> None:
        settings = SettingsLogic.load(); settings['last_save_dir'] = path; SettingsLogic.save(settings)

    @staticmethod
    def get_last_format() -> str:
        return SettingsLogic.load().get('last_format', 'PNG').upper()

    @staticmethod
    def set_last_format(fmt: str) -> None:
        settings = SettingsLogic.load(); settings['last_format'] = fmt.upper(); SettingsLogic.save(settings)

    @staticmethod
    def get_output_suffix() -> str:
        return SettingsLogic.load().get('output_suffix', '_AC')

    @staticmethod
    def get_languages() -> list[tuple[str, str, str]]:
        return LANGUAGES

    @staticmethod
    def get_theme_codes() -> list[str]:
        return ['dark', 'light', 'creative', 'relax', 'arctic', 'system']

    @staticmethod
    def get_translations(lang_code: str | None = None) -> dict:
        code = lang_code or SettingsLogic.get_language_code()
        if code in _TRANSLATION_CACHE:
            return _TRANSLATION_CACHE[code]
        fallback = {}
        try:
            fallback = json.loads((I18N_DIR / 'en.json').read_text(encoding='utf-8'))
        except Exception:
            pass
        path = I18N_DIR / f'{code}.json'
        data = dict(fallback)
        if path.exists():
            try:
                data.update(json.loads(path.read_text(encoding='utf-8')))
            except Exception:
                pass
        _TRANSLATION_CACHE[code] = data
        return data

    @staticmethod
    def tr(key: str, default: str | None = None) -> str:
        return SettingsLogic.get_translations().get(key, default if default is not None else key)

    @staticmethod
    def get_available_target_formats() -> list[str]:
        if Image is None:
            return [fmt for fmt in TARGET_FORMATS if fmt != 'HEIC']
        Image.init()
        return [fmt for fmt in TARGET_FORMATS if FORMAT_MAP_FOR_SAVE.get(fmt, fmt) in Image.SAVE]
