import unittest

from core.convert_settings_logic import SettingsLogic


class SettingsLogicTests(unittest.TestCase):
    def test_translations_return_existing_key(self):
        self.assertTrue(SettingsLogic.tr('btn_run'))


if __name__ == '__main__':
    unittest.main()
