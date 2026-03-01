"""
Motyw Relaksacyjny (Sage & Green)
"""

_MAIN_STYLE = """
/* =========================
   MOTYW RELAKSACYJNY
   ========================= */

QMainWindow {
    background-color: #a3b18a;
}

QDialog {
    background-color: #a3b18a;
}

/* =========================
   RAMKI / PANELE
   ========================= */
QFrame {
    background-color: #dad7cd;
    border: 1px solid #588157;
}

/* =========================
   TEKST
   ========================= */
QLabel {
    color: #344e41;
}

QLabel[secondary="true"] {
    color: #588157;
}

QLabel#scaleLabel {
    color: #344e41;
}

QLabel#statusLabel {
    color: #000000;
    font-weight: bold;
    font-size: 13px;
}

/* =========================
   PRZYCISKI
   ========================= */
QPushButton {
    padding: 8px 14px;
    background-color: #dad7cd;
    border: 1px solid #588157;
    border-radius: 6px;
    color: #344e41;
    font-weight: bold;
}

QPushButton:hover {
    background-color: #e8e6df;
}

QPushButton:pressed {
    background-color: #c4c1b7;
}

QPushButton:disabled {
    background-color: #b5bca5;
    color: #7a8c7f;
    border: 1px solid #8fa38e;
}

/* =========================
   PRZYCISK WYKONAJ (AKCENT)
   ========================= */
QPushButton#runButton {
    background-color: #588157;
    border: none;
    color: #dad7cd;
}

QPushButton#runButton:hover {
    background-color: #6a9669;
}

QPushButton#runButton:pressed {
    background-color: #466845;
}

/* =========================
   SUWAK SKALI
   ========================= */
QSlider::groove:horizontal {
    height: 6px;
    background: #dad7cd;
    border-radius: 3px;
}

QSlider::handle:horizontal {
    background: #588157;
    width: 16px;
    margin: -5px 0;
    border-radius: 8px;
}

QSlider::sub-page:horizontal {
    background: #344e41;
    border-radius: 3px;
}

QSlider::add-page:horizontal {
    background: #dad7cd;
    border-radius: 3px;
}

/* =========================
   KONTROLKI FORMULARZY
   ========================= */
QComboBox {
    background-color: #dad7cd;
    color: #344e41;
    border: 1px solid #588157;
    padding: 4px;
}

QComboBox::drop-down {
    border: none;
}

QListView, QTreeView {
    background-color: #dad7cd;
    color: #344e41;
    border: 1px solid #588157;
}
"""

_DROP_ZONE_STYLE = """
    QLabel#dropArea {
        background-color: #dad7cd;
        border: 2px dashed #588157;
        border-radius: 10px;
        color: #344e41;
        font-size: 18px;
    }
"""

STYLESHEET = _MAIN_STYLE + "\n" + _DROP_ZONE_STYLE