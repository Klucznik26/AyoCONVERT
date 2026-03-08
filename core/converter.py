from pathlib import Path

from PIL import Image

from .logger import get_logger


logger = get_logger(__name__)

FORMAT_MAP = {
    "JPG": "JPEG",
    "HEIC": "HEIF",
}


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
        target_upper = target_format.upper()
        pil_format = FORMAT_MAP.get(target_upper, target_upper)
        if pil_format == "SVG":
            logger.warning("Format SVG nie jest wspierany jako format wyjściowy.")
            return False, "Format SVG nie jest wspierany jako format wyjściowy."
        if not self._is_save_format_supported(pil_format):
            logger.warning("Format %s nie jest wspierany przez aktualną instalację Pillow.", target_upper)
            return False, f"Format {target_upper} nie jest wspierany przez aktualną instalację Pillow."

        for path in file_paths:
            try:
                img_path = Path(path)

                with Image.open(img_path) as img:
                    # Budujemy nową nazwę: nazwa + _AC + nowy format
                    new_filename = f"{img_path.stem}{suffix}.{target_format.lower()}"
                    save_path = output_path / new_filename
                    
                    # Konwersja kolorów (np. przezroczystość PNG na białe tło JPG)
                    final_img = img
                    if pil_format == "JPEG" and img.mode in ("RGBA", "P"):
                        final_img = img.convert("RGB")
                    
                    # Parametry zapisu (quality tylko dla wspieranych formatów)
                    save_params = {}
                    if pil_format in ["JPEG", "WEBP", "AVIF", "HEIF"]:
                        save_params["quality"] = 95
                        
                    final_img.save(save_path, pil_format, **save_params)
                    results.append(str(save_path))
            except Exception as e:
                logger.error("Błąd konwersji %s: %s", path, e)

        if not results:
            return False, "Nie udało się skonwertować żadnego pliku."
        return True, results

    @staticmethod
    def _is_save_format_supported(pil_format):
        """Sprawdza, czy Pillow potrafi zapisać do zadanego formatu."""
        Image.init()
        return pil_format in Image.SAVE
