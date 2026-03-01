from pathlib import Path

from PySide6.QtWidgets import QFileDialog

def _prepare_custom_dialog(parent, translator, title, directory, file_filter=None):
    """Pomocnicza funkcja konfigurująca styl i tłumaczenia dialogu."""
    dialog = QFileDialog(parent, title, directory)
    dialog.setOption(QFileDialog.Option.DontUseNativeDialog, True)
    
    if file_filter:
        dialog.setNameFilter(file_filter)
        
    # Tłumaczenie standardowych przycisków i etykiet Qt
    dialog.setLabelText(QFileDialog.Accept, translator.get("btn_open") if file_filter else translator.get("btn_save"))
    dialog.setLabelText(QFileDialog.Reject, translator.get("btn_cancel"))
    dialog.setLabelText(QFileDialog.FileName, translator.get("lbl_file_name"))
    dialog.setLabelText(QFileDialog.FileType, translator.get("lbl_file_type"))
    dialog.setLabelText(QFileDialog.LookIn, translator.get("lbl_look_in"))
    
    return dialog

def select_save_directory(parent, translator, start_dir):
    """Otwiera dialog wyboru katalogu zapisu i zwraca ścieżkę lub None."""
    title = translator.get("btn_save_dir")
    dialog = _prepare_custom_dialog(parent, translator, title, start_dir)
    dialog.setFileMode(QFileDialog.FileMode.Directory)
    dialog.setOption(QFileDialog.Option.ShowDirsOnly, True)
    dialog.setLabelText(QFileDialog.Accept, translator.get("btn_save"))
    
    if dialog.exec():
        selected = dialog.selectedFiles()
        if selected:
            return selected[0]
    return None

def open_files_dialog(parent, translator, start_dir):
    """Otwiera dialog wyboru plików i zwraca listę ścieżek lub None."""
    title = translator.get("btn_open")
    img_label = translator.get("dlg_filter_images")
    all_label = translator.get("dlg_filter_all")
    file_filter = f"{img_label} (*.png *.jpg *.jpeg *.bmp *.webp *.tiff);;{all_label} (*.*)"
    
    dialog = _prepare_custom_dialog(parent, translator, title, start_dir, file_filter)
    dialog.setFileMode(QFileDialog.FileMode.ExistingFiles)
    
    if dialog.exec():
        return dialog.selectedFiles()
    return None

def open_directory_scan(parent, translator, start_dir):
    """Wybiera folder, skanuje go i zwraca listę obsługiwanych obrazów."""
    title = translator.get("btn_open_dir")
    dialog = _prepare_custom_dialog(parent, translator, title, start_dir)
    dialog.setFileMode(QFileDialog.FileMode.Directory)
    dialog.setOption(QFileDialog.Option.ShowDirsOnly, True)
    dialog.setLabelText(QFileDialog.Accept, translator.get("btn_open"))

    if dialog.exec():
        selected = dialog.selectedFiles()
        if selected:
            folder = Path(selected[0])
            valid_exts = {'.png', '.jpg', '.jpeg', '.bmp', '.webp', '.tiff'}
            try:
                return [str(p) for p in folder.iterdir() if p.is_file() and p.suffix.lower() in valid_exts]
            except Exception:
                return []
    return None
