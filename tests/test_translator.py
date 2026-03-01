import unittest

from core.translator import Translator


class DummyConfig:
    def __init__(self, language):
        self._language = language

    def get(self, key, default=None):
        if key == "language":
            return self._language
        return default


class TranslatorTests(unittest.TestCase):
    def test_estonian_language_uses_ee_file_mapping(self):
        tr = Translator(DummyConfig("Eesti"))
        self.assertEqual(tr.get("btn_settings"), "Seaded")

    def test_theme_fallback_translations_are_injected(self):
        tr = Translator(DummyConfig("Українська"))
        self.assertEqual(tr.get("theme_dark"), "Темна")


if __name__ == "__main__":
    unittest.main()
