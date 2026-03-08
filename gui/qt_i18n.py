import logging
from PySide6.QtCore import QTranslator, QLibraryInfo


def update_qt_translator(app, translator, lang_code):
    """Ładuje systemowe tłumaczenia Qt dla aktualnego języka."""
    app.removeTranslator(translator)
    qt_translations_path = QLibraryInfo.path(QLibraryInfo.TranslationsPath)

    if translator.load(f"qtbase_{lang_code}.qm", qt_translations_path):
        app.installTranslator(translator)
        logging.info(f"[Qt] Załadowano tłumaczenie systemowe dla: {lang_code}")
    elif translator.load(f"qt_{lang_code}.qm", qt_translations_path):
        app.installTranslator(translator)
        logging.info(f"[Qt] Załadowano zbiorcze tłumaczenie: {lang_code}")
    else:
        logging.warning(f"[Qt] Brak systemowego pliku .qm dla: {lang_code}")


class AyoQtTranslator(QTranslator):
    """
    Niestandardowy tłumacz Qt, który przechwytuje systemowe frazy (np. nagłówki kolumn)
    i tłumaczy je używając naszych kluczy.
    """

    def __init__(self, translations_dict):
        super().__init__()
        self.translations = translations_dict

    def update_translations(self, translations_dict):
        self.translations = translations_dict

    def translate(self, context, source_text, disambiguation=None, n=-1):
        if not source_text:
            return ""

        qt_map = {
            "Name": "qt_col_name",
            "Size": "qt_col_size",
            "Type": "qt_col_type",
            "Date Modified": "qt_col_date",
        }

        if source_text in qt_map:
            key = qt_map[source_text]
            if key in self.translations:
                return self.translations[key]

        return super().translate(context, source_text, disambiguation, n)
