import json
from pathlib import Path

def get_style(theme_name="Systemowy"):
    # Mapowanie nazw motywów na pliki JSON
    theme_files = {
        "Systemowy": "system.json",
        "Jasny": "light.json",
        "Ciemny": "dark.json",
        "Relaksacyjny": "relax.json"
    }

    # Domyślna paleta (fallback - Systemowy)
    p = {
        "bg": "#1a1b26", "widget": "#24283b", "text": "#e0af68", 
        "border": "#414868", "drag": "#1f2335"
    }

    # Ładowanie z pliku
    theme_filename = theme_files.get(theme_name, "system.json")
    theme_path = Path(__file__).resolve().parent.parent / "themes" / theme_filename

    if theme_path.exists():
        try:
            with open(theme_path, "r", encoding="utf-8") as f:
                p = json.load(f)
        except Exception as e:
            print(f"[Style] Błąd ładowania motywu {theme_name}: {e}")

    # Dynamiczne zaokrąglenie: średnie (12px) dla Relaksacyjnego, Jasnego i Systemowego, małe (4px) dla reszty
    radius = "12px" if theme_name in ["Relaksacyjny", "Jasny", "Systemowy"] else "4px"

    return f"""
        /* Główne okna */
        QMainWindow, QDialog {{ 
            background-color: {p['bg']}; 
        }}
        
        /* Etykiety tekstowe */
        QLabel {{ 
            color: {p['text']}; 
            font-family: 'Segoe UI', sans-serif; 
            font-size: 13px; 
        }}
        
        /* Przyciski standardowe */
        QPushButton {{ 
            background-color: {p['widget']}; 
            color: {p['text']}; 
            border: 1px solid {p['border']}; 
            border-radius: {radius}; 
            padding: 10px; 
        }}
        QPushButton:hover {{ 
            background-color: {p['border']}; 
        }}
        QPushButton:disabled {{
            opacity: 0.5;
            color: {p['border']};
        }}
        
        /* Specyficzny przycisk Wykonaj */
        #WykonajBtn {{ 
            border: 1px solid {p['text']}; 
            font-weight: bold; 
            font-size: 15px; 
        }}
        
        /* Listy wyboru (ComboBox) */
        QComboBox {{ 
            background-color: {p['widget']}; 
            color: {p['text']}; 
            border: 1px solid {p['border']}; 
            border-radius: {radius}; 
            padding: 5px; 
        }}
        
        /* Naprawa wyglądu listy rozwijanej ComboBox */
        QComboBox QAbstractItemView {{
            background-color: {p['widget']};
            color: {p['text']};
            selection-background-color: {p['border']};
            border: 1px solid {p['border']};
            outline: none;
        }}
        
        /* Menu rozwijane przycisków */
        QMenu {{
            background-color: {p['widget']};
            color: {p['text']};
            border: 1px solid {p['border']};
        }}
        QMenu::item {{
            padding: 5px 20px;
        }}
        QMenu::item:selected {{
            background-color: {p['border']};
        }}
        
        /* Pole Drag & Drop */
        #DragArea {{ 
            border: 1px dashed {p['border']}; 
            border-radius: 12px; 
            background-color: {p['drag']}; 
            color: {p['text']}; 
            font-size: 16px; 
        }}
        
        /* Style dla okna Info */
        QLabel#Section {{ 
            font-size: 15px; 
            font-weight: bold; 
            color: {p['text']}; 
        }}
        
        #SubSection {{ 
            color: {p['text']}; 
            font-size: 11px; 
            opacity: 0.7; 
        }}
        
        QLabel#Lang {{ 
            font-size: 11px; 
            font-style: italic; 
        }}
    """