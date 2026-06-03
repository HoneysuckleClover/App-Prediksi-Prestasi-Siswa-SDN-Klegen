import customtkinter as ctk
from tkinter import ttk, messagebox

from database.koneksi import connect_db


class HasilPage(ctk.CTkFrame):

    def __init__(self, parent):
        super().__init__(parent)

        ctk.CTkLabel(
            self,
            text="HASIL PREDIKSI SISWA",
            font=("Arial", 24, "bold")
        ).pack(pady=10)

        # ==========================
        # SEARCH
        # ==========================

        search_frame = ctk.CTkFrame(self)
        search_frame.pack(fill="x", padx=10, pady=10)

        self.entry_search = ctk.CTkEntry(
            search_frame,
            placeholder_text="Cari Nama Siswa..."
        )
        self.entry_search.pack(
            side="left",
            padx=5,
            pady=5
        )

        ctk.CTkButton(
            search_frame,
            text="Cari",
            command=self.cari_data
        ).pack(side="left", padx=5)

        ctk.CTkButton(
            search_frame,
            text="Refresh",
            command=self.load_data
        ).pack(side="left", padx=5)

        # ==========================
        # TABEL
        # ==========================

        table_frame = ctk.CTkFrame(self)
        table_frame.pack(
            fill="both",
            expand=True,
            padx=10,
            pady=10
        )

        columns = (
            "id_prediksi",
            "nama_siswa",
            "kelas",
            "probabilitas",
            "hasil",
            "tanggal"
        )

        self.table = ttk.Treeview(
            table_frame,
            columns=columns,
            show="headings"
        )

        self.table.heading(
            "id_prediksi",
            text="ID Prediksi"
        )

        self.table.heading(
            "nama_siswa",
            text="Nama Siswa"
        )

        self.table.heading(
            "kelas",
            text="Kelas"
        )

        self.table.heading(
            "probabilitas",
            text="Probabilitas (%)"
        )

        self.table.heading(
            "hasil",
            text="Hasil Prediksi"
        )

        self.table.heading(
            "tanggal",
            text="Tanggal Prediksi"
        )

        self.table.column(
            "id_prediksi",
            width=100
        )

        self.table.column(
            "nama_siswa",
            width=250
        )

        self.table.column(
            "kelas",
            width=120
        )

        self.table.column(
            "probabilitas",
            width=120
        )

        self.table.column(
            "hasil",
            width=150
        )

        self.table.column(
            "tanggal",
            width=150
        )

        self.table.pack(
            fill="both",
            expand=True
        )

        self.load_data()

    # ==================================
    # LOAD DATA
    # ==================================

    def load_data(self):

        for row in self.table.get_children():
            self.table.delete(row)

        try:

            conn = connect_db()
            cursor = conn.cursor()

            cursor.execute("""
                SELECT
                    hp.id_prediksi,
                    s.nama_siswa,
                    k.nama_kelas,
                    hp.probabilitas,
                    hp.hasil,
                    hp.tanggal_prediksi
                FROM hasil_prediksi hp
                JOIN siswa s
                    ON hp.id_siswa = s.id_siswa
                JOIN kelas k
                    ON s.id_kelas = k.id_kelas
                ORDER BY hp.id_prediksi DESC
            """)

            data = cursor.fetchall()

            for row in data:

                self.table.insert(
                    "",
                    "end",
                    values=row
                )

            conn.close()

        except Exception as e:

            messagebox.showerror(
                "Error",
                str(e)
            )

    # ==================================
    # CARI DATA
    # ==================================

    def cari_data(self):

        keyword = self.entry_search.get()

        for row in self.table.get_children():
            self.table.delete(row)

        try:

            conn = connect_db()
            cursor = conn.cursor()

            cursor.execute("""
                SELECT
                    hp.id_prediksi,
                    s.nama_siswa,
                    k.nama_kelas,
                    hp.probabilitas,
                    hp.hasil,
                    hp.tanggal_prediksi
                FROM hasil_prediksi hp
                JOIN siswa s
                    ON hp.id_siswa = s.id_siswa
                JOIN kelas k
                    ON s.id_kelas = k.id_kelas
                WHERE s.nama_siswa LIKE %s
                ORDER BY hp.id_prediksi DESC
            """, (
                f"%{keyword}%",
            ))

            data = cursor.fetchall()

            for row in data:

                self.table.insert(
                    "",
                    "end",
                    values=row
                )

            conn.close()

        except Exception as e:

            messagebox.showerror(
                "Error",
                str(e)
            )