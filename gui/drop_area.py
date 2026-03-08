from pathlib import Path

from PySide6.QtCore import Qt, Signal, QVariantAnimation, QEasingCurve
from PySide6.QtGui import QDragEnterEvent, QDropEvent, QPixmap, QPainter
from PySide6.QtWidgets import QLabel, QSizePolicy
from core.app_config import SUPPORTED_IMAGE_EXTENSIONS

class DropArea(QLabel):
    # Sygnał wysyłany po upuszczeniu plików
    files_dropped = Signal(list)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.error_loading_text = "Image loading error"
        self.setObjectName("DragArea") # Dla stylów CSS
        self.setAlignment(Qt.AlignCenter)
        self.setAcceptDrops(True)
        self.setScaledContents(False) # Chcemy sami kontrolować skalowanie
        self.setFixedWidth(465)
        self.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Expanding)
        
        # Zmienne do animacji
        self._animating = False
        self._anim_progress = 0.0

    def set_preview(self, file_path):
        """Ładuje i wyświetla podgląd wybranego obrazu."""
        self.setStyleSheet("") # Reset stylu (np. po komunikacie sukcesu)
        pixmap = QPixmap(file_path)
        if not pixmap.isNull():
            # Skalujemy obraz do rozmiaru okna, zachowując proporcje
            scaled_pixmap = pixmap.scaled(
                self.size() * 0.9, # Mały margines, żeby nie dotykało ramek
                Qt.KeepAspectRatio, 
                Qt.SmoothTransformation
            )
            self.setPixmap(scaled_pixmap)
        else:
            self.setText(self.error_loading_text)

    def set_error_loading_text(self, text):
        self.error_loading_text = text

    def animate_success(self, on_finished_callback):
        """Uruchamia animację przechylania i znikania obrazu."""
        self._animating = True
        
        # Animacja wartości od 0.0 do 1.0
        self.anim = QVariantAnimation()
        self.anim.setStartValue(0.0)
        self.anim.setEndValue(1.0)
        self.anim.setDuration(400) # Szybka animacja (400ms)
        self.anim.setEasingCurve(QEasingCurve.InBack) # Efekt cofnięcia przed wyrzutem
        
        self.anim.valueChanged.connect(self._update_anim_step)
        self.anim.finished.connect(lambda: self._finish_animation(on_finished_callback))
        self.anim.start()

    def _update_anim_step(self, value):
        self._anim_progress = value
        self.update() # Wymusza przerysowanie w paintEvent

    def _finish_animation(self, callback):
        self._animating = False
        self._anim_progress = 0.0
        self.clear() # Usuwamy obraz fizycznie
        if callback:
            callback()

    def show_success(self, text):
        """Wyświetla komunikat o sukcesie w kontrastowym stylu."""
        # self.clear() jest już wołane w _finish_animation
        self.setText(text)
        # Styl kontrastowy: duży font, zielony kolor (neonowy)
        self.setStyleSheet("""
            font-size: 32px; 
            font-weight: bold; 
            color: #9ece6a; 
            border: 3px solid #9ece6a;
            background-color: rgba(158, 206, 106, 0.1);
        """)

    def paintEvent(self, event):
        """Nadpisujemy rysowanie, aby obsłużyć animację obrotu."""
        if self._animating and self.pixmap() and not self.pixmap().isNull():
            painter = QPainter(self)
            painter.setRenderHint(QPainter.Antialiasing)
            painter.setRenderHint(QPainter.SmoothPixmapTransform)

            pix = self.pixmap()
            # Obliczamy pozycję obrazka (jest wyśrodkowany)
            x = (self.width() - pix.width()) / 2
            y = (self.height() - pix.height()) / 2
            
            painter.save()
            
            # Punkt obrotu: Lewy Dolny róg OBRAZU (nie widgetu)
            pivot_x = x
            pivot_y = y + pix.height()
            
            painter.translate(pivot_x, pivot_y)
            painter.rotate(self._anim_progress * -45) # Obrót o 45 stopni w lewo
            painter.setOpacity(1.0 - self._anim_progress) # Zanikanie
            painter.translate(-pivot_x, -pivot_y)
            
            painter.drawPixmap(int(x), int(y), pix)
            painter.restore()
        else:
            super().paintEvent(event)

    def dragEnterEvent(self, event: QDragEnterEvent):
        """Obsługa wejścia plikiem w obszar pola."""
        if event.mimeData().hasUrls():
            event.acceptProposedAction()
            self.setStyleSheet("border: 2px dashed #e0af68; background-color: rgba(224, 175, 104, 0.1);")

    def dragLeaveEvent(self, event):
        """Powrót do normalnego wyglądu po wyjściu plikiem poza pole."""
        self.setStyleSheet("")

    def dropEvent(self, event: QDropEvent):
        """Obsługa upuszczenia pliku."""
        self.setStyleSheet("")
        urls = event.mimeData().urls()
        if urls:
            final_paths = []
            for url in urls:
                path_str = url.toLocalFile()
                path_obj = Path(path_str)
                
                if path_obj.is_dir():
                    try:
                        images = [str(p) for p in path_obj.iterdir() if p.is_file() and p.suffix.lower() in SUPPORTED_IMAGE_EXTENSIONS]
                        final_paths.extend(images)
                    except Exception:
                        pass
                elif path_obj.suffix.lower() in SUPPORTED_IMAGE_EXTENSIONS:
                    final_paths.append(path_str)
            
            if final_paths:
                self.files_dropped.emit(final_paths)
            
            event.acceptProposedAction()
