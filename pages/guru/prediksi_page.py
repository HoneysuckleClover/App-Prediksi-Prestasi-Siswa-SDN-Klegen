import customtkinter as ctk
from tkinter import ttk, messagebox

import joblib
import os
from datetime import date

from database.koneksi import connect_db


class PrediksiPage(ctk.CTkFrame):

    def __init__(self, parent):
        super().__init__(parent)

        # =========================
        # LOAD MODEL (FIX PATH)
        # =========================
        try:
            BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
            MODEL_PATH = os.path.join(BASE_DIR, "model", "model_logistic.pkl")

            self.model = joblib.load(MODEL_PATH)    
        except Exception as e:
            messagebox.showerror("Error Model", f"Gagal load model:\n{e}")
            self.model = None

        # =========================
        # TITLE
        # =========================
        ctk.CTkLabel(
            self,
            text="PREDIKSI PRESTASI SISWA",
            font=("Arial", 24, "bold")
        ).pack(pady=10)

        # =========================
        # FORM INPUT
        # =========================
        form = ctk.CTkFrame(self)
        form.pack(fill="x", padx=10, pady=10)

        ctk.CTkLabel(form, text="ID Siswa").grid(row=0, column=0, padx=10, pady=10)

        self.entry_id_siswa = ctk.CTkEntry(form, width=250)
        self.entry_id_siswa.grid(row=0, column=1)

        ctk.CTkButton(
            form,
            text="Prediksi",
            command=self.prediksi
        ).grid(row=0, column=2, padx=10)

        # =========================
        # HASIL LABEL
        # =========================
        self.lbl_hasil = ctk.CTkLabel(
            self,
            text="Belum Ada Prediksi",
            font=("Arial", 20, "bold")
        )
        self.lbl_hasil.pack(pady=20)

        # =========================
        # TABEL HASIL
        # =========================
        columns = (
            "id_prediksi",
            "id_siswa",
            "probabilitas",
            "hasil",
            "tanggal"
        )

        self.table = ttk.Treeview(self, columns=columns, show="headings")

        for col in columns:
            self.table.heading(col, text=col)
            self.table.column(col, width=150)

        self.table.pack(fill="both", expand=True, padx=10, pady=10)

        self.load_data()

    # =================================
    # LOAD DATA
    # =================================
    def load_data(self):

        for item in self.table.get_children():
            self.table.delete(item)

        try:
            conn = connect_db()
            cursor = conn.cursor()

            cursor.execute("""
                SELECT
                    id_prediksi,
                    id_siswa,
                    probabilitas,
                    hasil,
                    tanggal_prediksi
                FROM hasil_prediksi
                ORDER BY id_prediksi DESC
            """)

            rows = cursor.fetchall()

            for row in rows:
                self.table.insert("", "end", values=row)

            conn.close()

        except Exception as e:
            messagebox.showerror("Error Load Data", str(e))

    # =================================
    # PREDIKSI
    # =================================
    def prediksi(self):

        print("DEBUG: tombol prediksi ditekan")

        if self.model is None:
            messagebox.showerror("Error", "Model tidak berhasil dimuat!")
            return

        id_siswa = self.entry_id_siswa.get().strip()

        if not id_siswa:
            messagebox.showwarning("Peringatan", "Masukkan ID Siswa!")
            return

        try:
            conn = connect_db()
            cursor = conn.cursor()

            # =====================
            # NILAI
            # =====================
            cursor.execute("""
                SELECT rata_nilai
                FROM nilai
                WHERE id_siswa=%s
                ORDER BY id_nilai DESC
                LIMIT 1
            """, (id_siswa,))
            nilai = cursor.fetchone()

            # =====================
            # KEHADIRAN
            # =====================
            cursor.execute("""
                SELECT hadir, alpha
                FROM kehadiran
                WHERE id_siswa=%s
                ORDER BY id_kehadiran DESC
                LIMIT 1
            """, (id_siswa,))
            hadir = cursor.fetchone()

            # =====================
            # MOTIVASI
            # =====================
            cursor.execute("""
                SELECT skor_motivasi
                FROM motivasi
                WHERE id_siswa=%s
                ORDER BY id_motivasi DESC
                LIMIT 1
            """, (id_siswa,))
            motivasi = cursor.fetchone()

            # =====================
            # DISIPLIN
            # =====================
            cursor.execute("""
                SELECT skor_disiplin
                FROM disiplin_belajar
                WHERE id_siswa=%s
                ORDER BY id_disiplin DESC
                LIMIT 1
            """, (id_siswa,))
            disiplin = cursor.fetchone()

            conn.close()

            # =====================
            # CEK DATA
            # =====================
            if not nilai or not hadir or not motivasi or not disiplin:
                messagebox.showwarning(
                    "Data Tidak Lengkap",
                    "Data siswa belum lengkap!"
                )
                return

            # =====================
            # FITUR MODEL
            # =====================
            fitur = [[
                float(nilai[0]),
                int(hadir[0]),
                int(hadir[1]),
                int(motivasi[0]),
                int(disiplin[0])
            ]]

            # =====================
            # PREDIKSI
            # =====================
            hasil = self.model.predict(fitur)[0]

            probabilitas = self.model.predict_proba(fitur)[0][1] * 100

            status = "Berisiko" if hasil == 1 else "Tidak Berisiko"

            # =====================
            # UPDATE UI
            # =====================
            self.lbl_hasil.configure(
                text=f"Hasil Prediksi : {status}\nProbabilitas : {probabilitas:.2f}%"
            )

            # =====================
            # SIMPAN HASIL
            # =====================
            conn = connect_db()
            cursor = conn.cursor()

            cursor.execute("""
                INSERT INTO hasil_prediksi
                (id_siswa, probabilitas, hasil, tanggal_prediksi)
                VALUES (%s,%s,%s,%s)
            """, (
                id_siswa,
                round(probabilitas, 2),
                status,
                date.today()
            ))

            conn.commit()
            conn.close()

            # =====================
            # REFRESH TABLE
            # =====================
            self.load_data()

            messagebox.showinfo("Sukses", "Prediksi berhasil dilakukan")

        except Exception as e:
            print("ERROR:", e)
            messagebox.showerror("Error", str(e))