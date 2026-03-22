#!/usr/bin/env python3
import logging
import sys

from PySide6.QtCore import qInstallMessageHandler
from PySide6.QtWidgets import QApplication

from core.convert_settings_logic import SettingsLogic
from gui.convert_main_ui import MainUI


def _qt_message_filter(_msg_type, _context, message):
    if "QString::arg: 2 argument(s) missing in" in message:
        return
    print(message)


def main():
    logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
    qInstallMessageHandler(_qt_message_filter)
    SettingsLogic.ensure_translation_files()
    app = QApplication(sys.argv)
    window = MainUI()
    window.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
