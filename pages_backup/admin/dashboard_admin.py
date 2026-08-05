import customtkinter as ctk
from tkinter import ttk, messagebox
from database.koneksi_sqlite import connect_db
from datetime import datetime

from pages.admin.siswa_page import SiswaPage
from pages.admin.kelas_page import KelasPage
from pages.admin.user_page import UserPage
from pages.guru.hasil_page import HasilPage  # Import dari guru


class DashboardAdmin(ctk.CTk):

    def __init__(self):
        super().__init__()

        self.title("Dashboard Admin - SDN Klegen")
        self.geometry("1200x700")
        self.resizable(True, True)

        # ==========================
        # BAGIAN GANTI IKON APLIKASI
        # ==========================
        try:
            self.iconbitmap("assets/app_icon.ico")
        except Exception as e:
            print(f"Gagal memuat ikon aplikasi (.ico): {e}")

        # Mengatur konfigurasi tema visual global
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")
        self.configure(fg_color="#0F172A")

        # =========================
        # SIDEBAR (NAVIGASI KIRI)
        # =========================

        self.sidebar = ctk.CTkFrame(
            self,
            width=240,
            corner_radius=0,
            fg_color="#1E293B",
            border_width=0
        )
        self.sidebar.pack(
            side="left",
            fill="y"
        )
        self.sidebar.pack_propagate(False)

        # Header Sidebar
        ctk.CTkLabel(
            self.sidebar,
            text="👨‍💼 ADMIN PANEL",
            font=("Segoe UI", 20, "bold"),
            text_color="#60A5FA"
        ).pack(pady=(30, 25))

        # =========================
        # TOMBOL NAVIGASI MENU
        # =========================

        ctk.CTkButton(
            self.sidebar,
            text="📊 Dashboard Utama",
            width=200,
            height=40,
            corner_radius=8,
            font=("Segoe UI", 12, "bold"),
            command=self.show_dashboard
        ).pack(pady=6)

        ctk.CTkButton(
            self.sidebar,
            text="👥 Data Siswa",
            width=200,
            height=40,
            corner_radius=8,
            font=("Segoe UI", 12, "bold"),
            command=self.buka_siswa
        ).pack(pady=6)

        ctk.CTkButton(
            self.sidebar,
            text="📚 Data Kelas",
            width=200,
            height=40,
            corner_radius=8,
            font=("Segoe UI", 12, "bold"),
            command=self.buka_kelas
        ).pack(pady=6)

        ctk.CTkButton(
            self.sidebar,
            text="👤 Kelola Akun User",
            width=200,
            height=40,
            corner_radius=8,
            font=("Segoe UI", 12, "bold"),
            command=self.buka_user
        ).pack(pady=6)

        # Separator
        ctk.CTkFrame(
            self.sidebar,
            fg_color="#334155",
            height=2
        ).pack(fill="x", padx=20, pady=10)

        ctk.CTkButton(
            self.sidebar,
            text="📊 Hasil Prediksi",
            width=200,
            height=40,
            corner_radius=8,
            font=("Segoe UI", 12, "bold"),
            fg_color="#8B5CF6",
            hover_color="#7C3AED",
            command=self.buka_hasil
        ).pack(pady=6)

        # Tombol Logout
        ctk.CTkButton(
            self.sidebar,
            text="🚪 Logout",
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

        # Menampilkan dashboard pertama kali
        self.show_dashboard()

    # =========================
    # TOTAL SISWA
    # =========================

    def get_total_siswa(self):
        try:
            conn = connect_db()
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM siswa")
            total = cursor.fetchone()[0]
            conn.close()
            return total
        except Exception as e:
            print("Error total siswa:", e)
            return 0

    # =========================
    # TOTAL GURU
    # =========================

    def get_total_guru(self):
        try:
            conn = connect_db()
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM users WHERE role='guru'")
            total = cursor.fetchone()[0]
            conn.close()
            return total
        except Exception as e:
            print("Error total guru:", e)
            return 0

    # =========================
    # TOTAL KELAS
    # =========================

    def get_total_kelas(self):
        try:
            conn = connect_db()
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM kelas")
            total = cursor.fetchone()[0]
            conn.close()
            return total
        except Exception as e:
            print("Error total kelas:", e)
            return 0

    # =========================
    # TOTAL USER
    # =========================

    def get_total_user(self):
        try:
            conn = connect_db()
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM users")
            total = cursor.fetchone()[0]
            conn.close()
            return total
        except Exception as e:
            print("Error total user:", e)
            return 0

    # =========================
    # TOTAL PREDIKSI
    # =========================

    def get_total_prediksi(self):
        try:
            conn = connect_db()
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM hasil_prediksi")
            total = cursor.fetchone()[0]
            conn.close()
            return total
        except Exception as e:
            print("Error total prediksi:", e)
            return 0

    # =========================
    # TOTAL BERISIKO
    # =========================

    def get_total_berisiko(self):
        try:
            conn = connect_db()
            cursor = conn.cursor()
            cursor.execute("""
                SELECT COUNT(*) 
                FROM hasil_prediksi 
                WHERE hasil='Berisiko'
            """)
            total = cursor.fetchone()[0]
            conn.close()
            return total
        except Exception as e:
            print("Error total berisiko:", e)
            return 0

    # =========================
    # TOTAL TIDAK BERISIKO
    # =========================

    def get_total_tidak_berisiko(self):
        try:
            conn = connect_db()
            cursor = conn.cursor()
            cursor.execute("""
                SELECT COUNT(*) 
                FROM hasil_prediksi 
                WHERE hasil='Tidak Berisiko'
            """)
            total = cursor.fetchone()[0]
            conn.close()
            return total
        except Exception as e:
            print("Error total tidak berisiko:", e)
            return 0

    # =========================
    # ELEMEN HALAMAN DASHBOARD
    # =========================

    def show_dashboard(self):
        self.clear_content()

        total_siswa = self.get_total_siswa()
        total_guru = self.get_total_guru()
        total_kelas = self.get_total_kelas()
        total_user = self.get_total_user()
        total_prediksi = self.get_total_prediksi()
        total_berisiko = self.get_total_berisiko()
        total_tidak = self.get_total_tidak_berisiko()

        # Judul Utama Dashboard
        ctk.CTkLabel(
            self.content,
            text="📊 DASHBOARD ADMIN",
            font=("Segoe UI", 28, "bold"),
            text_color="#F8FAFC"
        ).pack(anchor="w", pady=(10, 5))
        
        ctk.CTkLabel(
            self.content,
            text=f"Selamat Datang Kembali, Administrator. {datetime.now().strftime('%A, %d %B %Y')}",
            font=("Segoe UI", 13),
            text_color="#94A3B8"
        ).pack(anchor="w", pady=(0, 25))

        # Card Container (Baris 1)
        card_frame1 = ctk.CTkFrame(self.content, fg_color="transparent")
        card_frame1.pack(fill="x", pady=10)

        # --- CARD 1: TOTAL SISWA ---
        card_siswa = self.create_card(
            card_frame1,
            "👥 Total Siswa",
            str(total_siswa),
            "#60A5FA"
        )
        card_siswa.pack(side="left", padx=(0, 20))

        # --- CARD 2: TOTAL GURU ---
        card_guru = self.create_card(
            card_frame1,
            "👨‍🏫 Total Guru",
            str(total_guru),
            "#10B981"
        )
        card_guru.pack(side="left", padx=20)

        # --- CARD 3: TOTAL KELAS ---
        card_kelas = self.create_card(
            card_frame1,
            "📚 Total Kelas",
            str(total_kelas),
            "#F59E0B"
        )
        card_kelas.pack(side="left", padx=20)

        # --- CARD 4: TOTAL USER ---
        card_user = self.create_card(
            card_frame1,
            "👤 Total User",
            str(total_user),
            "#8B5CF6"
        )
        card_user.pack(side="left", padx=20)

        # Card Container (Baris 2)
        card_frame2 = ctk.CTkFrame(self.content, fg_color="transparent")
        card_frame2.pack(fill="x", pady=10)

        # --- CARD 5: TOTAL PREDIKSI ---
        card_prediksi = self.create_card(
            card_frame2,
            "📈 Total Prediksi",
            str(total_prediksi),
            "#EF4444"
        )
        card_prediksi.pack(side="left", padx=(0, 20))

        # --- CARD 6: BERISIKO ---
        card_berisiko = self.create_card(
            card_frame2,
            "⚠️ Berisiko",
            str(total_berisiko),
            "#EF4444"
        )
        card_berisiko.pack(side="left", padx=20)

        # --- CARD 7: TIDAK BERISIKO ---
        card_tidak = self.create_card(
            card_frame2,
            "✅ Tidak Berisiko",
            str(total_tidak),
            "#10B981"
        )
        card_tidak.pack(side="left", padx=20)

        # ===================================
        # TABEL 5 USER TERBARU
        # ===================================

        ctk.CTkLabel(
            self.content,
            text="👤 5 User Terbaru",
            font=("Segoe UI", 20, "bold"),
            text_color="#F8FAFC"
        ).pack(anchor="w", pady=(30, 10))

        # Frame tabel
        table_frame = ctk.CTkFrame(
            self.content,
            fg_color="#1E293B",
            corner_radius=12,
            border_width=1,
            border_color="#334155"
        )
        table_frame.pack(fill="x", pady=(0, 10))

        columns = ("username", "role", "created_at")
        
        style = ttk.Style()
        style.theme_use("clam")
        style.configure(
            "Treeview",
            background="#1E293B",
            foreground="white",
            fieldbackground="#1E293B",
            rowheight=34,
            borderwidth=0,
            font=("Segoe UI", 10)
        )
        style.configure(
            "Treeview.Heading",
            background="#334155",
            foreground="white",
            font=("Segoe UI", 10, "bold")
        )
        style.map(
            "Treeview",
            background=[("selected", "#2563EB")]
        )

        table = ttk.Treeview(
            table_frame,
            columns=columns,
            show="headings",
            height=5
        )

        table.heading("username", text="👤 Username")
        table.heading("role", text="🎯 Role")
        table.heading("created_at", text="📅 Tanggal Dibuat")

        table.column("username", width=300)
        table.column("role", width=150, anchor="center")
        table.column("created_at", width=200, anchor="center")

        table.pack(fill="x", padx=10, pady=10)

        # Ambil data
        try:
            conn = connect_db()
            cursor = conn.cursor()
            cursor.execute("""
                SELECT username, role, created_at
                FROM users
                ORDER BY id_user DESC
                LIMIT 5
            """)
            rows = cursor.fetchall()
            conn.close()

            for index, row in enumerate(rows):
                tag = "evenrow" if index % 2 == 0 else "oddrow"
                table.insert("", "end", values=row, tags=(tag,))

            table.tag_configure("oddrow", background="#1E293B")
            table.tag_configure("evenrow", background="#273549")

        except Exception as e:
            print(f"Error loading data: {e}")

    # =========================
    # CREATE CARD HELPER
    # =========================

    def create_card(self, parent, title, value, color):
        card = ctk.CTkFrame(
            parent,
            width=220,
            height=130,
            fg_color="#1E293B",
            corner_radius=12,
            border_width=1,
            border_color="#334155"
        )
        card.pack_propagate(False)

        ctk.CTkLabel(
            card,
            text=title,
            font=("Segoe UI", 14),
            text_color="#94A3B8"
        ).pack(anchor="w", padx=20, pady=(20, 5))

        ctk.CTkLabel(
            card,
            text=value,
            font=("Segoe UI", 32, "bold"),
            text_color=color
        ).pack(anchor="w", padx=20)

        return card

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

    def buka_hasil(self):
        self.clear_content()
        page = HasilPage(self.content)  # Panggil HasilPage dari guru
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
            from pages.login_page import LoginPage
            app = LoginPage()
            app.mainloop()
