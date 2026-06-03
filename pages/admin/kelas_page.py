import customtkinter as ctk
from tkinter import ttk, messagebox

from database.koneksi import connect_db


class KelasPage(ctk.CTkFrame):

    def __init__(self, parent=None):
        super().__init__(parent)

        self.id_kelas = None
        self.user_dict = {}

        # ======================
        # FORM
        # ======================

        form_frame = ctk.CTkFrame(self)
        form_frame.pack(fill="x", padx=10, pady=10)

        ctk.CTkLabel(
            form_frame,
            text="Guru/Wali Kelas"
        ).grid(row=0, column=0, padx=10, pady=10)

        self.combo_user = ctk.CTkOptionMenu(
            form_frame,
            values=["Pilih Guru"]
        )
        self.combo_user.grid(row=0, column=1)

        ctk.CTkLabel(
            form_frame,
            text="Nama Kelas"
        ).grid(row=1, column=0, padx=10, pady=10)

        self.entry_kelas = ctk.CTkEntry(
            form_frame,
            width=250
        )
        self.entry_kelas.grid(row=1, column=1)

        ctk.CTkLabel(
            form_frame,
            text="Tahun Ajaran"
        ).grid(row=0, column=2, padx=10)

        self.entry_tahun = ctk.CTkEntry(
            form_frame,
            width=250,
            placeholder_text="2025/2026"
        )
        self.entry_tahun.grid(row=0, column=3)

        ctk.CTkLabel(
            form_frame,
            text="Semester"
        ).grid(row=1, column=2, padx=10)

        self.combo_semester = ctk.CTkOptionMenu(
            form_frame,
            values=[
                "Ganjil",
                "Genap"
            ]
        )
        self.combo_semester.grid(row=1, column=3)

        # ======================
        # BUTTON
        # ======================

        btn_frame = ctk.CTkFrame(self)
        btn_frame.pack(fill="x", padx=10)

        ctk.CTkButton(
            btn_frame,
            text="Tambah",
            command=self.tambah_kelas
        ).pack(side="left", padx=5)

        ctk.CTkButton(
            btn_frame,
            text="Edit",
            command=self.edit_kelas
        ).pack(side="left", padx=5)

        ctk.CTkButton(
            btn_frame,
            text="Hapus",
            command=self.hapus_kelas
        ).pack(side="left", padx=5)

        ctk.CTkButton(
            btn_frame,
            text="Reset",
            command=self.reset_form
        ).pack(side="left", padx=5)

        # ======================
        # TABLE
        # ======================

        table_frame = ctk.CTkFrame(self)
        table_frame.pack(
            fill="both",
            expand=True,
            padx=10,
            pady=10
        )

        columns = (
            "id",
            "guru",
            "kelas",
            "tahun",
            "semester"
        )

        self.table = ttk.Treeview(
            table_frame,
            columns=columns,
            show="headings"
        )

        self.table.heading("id", text="ID")
        self.table.heading("guru", text="Guru")
        self.table.heading("kelas", text="Kelas")
        self.table.heading("tahun", text="Tahun Ajaran")
        self.table.heading("semester", text="Semester")

        self.table.pack(
            fill="both",
            expand=True
        )

        self.table.bind(
            "<<TreeviewSelect>>",
            self.pilih_data
        )

        self.load_guru()
        self.load_data()

    # ======================
    # LOAD GURU
    # ======================

    def load_guru(self):

        conn = connect_db()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT id_user,nama
            FROM users
            WHERE role='guru'
        """)

        data = cursor.fetchall()

        list_guru = []

        self.user_dict.clear()

        for row in data:

            self.user_dict[row[1]] = row[0]
            list_guru.append(row[1])

        if list_guru:
            self.combo_user.configure(
                values=list_guru
            )

            self.combo_user.set(
                list_guru[0]
            )

        conn.close()

    # ======================
    # LOAD DATA
    # ======================

    def load_data(self):

        for row in self.table.get_children():
            self.table.delete(row)

        conn = connect_db()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT
                k.id_kelas,
                u.nama,
                k.nama_kelas,
                k.tahun_ajaran,
                k.semester
            FROM kelas k
            LEFT JOIN users u
            ON k.id_user=u.id_user
        """)

        data = cursor.fetchall()

        for row in data:
            self.table.insert(
                "",
                "end",
                values=row
            )

        conn.close()

    # ======================
    # TAMBAH
    # ======================

    def tambah_kelas(self):

        try:

            guru = self.combo_user.get()
            id_user = self.user_dict[guru]

            conn = connect_db()
            cursor = conn.cursor()

            cursor.execute("""
                INSERT INTO kelas
                (
                    id_user,
                    nama_kelas,
                    tahun_ajaran,
                    semester
                )
                VALUES (%s,%s,%s,%s)
            """, (
                id_user,
                self.entry_kelas.get(),
                self.entry_tahun.get(),
                self.combo_semester.get()
            ))

            conn.commit()
            conn.close()

            messagebox.showinfo(
                "Sukses",
                "Data kelas berhasil ditambahkan"
            )

            self.load_data()
            self.reset_form()

        except Exception as e:
            messagebox.showerror(
                "Error",
                str(e)
            )

    # ======================
    # PILIH DATA
    # ======================

    def pilih_data(self, event):

        selected = self.table.focus()

        data = self.table.item(
            selected,
            "values"
        )

        if not data:
            return

        self.id_kelas = data[0]

        self.combo_user.set(data[1])

        self.entry_kelas.delete(0, "end")
        self.entry_kelas.insert(0, data[2])

        self.entry_tahun.delete(0, "end")
        self.entry_tahun.insert(0, data[3])

        self.combo_semester.set(data[4])

    # ======================
    # EDIT
    # ======================

    def edit_kelas(self):

        if not self.id_kelas:
            return

        guru = self.combo_user.get()
        id_user = self.user_dict[guru]

        conn = connect_db()
        cursor = conn.cursor()

        cursor.execute("""
            UPDATE kelas
            SET
                id_user=%s,
                nama_kelas=%s,
                tahun_ajaran=%s,
                semester=%s
            WHERE id_kelas=%s
        """, (
            id_user,
            self.entry_kelas.get(),
            self.entry_tahun.get(),
            self.combo_semester.get(),
            self.id_kelas
        ))

        conn.commit()
        conn.close()

        self.load_data()

    # ======================
    # HAPUS
    # ======================

    def hapus_kelas(self):

        if not self.id_kelas:
            return

        if not messagebox.askyesno(
            "Konfirmasi",
            "Hapus data kelas?"
        ):
            return

        conn = connect_db()
        cursor = conn.cursor()

        cursor.execute(
            "DELETE FROM kelas WHERE id_kelas=%s",
            (self.id_kelas,)
        )

        conn.commit()
        conn.close()

        self.load_data()
        self.reset_form()

    # ======================
    # RESET
    # ======================

    def reset_form(self):

        self.id_kelas = None

        self.entry_kelas.delete(0, "end")
        self.entry_tahun.delete(0, "end")