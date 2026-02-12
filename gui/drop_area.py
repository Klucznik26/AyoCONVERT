from PySide6.QtWidgets import QLabel
from PySide6.QtGui import QPixmap, QDragEnterEvent, QDropEvent
from PySide6.QtCore import Qt, Signal
from pathlib import Path

class DropArea(QLabel):
    # Sygnał wysyłany po upuszczeniu plików
    files_dropped = Signal(list)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("DragArea") # Dla stylów CSS
        self.setAlignment(Qt.AlignCenter)
        self.setAcceptDrops(True)
        self.setScaledContents(False) # Chcemy sami kontrolować skalowanie
        self.setFixedSize(400, 400)

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
            self.setText("Błąd ładowania obrazu")

    def show_success(self, text):
        """Wyświetla komunikat o sukcesie w kontrastowym stylu."""
        self.clear() # Usuwa pixmapę (wyrzuca obraz)
        self.setText(text)
        # Styl kontrastowy: duży font, zielony kolor (neonowy)
        self.setStyleSheet("""
            font-size: 32px; 
            font-weight: bold; 
            color: #9ece6a; 
            border: 3px solid #9ece6a;
            background-color: rgba(158, 206, 106, 0.1);
        """)

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
            valid_exts = {'.png', '.jpg', '.jpeg', '.bmp', '.webp', '.tiff'}
            
            for url in urls:
                path_str = url.toLocalFile()
                path_obj = Path(path_str)
                
                if path_obj.is_dir():
                    try:
                        images = [str(p) for p in path_obj.iterdir() if p.is_file() and p.suffix.lower() in valid_exts]
                        final_paths.extend(images)
                    except Exception:
                        pass
                elif path_obj.suffix.lower() in valid_exts:
                    final_paths.append(path_str)
            
            if final_paths:
                self.files_dropped.emit(final_paths)
            
            event.acceptProposedAction()