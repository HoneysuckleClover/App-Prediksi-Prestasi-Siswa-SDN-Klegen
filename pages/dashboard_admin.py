import customtkinter as ctk
import mysql.connector
import matplotlib.pyplot as plt

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

from pages.siswa_page import SiswaPage
from pages.nilai_page import NilaiPage
from pages.kehadiran_page import KehadiranPage
from pages.motivasi_page import MotivasiPage
from pages.disiplin_page import DisiplinPage
from pages.prediksi_page import PrediksiPage
from pages.riwayat_prediksi_page import RiwayatPrediksiPage
from pages.ranking_risiko import RankingRisikoPage



class DashboardAdmin(ctk.CTk):

    def __init__(self):
        super().__init__()

        self.title("Dashboard Admin")
        self.geometry("1000x700")

        # =========================
        # JUDUL
        # =========================

        ctk.CTkLabel(
            self,
            text="DASHBOARD ADMIN",
            font=("Arial", 28, "bold")
        ).pack(pady=20)

        # =========================
        # KONEKSI DATABASE
        # =========================

        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="db_deteksi_prestasi"
        )

        cursor = conn.cursor()

        # =========================
        # TOTAL SISWA
        # =========================

        cursor.execute("SELECT COUNT(*) FROM siswa")
        total_siswa = cursor.fetchone()[0]

        # =========================
        # SISWA BERISIKO
        # =========================

        cursor.execute("""
            SELECT COUNT(*)
            FROM siswa
            WHERE status_risiko = 1
        """)

        total_risiko = cursor.fetchone()[0]

        # =========================
        # TIDAK BERISIKO
        # =========================

        cursor.execute("""
            SELECT COUNT(*)
            FROM siswa
            WHERE status_risiko = 0
        """)

        total_tidak = cursor.fetchone()[0]

        # =========================
        # FRAME STATISTIK
        # =========================

        stat_frame = ctk.CTkFrame(self)
        stat_frame.pack(pady=20)

        # TOTAL SISWA

        total_box = ctk.CTkFrame(stat_frame)
        total_box.grid(row=0, column=0, padx=15)

        ctk.CTkLabel(
            total_box,
            text="Total Siswa",
            font=("Arial", 18, "bold")
        ).pack(pady=10, padx=30)

        ctk.CTkLabel(
            total_box,
            text=str(total_siswa),
            font=("Arial", 32, "bold"),
            text_color="cyan"
        ).pack(pady=10)

        # SISWA BERISIKO

        risiko_box = ctk.CTkFrame(stat_frame)
        risiko_box.grid(row=0, column=1, padx=15)

        ctk.CTkLabel(
            risiko_box,
            text="Siswa Berisiko",
            font=("Arial", 18, "bold")
        ).pack(pady=10, padx=30)

        ctk.CTkLabel(
            risiko_box,
            text=str(total_risiko),
            font=("Arial", 32, "bold"),
            text_color="red"
        ).pack(pady=10)

        # TIDAK BERISIKO

        tidak_box = ctk.CTkFrame(stat_frame)
        tidak_box.grid(row=0, column=2, padx=15)

        ctk.CTkLabel(
            tidak_box,
            text="Tidak Berisiko",
            font=("Arial", 18, "bold")
        ).pack(pady=10, padx=30)

        ctk.CTkLabel(
            tidak_box,
            text=str(total_tidak),
            font=("Arial", 32, "bold"),
            text_color="green"
        ).pack(pady=10)

        # =========================
        # GRAFIK
        # =========================

        fig, ax = plt.subplots(figsize=(5, 4))

        kategori = [
            "Berisiko",
            "Tidak Berisiko"
        ]

        jumlah = [
            total_risiko,
            total_tidak
        ]

        warna = [
            "red",
            "green"
        ]

        ax.bar(kategori, jumlah, color=warna)

        ax.set_title("Grafik Risiko Siswa")
        ax.set_ylabel("Jumlah Siswa")

        canvas = FigureCanvasTkAgg(fig, master=self)

        canvas.draw()

        canvas.get_tk_widget().pack(pady=20)

        # =========================
        # MENU BUTTON
        # =========================

        menu_frame = ctk.CTkFrame(self)
        menu_frame.pack(pady=20)

        ctk.CTkButton(
            menu_frame,
            text="Data Siswa",
            width=200,
            command=self.open_siswa
        ).grid(row=0, column=0, padx=10, pady=10)

        ctk.CTkButton(
            menu_frame,
            text="Data Nilai",
            width=200,
            command=self.open_nilai
        ).grid(row=0, column=1, padx=10, pady=10)

        ctk.CTkButton(
            menu_frame,
            text="Data Kehadiran",
            width=200,
            command=self.open_kehadiran
        ).grid(row=1, column=0, padx=10, pady=10)

        ctk.CTkButton(
            menu_frame,
            text="Data Motivasi",
            width=200,
            command=self.open_motivasi
        ).grid(row=1, column=1, padx=10, pady=10)

        ctk.CTkButton(
            menu_frame,
            text="Data Disiplin",
            width=200,
            command=self.open_disiplin
        ).grid(row=2, column=0, padx=10, pady=10)

        ctk.CTkButton(
            menu_frame,
            text="Prediksi Risiko",
            width=200,
            command=self.open_prediksi
        ).grid(row=2, column=1, padx=10, pady=10)
        
        ctk.CTkButton(
            menu_frame,
            text="Riwayat Prediksi",
            width=200,
            command=self.open_riwayat
        ).grid(row=3, column=0, padx=10, pady=10)

        ctk.CTkButton(
            menu_frame,
            text="Ranking Risiko",
            width=200,
            command=self.open_ranking
        ).grid(row=3, column=1, padx=10, pady=10)


        # TUTUP KONEKSI

        cursor.close()
        conn.close()

    # =========================
    # OPEN PAGE
    # =========================

    def open_siswa(self):
        app = SiswaPage()
        app.mainloop()

    def open_nilai(self):
        app = NilaiPage()
        app.mainloop()

    def open_kehadiran(self):
        app = KehadiranPage()
        app.mainloop()

    def open_motivasi(self):
        app = MotivasiPage()
        app.mainloop()

    def open_disiplin(self):
        app = DisiplinPage()
        app.mainloop()

    def open_prediksi(self):
        app = PrediksiPage()
        app.mainloop()
        
    def open_riwayat(self):
        app = RiwayatPrediksiPage()
        app.mainloop()
        
    def open_ranking(self):
        app = RankingRisikoPage()
        app.mainloop()




if __name__ == "__main__":
    app = DashboardAdmin()
    app.mainloop()