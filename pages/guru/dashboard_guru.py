import customtkinter as ctk
from tkinter import messagebox

from pages.guru.nilai_page import NilaiPage
from pages.guru.kehadiran_page import KehadiranPage
from pages.guru.motivasi_page import MotivasiPage
from pages.guru.disiplin_page import DisiplinPage
from pages.guru.prediksi_page import PrediksiPage
from pages.guru.hasil_page import HasilPage


class DashboardGuru(ctk.CTk):

    def __init__(self):
        super().__init__()

        self.title("Dashboard Guru - SDN Klegen")
        self.geometry("1200x700")
        self.resizable(True, True)

        # ==========================
        # BAGIAN GANTI IKON APLIKASI
        # ==========================
        try:
            # Mengganti ikon window (.ico disarankan untuk Windows)
            self.iconbitmap("assets/app_icon.ico")
        except Exception as e:
            print(f"Gagal memuat ikon aplikasi (.ico): {e}")

        # Mengatur konfigurasi tema visual global (Tema Gelap Premium)
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")
        self.configure(fg_color="#0F172A") # Latar belakang Slate Dark Premium

        # =========================
        # SIDEBAR (NAVIGASI KIRI)
        # =========================

        self.sidebar = ctk.CTkFrame(
            self,
            width=240,
            corner_radius=0,
            fg_color="#1E293B", # Latar sidebar sedikit lebih terang dari background utama
            border_width=0
        )
        self.sidebar.pack(
            side="left",
            fill="y"
        )
        self.sidebar.pack_propagate(False) # Mengunci lebar sidebar tetap 240px

        # Header Sidebar
        ctk.CTkLabel(
            self.sidebar,
            text="👩‍🏫 PANEL GURU",
            font=("Segoe UI", 20, "bold"),
            text_color="#60A5FA"
        ).pack(pady=(30, 25))

        # =========================
        # TOMBOL NAVIGASI MENU
        # =========================

        ctk.CTkButton(
            self.sidebar,
            text="Dashboard Utama",
            width=200,
            height=40,
            corner_radius=8,
            font=("Segoe UI", 12, "bold"),
            command=self.show_dashboard
        ).pack(pady=6)

        ctk.CTkButton(
            self.sidebar,
            text="Data Nilai",
            width=200,
            height=40,
            corner_radius=8,
            font=("Segoe UI", 12, "bold"),
            command=self.buka_nilai
        ).pack(pady=6)

        ctk.CTkButton(
            self.sidebar,
            text="Data Kehadiran",
            width=200,
            height=40,
            corner_radius=8,
            font=("Segoe UI", 12, "bold"),
            command=self.buka_kehadiran
        ).pack(pady=6)

        ctk.CTkButton(
            self.sidebar,
            text="Data Motivasi",
            width=200,
            height=40,
            corner_radius=8,
            font=("Segoe UI", 12, "bold"),
            command=self.buka_motivasi
        ).pack(pady=6)

        ctk.CTkButton(
            self.sidebar,
            text="Data Disiplin",
            width=200,
            height=40,
            corner_radius=8,
            font=("Segoe UI", 12, "bold"),
            command=self.buka_disiplin
        ).pack(pady=6)

        ctk.CTkButton(
            self.sidebar,
            text="Prediksi Prestasi",
            width=200,
            height=40,
            corner_radius=8,
            font=("Segoe UI", 12, "bold"),
            command=self.buka_prediksi
        ).pack(pady=6)

        ctk.CTkButton(
            self.sidebar,
            text="Hasil Prediksi",
            width=200,
            height=40,
            corner_radius=8,
            font=("Segoe UI", 12, "bold"),
            command=self.buka_hasil
        ).pack(pady=6)

        # Tombol Logout (Ditempatkan di bagian paling bawah sidebar)
        ctk.CTkButton(
            self.sidebar,
            text="Logout",
            width=200,
            height=38,
            corner_radius=8,
            font=("Segoe UI", 12, "bold"),
            fg_color="#EF4444",
            hover_color="#DC2626",
            command=self.logout
        ).pack(
            side="bottom",
            pady=30
        )

        # =========================
        # CONTENT AREA (KANAN)
        # =========================

        self.content = ctk.CTkFrame(self, fg_color="transparent")
        self.content.pack(
            side="right",
            fill="both",
            expand=True,
            padx=30,
            pady=30
        )

        # Menampilkan dashboard pertama kali saat dijalankan
        self.show_dashboard()

    # ===================================
    # ELEMEN HALAMAN DASHBOARD
    # ===================================

    def show_dashboard(self):

        self.clear_content()

        # Judul Utama Dashboard
        ctk.CTkLabel(
            self.content,
            text="DASHBOARD AKADEMIK GURU",
            font=("Segoe UI", 26, "bold"),
            text_color="#F8FAFC"
        ).pack(anchor="w", pady=(10, 5))
        
        # Sub-judul teks ucapan selamat datang (Diposisikan di atas agar hirarki visual rapi)
        ctk.CTkLabel(
            self.content,
            text="Selamat Datang, Bapak/Ibu Guru SDN Klegen.",
            font=("Segoe UI", 13),
            text_color="#94A3B8"
        ).pack(anchor="w", pady=(0, 25))

        # Card Container (Wadah horizontal untuk menampung kotak statistik)
        card_frame = ctk.CTkFrame(self.content, fg_color="transparent")
        card_frame.pack(fill="x", pady=10)

        # --- CARD 1: DATA NILAI ---
        card_nilai = ctk.CTkFrame(card_frame, width=240, height=130, fg_color="#1E293B", corner_radius=12, border_width=1, border_color="#334155")
        card_nilai.pack(side="left", padx=(0, 20))
        card_nilai.pack_propagate(False)

        ctk.CTkLabel(card_nilai, text="📊 Data Nilai", font=("Segoe UI", 14), text_color="#94A3B8").pack(anchor="w", padx=20, pady=(20, 5))
        ctk.CTkLabel(card_nilai, text="0", font=("Segoe UI", 32, "bold"), text_color="#60A5FA").pack(anchor="w", padx=20)

        # --- CARD 2: KEHADIRAN ---
        card_hadir = ctk.CTkFrame(card_frame, width=240, height=130, fg_color="#1E293B", corner_radius=12, border_width=1, border_color="#334155")
        card_hadir.pack(side="left", padx=20)
        card_hadir.pack_propagate(False)

        ctk.CTkLabel(card_hadir, text="📅 Kehadiran", font=("Segoe UI", 14), text_color="#94A3B8").pack(anchor="w", padx=20, pady=(20, 5))
        ctk.CTkLabel(card_hadir, text="0", font=("Segoe UI", 32, "bold"), text_color="#10B981").pack(anchor="w", padx=20)

        # --- CARD 3: PREDIKSI ---
        card_prediksi = ctk.CTkFrame(card_frame, width=240, height=130, fg_color="#1E293B", corner_radius=12, border_width=1, border_color="#334155")
        card_prediksi.pack(side="left", padx=20)
        card_prediksi.pack_propagate(False)

        ctk.CTkLabel(card_prediksi, text="🔮 Prediksi", font=("Segoe UI", 14), text_color="#94A3B8").pack(anchor="w", padx=20, pady=(20, 5))
        ctk.CTkLabel(card_prediksi, text="0", font=("Segoe UI", 32, "bold"), text_color="#F59E0B").pack(anchor="w", padx=20)

    # ===================================
    # CLEAR CONTENT UTILITY
    # ===================================

    def clear_content(self):
        for widget in self.content.winfo_children():
            widget.destroy()

    # ===================================
    # SISTEM NAVIGASI SUB-PAGES
    # ===================================

    def buka_nilai(self):
        self.clear_content()
        page = NilaiPage(self.content)
        page.pack(fill="both", expand=True)

    def buka_kehadiran(self):
        self.clear_content()
        page = KehadiranPage(self.content)
        page.pack(fill="both", expand=True)

    def buka_motivasi(self):
        self.clear_content()
        page = MotivasiPage(self.content)
        page.pack(fill="both", expand=True)

    def buka_disiplin(self):
        self.clear_content()
        page = DisiplinPage(self.content)
        page.pack(fill="both", expand=True)

    def buka_prediksi(self):
        self.clear_content()
        page = PrediksiPage(self.content)
        page.pack(fill="both", expand=True)

    def buka_hasil(self):
        self.clear_content()
        page = HasilPage(self.content)
        page.pack(fill="both", expand=True)

    # ===================================
    # PROSES LOGOUT
    # ===================================

    def logout(self):
        konfirmasi = messagebox.askyesno(
            "Konfirmasi Keluar",
            "Apakah Anda yakin ingin keluar dari sistem?"
        )

        if konfirmasi:
            self.destroy()
            from pages.login_page import LoginPage
            app = LoginPage()
            app.mainloop()