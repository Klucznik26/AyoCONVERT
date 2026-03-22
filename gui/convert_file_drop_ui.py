from PySide6.QtWidgets import QFrame, QSizePolicy, QVBoxLayout

from gui.convert_file_drop_widgets import FileDropLabel


class FileDropUI(QFrame):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName('rightPanel')
        self.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Expanding)
        layout = QVBoxLayout(self)
        layout.setContentsMargins(15, 15, 15, 15)
        self.drop_label = FileDropLabel(self)
        self.drop_label.setObjectName('dropArea')
        layout.addWidget(self.drop_label)
        self.files_dropped = self.drop_label.files_dropped

    def resizeEvent(self, event):
        super().resizeEvent(event)
        drop_height = event.size().height() - 30
        if drop_height <= 0:
            return
        drop_width = int(drop_height * (2 / 3))
        panel_width = drop_width + 30
        if self.width() != panel_width:
            self.setFixedWidth(panel_width)
        self.drop_label.setFixedSize(drop_width, drop_height)

    def retranslate_ui(self):
        self.drop_label.retranslate_ui()

    def show_preview(self, path: str):
        self.drop_label.set_preview(path)

    def show_success(self, text: str):
        self.drop_label.show_success(text)

    def animate_success(self, callback):
        self.drop_label.animate_success(callback)

    def reset_preview(self):
        self.drop_label.reset()
