from pathlib import Path
try:
    from PIL import Image
except Exception:  # Pillow może nie być dostępny w środowisku narzędziowym
    Image = None

# --- Ścieżki aplikacji ---
PROJECT_ROOT = Path(__file__).resolve().parent.parent
CONFIG_DIR = PROJECT_ROOT / "config"
CONFIG_PATH = CONFIG_DIR / "config.json"
I18N_DIR = PROJECT_ROOT / "i18n"

# --- Domyślne ustawienia ---
DEFAULT_LANGUAGE = "Polski"
DEFAULT_THEME = "system"
DEFAULT_LAST_FORMAT = "png"
DEFAULT_OUTPUT_SUFFIX = "_AC"

DEFAULT_SETTINGS = {
    "language": DEFAULT_LANGUAGE,
    "theme": DEFAULT_THEME,
    "last_format": DEFAULT_LAST_FORMAT,
    "output_suffix": DEFAULT_OUTPUT_SUFFIX,
}

TARGET_FORMAT_OPTIONS = [
    "PNG",
    "JPG",
    "WEBP",
    "BMP",
    "TIFF",
    "GIF",
    "AVIF",
    "HEIC",
    "ICO",
]

FORMAT_MAP_FOR_SAVE = {
    "JPG": "JPEG",
    "HEIC": "HEIF",
}

SUPPORTED_IMAGE_EXTENSIONS = {
    ".png",
    ".jpg",
    ".jpeg",
    ".bmp",
    ".webp",
    ".tiff",
    ".gif",
    ".avif",
    ".heic",
    ".heif",
    ".svg",
    ".ico",
}


def get_available_target_formats():
    """
    Zwraca formaty docelowe wspierane przez aktualną instalację Pillow.
    SVG pozostaje tylko formatem wejściowym (Pillow nie zapisuje do SVG).
    """
    if Image is None:
        return [fmt for fmt in TARGET_FORMAT_OPTIONS if fmt not in {"SVG", "HEIC"}]

    Image.init()
    available = []
    for fmt in TARGET_FORMAT_OPTIONS:
        if fmt == "SVG":
            continue
        pil_fmt = FORMAT_MAP_FOR_SAVE.get(fmt, fmt)
        if pil_fmt in Image.SAVE:
            available.append(fmt)
    return available

# --- Języki interfejsu ---
# (Nazwa wyświetlana, Kod pliku/Qt, Flaga)
LANGUAGES_DATA = [
    ("Polski", "pl", "🇵🇱"),
    ("English", "en", "🇺🇸"),
    ("Български", "bg", "🇧🇬"),
    ("Čeština", "cs", "🇨🇿"),
    ("Dansk", "da", "🇩🇰"),
    ("Deutsch", "de", "🇩🇪"),
    ("Español", "es", "🇪🇸"),
    ("Eesti", "et", "🇪🇪"),
    ("Suomi", "fi", "🇫🇮"),
    ("Français", "fr", "🇫🇷"),
    ("Magyar", "hu", "🇭🇺"),
    ("Íslenska", "is", "🇮🇸"),
    ("Italiano", "it", "🇮🇹"),
    ("Lietuvių", "lt", "🇱🇹"),
    ("Latviešu", "lv", "🇱🇻"),
    ("Nederlands", "nl", "🇳🇱"),
    ("Norsk", "no", "🇳🇴"),
    ("Português", "pt", "🇵🇹"),
    ("Română", "ro", "🇷🇴"),
    ("Slovenčina", "sk", "🇸🇰"),
    ("Svenska", "sv", "🇸🇪"),
    ("Українська", "uk", "🇺🇦"),
    ("Ελληνικά", "el", "🇬🇷"),
    ("ქართული", "ka", "🇬🇪"),
    ("Türkçe", "tr", "🇹🇷"),
    ("Српски", "sr", "🇷🇸"),
    ("Slovenščina", "sl", "🇸🇮"),
    ("Català", "ca", "🇪🇸"),
    ("Hrvatski", "hr", "🇭🇷"),
    ("Shqip", "sq", "🇦🇱"),
    ("Malti", "mt", "🇲🇹"),
]

