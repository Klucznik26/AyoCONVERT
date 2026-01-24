import os
from PIL import Image
from pathlib import Path

class ImageConverter:
    def __init__(self, config):
        """Inicjalizacja konwertera z dostępem do konfiguracji."""
        self.config = config

    def convert(self, file_paths, target_format):
        """
        Konwertuje obrazy na wybrany format.
        Zapisuje je jako oryginalna_nazwa_AC.rozszerzenie.
        """
        output_dir = self.config.get("last_save_dir")
        # Ustawiamy sufiks na _AC zgodnie z Twoim życzeniem
        suffix = "_AC"
        
        if not output_dir:
            return False, "Nie wybrano katalogu zapisu!"

        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)

        results = []
        for path in file_paths:
            try:
                img_path = Path(path)
                # Sprawdzamy, czy format docelowy jest inny niż źródłowy
                source_ext = img_path.suffix[1:].upper()
                if source_ext == target_format.upper():
                    continue # Pomijamy konwersję na ten sam format

                with Image.open(img_path) as img:
                    # Budujemy nową nazwę: nazwa + _AC + nowy format
                    new_filename = f"{img_path.stem}{suffix}.{target_format.lower()}"
                    save_path = output_path / new_filename
                    
                    # Konwersja kolorów (np. przezroczystość PNG na białe tło JPG)
                    final_img = img
                    if target_format.upper() in ["JPG", "JPEG"] and img.mode in ("RGBA", "P"):
                        final_img = img.convert("RGB")
                    
                    final_img.save(save_path, target_format.upper(), quality=95)
                    results.append(str(save_path))
            except Exception as e:
                print(f"[AyoError] Błąd konwersji {path}: {e}")
                
        return True, results