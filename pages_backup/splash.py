import customtkinter as ctk
from PIL import Image
import time


class SplashScreen(ctk.CTk):

    def __init__(self):
        super().__init__()

        self.title("")
        self.geometry("500x400")
        self.resizable(False, False)
        
        # Hilangkan title bar
        self.overrideredirect(True)
        
        # Center di tengah layar
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        x = (screen_width - 500) // 2
        y = (screen_height - 400) // 2
        self.geometry(f"500x400+{x}+{y}")

        # Set transparansi awal (0 = transparan, 1 = solid)
        self.attributes('-alpha', 0.0)

        # ==========================
        # BAGIAN GANTI IKON APLIKASI
        # ==========================
        try:
            self.iconbitmap("assets/app_icon.ico")
        except Exception as e:
            print(f"Gagal memuat ikon aplikasi (.ico): {e}")

        # Mengatur tema
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")
        self.configure(fg_color="#0F172A")

        # ==========================
        # MAIN FRAME
        # ==========================

        main_frame = ctk.CTkFrame(
            self,
            fg_color="#1E293B",
            corner_radius=24,
            border_width=1,
            border_color="#334155"
        )
        main_frame.pack(expand=True, fill="both", padx=30, pady=30)

        # ==========================
        # LOGO
        # ==========================

        # Logo
        try:
            logo_image = ctk.CTkImage(
                light_image=Image.open("assets/logo.png"),
                dark_image=Image.open("assets/logo.png"),
                size=(120, 110)
            )
            logo_label = ctk.CTkLabel(main_frame, image=logo_image, text="")
            logo_label.pack(pady=(30, 10))
        except Exception as e:
            print(f"Gagal memuat logo: {e}")
            ctk.CTkLabel(
                main_frame,
                text="🏫",
                font=("Segoe UI", 60)
            ).pack(pady=(30, 10))

        # Nama Sekolah
        ctk.CTkLabel(
            main_frame,
            text="SDN KLEGEN",
            font=("Segoe UI", 32, "bold"),
            text_color="#60A5FA"
        ).pack(pady=(0, 5))

        # Sub Judul
        ctk.CTkLabel(
            main_frame,
            text="Sistem Prediksi Prestasi Siswa",
            font=("Segoe UI", 14),
            text_color="#94A3B8"
        ).pack(pady=(0, 20))

        # Garis dekoratif
        ctk.CTkFrame(
            main_frame,
            fg_color="#60A5FA",
            height=2,
            width=80
        ).pack(pady=(0, 20))

        # ==========================
        # PROGRESS BAR
        # ==========================

        self.progress = ctk.CTkProgressBar(
            main_frame,
            width=300,
            height=8,
            corner_radius=4,
            fg_color="#334155",
            progress_color="#60A5FA"
        )
        self.progress.pack(pady=(10, 10))
        self.progress.set(0)

        # Loading Text
        self.loading_text = ctk.CTkLabel(
            main_frame,
            text="Memuat sistem...",
            font=("Segoe UI", 11),
            text_color="#64748B"
        )
        self.loading_text.pack(pady=(0, 10))

        # Versi
        ctk.CTkLabel(
            main_frame,
            text="v1.0",
            font=("Segoe UI", 10),
            text_color="#475569"
        ).pack(side="bottom", pady=15)

        # ==========================
        # PROSES LOADING
        # ==========================

        # Fade in effect
        self.fade_in()

    def fade_in(self):
        """Efek fade in pada splash screen"""
        alpha = 0.0
        while alpha < 1.0:
            alpha += 0.05
            self.attributes('-alpha', alpha)
            self.update()
            time.sleep(0.02)
        
        # Mulai loading setelah fade in selesai
        self.loading()

    def loading(self):
        """Simulasi loading dengan progress bar"""
        
        steps = [
            (0.2, "Memuat sistem..."),
            (0.4, "Menyambungkan database..."),
            (0.6, "Memuat modul..."),
            (0.8, "Menverifikasi pengguna..."),
            (1.0, "Siap!")
        ]

        for progress, text in steps:
            self.progress.set(progress)
            self.loading_text.configure(text=text)
            self.update()
            time.sleep(0.5)

        # Fade out effect
        self.fade_out()

    def fade_out(self):
        """Efek fade out sebelum pindah ke LoginPage"""
        alpha = 1.0
        while alpha > 0.0:
            alpha -= 0.05
            self.attributes('-alpha', alpha)
            self.update()
            time.sleep(0.02)

        self.destroy()
        from pages.login_page import LoginPage
        app = LoginPage()
        app.mainloop()
