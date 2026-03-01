from . import creative
from . import dark
from . import light
from . import relax

def get_style(theme_name):
    """Zwraca arkusz stylów CSS dla wybranego motywu."""
    
    # Mapowanie starych nazw na nowe kody (dla wstecznej kompatybilności)
    if theme_name == "Kreatywny": theme_name = "creative"
    elif theme_name == "Ciemny": theme_name = "dark"
    elif theme_name == "Jasny": theme_name = "light"
    elif theme_name == "Relaksacyjny": theme_name = "relax"
    elif theme_name == "Systemowy": theme_name = "system"
    
    if theme_name == "creative":
        return creative.STYLESHEET
        
    elif theme_name == "dark":
        return dark.STYLESHEET
        
    elif theme_name == "light":
        return light.STYLESHEET
        
    elif theme_name == "relax":
        return relax.STYLESHEET
        
    # Domyślny / Systemowy
    return ""
