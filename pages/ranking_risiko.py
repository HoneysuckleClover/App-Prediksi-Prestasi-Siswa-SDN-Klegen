import customtkinter as ctk
from tkinter import ttk
import mysql.connector
import joblib
import numpy as np


# =========================
# LOAD MODEL
# =========================

model = joblib.load(
    "models/model_logistic.pkl"
)


class RankingRisikoPage(ctk.CTk):

    def __init__(self):
        super().__init__()

        self.title("Ranking Risiko Siswa")
        self.geometry("950x550")

        ctk.CTkLabel(
            self,
            text="RANKING RISIKO SISWA",
            font=("Arial", 26, "bold")
        ).pack(pady=20)

        # =========================
        # TABLE
        # =========================

        self.table = ttk.Treeview(
            self,
            columns=(
                "ranking",
                "nama",
                "probabilitas",
                "kategori"
            ),
            show="headings"
        )

        self.table.heading(
            "ranking",
            text="Ranking"
        )

        self.table.heading(
            "nama",
            text="Nama Siswa"
        )

        self.table.heading(
            "probabilitas",
            text="Probabilitas Risiko"
        )

        self.table.heading(
            "kategori",
            text="Kategori"
        )

        self.table.pack(
            fill="both",
            expand=True,
            pady=20
        )

        self.load_ranking()

    # =========================
    # LOAD RANKING
    # =========================

    def load_ranking(self):

        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="db_deteksi_prestasi"
        )

        cursor = conn.cursor()

        query = """
            SELECT
                siswa.nama_siswa,
                nilai.rata_nilai,
                kehadiran.hadir,
                kehadiran.alpha,
                motivasi.skor_motivasi,
                disiplin.skor_disiplin

            FROM siswa

            JOIN nilai
            ON siswa.id_siswa = nilai.id_siswa

            JOIN kehadiran
            ON siswa.id_siswa = kehadiran.id_siswa

            JOIN motivasi
            ON siswa.id_siswa = motivasi.id_siswa

            JOIN disiplin
            ON siswa.id_siswa = disiplin.id_siswa
        """

        cursor.execute(query)

        rows = cursor.fetchall()

        hasil_ranking = []

        # =========================
        # PREDIKSI PROBABILITAS
        # =========================

        for row in rows:

            nama = row[0]

            fitur = np.array([
                [
                    row[1],
                    row[2],
                    row[3],
                    row[4],
                    row[5]
                ]
            ])

            probabilitas = model.predict_proba(
                fitur
            )[0][1]

            persen = round(
                probabilitas * 100,
                2
            )

            # =========================
            # KATEGORI
            # =========================

            if persen >= 75:
                kategori = "Tinggi"

            elif persen >= 50:
                kategori = "Sedang"

            else:
                kategori = "Rendah"

            hasil_ranking.append(
                (
                    nama,
                    persen,
                    kategori
                )
            )

        # =========================
        # SORTING
        # =========================

        hasil_ranking.sort(
            key=lambda x: x[1],
            reverse=True
        )

        # =========================
        # TAMPILKAN
        # =========================

        no = 1

        for item in hasil_ranking:

            self.table.insert(
                "",
                "end",
                values=(
                    no,
                    item[0],
                    f"{item[1]}%",
                    item[2]
                )
            )

            no += 1

        cursor.close()
        conn.close()


if __name__ == "__main__":
    app = RankingRisikoPage()
    app.mainloop()
