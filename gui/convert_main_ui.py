from pathlib import Path

from PySide6.QtCore import QTimer
from PySide6.QtWidgets import QFileDialog, QHBoxLayout, QMainWindow, QMessageBox, QWidget

from core.convert_image_convert_logic import ImageConvertLogic
from core.convert_settings_logic import SUPPORTED_IMAGE_EXTENSIONS, SettingsLogic
from core.convert_theme_selector_logic import ThemeSelectorLogic
from gui.convert_file_drop_ui import FileDropUI
from gui.convert_image_convert_ui import ImageConvertUI
from gui.convert_preview_ui import PreviewUI
from gui.convert_settings_ui import SettingsUI


class MainUI(QMainWindow):
    VERSION = '1.7.0'

    def __init__(self):
        super().__init__()
        self.current_files = []
        self.setMinimumSize(1050, 700)
        self.resize(1050, 700)
        central = QWidget(); central.setObjectName('main_widget'); self.setCentralWidget(central)
        layout = QHBoxLayout(central); layout.setContentsMargins(10, 10, 10, 10); layout.setSpacing(10)
        self.settings_ui = SettingsUI(self)
        self.image_convert_ui = ImageConvertUI(self)
        self.file_drop_ui = FileDropUI(self)
        self.preview_ui = PreviewUI(self)
        layout.addWidget(self.settings_ui); layout.addWidget(self.image_convert_ui); layout.addWidget(self.file_drop_ui); layout.addWidget(self.preview_ui)
        self.settings_ui.close_requested.connect(self.close)
        self.settings_ui.language_changed.connect(self.retranslate_ui)
        self.settings_ui.theme_changed.connect(self.apply_theme)
        self.file_drop_ui.files_dropped.connect(self._load)
        self.image_convert_ui.open_files_requested.connect(self._open_files)
        self.image_convert_ui.open_dir_requested.connect(self._open_dir)
        self.image_convert_ui.save_dir_requested.connect(self._select_output_dir)
        self.image_convert_ui.run_requested.connect(self._run)
        self.preview_ui.file_list.currentRowChanged.connect(self._preview_selected_file)
        output_dir = SettingsLogic.get_output_dir()
        if output_dir:
            self.image_convert_ui.update_output_dir_tooltip(output_dir)
        self.apply_theme(SettingsLogic.get_theme())
        self.retranslate_ui()

    def retranslate_ui(self, *_args):
        self.setWindowTitle(f'AyoCONVERT {self.VERSION}')
        self.settings_ui.retranslate_ui(); self.image_convert_ui.retranslate_ui(); self.file_drop_ui.retranslate_ui(); self.preview_ui.retranslate_ui()
        self._refresh_ready_state()

    def apply_theme(self, theme_name: str | None = None):
        self.setStyleSheet(ThemeSelectorLogic.get_stylesheet(theme_name or SettingsLogic.get_theme()))

    def _open_files(self):
        dialog = self._file_dialog(SettingsLogic.tr('btn_open'))
        dialog.setFileMode(QFileDialog.FileMode.ExistingFiles)
        img_label = SettingsLogic.tr('dlg_filter_images')
        all_label = SettingsLogic.tr('dlg_filter_all')
        dialog.setNameFilter(f"{img_label} (*.png *.jpg *.jpeg *.bmp *.webp *.tiff *.gif *.avif *.heic *.heif *.svg *.ico);;{all_label} (*.*)")
        if dialog.exec():
            self._load(dialog.selectedFiles())

    def _open_dir(self):
        dialog = self._file_dialog(SettingsLogic.tr('btn_open_dir'))
        dialog.setFileMode(QFileDialog.FileMode.Directory)
        dialog.setOption(QFileDialog.Option.ShowDirsOnly, True)
        if dialog.exec() and dialog.selectedFiles():
            self._load(dialog.selectedFiles())

    def _select_output_dir(self):
        dialog = self._file_dialog(SettingsLogic.tr('btn_save_dir'))
        dialog.setFileMode(QFileDialog.FileMode.Directory)
        dialog.setOption(QFileDialog.Option.ShowDirsOnly, True)
        dialog.setLabelText(QFileDialog.DialogLabel.Accept, SettingsLogic.tr('btn_save'))
        if dialog.exec() and dialog.selectedFiles():
            path = dialog.selectedFiles()[0]
            SettingsLogic.set_output_dir(path)
            self.image_convert_ui.update_output_dir_tooltip(path)
            self._refresh_ready_state()

    def _file_dialog(self, title: str) -> QFileDialog:
        dialog = QFileDialog(self, title, str(Path.home()))
        dialog.setOption(QFileDialog.Option.DontUseNativeDialog, True)
        dialog.setLabelText(QFileDialog.DialogLabel.Accept, SettingsLogic.tr('btn_open'))
        dialog.setLabelText(QFileDialog.DialogLabel.Reject, SettingsLogic.tr('btn_cancel'))
        dialog.setLabelText(QFileDialog.DialogLabel.FileName, SettingsLogic.tr('lbl_file_name'))
        dialog.setLabelText(QFileDialog.DialogLabel.FileType, SettingsLogic.tr('lbl_file_type'))
        dialog.setLabelText(QFileDialog.DialogLabel.LookIn, SettingsLogic.tr('lbl_look_in'))
        dialog.setStyleSheet(self.styleSheet())
        return dialog

    def _load(self, paths):
        valid = ImageConvertLogic.filter_valid_images(paths)
        if not valid:
            return
        self.current_files = valid
        self.file_drop_ui.show_preview(valid[0])
        self.preview_ui.update_files(valid)
        self.image_convert_ui.update_format_availability(ImageConvertLogic.normalize_source_format(valid[0]))
        self._refresh_ready_state()

    def _refresh_ready_state(self):
        if not self.current_files:
            self.image_convert_ui.set_status_message('lbl_status_select_img')
            self.image_convert_ui.set_ready_state(False)
            return
        output_dir = SettingsLogic.get_output_dir()
        if not output_dir or not Path(output_dir).exists():
            self.image_convert_ui.set_status_message('lbl_status_select_dir')
            self.image_convert_ui.set_ready_state(False)
            return
        self.image_convert_ui.set_status_message('')
        self.image_convert_ui.set_ready_state(True)

    def _run(self, target_format: str):
        if not self.current_files:
            return
        self.image_convert_ui.btn_run.set_progress(0.2)
        success, result = ImageConvertLogic.convert_files(self.current_files, target_format)
        if not success:
            QMessageBox.critical(self, SettingsLogic.tr('info_title'), str(result))
            self.image_convert_ui.reset_progress()
            return
        self.image_convert_ui.btn_run.set_progress(1.0)
        self.preview_ui.clear_files(completed=True)
        self.current_files = []
        self.file_drop_ui.animate_success(lambda: self.file_drop_ui.show_success(SettingsLogic.tr('lbl_done')))
        QTimer.singleShot(1200, self.file_drop_ui.reset_preview)
        QTimer.singleShot(1200, self.image_convert_ui.reset_progress)
        self._refresh_ready_state()

    def _preview_selected_file(self, index: int):
        if 0 <= index < len(self.current_files):
            self.file_drop_ui.show_preview(self.current_files[index])
