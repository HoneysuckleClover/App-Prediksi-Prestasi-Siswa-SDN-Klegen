import customtkinter as ctk
from tkinter import messagebox

from pages.admin.siswa_page import SiswaPage
from pages.admin.kelas_page import KelasPage
from pages.admin.user_page import UserPage


class DashboardAdmin(ctk.CTk):

    def __init__(self):
        super().__init__()

        self.title("Dashboard Admin - SDN Klegen")
        self.geometry("1200x700")
        self.resizable(True, True) # Mengizinkan resize agar tampilan fleksibel

        # ==========================
        # BAGIAN GANTI IKON APLIKASI
        # ==========================
        try:
            # Mengganti ikon window (.ico disarankan untuk Windows)
            self.iconbitmap("assets/app_icon.ico")
        except Exception as e:
            print(f"Gagal memuat ikon aplikasi (.ico): {e}")

        # Mengatur konfigurasi tema visual global
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
            text="👨‍💼 ADMIN PANEL",
            font=("Segoe UI", 20, "bold"),
            text_color="#60A5FA"
        ).pack(pady=(30, 30))

        # Tombol Navigasi: Dashboard
        self.btn_dashboard = ctk.CTkButton(
            self.sidebar,
            text="Dashboard Utama",
            width=200,
            height=40,
            corner_radius=8,
            font=("Segoe UI", 12, "bold"),
            command=self.show_dashboard
        )
        self.btn_dashboard.pack(pady=8)

        # Tombol Navigasi: Data Siswa
        self.btn_siswa = ctk.CTkButton(
            self.sidebar,
            text="Data Siswa",
            width=200,
            height=40,
            corner_radius=8,
            font=("Segoe UI", 12, "bold"),
            command=self.buka_siswa
        )
        self.btn_siswa.pack(pady=8)

        # Tombol Navigasi: Data Kelas
        self.btn_kelas = ctk.CTkButton(
            self.sidebar,
            text="Data Kelas",
            width=200,
            height=40,
            corner_radius=8,
            font=("Segoe UI", 12, "bold"),
            command=self.buka_kelas
        )
        self.btn_kelas.pack(pady=8)

        # Tombol Navigasi: Kelola User
        self.btn_user = ctk.CTkButton(
            self.sidebar,
            text="Kelola Akun User",
            width=200,
            height=40,
            corner_radius=8,
            font=("Segoe UI", 12, "bold"),
            command=self.buka_user
        )
        self.btn_user.pack(pady=8)

        # Tombol Navigasi: Logout (Ditempatkan di bagian paling bawah sidebar)
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

        # Wadah kontainer utama halaman konten
        self.content = ctk.CTkFrame(self, fg_color="transparent")
        self.content.pack(
            side="right",
            fill="both",
            expand=True,
            padx=30,
            pady=30
        )

        # Menampilkan halaman dashboard utama saat aplikasi pertama dibuka
        self.show_dashboard()

    # =========================
    # ELEMEN HALAMAN DASHBOARD
    # =========================

    def show_dashboard(self):

        self.clear_content()

        # Judul Utama Dashboard
        ctk.CTkLabel(
            self.content,
            text="DASHBOARD ANALISIS ADMIN",
            font=("Segoe UI", 26, "bold"),
            text_color="#F8FAFC"
        ).pack(anchor="w", pady=(10, 5))
        
        # Sub-judul teks ucapan selamat datang (Diposisikan di atas agar hirarki visual rapi)
        ctk.CTkLabel(
            self.content,
            text="Selamat Datang Kembali, Administrator.",
            font=("Segoe UI", 13),
            text_color="#94A3B8"
        ).pack(anchor="w", pady=(0, 25))

        # Card Container (Wadah horizontal untuk menampung kotak statistik)
        card_frame = ctk.CTkFrame(self.content, fg_color="transparent")
        card_frame.pack(fill="x", pady=10)

        # --- CARD 1: DATA SISWA ---
        card_siswa = ctk.CTkFrame(card_frame, width=240, height=130, fg_color="#1E293B", corner_radius=12, border_width=1, border_color="#334155")
        card_siswa.pack(side="left", padx=(0, 20))
        card_siswa.pack_propagate(False)

        ctk.CTkLabel(card_siswa, text="👥 Total Siswa", font=("Segoe UI", 14), text_color="#94A3B8").pack(anchor="w", padx=20, pady=(20, 5))
        ctk.CTkLabel(card_siswa, text="0", font=("Segoe UI", 32, "bold"), text_color="#60A5FA").pack(anchor="w", padx=20)

        # --- CARD 2: DATA GURU ---
        card_guru = ctk.CTkFrame(card_frame, width=240, height=130, fg_color="#1E293B", corner_radius=12, border_width=1, border_color="#334155")
        card_guru.pack(side="left", padx=20)
        card_guru.pack_propagate(False)

        ctk.CTkLabel(card_guru, text="👨‍🏫 Total Guru", font=("Segoe UI", 14), text_color="#94A3B8").pack(anchor="w", padx=20, pady=(20, 5))
        ctk.CTkLabel(card_guru, text="0", font=("Segoe UI", 32, "bold"), text_color="#10B981").pack(anchor="w", padx=20)

        # --- CARD 3: DATA PREDIKSI ---
        card_prediksi = ctk.CTkFrame(card_frame, width=240, height=130, fg_color="#1E293B", corner_radius=12, border_width=1, border_color="#334155")
        card_prediksi.pack(side="left", padx=20)
        card_prediksi.pack_propagate(False)

        ctk.CTkLabel(card_prediksi, text="📈 Total Prediksi", font=("Segoe UI", 14), text_color="#94A3B8").pack(anchor="w", padx=20, pady=(20, 5))
        ctk.CTkLabel(card_prediksi, text="0", font=("Segoe UI", 32, "bold"), text_color="#F59E0B").pack(anchor="w", padx=20)

    # =========================
    # SISTEM NAVIGASI SUB-PAGES
    # =========================

    def buka_siswa(self):
        self.clear_content()
        page = SiswaPage(self.content)
        page.pack(fill="both", expand=True)

    def buka_kelas(self):
        self.clear_content()
        page = KelasPage(self.content)
        page.pack(fill="both", expand=True)

    def buka_user(self):
        self.clear_content()
        page = UserPage(self.content)
        page.pack(fill="both", expand=True)

    # =========================
    # CLEAR CONTENT UTILITY
    # =========================

    def clear_content(self):
        for widget in self.content.winfo_children():
            widget.destroy()

    # =========================
    # PROSES LOGOUT
    # =========================

    def logout(self):
        konfirmasi = messagebox.askyesno(
            "Konfirmasi Keluar",
            "Apakah Anda yakin ingin keluar dari sistem?"
        )

        if konfirmasi:
            self.destroy()
            
            # Memanggil ulang halaman login saat logout sukses dilakukan
            from pages.login_page import LoginPage
            app = LoginPage()
            app.mainloop()