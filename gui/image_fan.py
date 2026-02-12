import random
from pathlib import Path
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel
from PySide6.QtGui import QPainter, QPixmap, QColor, QPen
from PySide6.QtCore import Qt, QPoint

class FanCanvas(QWidget):
    """Widget odpowiedzialny wyłącznie za rysowanie wachlarza kart."""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedSize(250, 180) # Rozmiar obszaru wachlarza
        self.images = [] # Lista krotek (QPixmap, kąt_obrotu)

    def update_cards(self, images_data):
        self.images = images_data
        self.update()

    def paintEvent(self, event):
        """Rysuje karty w formie wachlarza."""
        if not self.images:
            return

        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setRenderHint(QPainter.SmoothPixmapTransform)

        # Środek wachlarza (punkt zaczepienia na dole widgetu)
        center_x = self.width() // 2
        center_y = self.height() - 20

        for pixmap, angle in self.images:
            painter.save()
            painter.translate(center_x, center_y)
            painter.rotate(angle)
            
            card_w = pixmap.width() + 10
            card_h = pixmap.height() + 10
            offset_x = -card_w // 2
            offset_y = -card_h - 20 

            painter.setPen(QPen(QColor(0, 0, 0, 50), 1))
            painter.setBrush(QColor(240, 240, 240))
            painter.drawRect(offset_x, offset_y, card_w, card_h)
            painter.drawPixmap(offset_x + 5, offset_y + 5, pixmap)
            painter.restore()

class ImageFan(QWidget):
    """Główny kontener zawierający wachlarz i licznik plików."""
    def __init__(self, translator, parent=None):
        super().__init__(parent)
        self.translator = translator
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(5)
        
        self.canvas = FanCanvas()
        self.lbl_count = QLabel()
        self.lbl_count.setAlignment(Qt.AlignCenter)
        self.lbl_count.setStyleSheet("font-weight: bold; font-size: 11px; color: #d4a373;")
        
        layout.addWidget(self.canvas)
        layout.addWidget(self.lbl_count)
        
        self.setVisible(False) # Domyślnie ukryty

    def set_images(self, file_paths):
        """
        Przyjmuje listę ścieżek, losuje do 5 sztuk i przygotowuje miniatury.
        """
        # Filtrujemy tylko obrazy (na wypadek gdyby na liście były inne pliki)
        valid_exts = {'.png', '.jpg', '.jpeg', '.bmp', '.webp', '.tiff'}
        image_paths = [p for p in file_paths if Path(p).suffix.lower() in valid_exts]

        # Warunek: Pokaż tylko jeśli wybrano więcej niż 1 plik
        if len(image_paths) <= 1:
            self.canvas.update_cards([])
            self.setVisible(False)
            return

        self.setVisible(True)
        
        # Aktualizacja licznika
        txt_queue = self.translator.get("lbl_queue_count", "Plików w kolejce:")
        self.lbl_count.setText(f"{txt_queue} {len(image_paths)}")

        # Losowanie max 5 plików
        count = min(len(image_paths), 5)
        selected_paths = random.sample(image_paths, count)

        # Przygotowanie miniatur
        cards_data = []
        
        # Obliczanie kątów dla wachlarza (rozłożone symetrycznie)
        # Np. dla 3 kart: -15, 0, 15 stopni
        start_angle = -20
        step = 40 / (count - 1) if count > 1 else 0
        
        for i, path in enumerate(selected_paths):
            pix = QPixmap(path)
            if not pix.isNull():
                # Skalujemy do małego rozmiaru (karta)
                scaled = pix.scaled(100, 100, Qt.KeepAspectRatio, Qt.SmoothTransformation)
                
                angle = start_angle + (i * step)
                cards_data.append((scaled, angle))
        
        self.canvas.update_cards(cards_data)