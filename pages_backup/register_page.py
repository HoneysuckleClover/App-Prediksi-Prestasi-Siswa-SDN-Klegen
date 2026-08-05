import customtkinter as ctk
from tkinter import messagebox
from PIL import Image
from database.koneksi_sqlite import connect_db


class RegisterPage(ctk.CTk):

    def __init__(self):
        super().__init__()

        self.title("Register User - SDN Klegen")
        self.geometry("480x720")
        self.resizable(False, False)

        # ==========================
        # BAGIAN GANTI IKON APLIKASI
        # ==========================
        try:
            self.iconbitmap("assets/app_icon.ico")
        except Exception as e:
            print(f"Gagal memuat ikon aplikasi (.ico): {e}")

        # Menyelaraskan tema gelap modern
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
                size=(80, 75)
            )
            logo_label = ctk.CTkLabel(main_frame, image=logo_image, text="")
            logo_label.pack(pady=(20, 5))
        except Exception as e:
            print(f"Gagal memuat logo: {e}")
            ctk.CTkLabel(
                main_frame,
                text="🏫",
                font=("Segoe UI", 48)
            ).pack(pady=(20, 5))

        # Judul Halaman
        ctk.CTkLabel(
            main_frame,
            text="Buat Akun Baru",
            font=("Segoe UI", 26, "bold"),
            text_color="white"
        ).pack(pady=(0, 2))

        ctk.CTkLabel(
            main_frame,
            text="Sistem Prediksi Prestasi Siswa",
            font=("Segoe UI", 12),
            text_color="#94A3B8"
        ).pack(pady=(0, 15))

        # Garis dekoratif
        ctk.CTkFrame(
            main_frame,
            fg_color="#60A5FA",
            height=2,
            width=50
        ).pack(pady=(0, 20))

        # ==========================
        # FORM REGISTRASI
        # ==========================

        # Nama Lengkap dengan icon
        nama_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        nama_frame.pack(fill="x", padx=40, pady=(5, 2))
        
        ctk.CTkLabel(
            nama_frame,
            text="👤",
            font=("Segoe UI", 14),
            text_color="#94A3B8"
        ).pack(side="left", padx=(0, 8))
        
        self.nama = ctk.CTkEntry(
            nama_frame,
            width=280,
            height=44,
            corner_radius=10,
            border_width=1,
            border_color="#475569",
            fg_color="#0F172A",
            placeholder_text="Nama Lengkap",
            placeholder_text_color="#64748B",
            font=("Segoe UI", 13)
        )
        self.nama.pack(side="left", fill="x", expand=True)
        self.nama.bind("<Return>", lambda e: self.username.focus())

        # Username dengan icon
        username_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        username_frame.pack(fill="x", padx=40, pady=8)
        
        ctk.CTkLabel(
            username_frame,
            text="🔑",
            font=("Segoe UI", 14),
            text_color="#94A3B8"
        ).pack(side="left", padx=(0, 8))
        
        self.username = ctk.CTkEntry(
            username_frame,
            width=280,
            height=44,
            corner_radius=10,
            border_width=1,
            border_color="#475569",
            fg_color="#0F172A",
            placeholder_text="Username",
            placeholder_text_color="#64748B",
            font=("Segoe UI", 13)
        )
        self.username.pack(side="left", fill="x", expand=True)
        self.username.bind("<Return>", lambda e: self.password.focus())

        # Password dengan icon
        password_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        password_frame.pack(fill="x", padx=40, pady=8)
        
        ctk.CTkLabel(
            password_frame,
            text="🔒",
            font=("Segoe UI", 14),
            text_color="#94A3B8"
        ).pack(side="left", padx=(0, 8))
        
        self.password = ctk.CTkEntry(
            password_frame,
            width=280,
            height=44,
            corner_radius=10,
            border_width=1,
            border_color="#475569",
            fg_color="#0F172A",
            placeholder_text="Password (min. 6 karakter)",
            placeholder_text_color="#64748B",
            show="*",
            font=("Segoe UI", 13)
        )
        self.password.pack(side="left", fill="x", expand=True)
        self.password.bind("<Return>", lambda e: self.role.focus())

        # Role dengan icon
        role_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        role_frame.pack(fill="x", padx=40, pady=8)
        
        ctk.CTkLabel(
            role_frame,
            text="🎯",
            font=("Segoe UI", 14),
            text_color="#94A3B8"
        ).pack(side="left", padx=(0, 8))
        
        self.role = ctk.CTkOptionMenu(
            role_frame,
            width=280,
            height=44,
            corner_radius=10,
            font=("Segoe UI", 13),
            fg_color="#0F172A",
            button_color="#334155",
            button_hover_color="#475569",
            dropdown_fg_color="#1E293B",
            dropdown_text_color="white",
            dropdown_hover_color="#334155",
            values=["admin", "guru", "kepala_sekolah"]
        )
        self.role.pack(side="left", fill="x", expand=True)
        self.role.set("guru")

        # ==========================
        # TOMBOL REGISTER
        # ==========================

        ctk.CTkButton(
            main_frame,
            text="Daftar",
            width=320,
            height=46,
            corner_radius=12,
            font=("Segoe UI", 14, "bold"),
            fg_color="#2563EB",
            hover_color="#1D4ED8",
            command=self.register_user
        ).pack(pady=(25, 15))

        # ==========================
        # DIVIDER
        # ==========================

        ctk.CTkFrame(
            main_frame,
            fg_color="#334155",
            height=1
        ).pack(fill="x", padx=40, pady=5)

        # ==========================
        # LOGIN LINK
        # ==========================

        login_container = ctk.CTkFrame(main_frame, fg_color="transparent")
        login_container.pack(pady=(12, 20))

        ctk.CTkLabel(
            login_container,
            text="Sudah punya akun? ",
            font=("Segoe UI", 12),
            text_color="#94A3B8"
        ).pack(side="left")

        login_link = ctk.CTkLabel(
            login_container,
            text="Login Sekarang",
            font=("Segoe UI", 12, "bold"),
            text_color="#60A5FA",
            cursor="hand2"
        )
        login_link.pack(side="left")
        login_link.bind("<Button-1>", lambda e: self.buka_login())
        login_link.bind("<Enter>", lambda e: login_link.configure(text_color="#93C5FD"))
        login_link.bind("<Leave>", lambda e: login_link.configure(text_color="#60A5FA"))

        # ==========================
        # FOOTER
        # ==========================

        ctk.CTkLabel(
            main_frame,
            text="© 2024 SDN Klegen • v1.0",
            font=("Segoe UI", 10),
            text_color="#475569"
        ).pack(side="bottom", pady=12)

    # ==========================
    # NAVIGASI KEMBALI KE LOGIN
    # ==========================

    def buka_login(self):
        self.destroy()
        from pages.login_page import LoginPage
        app = LoginPage()
        app.mainloop()

    # ==========================
    # LOGIKA UTAMA REGISTER USER
    # ==========================

    def register_user(self):
        nama = self.nama.get().strip()
        username = self.username.get().strip()
        password = self.password.get().strip()
        role = self.role.get()

        # Validasi
        if not nama or not username or not password:
            messagebox.showwarning(
                "Peringatan",
                "Semua field wajib diisi!"
            )
            return

        if len(password) < 6:
            messagebox.showwarning(
                "Peringatan",
                "Password minimal 6 karakter!"
            )
            return

        try:
            conn = connect_db()
            cursor = conn.cursor()

            # Cek keunikan username
            cursor.execute(
                "SELECT username FROM users WHERE username=?",
                (username,)
            )

            if cursor.fetchone():
                messagebox.showerror(
                    "Error",
                    f"Username '{username}' sudah digunakan!"
                )
                cursor.close()
                conn.close()
                return

            # Insert user baru
            query = """
                INSERT INTO users (nama, username, password, role)
                VALUES (?, ?, ?, ?)
            """

            cursor.execute(query, (nama, username, password, role))
            conn.commit()

            cursor.close()
            conn.close()

            messagebox.showinfo(
                "Sukses",
                f"Akun berhasil dibuat!\n\n"
                f"Nama: {nama}\n"
                f"Username: {username}\n"
                f"Role: {role}"
            )

            # Reset form
            self.nama.delete(0, 'end')
            self.username.delete(0, 'end')
            self.password.delete(0, 'end')
            self.role.set("guru")

            # Buka halaman login
            self.destroy()
            from pages.login_page import LoginPage
            app = LoginPage()
            app.mainloop()

        except Exception as e:
            messagebox.showerror("Error Database", str(e))
