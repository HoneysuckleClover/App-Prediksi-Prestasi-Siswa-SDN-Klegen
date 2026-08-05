import os

import customtkinter as ctk
from tkinter import ttk, messagebox, filedialog
from database.koneksi_sqlite import connect_db
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib.units import inch
from datetime import datetime

from pages.guru.nilai_page import NilaiPage
from pages.guru.kehadiran_page import KehadiranPage
from pages.guru.motivasi_page import MotivasiPage
from pages.guru.disiplin_page import DisiplinPage
from pages.guru.prediksi_page import PrediksiPage
from pages.guru.hasil_page import HasilPage
from utils.helpers import resource_path


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
            icon_path = resource_path("assets/app_icon.ico")
            if os.path.exists(icon_path):
                self.iconbitmap(icon_path)
        except Exception as e:
            print(f"Gagal memuat ikon aplikasi (.ico): {e}")

        # Mengatur konfigurasi tema visual global (Tema Gelap Premium)
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")
        self.configure(fg_color="#0F172A")
        
        self.filter_option = None
        self.filter_combo = None
        self.table = None

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
            text="👩‍🏫 PANEL GURU",
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
            text="📘 Data Nilai",
            width=200,
            height=40,
            corner_radius=8,
            font=("Segoe UI", 12, "bold"),
            command=self.buka_nilai
        ).pack(pady=6)

        ctk.CTkButton(
            self.sidebar,
            text="📅 Data Kehadiran",
            width=200,
            height=40,
            corner_radius=8,
            font=("Segoe UI", 12, "bold"),
            command=self.buka_kehadiran
        ).pack(pady=6)

        ctk.CTkButton(
            self.sidebar,
            text="🔥 Data Motivasi",
            width=200,
            height=40,
            corner_radius=8,
            font=("Segoe UI", 12, "bold"),
            command=self.buka_motivasi
        ).pack(pady=6)

        ctk.CTkButton(
            self.sidebar,
            text="📊 Data Disiplin",
            width=200,
            height=40,
            corner_radius=8,
            font=("Segoe UI", 12, "bold"),
            command=self.buka_disiplin
        ).pack(pady=6)

        ctk.CTkButton(
            self.sidebar,
            text="🎯 Prediksi Prestasi",
            width=200,
            height=40,
            corner_radius=8,
            font=("Segoe UI", 12, "bold"),
            command=self.buka_prediksi
        ).pack(pady=6)

        ctk.CTkButton(
            self.sidebar,
            text="📊 Hasil Prediksi",
            width=200,
            height=40,
            corner_radius=8,
            font=("Segoe UI", 12, "bold"),
            command=self.buka_hasil
        ).pack(pady=6)

        # Separator
        ctk.CTkFrame(
            self.sidebar,
            fg_color="#334155",
            height=2
        ).pack(fill="x", padx=20, pady=10)

        # =========================
        # TOMBOL DOWNLOAD PDF
        # =========================

        ctk.CTkButton(
            self.sidebar,
            text="📥 Download Hasil Prediksi",
            width=200,
            height=40,
            corner_radius=8,
            font=("Segoe UI", 12, "bold"),
            fg_color="#8B5CF6",
            hover_color="#7C3AED",
            command=self.show_download_page
        ).pack(pady=6)

        # Tombol Logout (Ditempatkan di bagian paling bawah sidebar)
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

        # Menampilkan dashboard pertama kali saat dijalankan
        self.show_dashboard()

    # ===================================
    # TOTAL DATA NILAI
    # ===================================

    def get_total_nilai(self):
        try:
            conn = connect_db()
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM nilai")
            total = cursor.fetchone()[0]
            conn.close()
            return total
        except:
            return 0

    # ===================================
    # TOTAL KEHADIRAN
    # ===================================

    def get_total_kehadiran(self):
        try:
            conn = connect_db()
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM kehadiran")
            total = cursor.fetchone()[0]
            conn.close()
            return total
        except:
            return 0

    # ===================================
    # TOTAL PREDIKSI
    # ===================================

    def get_total_prediksi(self):
        try:
            conn = connect_db()
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM hasil_prediksi")
            total = cursor.fetchone()[0]
            conn.close()
            return total
        except:
            return 0

    # ===================================
    # TOTAL SISWA
    # ===================================

    def get_total_siswa(self):
        try:
            conn = connect_db()
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM siswa")
            total = cursor.fetchone()[0]
            conn.close()
            return total
        except:
            return 0

    # ===================================
    # TOTAL BERISIKO
    # ===================================

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
        except:
            return 0

    # ===================================
    # TOTAL TIDAK BERISIKO
    # ===================================

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
        except:
            return 0

    # ===================================
    # SHOW DASHBOARD
    # ===================================

    def show_dashboard(self):
        self.clear_content()

        total_nilai = self.get_total_nilai()
        total_kehadiran = self.get_total_kehadiran()
        total_prediksi = self.get_total_prediksi()
        total_siswa = self.get_total_siswa()
        total_berisiko = self.get_total_berisiko()
        total_tidak = self.get_total_tidak_berisiko()

        # Judul Utama Dashboard
        ctk.CTkLabel(
            self.content,
            text="📊 DASHBOARD AKADEMIK GURU",
            font=("Segoe UI", 28, "bold"),
            text_color="#F8FAFC"
        ).pack(anchor="w", pady=(10, 5))
        
        ctk.CTkLabel(
            self.content,
            text=f"Selamat Datang, Bapak/Ibu Guru SDN Klegen. {datetime.now().strftime('%A, %d %B %Y')}",
            font=("Segoe UI", 13),
            text_color="#94A3B8"
        ).pack(anchor="w", pady=(0, 25))

        # Card Container (Baris 1)
        card_frame1 = ctk.CTkFrame(self.content, fg_color="transparent")
        card_frame1.pack(fill="x", pady=10)

        # --- CARD 1: DATA SISWA ---
        card_siswa = self.create_card(
            card_frame1,
            "👥 Total Siswa",
            str(total_siswa),
            "#3B82F6"
        )
        card_siswa.pack(side="left", padx=(0, 20))

        # --- CARD 2: DATA NILAI ---
        card_nilai = self.create_card(
            card_frame1,
            "📊 Data Nilai",
            str(total_nilai),
            "#60A5FA"
        )
        card_nilai.pack(side="left", padx=20)

        # --- CARD 3: KEHADIRAN ---
        card_hadir = self.create_card(
            card_frame1,
            "📅 Kehadiran",
            str(total_kehadiran),
            "#10B981"
        )
        card_hadir.pack(side="left", padx=20)

        # --- CARD 4: PREDIKSI ---
        card_prediksi = self.create_card(
            card_frame1,
            "🔮 Prediksi",
            str(total_prediksi),
            "#F59E0B"
        )
        card_prediksi.pack(side="left", padx=20)

        # Card Container (Baris 2)
        card_frame2 = ctk.CTkFrame(self.content, fg_color="transparent")
        card_frame2.pack(fill="x", pady=10)

        # --- CARD 5: BERISIKO ---
        card_berisiko = self.create_card(
            card_frame2,
            "⚠️ Berisiko",
            str(total_berisiko),
            "#EF4444"
        )
        card_berisiko.pack(side="left", padx=(0, 20))

        # --- CARD 6: TIDAK BERISIKO ---
        card_tidak = self.create_card(
            card_frame2,
            "✅ Tidak Berisiko",
            str(total_tidak),
            "#10B981"
        )
        card_tidak.pack(side="left", padx=20)

        # ===================================
        # TABEL 5 PREDIKSI TERBARU
        # ===================================

        ctk.CTkLabel(
            self.content,
            text="📋 5 Prediksi Terbaru",
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

        columns = ("nama", "probabilitas", "hasil", "tanggal")
        
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

        table.heading("nama", text="👤 Nama Siswa")
        table.heading("probabilitas", text="📊 Probabilitas")
        table.heading("hasil", text="🎯 Hasil")
        table.heading("tanggal", text="📅 Tanggal")

        table.column("nama", width=300)
        table.column("probabilitas", width=150, anchor="center")
        table.column("hasil", width=150, anchor="center")
        table.column("tanggal", width=150, anchor="center")

        table.pack(fill="x", padx=10, pady=10)

        # Ambil data
        try:
            conn = connect_db()
            cursor = conn.cursor()
            cursor.execute("""
                SELECT
                    s.nama_siswa,
                    hp.probabilitas,
                    hp.hasil,
                    hp.tanggal_prediksi
                FROM hasil_prediksi hp
                JOIN siswa s ON hp.id_siswa = s.id_siswa
                ORDER BY hp.id_prediksi DESC
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

    # ===================================
    # CREATE CARD HELPER
    # ===================================

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
    # HALAMAN DOWNLOAD PDF
    # ===================================

    def show_download_page(self):
        """Tampilkan halaman download PDF dengan filter"""
        self.clear_content()

        ctk.CTkLabel(
            self.content,
            text="📥 DOWNLOAD LAPORAN PDF",
            font=("Segoe UI", 28, "bold"),
            text_color="#F8FAFC"
        ).pack(anchor="w", pady=(10, 5))

        ctk.CTkLabel(
            self.content,
            text="Download laporan hasil prediksi dengan filter",
            font=("Segoe UI", 13),
            text_color="#94A3B8"
        ).pack(anchor="w", pady=(0, 25))

        # ==================================
        # FILTER DOWNLOAD
        # ==================================

        filter_frame = ctk.CTkFrame(
            self.content,
            fg_color="#1E293B",
            corner_radius=12,
            border_width=1,
            border_color="#334155"
        )
        filter_frame.pack(fill="x", pady=(0, 15))

        ctk.CTkLabel(
            filter_frame,
            text="📥 Download Laporan",
            font=("Segoe UI", 16, "bold"),
            text_color="#60A5FA"
        ).pack(anchor="w", padx=20, pady=(15, 5))

        ctk.CTkLabel(
            filter_frame,
            text="Pilih filter untuk download PDF:",
            font=("Segoe UI", 12),
            text_color="#94A3B8"
        ).pack(anchor="w", padx=20, pady=(0, 15))

        filter_row = ctk.CTkFrame(filter_frame, fg_color="transparent")
        filter_row.pack(fill="x", padx=20, pady=(0, 15))

        ctk.CTkLabel(
            filter_row,
            text="Filter:",
            font=("Segoe UI", 12, "bold"),
            text_color="white"
        ).pack(side="left", padx=(0, 10))

        self.filter_option = ctk.CTkOptionMenu(
            filter_row,
            values=["Semua Data", "Per Siswa", "Per Kelas"],
            width=150,
            height=35,
            fg_color="#334155",
            button_color="#1E293B",
            button_hover_color="#475569",
            text_color="white",
            dropdown_fg_color="#1E293B",
            dropdown_text_color="white",
            dropdown_hover_color="#334155",
            font=("Segoe UI", 11),
            command=self.on_filter_change_download
        )
        self.filter_option.pack(side="left", padx=10)
        self.filter_option.set("Semua Data")

        self.filter_combo = ctk.CTkOptionMenu(
            filter_row,
            values=["Pilih..."],
            width=200,
            height=35,
            fg_color="#334155",
            button_color="#1E293B",
            button_hover_color="#475569",
            text_color="white",
            dropdown_fg_color="#1E293B",
            dropdown_text_color="white",
            dropdown_hover_color="#334155",
            font=("Segoe UI", 11)
        )
        self.filter_combo.pack(side="left", padx=10)
        self.filter_combo.pack_forget()

        ctk.CTkButton(
            filter_row,
            text="📥 Download PDF",
            width=150,
            height=38,
            fg_color="#8B5CF6",
            hover_color="#7C3AED",
            corner_radius=8,
            font=("Segoe UI", 12, "bold"),
            command=self.download_laporan_filtered_guru
        ).pack(side="left", padx=20)

        # Update combobox awal
        self.update_filter_combo_guru()

        # ==================================
        # TABEL PREVIEW
        # ==================================

        table_frame = ctk.CTkFrame(
            self.content,
            fg_color="#1E293B",
            corner_radius=12,
            border_width=1,
            border_color="#334155"
        )
        table_frame.pack(fill="both", expand=True)

        columns = ("id", "nama", "kelas", "probabilitas", "hasil", "tanggal")

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

        self.table = ttk.Treeview(
            table_frame,
            columns=columns,
            show="headings",
            height=15
        )

        self.table.heading("id", text="ID")
        self.table.heading("nama", text="👤 Nama Siswa")
        self.table.heading("kelas", text="📚 Kelas")
        self.table.heading("probabilitas", text="📊 Probabilitas")
        self.table.heading("hasil", text="🎯 Hasil")
        self.table.heading("tanggal", text="📅 Tanggal")

        self.table.column("id", width=60, anchor="center")
        self.table.column("nama", width=250)
        self.table.column("kelas", width=120, anchor="center")
        self.table.column("probabilitas", width=130, anchor="center")
        self.table.column("hasil", width=180, anchor="center")
        self.table.column("tanggal", width=150, anchor="center")

        scrollbar = ttk.Scrollbar(
            table_frame,
            orient="vertical",
            command=self.table.yview
        )
        self.table.configure(yscrollcommand=scrollbar.set)

        self.table.pack(
            side="left",
            fill="both",
            expand=True,
            padx=(10, 0),
            pady=10
        )
        scrollbar.pack(
            side="right",
            fill="y",
            padx=(0, 10),
            pady=10
        )

        # Load data preview
        self.load_download_data_guru()

    # ===================================
    # LOAD DATA PREVIEW
    # ===================================

    def load_download_data_guru(self):
        for row in self.table.get_children():
            self.table.delete(row)

        try:
            conn = connect_db()
            cursor = conn.cursor()
            cursor.execute("""
                SELECT
                    hp.id_prediksi,
                    s.nama_siswa,
                    COALESCE(k.nama_kelas, '-') AS kelas,
                    hp.probabilitas,
                    hp.hasil,
                    hp.tanggal_prediksi
                FROM hasil_prediksi hp
                JOIN siswa s ON hp.id_siswa = s.id_siswa
                LEFT JOIN kelas k ON s.id_kelas = k.id_kelas
                ORDER BY hp.id_prediksi DESC
            """)
            rows = cursor.fetchall()
            conn.close()

            for index, row in enumerate(rows):
                tag = "evenrow" if index % 2 == 0 else "oddrow"
                prob = row[3]
                prob_text = f"{float(prob):.1f}%" if prob is not None else "0%"
                values = (row[0], row[1], row[2], prob_text, row[4], row[5])
                self.table.insert("", "end", values=values, tags=(tag,))

            self.table.tag_configure("oddrow", background="#1E293B")
            self.table.tag_configure("evenrow", background="#273549")

        except Exception as e:
            messagebox.showerror("Error", str(e))

    # ===================================
    # UPDATE FILTER COMBOBOX
    # ===================================

    def update_filter_combo_guru(self):
        try:
            conn = connect_db()
            cursor = conn.cursor()
            
            filter_type = self.filter_option.get()
            
            if filter_type == "Per Siswa":
                cursor.execute("SELECT id_siswa, nama_siswa FROM siswa ORDER BY nama_siswa")
                data = cursor.fetchall()
                values = [f"{row[1]} (ID: {row[0]})" for row in data]
            elif filter_type == "Per Kelas":
                cursor.execute("SELECT nama_kelas FROM kelas ORDER BY nama_kelas")
                data = cursor.fetchall()
                values = [row[0] for row in data]
            else:
                values = ["Pilih..."]
            
            conn.close()
            
            if values:
                self.filter_combo.configure(values=values)
                self.filter_combo.set(values[0] if values else "Pilih...")
                self.filter_combo.pack(side="left", padx=10)
            else:
                self.filter_combo.configure(values=["Tidak ada data"])
                self.filter_combo.set("Tidak ada data")
                self.filter_combo.pack(side="left", padx=10)
                
        except Exception as e:
            print(f"Error update filter: {e}")

    # ===================================
    # ON FILTER CHANGE
    # ===================================

    def on_filter_change_download(self, choice):
        self.update_filter_combo_guru()

    # ===================================
    # DOWNLOAD LAPORAN FILTERED
    # ===================================

    def download_laporan_filtered_guru(self):
        try:
            filter_type = self.filter_option.get()
            
            if filter_type == "Semua Data":
                self.download_laporan_all_guru()
            elif filter_type == "Per Siswa":
                self.download_laporan_per_siswa_guru()
            elif filter_type == "Per Kelas":
                self.download_laporan_per_kelas_guru()
                
        except Exception as e:
            messagebox.showerror("Error", f"Gagal download PDF:\n{str(e)}")

    # ===================================
    # DOWNLOAD SEMUA DATA
    # ===================================

    def download_laporan_all_guru(self):
        file_path = filedialog.asksaveasfilename(
            defaultextension=".pdf",
            filetypes=[("PDF Files", "*.pdf")],
            title="Simpan Laporan Semua Data"
        )

        if not file_path:
            return

        try:
            conn = connect_db()
            cursor = conn.cursor()
            cursor.execute("""
                SELECT
                    s.nama_siswa,
                    COALESCE(k.nama_kelas, '-') AS kelas,
                    hp.probabilitas,
                    hp.hasil,
                    hp.tanggal_prediksi
                FROM hasil_prediksi hp
                JOIN siswa s ON hp.id_siswa = s.id_siswa
                LEFT JOIN kelas k ON s.id_kelas = k.id_kelas
                ORDER BY hp.id_prediksi DESC
            """)
            rows = cursor.fetchall()
            conn.close()

            if not rows:
                messagebox.showwarning("Data Kosong", "Tidak ada data!")
                return

            self._generate_pdf_guru(file_path, rows, "SEMUA DATA")

        except Exception as e:
            messagebox.showerror("Error", str(e))

    # ===================================
    # DOWNLOAD PER SISWA
    # ===================================

    def download_laporan_per_siswa_guru(self):
        selected = self.filter_combo.get()
        
        if not selected or selected == "Pilih..." or selected == "Tidak ada data":
            messagebox.showwarning("Peringatan", "Silakan pilih siswa terlebih dahulu!")
            return
        
        try:
            id_str = selected.split("ID: ")[1].replace(")", "")
            id_siswa = int(id_str)
        except:
            messagebox.showerror("Error", "Gagal mengambil ID siswa!")
            return
        
        file_path = filedialog.asksaveasfilename(
            defaultextension=".pdf",
            filetypes=[("PDF Files", "*.pdf")],
            title="Simpan Laporan Siswa"
        )

        if not file_path:
            return

        try:
            conn = connect_db()
            cursor = conn.cursor()
            cursor.execute("""
                SELECT
                    s.nama_siswa,
                    COALESCE(k.nama_kelas, '-') AS kelas,
                    hp.probabilitas,
                    hp.hasil,
                    hp.tanggal_prediksi
                FROM hasil_prediksi hp
                JOIN siswa s ON hp.id_siswa = s.id_siswa
                LEFT JOIN kelas k ON s.id_kelas = k.id_kelas
                WHERE hp.id_siswa = ?
                ORDER BY hp.id_prediksi DESC
            """, (id_siswa,))
            rows = cursor.fetchall()
            
            cursor.execute("SELECT nama_siswa FROM siswa WHERE id_siswa=?", (id_siswa,))
            nama = cursor.fetchone()
            conn.close()

            if not rows:
                messagebox.showwarning("Data Kosong", f"Siswa {nama[0] if nama else ''} belum punya prediksi!")
                return

            self._generate_pdf_guru(file_path, rows, f"SISWA: {nama[0] if nama else 'Unknown'}")

        except Exception as e:
            messagebox.showerror("Error", str(e))

    # ===================================
    # DOWNLOAD PER KELAS
    # ===================================

    def download_laporan_per_kelas_guru(self):
        nama_kelas = self.filter_combo.get()
        
        if not nama_kelas or nama_kelas == "Pilih..." or nama_kelas == "Tidak ada data":
            messagebox.showwarning("Peringatan", "Silakan pilih kelas terlebih dahulu!")
            return

        file_path = filedialog.asksaveasfilename(
            defaultextension=".pdf",
            filetypes=[("PDF Files", "*.pdf")],
            title=f"Simpan Laporan Kelas {nama_kelas}"
        )

        if not file_path:
            return

        try:
            conn = connect_db()
            cursor = conn.cursor()
            cursor.execute("""
                SELECT
                    s.nama_siswa,
                    COALESCE(k.nama_kelas, '-') AS kelas,
                    hp.probabilitas,
                    hp.hasil,
                    hp.tanggal_prediksi
                FROM hasil_prediksi hp
                JOIN siswa s ON hp.id_siswa = s.id_siswa
                LEFT JOIN kelas k ON s.id_kelas = k.id_kelas
                WHERE k.nama_kelas = ?
                ORDER BY s.nama_siswa
            """, (nama_kelas,))
            rows = cursor.fetchall()
            conn.close()

            if not rows:
                messagebox.showwarning("Data Kosong", f"Kelas {nama_kelas} belum ada data prediksi!")
                return

            self._generate_pdf_guru(file_path, rows, f"KELAS: {nama_kelas}")

        except Exception as e:
            messagebox.showerror("Error", str(e))

    # ===================================
    # GENERATE PDF (HELPER)
    # ===================================

    def _generate_pdf_guru(self, file_path, rows, title):
        from reportlab.lib.pagesizes import A4, landscape
        from reportlab.lib.units import inch
        from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
        from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
        from reportlab.lib.enums import TA_CENTER
        from reportlab.lib import colors

        pdf = SimpleDocTemplate(
            file_path,
            pagesize=landscape(A4),
            rightMargin=0.5*inch,
            leftMargin=0.5*inch,
            topMargin=0.5*inch,
            bottomMargin=0.5*inch
        )

        styles = getSampleStyleSheet()
        
        judul_style = ParagraphStyle(
            'JudulStyle',
            parent=styles['Heading1'],
            fontName='Helvetica-Bold',
            fontSize=18,
            textColor=colors.HexColor('#1E293B'),
            alignment=TA_CENTER,
            spaceAfter=5
        )
        
        sub_judul_style = ParagraphStyle(
            'SubJudulStyle',
            parent=styles['Normal'],
            fontName='Helvetica',
            fontSize=12,
            textColor=colors.HexColor('#475569'),
            alignment=TA_CENTER,
            spaceAfter=20
        )

        elements = []
        elements.append(Paragraph("LAPORAN HASIL PREDIKSI PRESTASI SISWA", judul_style))
        elements.append(Paragraph("SDN KLEGEN", sub_judul_style))
        elements.append(Paragraph(f"Filter: {title}", sub_judul_style))
        elements.append(Paragraph(f"Tanggal Cetak: {datetime.now().strftime('%d %B %Y %H:%M')}", sub_judul_style))
        elements.append(Spacer(1, 20))

        data = [["No", "Nama Siswa", "Kelas", "Probabilitas (%)", "Hasil Prediksi", "Tanggal"]]

        for i, row in enumerate(rows, 1):
            prob = f"{float(row[2]):.1f}" if row[2] else "0"
            data.append([
                str(i),
                str(row[0]),
                str(row[1]),
                prob,
                str(row[3]),
                str(row[4])
            ])

        table = Table(data, colWidths=[0.5*inch, 2.2*inch, 1.2*inch, 1.2*inch, 1.5*inch, 1.5*inch])

        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1E293B')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 10),
            ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 10),
            ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 1), (-1, -1), 9),
            ('ALIGN', (0, 1), (0, -1), 'CENTER'),
            ('ALIGN', (2, 1), (2, -1), 'CENTER'),
            ('ALIGN', (3, 1), (3, -1), 'CENTER'),
            ('ALIGN', (5, 1), (5, -1), 'CENTER'),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#CBD5E1')),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), 
             [colors.HexColor('#F8FAFC'), colors.HexColor('#F1F5F9')]),
            ('TEXTCOLOR', (0, 1), (-1, -1), colors.HexColor('#1E293B')),
        ]))

        elements.append(table)

        footer_style = ParagraphStyle(
            'FooterStyle',
            parent=styles['Normal'],
            fontName='Helvetica',
            fontSize=8,
            textColor=colors.HexColor('#94A3B8'),
            alignment=TA_CENTER,
            spaceBefore=20
        )
        elements.append(Paragraph("© 2024 SDN Klegen - Sistem Prediksi Prestasi Siswa", footer_style))

        pdf.build(elements)

        messagebox.showinfo("Sukses", f"Laporan PDF berhasil disimpan!\nFilter: {title}")

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