import customtkinter as ctk
from tkinter import ttk, messagebox

from database.koneksi import connect_db


class MotivasiPage(ctk.CTkFrame):

    def __init__(self, parent):
        super().__init__(parent)

        self.id_motivasi = None
        self.data_siswa = {}

        # =====================
        # JUDUL
        # =====================

        ctk.CTkLabel(
            self,
            text="DATA MOTIVASI",
            font=("Arial", 24, "bold")
        ).pack(pady=10)

        # =====================
        # FORM
        # =====================

        form_frame = ctk.CTkFrame(self)
        form_frame.pack(fill="x", padx=10, pady=10)

        ctk.CTkLabel(
            form_frame,
            text="Nama Siswa"
        ).grid(row=0, column=0, padx=10, pady=10)

        self.combo_siswa = ctk.CTkOptionMenu(
            form_frame,
            values=["Pilih Siswa"]
        )
        self.combo_siswa.grid(row=0, column=1)

        ctk.CTkLabel(
            form_frame,
            text="Semester"
        ).grid(row=1, column=0, padx=10, pady=10)

        self.entry_semester = ctk.CTkEntry(
            form_frame,
            width=200
        )
        self.entry_semester.grid(row=1, column=1)

        ctk.CTkLabel(
            form_frame,
            text="Skor Motivasi"
        ).grid(row=0, column=2, padx=10)

        self.entry_skor = ctk.CTkEntry(
            form_frame,
            width=200
        )
        self.entry_skor.grid(row=0, column=3)

        # =====================
        # BUTTON
        # =====================

        btn_frame = ctk.CTkFrame(self)
        btn_frame.pack(fill="x", padx=10)

        ctk.CTkButton(
            btn_frame,
            text="Tambah",
            command=self.tambah_data
        ).pack(side="left", padx=5)

        ctk.CTkButton(
            btn_frame,
            text="Edit",
            command=self.edit_data
        ).pack(side="left", padx=5)

        ctk.CTkButton(
            btn_frame,
            text="Hapus",
            command=self.hapus_data
        ).pack(side="left", padx=5)

        ctk.CTkButton(
            btn_frame,
            text="Reset",
            command=self.reset_form
        ).pack(side="left", padx=5)

        # =====================
        # SEARCH
        # =====================

        search_frame = ctk.CTkFrame(self)
        search_frame.pack(fill="x", padx=10, pady=10)

        self.entry_search = ctk.CTkEntry(
            search_frame,
            placeholder_text="Cari Nama Siswa..."
        )
        self.entry_search.pack(side="left", padx=5)

        ctk.CTkButton(
            search_frame,
            text="Cari",
            command=self.cari_data
        ).pack(side="left")

        ctk.CTkButton(
            search_frame,
            text="Refresh",
            command=self.load_data
        ).pack(side="left", padx=5)

        # =====================
        # TABLE
        # =====================

        table_frame = ctk.CTkFrame(self)
        table_frame.pack(
            fill="both",
            expand=True,
            padx=10,
            pady=10
        )

        columns = (
            "id",
            "nama_siswa",
            "semester",
            "skor_motivasi"
        )

        self.table = ttk.Treeview(
            table_frame,
            columns=columns,
            show="headings"
        )

        self.table.heading("id", text="ID")
        self.table.heading("nama_siswa", text="Nama Siswa")
        self.table.heading("semester", text="Semester")
        self.table.heading("skor_motivasi", text="Skor Motivasi")

        self.table.pack(
            fill="both",
            expand=True
        )

        self.table.bind(
            "<<TreeviewSelect>>",
            self.pilih_data
        )

        self.load_siswa()
        self.load_data()

    # =====================
    # LOAD SISWA
    # =====================

    def load_siswa(self):

        try:

            conn = connect_db()
            cursor = conn.cursor()

            cursor.execute("""
                SELECT id_siswa, nama_siswa
                FROM siswa
                ORDER BY nama_siswa
            """)

            data = cursor.fetchall()

            nama_siswa = []
            self.data_siswa = {}

            for row in data:
                self.data_siswa[row[1]] = row[0]
                nama_siswa.append(row[1])

            self.combo_siswa.configure(
                values=nama_siswa
            )

            conn.close()

        except Exception as e:
            messagebox.showerror(
                "Error",
                str(e)
            )

    # =====================
    # LOAD DATA
    # =====================

    def load_data(self):

        for row in self.table.get_children():
            self.table.delete(row)

        try:

            conn = connect_db()
            cursor = conn.cursor()

            cursor.execute("""
                SELECT
                    m.id_motivasi,
                    s.nama_siswa,
                    m.semester,
                    m.skor_motivasi
                FROM motivasi m
                JOIN siswa s
                ON m.id_siswa = s.id_siswa
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

    # =====================
    # TAMBAH
    # =====================

    def tambah_data(self):

        try:

            id_siswa = self.data_siswa[
                self.combo_siswa.get()
            ]

            conn = connect_db()
            cursor = conn.cursor()

            cursor.execute("""
                INSERT INTO motivasi
                (
                    id_siswa,
                    semester,
                    skor_motivasi
                )
                VALUES (%s,%s,%s)
            """, (
                id_siswa,
                self.entry_semester.get(),
                self.entry_skor.get()
            ))

            conn.commit()
            conn.close()

            messagebox.showinfo(
                "Sukses",
                "Data motivasi berhasil ditambahkan"
            )

            self.load_data()
            self.reset_form()

        except Exception as e:
            messagebox.showerror(
                "Error",
                str(e)
            )

    # =====================
    # PILIH DATA
    # =====================

    def pilih_data(self, event):

        selected = self.table.focus()

        data = self.table.item(
            selected,
            "values"
        )

        if not data:
            return

        self.id_motivasi = data[0]

        self.combo_siswa.set(data[1])

        self.entry_semester.delete(0, "end")
        self.entry_semester.insert(0, data[2])

        self.entry_skor.delete(0, "end")
        self.entry_skor.insert(0, data[3])

    # =====================
    # EDIT
    # =====================

    def edit_data(self):

        if not self.id_motivasi:
            return

        try:

            id_siswa = self.data_siswa[
                self.combo_siswa.get()
            ]

            conn = connect_db()
            cursor = conn.cursor()

            cursor.execute("""
                UPDATE motivasi
                SET
                    id_siswa=%s,
                    semester=%s,
                    skor_motivasi=%s
                WHERE id_motivasi=%s
            """, (
                id_siswa,
                self.entry_semester.get(),
                self.entry_skor.get(),
                self.id_motivasi
            ))

            conn.commit()
            conn.close()

            messagebox.showinfo(
                "Sukses",
                "Data berhasil diupdate"
            )

            self.load_data()

        except Exception as e:
            messagebox.showerror(
                "Error",
                str(e)
            )

    # =====================
    # HAPUS
    # =====================

    def hapus_data(self):

        if not self.id_motivasi:
            return

        try:

            conn = connect_db()
            cursor = conn.cursor()

            cursor.execute(
                "DELETE FROM motivasi WHERE id_motivasi=%s",
                (self.id_motivasi,)
            )

            conn.commit()
            conn.close()

            messagebox.showinfo(
                "Sukses",
                "Data berhasil dihapus"
            )

            self.load_data()
            self.reset_form()

        except Exception as e:
            messagebox.showerror(
                "Error",
                str(e)
            )

    # =====================
    # CARI
    # =====================

    def cari_data(self):

        keyword = self.entry_search.get()

        for row in self.table.get_children():
            self.table.delete(row)

        try:

            conn = connect_db()
            cursor = conn.cursor()

            cursor.execute("""
                SELECT
                    m.id_motivasi,
                    s.nama_siswa,
                    m.semester,
                    m.skor_motivasi
                FROM motivasi m
                JOIN siswa s
                ON m.id_siswa = s.id_siswa
                WHERE s.nama_siswa LIKE %s
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

    # =====================
    # RESET
    # =====================

    def reset_form(self):

        self.id_motivasi = None

        self.entry_semester.delete(0, "end")
        self.entry_skor.delete(0, "end")