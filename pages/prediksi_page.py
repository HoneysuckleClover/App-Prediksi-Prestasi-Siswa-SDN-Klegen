import customtkinter as ctk
from tkinter import ttk, messagebox
import mysql.connector
import joblib
import numpy as np
import os

# =========================
# LOAD MODEL
# =========================

model_path = os.path.join("models", "model_logistic.pkl")

try:
    model = joblib.load(model_path)

except Exception as e:

    messagebox.showerror(
        "Error Model",
        f"Gagal load model:\n{e}"
    )

# =========================
# KONEKSI DATABASE
# =========================

conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="db_deteksi_prestasi"
)


class PrediksiPage(ctk.CTk):

    def __init__(self):
        super().__init__()

        self.title("Prediksi Risiko Siswa")
        self.geometry("750x600")

        # =========================
        # TITLE
        # =========================

        title = ctk.CTkLabel(
            self,
            text="Prediksi Risiko Siswa",
            font=("Arial", 24, "bold")
        )

        title.pack(pady=20)

        # =========================
        # PILIH SISWA
        # =========================

        self.combo_siswa = ctk.CTkComboBox(
            self,
            values=[],
            width=300
        )

        self.combo_siswa.pack(pady=10)

        self.load_siswa()

        # =========================
        # BUTTON
        # =========================

        btn_prediksi = ctk.CTkButton(
            self,
            text="Prediksi",
            command=self.prediksi
        )

        btn_prediksi.pack(pady=15)

        # =========================
        # HASIL
        # =========================

        self.label_hasil = ctk.CTkLabel(
            self,
            text="-",
            font=("Arial", 30, "bold")
        )

        self.label_hasil.pack(pady=20)

        # =========================
        # TABLE
        # =========================

        self.table = ttk.Treeview(
            self,
            columns=("fitur", "nilai"),
            show="headings",
            height=6
        )

        self.table.heading("fitur", text="Feature")
        self.table.heading("nilai", text="Nilai")

        self.table.column("fitur", width=250)
        self.table.column("nilai", width=200)

        self.table.pack(pady=20)

    # =========================
    # LOAD SISWA
    # =========================

    def load_siswa(self):

        cursor = conn.cursor()

        query = """
            SELECT id_siswa, nama_siswa
            FROM siswa
        """

        cursor.execute(query)

        rows = cursor.fetchall()

        self.siswa_map = {}

        siswa_list = []

        for row in rows:

            siswa_id = row[0]
            nama = row[1]

            siswa_list.append(nama)

            self.siswa_map[nama] = siswa_id

        self.combo_siswa.configure(values=siswa_list)

        if siswa_list:
            self.combo_siswa.set(siswa_list[0])

        cursor.close()

    # =========================
    # PREDIKSI
    # =========================

    def prediksi(self):

        # HAPUS DATA TABLE SEBELUMNYA

        for item in self.table.get_children():
            self.table.delete(item)

        nama_siswa = self.combo_siswa.get()

        if nama_siswa == "":

            messagebox.showwarning(
                "Warning",
                "Pilih siswa terlebih dahulu"
            )

            return

        id_siswa = self.siswa_map.get(nama_siswa)

        cursor = conn.cursor()

        query = """
            SELECT
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

            WHERE siswa.id_siswa = %s
        """

        cursor.execute(query, (id_siswa,))

        data = cursor.fetchone()

        if data is None:

            messagebox.showerror(
                "Error",
                "Data siswa belum lengkap"
            )

            cursor.close()
            return

        try:

            rata_nilai = float(data[0])
            hadir = float(data[1])
            alpha = float(data[2])
            motivasi = float(data[3])
            disiplin = float(data[4])

            # =========================
            # TAMPILKAN DETAIL
            # =========================

            details = [
                ("Rata-rata Nilai", rata_nilai),
                ("Hadir", hadir),
                ("Alpha", alpha),
                ("Motivasi", motivasi),
                ("Disiplin", disiplin)
            ]

            for item in details:
                self.table.insert("", "end", values=item)

            # =========================
            # FITUR MODEL
            # =========================

            fitur = np.array([
                [
                    rata_nilai,
                    hadir,
                    alpha,
                    motivasi,
                    disiplin
                ]
            ])

            # =========================
            # PREDIKSI MODEL
            # =========================

            hasil = model.predict(fitur)

            # Probabilitas Logistic Regression
            probabilitas = model.predict_proba(fitur)[0][1]

            # =========================
            # HASIL LABEL
            # =========================

            if hasil[0] == 1:

                hasil_label = "Berisiko"

                self.label_hasil.configure(
                    text=hasil_label,
                    text_color="red"
                )

                status_risiko = 1

            else:

                hasil_label = "Tidak Berisiko"

                self.label_hasil.configure(
                    text=hasil_label,
                    text_color="green"
                )

                status_risiko = 0

            # =========================
            # UPDATE STATUS RISIKO
            # =========================

            update_query = """
                UPDATE siswa
                SET status_risiko = %s
                WHERE id_siswa = %s
            """

            cursor.execute(
                update_query,
                (status_risiko, id_siswa)
            )

            # =========================
            # SIMPAN HASIL PREDIKSI
            # =========================

            simpan_query = """
                INSERT INTO hasil_prediksi
                (id_siswa, probabilitas, hasil)
                VALUES (%s, %s, %s)
            """

            cursor.execute(
                simpan_query,
                (
                    id_siswa,
                    float(probabilitas),
                    hasil_label
                )
            )

            conn.commit()

            # =========================
            # INFO HASIL
            # =========================

            messagebox.showinfo(
                "Sukses",
                f"""
Hasil Prediksi : {hasil_label}

Probabilitas Risiko :
{probabilitas:.2f}
                """
            )

        except Exception as e:

            messagebox.showerror(
                "Error Prediksi",
                f"{e}"
            )

        cursor.close()


if __name__ == "__main__":

    app = PrediksiPage()
    app.mainloop()