from database.koneksi_sqlite import init_db
from pages.splash import SplashScreen
import sys
import os

if __name__ == "__main__":
    # Untuk PyInstaller, set base path
    if getattr(sys, 'frozen', False):
        os.chdir(os.path.dirname(sys.executable))
    
    # Inisialisasi database (auto-create)
    init_db()
    
    # Jalankan splash screen
    app = SplashScreen()
    app.mainloop()