import customtkinter as ctk
from tkinter import messagebox
from PIL import Image # Dibutuhkan untuk memproses gambar/logo

from database.koneksi import connect_db

from pages.register_page import RegisterPage
from pages.admin.dashboard_admin import DashboardAdmin
from pages.guru.dashboard_guru import DashboardGuru
from pages.kepsek.dashboard_kepsek import DashboardKepsek


class LoginPage(ctk.CTk):

    def __init__(self):
        super().__init__()

        self.title("Sistem Prediksi Prestasi Siswa - SDN Klegen")
        self.geometry("450x620") # Ukuran disesuaikan agar compact dan padat (tidak lowong)
        self.resizable(False, False)

        # ==========================
        # BAGIAN GANTI IKON APLIKASI
        # ==========================
        try:
            # Mengganti ikon window (.ico disarankan untuk Windows)
            self.iconbitmap("assets/app_icon.ico")
        except Exception as e:
            print(f"Gagal memuat ikon aplikasi (.ico): {e}")

        # Mengatur background utama window agar senada dengan frame interior
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")
        self.configure(fg_color="#111827") # Dark background ala aplikasi modern (Tailwind Gray 900)

        # Frame utama bertindak sebagai "Card Container"
        frame = ctk.CTkFrame(self, fg_color="#1F2937", corner_radius=20, border_width=1, border_color="#374151")
        frame.pack(expand=True, fill="both", padx=35, pady=35)

        # ==========================
        # BAGIAN LOGO & HEADER
        # ==========================
        try:
            # Load file logo dari folder assets
            logo_image = ctk.CTkImage(
                light_image=Image.open("assets/logo.png"),
                dark_image=Image.open("assets/logo.png"),
                size=(80, 75) # Dimensi square sempurna agar logo tidak gepeng
            )
            self.logo_label = ctk.CTkLabel(frame, image=logo_image, text="")
            self.logo_label.pack(pady=(30, 10))
        except Exception as e:
            print(f"Gagal memuat logo dari folder assets: {e}")

        # Judul Instansi Utama
        ctk.CTkLabel(
            frame,
            text="SDN KLEGEN",
            font=("Segoe UI", 26, "bold"),
            text_color="#60A5FA" # Biru modern konvensional
        ).pack(pady=(0, 2))

        # Deskripsi atau Sub-judul Aplikasi
        ctk.CTkLabel(
            frame,
            text="Sistem Prediksi Prestasi Siswa",
            font=("Segoe UI", 12),
            text_color="#9CA3AF" # Abu-abu soft agar tidak balapan dengan judul utama
        ).pack(pady=(0, 25))

        # ==========================
        # FIELD INPUT (USER & PASS)
        # ==========================
        
        # Input Username
        self.entry_username = ctk.CTkEntry(
            frame,
            width=280,
            height=44,
            corner_radius=10,
            border_width=1,
            border_color="#4B5563",
            fg_color="#1F2937",
            placeholder_text="Username",
            placeholder_text_color="#6B7280",
            font=("Segoe UI", 12)
        )
        self.entry_username.pack(pady=8)

        # Input Password
        self.entry_password = ctk.CTkEntry(
            frame,
            width=280,
            height=44,
            corner_radius=10,
            border_width=1,
            border_color="#4B5563",
            fg_color="#1F2937",
            placeholder_text="Password",
            placeholder_text_color="#6B7280",
            show="*",
            font=("Segoe UI", 12)
        )
        self.entry_password.pack(pady=8)

        # ==========================
        # TOMBOL AKSI (ACTION BUTTONS)
        # ==========================

        # Tombol Login Utama (Solid Blue Accent)
        ctk.CTkButton(
            frame,
            text="Masuk ke Akun",
            width=280,
            height=44,
            corner_radius=10,
            font=("Segoe UI", 13, "bold"),
            fg_color="#2563EB",
            hover_color="#1D4ED8",
            command=self.login
        ).pack(pady=(25, 15))

        # Pembatas Visual Garis Tipis (Divider)
        divider = ctk.CTkFrame(frame, height=1, width=200, fg_color="#374151")
        divider.pack(pady=10)

        # BAGIAN REGISTER BARU: Teks biasa & Link digabung satu baris horizontal
        register_container = ctk.CTkFrame(frame, fg_color="transparent")
        register_container.pack(pady=(10, 25))

        # 1. Teks Biasa (Kiri)
        label_tanya = ctk.CTkLabel(
            register_container,
            text="Belum punya akun? ",
            font=("Segoe UI", 12),
            text_color="#9CA3AF"
        )
        label_tanya.pack(side="left")

        # 2. Teks Link Aktif (Kanan)
        self.link_register = ctk.CTkLabel(
            register_container,
            text="Daftar Sekarang",
            font=("Segoe UI", 12, "underline"),
            text_color="#10B981", # Warna hijau emerald murni
            cursor="hand2"        # Mengubah kursor menjadi tangan menunjuk
        )
        self.link_register.pack(side="left")
        
        # Binding klik mouse pada link
        self.link_register.bind("<Button-1>", lambda event: self.buka_register())

    # ==========================
    # BUKA REGISTER
    # ==========================

    def buka_register(self):

        self.destroy()

        app = RegisterPage()
        app.mainloop()

    # ==========================
    # LOGIN
    # ==========================

    def login(self):

        username = self.entry_username.get()
        password = self.entry_password.get()

        if not username or not password:
            messagebox.showwarning(
                "Peringatan",
                "Username dan Password wajib diisi!"
            )
            return

        try:

            conn = connect_db()
            cursor = conn.cursor()

            query = """
                SELECT id_user, nama, role
                FROM users
                WHERE username=%s
                AND password=%s
            """

            cursor.execute(query, (username, password))

            user = cursor.fetchone()

            cursor.close()
            conn.close()

            if user:

                role = user[2]

                self.destroy()

                if role == "admin":

                    app = DashboardAdmin()
                    app.mainloop()

                elif role == "guru":

                    app = DashboardGuru()
                    app.mainloop()

                elif role == "kepala_sekolah":

                    app = DashboardKepsek()
                    app.mainloop()

                else:

                    messagebox.showerror(
                        "Error",
                        "Role tidak dikenali!"
                    )

            else:

                messagebox.showerror(
                    "Login Gagal",
                    "Username atau Password salah!"
                )

        except Exception as e:

            messagebox.showerror(
                "Error Database",
                str(e)
            )