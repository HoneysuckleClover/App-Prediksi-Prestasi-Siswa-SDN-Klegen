import customtkinter as ctk
from tkinter import ttk, messagebox

from database.koneksi import connect_db


class SiswaPage(ctk.CTkFrame):

    def __init__(self, parent=None):
        super().__init__(parent)
        # Theme CustomTkinter
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        self.configure(fg_color="#1E293B")

        self.id_siswa = None
        self.kelas_dict = {}

        ctk.CTkLabel(
            self,
            text="📚 Manajemen Data Siswa",
            font=("Segoe UI", 24, "bold"),
            text_color="white"
        ).pack(pady=(15, 10))

        # ==========================
        # FORM
        # ==========================

        form_frame = ctk.CTkFrame(
            self,
            fg_color="#334155"
        )
        form_frame.pack(fill="x", padx=10, pady=10)

        ctk.CTkLabel(
            form_frame,
            text="NIS"
        ).grid(row=0, column=0, padx=10, pady=10)

        self.entry_nis = ctk.CTkEntry(
            form_frame,
            width=250,
            fg_color="#475569",
            border_color="#64748B"
        )
        self.entry_nis.grid(row=0, column=1)

        ctk.CTkLabel(
            form_frame,
            text="Nama Siswa"
        ).grid(row=1, column=0, padx=10, pady=10)

        self.entry_nama = ctk.CTkEntry(
            form_frame,
            width=250
        )
        self.entry_nama.grid(row=1, column=1)

        ctk.CTkLabel(
            form_frame,
            text="Jenis Kelamin"
        ).grid(row=2, column=0, padx=10, pady=10)

        self.combo_jk = ctk.CTkOptionMenu(
            form_frame,
            values=["L", "P"],
            fg_color="#475569",
            button_color="#334155",
            button_hover_color="#1E293B"
        )
        self.combo_jk.grid(row=2, column=1)

        ctk.CTkLabel(
            form_frame,
            text="Kelas"
        ).grid(row=0, column=2, padx=10, pady=10)

        self.combo_kelas = ctk.CTkOptionMenu(
            form_frame,
            values=["Pilih Kelas"],
            fg_color="#475569",
            button_color="#334155",
            button_hover_color="#1E293B"
        )
        self.combo_kelas.grid(row=0, column=3)

        ctk.CTkLabel(
            form_frame,
            text="Tanggal Lahir"
        ).grid(row=1, column=2, padx=10, pady=10)

        self.entry_tgl = ctk.CTkEntry(
            form_frame,
            width=250,
            placeholder_text="YYYY-MM-DD"
        )
        self.entry_tgl.grid(row=1, column=3)

        ctk.CTkLabel(
            form_frame,
            text="Alamat"
        ).grid(row=2, column=2, padx=10, pady=10)

        self.entry_alamat = ctk.CTkEntry(
            form_frame,
            width=250
        )
        self.entry_alamat.grid(row=2, column=3)

        # ==========================
        # BUTTON
        # ==========================

        btn_frame = ctk.CTkFrame(
            self,
            fg_color="#334155"
        )
        btn_frame.pack(fill="x", padx=10)

        ctk.CTkButton(
            btn_frame,
            text="Tambah",
            fg_color="#22C55E",
            hover_color="#16A34A",
            text_color="white",
            command=self.tambah_siswa
        ).pack(side="left", padx=5)

        ctk.CTkButton(
            btn_frame,
            text="Edit",
            fg_color="#3B82F6",
            hover_color="#2563EB",
            text_color="white",
            command=self.edit_siswa
        ).pack(side="left", padx=5)

        ctk.CTkButton(
            btn_frame,
            text="Hapus",
            fg_color="#EF4444",
            hover_color="#DC2626",
            text_color="white",
            command=self.hapus_siswa
        ).pack(side="left", padx=5)

        ctk.CTkButton(
            btn_frame,
            text="Reset",
            fg_color="#F59E0B",
            hover_color="#D97706",
            text_color="white",
            command=self.reset_form
        ).pack(side="left", padx=5)

        # ==========================
        # SEARCH
        # ==========================

        search_frame = ctk.CTkFrame(
            self,
            fg_color="#334155"
        )
        search_frame.pack(fill="x", padx=10, pady=10)

        self.entry_search = ctk.CTkEntry(
            search_frame,
            placeholder_text="Cari Nama Siswa..."
        )
        self.entry_search.pack(side="left", padx=5)

        ctk.CTkButton(
            search_frame,
            text="Cari",
            fg_color="#06B6D4",
            hover_color="#0891B2",
            text_color="white",
            command=self.cari_siswa
        ).pack(side="left", padx=5)

        ctk.CTkButton(
            search_frame,
            text="Refresh",
            fg_color="#8B5CF6",
            hover_color="#7C3AED",
            text_color="white",
            command=self.load_data
        ).pack(side="left", padx=5)

        # ==========================
        # TABLE
        # ==========================

        table_frame = ctk.CTkFrame(
            self,
            fg_color="#334155"
        )
        table_frame.pack(
            fill="both",
            expand=True,
            padx=10,
            pady=10
        )

        columns = (
            "id",
            "nis",
            "nama",
            "jk",
            "kelas",
            "tgl",
            "alamat"
        )

        style = ttk.Style()

        style.theme_use("clam")

        style.configure(
            "Treeview",
            background="#1E293B",
            foreground="white",
            rowheight=30,
            fieldbackground="#1E293B",
            borderwidth=0
        )

        style.configure(
            "Treeview.Heading",
            background="#0F172A",
            foreground="white",
            font=("Segoe UI", 10, "bold")
        )

        style.map(
            "Treeview",
            background=[("selected", "#3B82F6")]
        )

        self.table = ttk.Treeview(
            table_frame,
            columns=columns,
            show="headings"
        )

        self.table.heading("id", text="ID")
        self.table.heading("nis", text="NIS")
        self.table.heading("nama", text="Nama Siswa")
        self.table.heading("jk", text="JK")
        self.table.heading("kelas", text="Kelas")
        self.table.heading("tgl", text="Tanggal Lahir")
        self.table.heading("alamat", text="Alamat")

        self.table.column("id", width=60)
        self.table.column("nis", width=120)
        self.table.column("nama", width=200)
        self.table.column("jk", width=80)
        self.table.column("kelas", width=150)
        self.table.column("tgl", width=120)
        self.table.column("alamat", width=250)

        self.table.pack(
            fill="both",
            expand=True
        )

        self.table.bind(
            "<<TreeviewSelect>>",
            self.pilih_data
        )

        self.load_kelas()
        self.load_data()

    # ==========================
    # LOAD KELAS
    # ==========================

    def load_kelas(self):

        try:
            conn = connect_db()
            cursor = conn.cursor()

            cursor.execute("""
                SELECT id_kelas,nama_kelas
                FROM kelas
                ORDER BY nama_kelas
            """)

            data = cursor.fetchall()

            self.kelas_dict.clear()

            list_kelas = []

            for row in data:

                id_kelas = row[0]
                nama_kelas = row[1]

                self.kelas_dict[nama_kelas] = id_kelas
                list_kelas.append(nama_kelas)

            if list_kelas:
                self.combo_kelas.configure(
                    values=list_kelas
                )
                self.combo_kelas.set(
                    list_kelas[0]
                )

            conn.close()

        except Exception as e:
            messagebox.showerror(
                "Error",
                str(e)
            )

    # ==========================
    # LOAD DATA
    # ==========================

    def load_data(self):

        for row in self.table.get_children():
            self.table.delete(row)

        try:

            conn = connect_db()
            cursor = conn.cursor()

            cursor.execute("""
                SELECT
                    s.id_siswa,
                    s.nis,
                    s.nama_siswa,
                    s.jenis_kelamin,
                    k.nama_kelas,
                    s.tanggal_lahir,
                    s.alamat
                FROM siswa s
                LEFT JOIN kelas k
                ON s.id_kelas = k.id_kelas
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

    # ==========================
    # TAMBAH
    # ==========================

    def tambah_siswa(self):

        try:

            nama_kelas = self.combo_kelas.get()
            id_kelas = self.kelas_dict[nama_kelas]

            conn = connect_db()
            cursor = conn.cursor()

            query = """
            INSERT INTO siswa
            (
                id_kelas,
                nis,
                nama_siswa,
                jenis_kelamin,
                tanggal_lahir,
                alamat
            )
            VALUES (%s,%s,%s,%s,%s,%s)
            """

            cursor.execute(query, (
                id_kelas,
                self.entry_nis.get(),
                self.entry_nama.get(),
                self.combo_jk.get(),
                self.entry_tgl.get(),
                self.entry_alamat.get()
            ))

            conn.commit()
            conn.close()

            messagebox.showinfo(
                "Sukses",
                "Data siswa berhasil ditambahkan"
            )

            self.load_data()
            self.reset_form()

        except Exception as e:
            messagebox.showerror(
                "Error",
                str(e)
            )

    # ==========================
    # PILIH DATA
    # ==========================

    def pilih_data(self, event):

        selected = self.table.focus()

        data = self.table.item(
            selected,
            "values"
        )

        if not data:
            return

        self.id_siswa = data[0]

        self.entry_nis.delete(0, "end")
        self.entry_nis.insert(0, data[1])

        self.entry_nama.delete(0, "end")
        self.entry_nama.insert(0, data[2])

        self.combo_jk.set(data[3])

        self.combo_kelas.set(data[4])

        self.entry_tgl.delete(0, "end")
        self.entry_tgl.insert(0, data[5])

        self.entry_alamat.delete(0, "end")
        self.entry_alamat.insert(0, data[6])

    # ==========================
    # EDIT
    # ==========================

    def edit_siswa(self):

        if not self.id_siswa:
            return

        try:

            nama_kelas = self.combo_kelas.get()
            id_kelas = self.kelas_dict[nama_kelas]

            conn = connect_db()
            cursor = conn.cursor()

            cursor.execute("""
                UPDATE siswa
                SET
                    id_kelas=%s,
                    nis=%s,
                    nama_siswa=%s,
                    jenis_kelamin=%s,
                    tanggal_lahir=%s,
                    alamat=%s
                WHERE id_siswa=%s
            """, (
                id_kelas,
                self.entry_nis.get(),
                self.entry_nama.get(),
                self.combo_jk.get(),
                self.entry_tgl.get(),
                self.entry_alamat.get(),
                self.id_siswa
            ))

            conn.commit()
            conn.close()

            messagebox.showinfo(
                "Sukses",
                "Data siswa berhasil diperbarui"
            )

            self.load_data()

        except Exception as e:
            messagebox.showerror(
                "Error",
                str(e)
            )

    # ==========================
    # HAPUS
    # ==========================

    def hapus_siswa(self):

        if not self.id_siswa:
            return

        if not messagebox.askyesno(
            "Konfirmasi",
            "Yakin ingin menghapus data?"
        ):
            return

        try:

            conn = connect_db()
            cursor = conn.cursor()

            cursor.execute(
                "DELETE FROM siswa WHERE id_siswa=%s",
                (self.id_siswa,)
            )

            conn.commit()
            conn.close()

            self.load_data()
            self.reset_form()

        except Exception as e:
            messagebox.showerror(
                "Error",
                str(e)
            )

    # ==========================
    # CARI
    # ==========================

    def cari_siswa(self):

        keyword = self.entry_search.get()

        for row in self.table.get_children():
            self.table.delete(row)

        try:

            conn = connect_db()
            cursor = conn.cursor()

            cursor.execute("""
                SELECT
                    s.id_siswa,
                    s.nis,
                    s.nama_siswa,
                    s.jenis_kelamin,
                    k.nama_kelas,
                    s.tanggal_lahir,
                    s.alamat
                FROM siswa s
                LEFT JOIN kelas k
                ON s.id_kelas = k.id_kelas
                WHERE s.nama_siswa LIKE %s
            """, (f"%{keyword}%",))

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

    # ==========================
    # RESET
    # ==========================

    def reset_form(self):

        self.id_siswa = None

        self.entry_nis.delete(0, "end")
        self.entry_nama.delete(0, "end")
        self.entry_tgl.delete(0, "end")
        self.entry_alamat.delete(0, "end")

        self.combo_jk.set("L")

        if self.kelas_dict:
            self.combo_kelas.set(
                list(self.kelas_dict.keys())[0]
            )