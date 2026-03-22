import os
from pathlib import Path

from PIL import Image

from core.convert_settings_logic import FORMAT_MAP_FOR_SAVE, SUPPORTED_IMAGE_EXTENSIONS, SettingsLogic


class ImageConvertLogic:
    @staticmethod
    def filter_valid_images(paths: list[str]) -> list[str]:
        valid = []
        for path in paths:
            if os.path.isdir(path):
                for root, _dirs, files in os.walk(path):
                    for file_name in files:
                        file_path = os.path.join(root, file_name)
                        if Path(file_path).suffix.lower() in SUPPORTED_IMAGE_EXTENSIONS:
                            valid.append(file_path)
            elif Path(path).suffix.lower() in SUPPORTED_IMAGE_EXTENSIONS:
                valid.append(path)
        return sorted(set(valid))

    @staticmethod
    def normalize_source_format(path: str) -> str:
        source_ext = Path(path).suffix[1:].upper()
        return {'JPEG': 'JPG', 'HEIF': 'HEIC', 'HEIC': 'HEIC'}.get(source_ext, source_ext)

    @staticmethod
    def output_path(input_path: str, target_format: str) -> Path:
        source = Path(input_path)
        output_dir = Path(SettingsLogic.get_output_dir())
        suffix = SettingsLogic.get_output_suffix()
        return output_dir / f'{source.stem}{suffix}.{target_format.lower()}'

    @staticmethod
    def convert_files(file_paths: list[str], target_format: str) -> tuple[bool, list[str] | str]:
        output_dir = SettingsLogic.get_output_dir()
        if not output_dir:
            return False, SettingsLogic.tr('lbl_status_select_dir')
        Path(output_dir).mkdir(parents=True, exist_ok=True)
        target_upper = target_format.upper()
        save_format = FORMAT_MAP_FOR_SAVE.get(target_upper, target_upper)
        if save_format == 'SVG':
            return False, 'SVG output is not supported.'
        Image.init()
        if save_format not in Image.SAVE:
            return False, f'{target_upper} is not supported by Pillow.'
        results = []
        for file_path in file_paths:
            try:
                with Image.open(file_path) as image:
                    final_image = image.convert('RGB') if save_format == 'JPEG' and image.mode in ('RGBA', 'P') else image
                    params = {'quality': 95} if save_format in {'JPEG', 'WEBP', 'AVIF', 'HEIF'} else {}
                    save_path = ImageConvertLogic.output_path(file_path, target_upper)
                    final_image.save(save_path, save_format, **params)
                    results.append(str(save_path))
            except Exception:
                continue
        if not results:
            return False, 'No files were converted.'
        SettingsLogic.set_last_format(target_upper)
        return True, results
