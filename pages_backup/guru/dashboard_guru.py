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
            self.iconbitmap("assets/app_icon.ico")
        except Exception as e:
            print(f"Gagal memuat ikon aplikasi (.ico): {e}")

        # Mengatur konfigurasi tema visual global (Tema Gelap Premium)
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
            text="📥 Download Hasil PDF",
            width=200,
            height=40,
            corner_radius=8,
            font=("Segoe UI", 12, "bold"),
            fg_color="#8B5CF6",
            hover_color="#7C3AED",
            command=self.download_laporan
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
    # DOWNLOAD LAPORAN PDF
    # ===================================

    def download_laporan(self):
        try:
            # Pilih lokasi save
            file_path = filedialog.asksaveasfilename(
                defaultextension=".pdf",
                filetypes=[("PDF Files", "*.pdf")],
                title="Simpan Laporan PDF"
            )

            if not file_path:
                return

            # Ambil data dari database
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
            """)

            rows = cursor.fetchall()
            conn.close()

            if not rows:
                messagebox.showwarning(
                    "Data Kosong",
                    "Tidak ada data hasil prediksi untuk diunduh!"
                )
                return

            # Buat PDF
            pdf = SimpleDocTemplate(
                file_path,
                pagesize=landscape(A4),
                rightMargin=0.5*inch,
                leftMargin=0.5*inch,
                topMargin=0.5*inch,
                bottomMargin=0.5*inch
            )

            # Data tabel
            data = [
                ["No", "Nama Siswa", "Probabilitas (%)", "Hasil Prediksi", "Tanggal"]
            ]

            for i, row in enumerate(rows, 1):
                prob = f"{float(row[1]):.1f}" if row[1] else "0"
                data.append([
                    str(i),
                    str(row[0]),
                    prob,
                    str(row[2]),
                    str(row[3])
                ])

            # Buat tabel
            table = Table(data, colWidths=[0.5*inch, 2.5*inch, 1.2*inch, 1.5*inch, 1.5*inch])
            
            # Style tabel
            table.setStyle(TableStyle([
                # Header
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1E293B')),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 10),
                ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 10),
                
                # Body
                ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
                ('FONTSIZE', (0, 1), (-1, -1), 9),
                ('ALIGN', (0, 1), (0, -1), 'CENTER'),
                ('ALIGN', (2, 1), (2, -1), 'CENTER'),
                ('ALIGN', (4, 1), (4, -1), 'CENTER'),
                
                # Grid
                ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#334155')),
                
                # Background row
                ('ROWBACKGROUNDS', (0, 1), (-1, -1), 
                 [colors.HexColor('#1E293B'), colors.HexColor('#273549')]),
                
                # Text color body
                ('TEXTCOLOR', (0, 1), (-1, -1), colors.white),
            ]))

            # Build PDF
            pdf.build([table])

            messagebox.showinfo(
                "Sukses",
                f"Laporan PDF berhasil disimpan di:\n{file_path}"
            )

        except Exception as e:
            messagebox.showerror(
                "Error",
                f"Gagal membuat PDF:\n{str(e)}"
            )

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
