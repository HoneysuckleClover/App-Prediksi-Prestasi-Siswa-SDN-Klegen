import customtkinter as ctk
from tkinter import messagebox
from PIL import Image

from database.koneksi_sqlite import connect_db
from pages.register_page import RegisterPage
from pages.admin.dashboard_admin import DashboardAdmin
from pages.guru.dashboard_guru import DashboardGuru
from pages.kepsek.dashboard_kepsek import DashboardKepalaSekolah


class LoginPage(ctk.CTk):

    def __init__(self):
        super().__init__()

        self.title("Sistem Prediksi Prestasi Siswa - SDN Klegen")
        self.geometry("500x660")
        self.resizable(False, False)

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
        # MAIN FRAME (CARD)
        # ==========================

        main_frame = ctk.CTkFrame(
            self,
            fg_color="#1E293B",
            corner_radius=24,
            border_width=1,
            border_color="#334155"
        )
        main_frame.pack(expand=True, fill="both", padx=35, pady=35)

        # ==========================
        # LOGO & HEADER
        # ==========================

        # Logo
        try:
            logo_image = ctk.CTkImage(
                light_image=Image.open("assets/logo.png"),
                dark_image=Image.open("assets/logo.png"),
                size=(100, 95)
            )
            logo_label = ctk.CTkLabel(main_frame, image=logo_image, text="")
            logo_label.pack(pady=(20, 5))
        except Exception as e:
            print(f"Gagal memuat logo: {e}")
            ctk.CTkLabel(
                main_frame,
                text="🏫",
                font=("Segoe UI", 52)
            ).pack(pady=(20, 5))

        # Nama Sekolah
        ctk.CTkLabel(
            main_frame,
            text="SDN KLEGEN",
            font=("Segoe UI", 30, "bold"),
            text_color="#60A5FA"
        ).pack(pady=(0, 2))

        # Sub Judul
        ctk.CTkLabel(
            main_frame,
            text="Sistem Prediksi Prestasi Siswa",
            font=("Segoe UI", 13),
            text_color="#94A3B8"
        ).pack(pady=(0, 15))

        # Decorative line
        ctk.CTkFrame(
            main_frame,
            fg_color="#60A5FA",
            height=3,
            width=60
        ).pack(pady=(0, 20))

        # ==========================
        # FORM LOGIN
        # ==========================

        # Label Username
        ctk.CTkLabel(
            main_frame,
            text="👤 Username",
            font=("Segoe UI", 13, "bold"),
            text_color="#E2E8F0"
        ).pack(anchor="w", padx=45, pady=(10, 5))

        self.entry_username = ctk.CTkEntry(
            main_frame,
            width=340,
            height=46,
            corner_radius=12,
            border_width=2,
            border_color="#475569",
            fg_color="#0F172A",
            placeholder_text="Masukkan username Anda",
            placeholder_text_color="#64748B",
            font=("Segoe UI", 13)
        )
        self.entry_username.pack(pady=(0, 12))
        self.entry_username.bind("<Return>", lambda e: self.entry_password.focus())

        # Label Password
        ctk.CTkLabel(
            main_frame,
            text="🔒 Password",
            font=("Segoe UI", 13, "bold"),
            text_color="#E2E8F0"
        ).pack(anchor="w", padx=45, pady=(5, 5))

        self.entry_password = ctk.CTkEntry(
            main_frame,
            width=340,
            height=46,
            corner_radius=12,
            border_width=2,
            border_color="#475569",
            fg_color="#0F172A",
            placeholder_text="Masukkan password Anda",
            placeholder_text_color="#64748B",
            show="*",
            font=("Segoe UI", 13)
        )
        self.entry_password.pack(pady=(0, 5))
        self.entry_password.bind("<Return>", lambda e: self.login())

        # ==========================
        # TOMBOL LOGIN
        # ==========================

        ctk.CTkButton(
            main_frame,
            text="Masuk ke Akun",
            width=340,
            height=50,
            corner_radius=12,
            font=("Segoe UI", 15, "bold"),
            fg_color="#2563EB",
            hover_color="#1D4ED8",
            command=self.login
        ).pack(pady=(25, 15))

        # ==========================
        # DIVIDER (Tanpa kata "atau")
        # ==========================

        ctk.CTkFrame(
            main_frame,
            fg_color="#334155",
            height=1
        ).pack(fill="x", padx=45, pady=5)

        # ==========================
        # REGISTER LINK
        # ==========================

        register_container = ctk.CTkFrame(main_frame, fg_color="transparent")
        register_container.pack(pady=(15, 20))

        ctk.CTkLabel(
            register_container,
            text="Belum punya akun? ",
            font=("Segoe UI", 13),
            text_color="#94A3B8"
        ).pack(side="left")

        register_link = ctk.CTkLabel(
            register_container,
            text="Daftar Sekarang",
            font=("Segoe UI", 13, "bold"),
            text_color="#60A5FA",
            cursor="hand2"
        )
        register_link.pack(side="left")
        register_link.bind("<Button-1>", lambda e: self.buka_register())
        register_link.bind("<Enter>", lambda e: register_link.configure(text_color="#93C5FD"))
        register_link.bind("<Leave>", lambda e: register_link.configure(text_color="#60A5FA"))

        # ==========================
        # FOOTER
        # ==========================

        ctk.CTkLabel(
            main_frame,
            text="© 2024 SDN Klegen • v1.0",
            font=("Segoe UI", 10),
            text_color="#475569"
        ).pack(side="bottom", pady=(5, 15))

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
        username = self.entry_username.get().strip()
        password = self.entry_password.get().strip()

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
                WHERE username=? AND password=?
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
                    app = DashboardKepalaSekolah()
                    app.mainloop()
                else:
                    messagebox.showerror("Error", "Role tidak dikenali!")

            else:
                messagebox.showerror(
                    "Login Gagal",
                    "Username atau Password salah!"
                )

        except Exception as e:
            messagebox.showerror("Error Database", str(e))
