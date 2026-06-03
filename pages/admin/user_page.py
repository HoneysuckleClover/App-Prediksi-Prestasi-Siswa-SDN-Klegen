import customtkinter as ctk
from tkinter import ttk, messagebox

from database.koneksi import connect_db


class UserPage(ctk.CTkFrame):

    def __init__(self, parent=None):
        super().__init__(parent)


        self.id_user = None

        # ======================
        # FORM
        # ======================

        form_frame = ctk.CTkFrame(self)
        form_frame.pack(fill="x", padx=10, pady=10)

        ctk.CTkLabel(
            form_frame,
            text="Nama"
        ).grid(row=0, column=0, padx=10, pady=10)

        self.entry_nama = ctk.CTkEntry(
            form_frame,
            width=250
        )
        self.entry_nama.grid(row=0, column=1)

        ctk.CTkLabel(
            form_frame,
            text="Username"
        ).grid(row=1, column=0, padx=10, pady=10)

        self.entry_username = ctk.CTkEntry(
            form_frame,
            width=250
        )
        self.entry_username.grid(row=1, column=1)

        ctk.CTkLabel(
            form_frame,
            text="Password"
        ).grid(row=2, column=0, padx=10, pady=10)

        self.entry_password = ctk.CTkEntry(
            form_frame,
            width=250,
            show="*"
        )
        self.entry_password.grid(row=2, column=1)

        ctk.CTkLabel(
            form_frame,
            text="Role"
        ).grid(row=0, column=2, padx=10, pady=10)

        self.combo_role = ctk.CTkOptionMenu(
            form_frame,
            values=[
                "admin",
                "guru",
                "kepala_sekolah"
            ]
        )
        self.combo_role.grid(row=0, column=3)

        # ======================
        # BUTTON
        # ======================

        btn_frame = ctk.CTkFrame(self)
        btn_frame.pack(fill="x", padx=10)

        ctk.CTkButton(
            btn_frame,
            text="Tambah",
            command=self.tambah_user
        ).pack(side="left", padx=5)

        ctk.CTkButton(
            btn_frame,
            text="Edit",
            command=self.edit_user
        ).pack(side="left", padx=5)

        ctk.CTkButton(
            btn_frame,
            text="Hapus",
            command=self.hapus_user
        ).pack(side="left", padx=5)

        ctk.CTkButton(
            btn_frame,
            text="Reset",
            command=self.reset_form
        ).pack(side="left", padx=5)

        # ======================
        # SEARCH
        # ======================

        search_frame = ctk.CTkFrame(self)
        search_frame.pack(fill="x", padx=10, pady=10)

        self.entry_search = ctk.CTkEntry(
            search_frame,
            placeholder_text="Cari Nama User..."
        )
        self.entry_search.pack(
            side="left",
            padx=5
        )

        ctk.CTkButton(
            search_frame,
            text="Cari",
            command=self.cari_user
        ).pack(side="left")

        ctk.CTkButton(
            search_frame,
            text="Refresh",
            command=self.load_data
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
            "nama",
            "username",
            "role"
        )

        self.table = ttk.Treeview(
            table_frame,
            columns=columns,
            show="headings"
        )

        self.table.heading("id", text="ID")
        self.table.heading("nama", text="Nama")
        self.table.heading("username", text="Username")
        self.table.heading("role", text="Role")

        self.table.column("id", width=80)
        self.table.column("nama", width=250)
        self.table.column("username", width=200)
        self.table.column("role", width=150)

        self.table.pack(
            fill="both",
            expand=True
        )

        self.table.bind(
            "<<TreeviewSelect>>",
            self.pilih_data
        )

        self.load_data()

    # ======================
    # LOAD DATA
    # ======================

    def load_data(self):

        for row in self.table.get_children():
            self.table.delete(row)

        try:

            conn = connect_db()
            cursor = conn.cursor()

            cursor.execute("""
                SELECT
                    id_user,
                    nama,
                    username,
                    role
                FROM users
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

    # ======================
    # TAMBAH
    # ======================

    def tambah_user(self):

        nama = self.entry_nama.get()
        username = self.entry_username.get()
        password = self.entry_password.get()
        role = self.combo_role.get()

        if not nama or not username or not password:
            messagebox.showwarning(
                "Peringatan",
                "Semua field wajib diisi!"
            )
            return

        try:

            conn = connect_db()
            cursor = conn.cursor()

            cursor.execute(
                "SELECT username FROM users WHERE username=%s",
                (username,)
            )

            if cursor.fetchone():
                messagebox.showerror(
                    "Error",
                    "Username sudah digunakan!"
                )
                return

            cursor.execute("""
                INSERT INTO users
                (
                    nama,
                    username,
                    password,
                    role
                )
                VALUES (%s,%s,%s,%s)
            """, (
                nama,
                username,
                password,
                role
            ))

            conn.commit()
            conn.close()

            messagebox.showinfo(
                "Sukses",
                "User berhasil ditambahkan"
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

        self.id_user = data[0]

        self.entry_nama.delete(0, "end")
        self.entry_nama.insert(0, data[1])

        self.entry_username.delete(0, "end")
        self.entry_username.insert(0, data[2])

        self.combo_role.set(data[3])

    # ======================
    # EDIT
    # ======================

    def edit_user(self):

        if not self.id_user:
            return

        try:

            conn = connect_db()
            cursor = conn.cursor()

            cursor.execute("""
                UPDATE users
                SET
                    nama=%s,
                    username=%s,
                    password=%s,
                    role=%s
                WHERE id_user=%s
            """, (
                self.entry_nama.get(),
                self.entry_username.get(),
                self.entry_password.get(),
                self.combo_role.get(),
                self.id_user
            ))

            conn.commit()
            conn.close()

            messagebox.showinfo(
                "Sukses",
                "User berhasil diperbarui"
            )

            self.load_data()

        except Exception as e:
            messagebox.showerror(
                "Error",
                str(e)
            )

    # ======================
    # HAPUS
    # ======================

    def hapus_user(self):

        if not self.id_user:
            return

        if not messagebox.askyesno(
            "Konfirmasi",
            "Yakin ingin menghapus user?"
        ):
            return

        try:

            conn = connect_db()
            cursor = conn.cursor()

            cursor.execute(
                "DELETE FROM users WHERE id_user=%s",
                (self.id_user,)
            )

            conn.commit()
            conn.close()

            messagebox.showinfo(
                "Sukses",
                "User berhasil dihapus"
            )

            self.load_data()
            self.reset_form()

        except Exception as e:
            messagebox.showerror(
                "Error",
                str(e)
            )

    # ======================
    # CARI
    # ======================

    def cari_user(self):

        keyword = self.entry_search.get()

        for row in self.table.get_children():
            self.table.delete(row)

        try:

            conn = connect_db()
            cursor = conn.cursor()

            cursor.execute("""
                SELECT
                    id_user,
                    nama,
                    username,
                    role
                FROM users
                WHERE nama LIKE %s
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

    # ======================
    # RESET
    # ======================

    def reset_form(self):

        self.id_user = None

        self.entry_nama.delete(0, "end")
        self.entry_username.delete(0, "end")
        self.entry_password.delete(0, "end")

        self.combo_role.set("guru")