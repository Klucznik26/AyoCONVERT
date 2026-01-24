from PySide6.QtWidgets import QLabel
from PySide6.QtGui import QPixmap, QDragEnterEvent, QDropEvent
from PySide6.QtCore import Qt, Signal

class DropArea(QLabel):
    # Sygnał wysyłany po upuszczeniu plików
    files_dropped = Signal(list)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("DragArea") # Dla stylów CSS
        self.setAlignment(Qt.AlignCenter)
        self.setAcceptDrops(True)
        self.setScaledContents(False) # Chcemy sami kontrolować skalowanie
        self.setMinimumSize(400, 400)

    def set_preview(self, file_path):
        """Ładuje i wyświetla podgląd wybranego obrazu."""
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
            self.setText("Błąd ładowania obrazu")

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
            file_paths = [url.toLocalFile() for url in urls]
            self.files_dropped.emit(file_paths)
            event.acceptProposedAction()