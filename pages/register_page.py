import customtkinter as ctk
from tkinter import messagebox
from PIL import Image # Dibutuhkan untuk memproses gambar/logo
from database.koneksi import connect_db


class RegisterPage(ctk.CTk):

    def __init__(self):
        super().__init__()

        self.title("Register User - SDN Klegen")
        self.geometry("450x660") # Tinggi sedikit dinaikkan agar pas dengan tambahan logo
        self.resizable(False, False)

        # ==========================
        # BAGIAN GANTI IKON APLIKASI
        # ==========================
        try:
            self.iconbitmap("assets/app_icon.ico")
        except Exception as e:
            print(f"Gagal memuat ikon aplikasi (.ico): {e}")

        # Menyelaraskan tema gelap modern dengan halaman login
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")
        self.configure(fg_color="#111827") # Tailwind Gray 900

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
            self.logo_label.pack(pady=(20, 5))
        except Exception as e:
            print(f"Gagal memuat logo dari folder assets: {e}")

        # Judul Halaman
        ctk.CTkLabel(
            frame,
            text="BUAT AKUN BARU",
            font=("Segoe UI", 22, "bold"),
            text_color="#60A5FA"
        ).pack(pady=(0, 2))
        
        ctk.CTkLabel(
            frame,
            text="Sistem Prediksi Prestasi Siswa",
            font=("Segoe UI", 12),
            text_color="#9CA3AF"
        ).pack(pady=(0, 20))

        # ==========================
        # FIELD INPUT FORM REGISTRASI
        # ==========================

        # Input Nama Lengkap
        self.nama = ctk.CTkEntry(
            frame,
            width=280,
            height=44,
            corner_radius=10,
            border_width=1,
            border_color="#4B5563",
            fg_color="#1F2937",
            placeholder_text="Nama Lengkap",
            placeholder_text_color="#6B7280",
            font=("Segoe UI", 12)
        )
        self.nama.pack(pady=6)

        # Input Username
        self.username = ctk.CTkEntry(
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
        self.username.pack(pady=6)

        # Input Password
        self.password = ctk.CTkEntry(
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
        self.password.pack(pady=6)

        # Pilihan Hak Akses / Role (Modern Dropdown CustomTkinter)
        self.role = ctk.CTkOptionMenu(
            frame,
            width=280,
            height=44,
            corner_radius=10,
            font=("Segoe UI", 12),
            fg_color="#374151",
            button_color="#4B5563",
            button_hover_color="#6B7280",
            values=["admin", "guru", "kepala_sekolah"]
        )
        self.role.pack(pady=6)
        self.role.set("guru")

        # ==========================
        # TOMBOL AKSI & NAVIGASI BACK
        # ==========================

        # Button Submit Register (Warna Hijau Emerald untuk Aksi Sukses/Baru)
        ctk.CTkButton(
            frame,
            text="Daftarkan Akun",
            width=280,
            height=44,
            corner_radius=10,
            font=("Segoe UI", 13, "bold"),
            fg_color="#10B981",
            hover_color="#059669",
            command=self.register_user
        ).pack(pady=(15, 12))

        # Divider garis tipis
        divider = ctk.CTkFrame(frame, height=1, width=200, fg_color="#374151")
        divider.pack(pady=5)

        # Teks Gabungan Link Horizontal untuk kembali ke Login Page
        login_container = ctk.CTkFrame(frame, fg_color="transparent")
        login_container.pack(pady=(5, 15))

        label_tanya = ctk.CTkLabel(
            login_container,
            text="Sudah punya akun? ",
            font=("Segoe UI", 12),
            text_color="#9CA3AF"
        )
        label_tanya.pack(side="left")

        self.link_login = ctk.CTkLabel(
            login_container,
            text="Login Sekarang",
            font=("Segoe UI", 12, "underline"),
            text_color="#60A5FA", 
            cursor="hand2"
        )
        self.link_login.pack(side="left")
        
        # Mengikat aksi klik ke fungsi buka_login
        self.link_login.bind("<Button-1>", lambda event: self.buka_login())

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

        nama = self.nama.get()
        username = self.username.get()
        password = self.password.get()
        role = self.role.get()

        if not nama or not username or not password:
            messagebox.showwarning("Peringatan", "Semua field wajib diisi!")
            return

        try:
            conn = connect_db()
            cursor = conn.cursor()

            # Cek keunikan username di database
            cursor.execute(
                "SELECT username FROM users WHERE username=%s",
                (username,)
            )

            if cursor.fetchone():
                messagebox.showerror("Error", "Username sudah digunakan!")
                cursor.close()
                conn.close()
                return

            # Proses memasukkan data user baru
            query = """
                INSERT INTO users (nama, username, password, role)
                VALUES (%s, %s, %s, %s)
            """

            cursor.execute(query, (nama, username, password, role))
            conn.commit()

            cursor.close()
            conn.close()

            messagebox.showinfo(
                "Sukses",
                "Registrasi akun berhasil!"
            )

            # Reset form input dibersihkan terlebih dahulu
            self.nama.delete(0, 'end')
            self.username.delete(0, 'end')
            self.password.delete(0, 'end')

            # Tutup halaman registrasi lalu oper pengguna ke halaman login utama
            self.destroy()
            from pages.login_page import LoginPage
            app = LoginPage()
            app.mainloop()

        except Exception as e:
            messagebox.showerror("Error Database", str(e))