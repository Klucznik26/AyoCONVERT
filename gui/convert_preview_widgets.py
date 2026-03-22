import random
from pathlib import Path

from PySide6.QtCore import Qt
from PySide6.QtGui import QColor, QPainter, QPixmap
from PySide6.QtWidgets import QWidget

from core.convert_settings_logic import SUPPORTED_IMAGE_EXTENSIONS


class PreviewFanWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.paths = []
        self.hub_compact = False
        self.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents)

    def set_images(self, file_paths):
        images = [path for path in file_paths if Path(path).suffix.lower() in SUPPORTED_IMAGE_EXTENSIONS]
        self.paths = random.sample(images, 5) if len(images) > 5 else images
        self.setVisible(len(images) > 1)
        self.update()

    def paintEvent(self, event):
        if len(self.paths) <= 1:
            return
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        painter.setRenderHint(QPainter.RenderHint.SmoothPixmapTransform)
        count = min(len(self.paths), 5)
        if self.hub_compact:
            dx, dy, margin = 10, 6, 3
        else:
            dx, dy, margin = 15, 10, 12
        image_width = self.width() - (count - 1) * dx - (margin * 2)
        image_height = self.height() - (count - 1) * dy - (margin * 2)
        if image_width <= 0 or image_height <= 0:
            return
        total_width = image_width + (count - 1) * dx
        total_height = image_height + (count - 1) * dy
        start_x = (self.width() - total_width) / 2
        start_y = (self.height() - total_height) / 2 + (count - 1) * dy
        for index, path in enumerate(self.paths[:count]):
            pixmap = QPixmap(path)
            if pixmap.isNull():
                continue
            scaled = pixmap.scaled(int(image_width), int(image_height), Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
            slot_x = start_x + index * dx
            slot_y = start_y - index * dy
            img_x = slot_x + (image_width - scaled.width()) / 2
            img_y = slot_y + (image_height - scaled.height()) / 2
            painter.setPen(Qt.PenStyle.NoPen)
            painter.setBrush(QColor(255, 255, 255))
            painter.drawRoundedRect(int(img_x) - 4, int(img_y) - 4, scaled.width() + 8, scaled.height() + 8, 3, 3)
            painter.drawPixmap(int(img_x), int(img_y), scaled)
