def get_style(theme_name="Systemowy"):
    # Definicje palet kolorystycznych Ayo
    palettes = {
        "Systemowy": { # Głęboki granat/tokyonight
            "bg": "#1a1b26", "widget": "#24283b", "text": "#e0af68", 
            "border": "#414868", "drag": "#1f2335"
        },
        "Jasny": { # Ciepła sepia
            "bg": "#e4d6c6",   
            "widget": "#e8dfd2", 
            "text": "#8c6a48",   
            "border": "#c0b0a0", 
            "drag": "#e8dfd2"    
        },
        "Ciemny": { # Czekoladowy brąz
            "bg": "#2b2621", "widget": "#3d352e", "text": "#e0af68", 
            "border": "#4d443c", "drag": "#3d352e"
        }
    }

    p = palettes.get(theme_name, palettes["Systemowy"])

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
            border-radius: 4px; 
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
            border-radius: 4px; 
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