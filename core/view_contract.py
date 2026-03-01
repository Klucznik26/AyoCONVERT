from typing import Callable, Protocol


class MainViewContract(Protocol):
    """Kontrakt widoku wymagany przez kontroler logiki aplikacji."""

    def bind_on_files_dropped(self, handler: Callable[[list[str]], None]) -> None:
        ...

    def bind_on_dir_selected(self, handler: Callable[[str], None]) -> None:
        ...

    def bind_on_conversion_requested(self, handler: Callable[[str], None]) -> None:
        ...

    def show_preview(self, file_path: str) -> None:
        ...

    def update_fan(self, file_paths: list[str]) -> None:
        ...

    def update_save_dir_tooltip(self, path: str) -> None:
        ...

    def set_status_message(self, key_msg: str) -> None:
        ...

    def set_run_enabled(self, enabled: bool) -> None:
        ...

    def show_success_message(self) -> None:
        ...

    def reset_after_conversion(self) -> None:
        ...

    def update_format_availability(self, source_ext: str) -> None:
        ...
