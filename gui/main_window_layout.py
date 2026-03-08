from pathlib import Path

from PySide6.QtCore import Qt, QSize
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import (
    QComboBox,
    QFrame,
    QLabel,
    QListView,
    QMenu,
    QPushButton,
    QSpacerItem,
    QSizePolicy,
    QGridLayout,
    QHBoxLayout,
    QVBoxLayout,
)

from .drop_area import DropArea
from .image_fan import ImageFan
from core.app_config import get_available_target_formats


def build_ui_panels(window, main_layout, add_shadow):
    _build_narrow_panel(window, main_layout, add_shadow)
    _build_sidebar_panel(window, add_shadow)
    _build_workspace_panel(window, add_shadow)

    main_layout.addWidget(window.panel_narrow)
    main_layout.addWidget(window.panel_sidebar)
    main_layout.addWidget(window.panel_workspace)


def _build_narrow_panel(window, main_layout, add_shadow):
    window.panel_narrow = QFrame()
    window.panel_narrow.setObjectName("narrowPanel")
    window.panel_narrow.setFixedWidth(60)
    add_shadow(window.panel_narrow)

    layout_narrow = QVBoxLayout(window.panel_narrow)
    layout_narrow.setContentsMargins(0, 20, 0, 20)
    layout_narrow.setSpacing(20)

    window.btn_narrow_logo = QPushButton()
    window.btn_narrow_logo.setObjectName("iconButton")

    logo_path = Path(__file__).resolve().parent.parent / "assets" / "ACONVERT.png"
    if logo_path.exists():
        window.btn_narrow_logo.setIcon(QIcon(str(logo_path)))
        window.btn_narrow_logo.setIconSize(QSize(39, 39))
    else:
        window.btn_narrow_logo.setText("A")
        window.btn_narrow_logo.setStyleSheet("color: #e0af68; font-weight: bold; font-size: 24px; border: none;")
    window.btn_narrow_logo.setCursor(Qt.PointingHandCursor)
    window.btn_narrow_logo.setToolTip(window.translator.get("btn_info", "Info"))
    window.btn_narrow_logo.clicked.connect(window.show_info_window)

    spacer_narrow = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

    btn_lang = QPushButton("🌐\uFE0E")
    btn_lang.setObjectName("iconButton")
    btn_lang.setCursor(Qt.PointingHandCursor)
    btn_lang.setToolTip(window.translator.get("lbl_lang"))
    btn_lang.clicked.connect(window.show_language_window)

    btn_theme = QPushButton("⚙")
    btn_theme.setObjectName("iconButton")
    btn_theme.setCursor(Qt.PointingHandCursor)
    btn_theme.setToolTip("Motyw / Theme")
    btn_theme.clicked.connect(window.show_theme_window)

    btn_close = QPushButton("⏻")
    btn_close.setObjectName("iconButton")
    btn_close.setProperty("danger", True)
    btn_close.setCursor(Qt.PointingHandCursor)
    btn_close.setToolTip(window.translator.get("btn_close"))
    btn_close.clicked.connect(window.close)

    layout_narrow.addWidget(window.btn_narrow_logo, 0, Qt.AlignCenter)
    layout_narrow.addItem(spacer_narrow)
    layout_narrow.addWidget(btn_lang, 0, Qt.AlignCenter)
    layout_narrow.addWidget(btn_theme, 0, Qt.AlignCenter)
    layout_narrow.addWidget(btn_close, 0, Qt.AlignCenter)

    unified_font = btn_lang.font()
    if unified_font.pixelSize() > 0:
        unified_font.setPixelSize(unified_font.pixelSize())
    else:
        unified_font.setPointSize(24)
    for btn in (btn_lang, btn_theme, btn_close):
        btn.setFont(unified_font)
        btn.setFixedSize(44, 44)

    close_font = btn_close.font()
    base_px = unified_font.pixelSize()
    if base_px > 0:
        close_font.setPixelSize(int(round(base_px * 1.3)))
    else:
        close_font.setPointSize(int(round(unified_font.pointSizeF() * 1.3)))
    btn_close.setFont(close_font)

    return


