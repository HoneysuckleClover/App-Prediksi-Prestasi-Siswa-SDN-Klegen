import sys
import os
from pathlib import Path

def resource_path(relative_path):
    """Mendapatkan path absolut untuk file, baik saat running sebagai .py atau .exe"""
    try:
        # PyInstaller membuat folder temp dan menyimpan path di _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        # Jika running sebagai script biasa
        base_path = os.path.abspath(".")
    
    return os.path.join(base_path, relative_path)

def get_model_path():
    """Mendapatkan path untuk model dengan fallback"""
    # Coba beberapa kemungkinan path
    possible_paths = [
        resource_path("models/model_logistic.pkl"),  # Path dari PyInstaller
        os.path.join(os.path.dirname(sys.executable), "models", "model_logistic.pkl") if getattr(sys, 'frozen', False) else None,  # Path di folder .exe
        "models/model_logistic.pkl",  # Path lokal
        os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "models", "model_logistic.pkl"),  # Path relatif dari helpers
    ]
    
    for path in possible_paths:
        if path and os.path.exists(path):
            print(f"✅ Model ditemukan di: {path}")
            return path
    
    # Jika tidak ditemukan, return default
    print("❌ Model tidak ditemukan di semua path!")
    return resource_path("models/model_logistic.pkl")

def get_asset_path(filename):
    """Mendapatkan path untuk file di folder assets"""
    return resource_path(os.path.join("assets", filename))

def get_icon_path():
    """Mendapatkan path untuk icon aplikasi"""
    return resource_path("assets/app_icon.ico")