LANG_MAP = {name: code for name, code, _flag in LANGUAGES_DATA}

# Mapowanie kodów języków na nazwy plików JSON w i18n/.
# Obsługuje starsze/niestandardowe nazwy plików użyte w projekcie.
I18N_FILE_CODE_MAP = {
    "uk": "ua",
    "cs": "cz",
    "sl": "si",
    "ka": "ge",
    "et": "ee",
}

# --- Motywy ---
THEME_OPTIONS = [
    ("system", "theme_system"),
    ("dark", "theme_dark"),
    ("light", "theme_light"),
    ("relax", "theme_relax"),
    ("creative", "theme_creative"),
]

LEGACY_THEME_MAP = {
    "Systemowy": "system",
    "Ciemny": "dark",
    "Jasny": "light",
    "Relaksacyjny": "relax",
    "Kreatywny": "creative",
}

# Awaryjne tłumaczenia nazw motywów, wstrzykiwane gdy brakuje ich w plikach JSON
THEME_TRANSLATIONS = {
    "ua": {"theme_system": "Системна", "theme_dark": "Темна", "theme_light": "Світла", "theme_relax": "Релакс", "theme_creative": "Креативна"},
    "lv": {"theme_system": "Sistēmas", "theme_dark": "Tumšs", "theme_light": "Gaišs", "theme_relax": "Relaksējošs", "theme_creative": "Radošs"},
    "lt": {"theme_system": "Sistemos", "theme_dark": "Tamsi", "theme_light": "Šviesi", "theme_relax": "Atpalaiduojanti", "theme_creative": "Kūrybinė"},
    "ee": {"theme_system": "Süsteemi", "theme_dark": "Tume", "theme_light": "Hele", "theme_relax": "Lõõgastav", "theme_creative": "Loominguline"},
    "pt": {"theme_system": "Sistema", "theme_dark": "Escuro", "theme_light": "Claro", "theme_relax": "Relaxante", "theme_creative": "Criativo"},
    "cz": {"theme_system": "Systémový", "theme_dark": "Tmavý", "theme_light": "Světlý", "theme_relax": "Relaxační", "theme_creative": "Kreativní"},
    "si": {"theme_system": "Sistemska", "theme_dark": "Temna", "theme_light": "Svetla", "theme_relax": "Sproščujoča", "theme_creative": "Ustvarjalna"},
    "ge": {"theme_system": "სისტემური", "theme_dark": "მუქი", "theme_light": "ღია", "theme_relax": "სარელაქსაციო", "theme_creative": "კრეატიული"},
    "es": {"theme_system": "Sistema", "theme_dark": "Oscuro", "theme_light": "Claro", "theme_relax": "Relajante", "theme_creative": "Creativo"},
    "fr": {"theme_system": "Système", "theme_dark": "Sombre", "theme_light": "Clair", "theme_relax": "Relaxant", "theme_creative": "Créatif"},
    "it": {"theme_system": "Sistema", "theme_dark": "Scuro", "theme_light": "Chiaro", "theme_relax": "Rilassante", "theme_creative": "Creativo"},
    "ro": {"theme_system": "Sistem", "theme_dark": "Întunecat", "theme_light": "Luminos", "theme_relax": "Relaxant", "theme_creative": "Creativ"},
    "el": {"theme_system": "Σύστημα", "theme_dark": "Σκοτεινό", "theme_light": "Φωτεινό", "theme_relax": "Χαλαρωτικό", "theme_creative": "Δημιουργικό"},
    "nl": {"theme_system": "Systeem", "theme_dark": "Donker", "theme_light": "Licht", "theme_relax": "Ontspannend", "theme_creative": "Creatief"},
    "is": {"theme_system": "Kerfis", "theme_dark": "Dökkt", "theme_light": "Ljóst", "theme_relax": "Slakandi", "theme_creative": "Skapandi"},
}
