import customtkinter as ctk
from tkinter import ttk, messagebox

from database.koneksi import connect_db


class KehadiranPage(ctk.CTkFrame):

    def __init__(self, parent):
        super().__init__(parent)

        self.id_kehadiran = None
        self.data_siswa = {}

        # =====================
        # JUDUL
        # =====================

        ctk.CTkLabel(
            self,
            text="DATA KEHADIRAN",
            font=("Arial", 24, "bold")
        ).pack(pady=10)

        # =====================
        # FORM
        # =====================

        form = ctk.CTkFrame(self)
        form.pack(fill="x", padx=10, pady=10)

        ctk.CTkLabel(
            form,
            text="Siswa"
        ).grid(row=0, column=0, padx=10, pady=10)

        self.combo_siswa = ctk.CTkOptionMenu(
            form,
            values=["Pilih Siswa"]
        )
        self.combo_siswa.grid(row=0, column=1)

        ctk.CTkLabel(
            form,
            text="Semester"
        ).grid(row=1, column=0, padx=10, pady=10)

        self.entry_semester = ctk.CTkEntry(
            form,
            width=200
        )
        self.entry_semester.grid(row=1, column=1)

        ctk.CTkLabel(
            form,
            text="Hadir"
        ).grid(row=0, column=2, padx=10)

        self.entry_hadir = ctk.CTkEntry(
            form,
            width=120
        )
        self.entry_hadir.grid(row=0, column=3)

        ctk.CTkLabel(
            form,
            text="Sakit"
        ).grid(row=1, column=2, padx=10)

        self.entry_sakit = ctk.CTkEntry(
            form,
            width=120
        )
        self.entry_sakit.grid(row=1, column=3)

        ctk.CTkLabel(
            form,
            text="Izin"
        ).grid(row=0, column=4, padx=10)

        self.entry_izin = ctk.CTkEntry(
            form,
            width=120
        )
        self.entry_izin.grid(row=0, column=5)

        ctk.CTkLabel(
            form,
            text="Alpha"
        ).grid(row=1, column=4, padx=10)

        self.entry_alpha = ctk.CTkEntry(
            form,
            width=120
        )
        self.entry_alpha.grid(row=1, column=5)

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
            "nama",
            "semester",
            "hadir",
            "sakit",
            "izin",
            "alpha"
        )

        self.table = ttk.Treeview(
            table_frame,
            columns=columns,
            show="headings"
        )

        for col in columns:
            self.table.heading(col, text=col.upper())

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
                SELECT id_siswa,nama_siswa
                FROM siswa
                ORDER BY nama_siswa
            """)

            data = cursor.fetchall()

            self.data_siswa = {}

            nama_siswa = []

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

        conn = connect_db()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT
                k.id_kehadiran,
                s.nama_siswa,
                k.semester,
                k.hadir,
                k.sakit,
                k.izin,
                k.alpha
            FROM kehadiran k
            JOIN siswa s
            ON k.id_siswa = s.id_siswa
        """)

        data = cursor.fetchall()

        for row in data:
            self.table.insert(
                "",
                "end",
                values=row
            )

        conn.close()

    # =====================
    # TAMBAH
    # =====================

    def tambah_data(self):

        try:

            nama = self.combo_siswa.get()
            id_siswa = self.data_siswa[nama]

            conn = connect_db()
            cursor = conn.cursor()

            cursor.execute("""
                INSERT INTO kehadiran
                (
                    id_siswa,
                    semester,
                    hadir,
                    sakit,
                    izin,
                    alpha
                )
                VALUES (%s,%s,%s,%s,%s,%s)
            """, (
                id_siswa,
                self.entry_semester.get(),
                self.entry_hadir.get(),
                self.entry_sakit.get(),
                self.entry_izin.get(),
                self.entry_alpha.get()
            ))

            conn.commit()
            conn.close()

            messagebox.showinfo(
                "Sukses",
                "Data berhasil ditambahkan"
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

        self.id_kehadiran = data[0]

        self.combo_siswa.set(data[1])

        self.entry_semester.delete(0, "end")
        self.entry_semester.insert(0, data[2])

        self.entry_hadir.delete(0, "end")
        self.entry_hadir.insert(0, data[3])

        self.entry_sakit.delete(0, "end")
        self.entry_sakit.insert(0, data[4])

        self.entry_izin.delete(0, "end")
        self.entry_izin.insert(0, data[5])

        self.entry_alpha.delete(0, "end")
        self.entry_alpha.insert(0, data[6])

    # =====================
    # EDIT
    # =====================

    def edit_data(self):
        messagebox.showinfo(
            "Info",
            "Fitur edit siap ditambahkan"
        )

    # =====================
    # HAPUS
    # =====================

    def hapus_data(self):
        messagebox.showinfo(
            "Info",
            "Fitur hapus siap ditambahkan"
        )

    # =====================
    # CARI
    # =====================

    def cari_data(self):
        pass

    # =====================
    # RESET
    # =====================

    def reset_form(self):

        self.id_kehadiran = None

        self.entry_semester.delete(0, "end")
        self.entry_hadir.delete(0, "end")
        self.entry_sakit.delete(0, "end")
        self.entry_izin.delete(0, "end")
        self.entry_alpha.delete(0, "end")