def _build_sidebar_panel(window, add_shadow):
    window.panel_sidebar = QFrame()
    window.panel_sidebar.setObjectName("leftPanel")
    window.panel_sidebar.setFixedWidth(200)
    add_shadow(window.panel_sidebar)

    layout_sidebar = QVBoxLayout(window.panel_sidebar)
    layout_sidebar.setContentsMargins(15, 20, 15, 20)
    layout_sidebar.setSpacing(10)

    window.btn_open = QPushButton(window.translator.get("btn_select_source", "Wybierz źródło"))
    window.btn_open.setObjectName("runButton")
    window.btn_open.setMinimumHeight(40)

    window.menu_source = QMenu(window)
    window.action_open_file = window.menu_source.addAction(window.translator.get("btn_open", "Otwórz plik"))
    window.action_open_dir = window.menu_source.addAction(window.translator.get("btn_open_dir", "Otwórz katalog"))
    window.btn_open.setMenu(window.menu_source)

    window.action_open_file.triggered.connect(window.open_file_dialog)
    window.action_open_dir.triggered.connect(window.open_source_directory)

    window.btn_save_dir = QPushButton(window.translator.get("btn_save_dir", "Katalog zapisu"))
    window.btn_save_dir.setMinimumHeight(40)
    window.btn_save_dir.clicked.connect(window.select_save_directory)

    window.format_choice = QComboBox()
    window.format_choice.addItems(get_available_target_formats())
    window.format_choice.setMinimumHeight(35)
    window.lbl_target_format = QLabel("Format docelowy")
    window.lbl_target_format.setStyleSheet("")

    window.btn_run = window.progress_button_cls(window.translator.get("btn_run", "Wykonaj"))
    window.btn_run.setObjectName("runButton")
    window.btn_run.setMinimumHeight(80)
    window.btn_run.clicked.connect(window.start_conversion)
    window.btn_run.setEnabled(False)

    window.file_list = QListView()
    window.file_list_model = window.string_list_model_cls(window)
    window.file_list.setModel(window.file_list_model)
    window.file_list.setVisible(False)
    window.lbl_files = QLabel("Pliki:")
    window.lbl_files.setVisible(False)

    window.lbl_status = QLabel("")
    window.lbl_status.setStyleSheet("")
    window.lbl_status.setWordWrap(True)

    layout_sidebar.addWidget(window.btn_open)
    layout_sidebar.addWidget(window.lbl_status)
    layout_sidebar.addWidget(window.btn_save_dir)
    layout_sidebar.addWidget(window.lbl_files)
    layout_sidebar.addWidget(window.file_list)
    layout_sidebar.addStretch(1)
    layout_sidebar.addWidget(window.lbl_target_format)
    layout_sidebar.addWidget(window.format_choice)
    layout_sidebar.addWidget(window.btn_run)


def _build_workspace_panel(window, add_shadow):
    window.panel_workspace = QFrame()
    window.panel_workspace.setObjectName("rightPanel")
    window.panel_workspace.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
    add_shadow(window.panel_workspace)

    layout_workspace = QGridLayout(window.panel_workspace)
    layout_workspace.setContentsMargins(10, 10, 10, 10)

    layout_workspace.setColumnStretch(0, 1)
    layout_workspace.setColumnStretch(2, 6)
    layout_workspace.setColumnMinimumWidth(2, 220)
    layout_workspace.setRowStretch(0, 1)
    layout_workspace.setRowStretch(1, 1)

    window.drop_area = DropArea()
    window.drop_area.setObjectName("dropArea")
    window.drop_area.setFixedWidth(480)
    window.drop_area.setText(window.translator.get("lbl_drop"))
    window.drop_area.files_dropped.connect(window.handle_files)

    window.image_fan = ImageFan(window.translator)

    window.mini_logo = QLabel()
    window.load_logo()

    layout_workspace.addWidget(window.drop_area, 0, 1, 2, 1, Qt.AlignRight)
    layout_workspace.addWidget(window.image_fan, 0, 2, Qt.AlignTop | Qt.AlignRight)
    layout_workspace.addWidget(window.mini_logo, 1, 2, Qt.AlignBottom | Qt.AlignRight)
