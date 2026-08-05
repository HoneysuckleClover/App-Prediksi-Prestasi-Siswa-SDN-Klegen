import customtkinter as ctk
from tkinter import ttk, messagebox
from database.koneksi_sqlite import connect_db


class SiswaPage(ctk.CTkFrame):

    def __init__(self, parent=None):
        super().__init__(parent)

        self.configure(fg_color="#0F172A")

        self.id_siswa = None
        self.kelas_dict = {}

        # ==================================
        # STYLE TABLE
        # ==================================

        style = ttk.Style()
        style.theme_use("clam")

        # TREEVIEW BODY
        style.configure(
            "Treeview",
            background="#1E293B",
            foreground="white",
            fieldbackground="#1E293B",
            rowheight=34,
            borderwidth=0,
            relief="flat",
            font=("Segoe UI", 10)
        )

        # TREEVIEW HEADER
        style.configure(
            "Treeview.Heading",
            background="#334155",
            foreground="white",
            borderwidth=0,
            relief="flat",
            font=("Segoe UI", 10, "bold")
        )

        style.map(
            "Treeview.Heading",
            background=[("active", "#475569")]
        )

        # ROW SELECTED
        style.map(
            "Treeview",
            background=[("selected", "#2563EB")],
            foreground=[("selected", "white")]
        )

        # SCROLLBAR
        style.configure(
            "Vertical.TScrollbar",
            background="#334155",
            troughcolor="#1E293B",
            bordercolor="#1E293B",
            arrowcolor="white"
        )

        # ==================================
        # HEADER
        # ==================================

        header_frame = ctk.CTkFrame(
            self,
            fg_color="transparent"
        )
        header_frame.pack(fill="x", padx=20, pady=(20, 10))

        ctk.CTkLabel(
            header_frame,
            text="👥 DATA SISWA",
            font=("Segoe UI", 28, "bold"),
            text_color="white"
        ).pack(anchor="w")

        ctk.CTkLabel(
            header_frame,
            text="Kelola data siswa",
            font=("Segoe UI", 13),
            text_color="#94A3B8"
        ).pack(anchor="w")

        # ==================================
        # MAIN CONTENT - SCROLLABLE
        # ==================================

        main_scroll = ctk.CTkScrollableFrame(
            self,
            fg_color="transparent"
        )
        main_scroll.pack(fill="both", expand=True, padx=20, pady=10)

        # ==================================
        # FORM INPUT
        # ==================================

        form_frame = ctk.CTkFrame(
            main_scroll,
            fg_color="#1E293B",
            corner_radius=15,
            border_width=1,
            border_color="#334155"
        )
        form_frame.pack(fill="x", pady=(0, 15))
        
        for i in range(4):
            form_frame.grid_columnconfigure(i, weight=1)

        # Row 0: NIS & Nama Siswa
        ctk.CTkLabel(
            form_frame,
            text="🆔 NIS",
            text_color="white",
            font=("Segoe UI", 12, "bold")
        ).grid(row=0, column=0, padx=15, pady=(15, 10), sticky="w")

        self.entry_nis = ctk.CTkEntry(
            form_frame,
            width=200,
            height=35,
            fg_color="#334155",
            border_color="#475569",
            border_width=2,
            text_color="white",
            corner_radius=8,
            font=("Segoe UI", 11)
        )
        self.entry_nis.grid(row=0, column=1, padx=10, pady=(15, 10), sticky="w")

        ctk.CTkLabel(
            form_frame,
            text="👤 Nama Siswa",
            text_color="white",
            font=("Segoe UI", 12, "bold")
        ).grid(row=0, column=2, padx=15, pady=(15, 10), sticky="w")

        self.entry_nama = ctk.CTkEntry(
            form_frame,
            width=200,
            height=35,
            fg_color="#334155",
            border_color="#475569",
            border_width=2,
            text_color="white",
            corner_radius=8,
            font=("Segoe UI", 11)
        )
        self.entry_nama.grid(row=0, column=3, padx=10, pady=(15, 10), sticky="w")

        # Row 1: Jenis Kelamin & Kelas
        ctk.CTkLabel(
            form_frame,
            text="⚧ Jenis Kelamin",
            text_color="white",
            font=("Segoe UI", 12, "bold")
        ).grid(row=1, column=0, padx=15, pady=(10, 10), sticky="w")

        self.combo_jk = ctk.CTkOptionMenu(
            form_frame,
            values=["L", "P"],
            fg_color="#334155",
            button_color="#1E293B",
            button_hover_color="#475569",
            text_color="white",
            dropdown_fg_color="#1E293B",
            dropdown_text_color="white",
            dropdown_hover_color="#334155",
            width=180,
            height=35,
            corner_radius=8
        )
        self.combo_jk.grid(row=1, column=1, padx=10, pady=(10, 10), sticky="w")

        ctk.CTkLabel(
            form_frame,
            text="📚 Kelas",
            text_color="white",
            font=("Segoe UI", 12, "bold")
        ).grid(row=1, column=2, padx=15, pady=(10, 10), sticky="w")

        self.combo_kelas = ctk.CTkOptionMenu(
            form_frame,
            values=["Pilih Kelas"],
            fg_color="#334155",
            button_color="#1E293B",
            button_hover_color="#475569",
            text_color="white",
            dropdown_fg_color="#1E293B",
            dropdown_text_color="white",
            dropdown_hover_color="#334155",
            width=180,
            height=35,
            corner_radius=8
        )
        self.combo_kelas.grid(row=1, column=3, padx=10, pady=(10, 10), sticky="w")

        # Row 2: Tanggal Lahir & Alamat
        ctk.CTkLabel(
            form_frame,
            text="📅 Tanggal Lahir",
            text_color="white",
            font=("Segoe UI", 12, "bold")
        ).grid(row=2, column=0, padx=15, pady=(10, 15), sticky="w")

        self.entry_tgl = ctk.CTkEntry(
            form_frame,
            width=200,
            height=35,
            fg_color="#334155",
            border_color="#475569",
            border_width=2,
            text_color="white",
            corner_radius=8,
            font=("Segoe UI", 11),
            placeholder_text="YYYY-MM-DD"
        )
        self.entry_tgl.grid(row=2, column=1, padx=10, pady=(10, 15), sticky="w")

        ctk.CTkLabel(
            form_frame,
            text="📍 Alamat",
            text_color="white",
            font=("Segoe UI", 12, "bold")
        ).grid(row=2, column=2, padx=15, pady=(10, 15), sticky="w")

        self.entry_alamat = ctk.CTkEntry(
            form_frame,
            width=200,
            height=35,
            fg_color="#334155",
            border_color="#475569",
            border_width=2,
            text_color="white",
            corner_radius=8,
            font=("Segoe UI", 11)
        )
        self.entry_alamat.grid(row=2, column=3, padx=10, pady=(10, 15), sticky="w")

        # ==================================
        # BUTTON
        # ==================================

        btn_frame = ctk.CTkFrame(
            main_scroll,
            fg_color="transparent"
        )
        btn_frame.pack(fill="x", pady=(0, 15))

        button_style = {
            "height": 42,
            "corner_radius": 10,
            "font": ("Segoe UI", 12, "bold"),
            "border_width": 0
        }

        ctk.CTkButton(
            btn_frame,
            text="➕ Tambah",
            fg_color="#22C55E",
            hover_color="#16A34A",
            command=self.tambah_siswa,
            **button_style
        ).pack(side="left", padx=5)

        ctk.CTkButton(
            btn_frame,
            text="✏️ Edit",
            fg_color="#3B82F6",
            hover_color="#2563EB",
            command=self.edit_siswa,
            **button_style
        ).pack(side="left", padx=5)

        ctk.CTkButton(
            btn_frame,
            text="🗑️ Hapus",
            fg_color="#EF4444",
            hover_color="#DC2626",
            command=self.hapus_siswa,
            **button_style
        ).pack(side="left", padx=5)

        ctk.CTkButton(
            btn_frame,
            text="🔄 Reset",
            fg_color="#F59E0B",
            hover_color="#D97706",
            command=self.reset_form,
            **button_style
        ).pack(side="left", padx=5)

        # ==================================
        # SEARCH
        # ==================================

        search_frame = ctk.CTkFrame(
            main_scroll,
            fg_color="#1E293B",
            corner_radius=12,
            border_width=1,
            border_color="#334155"
        )
        search_frame.pack(fill="x", pady=(0, 10))

        self.entry_search = ctk.CTkEntry(
            search_frame,
            placeholder_text="🔍 Cari Nama Siswa...",
            width=300,
            height=38,
            fg_color="#334155",
            border_color="#475569",
            border_width=2,
            text_color="white",
            corner_radius=8,
            font=("Segoe UI", 11)
        )
        self.entry_search.pack(side="left", padx=15, pady=10)

        ctk.CTkButton(
            search_frame,
            text="🔍 Cari",
            width=120,
            height=38,
            fg_color="#2563EB",
            hover_color="#1D4ED8",
            corner_radius=8,
            font=("Segoe UI", 11, "bold"),
            command=self.cari_siswa
        ).pack(side="left", padx=5)

        ctk.CTkButton(
            search_frame,
            text="🔄 Refresh",
            width=120,
            height=38,
            fg_color="#475569",
            hover_color="#334155",
            corner_radius=8,
            font=("Segoe UI", 11, "bold"),
            command=self.load_data
        ).pack(side="left", padx=5)

        # ==================================
        # TABLE
        # ==================================

        table_frame = ctk.CTkFrame(
            main_scroll,
            fg_color="#1E293B",
            corner_radius=15,
            border_width=1,
            border_color="#334155"
        )
        table_frame.pack(
            fill="both",
            expand=True,
            pady=(0, 10)
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

        self.table = ttk.Treeview(
            table_frame,
            columns=columns,
            show="headings",
            height=12
        )

        # HEADING
        self.table.heading("id", text="ID")
        self.table.heading("nis", text="🆔 NIS")
        self.table.heading("nama", text="👤 Nama Siswa")
        self.table.heading("jk", text="⚧ JK")
        self.table.heading("kelas", text="📚 Kelas")
        self.table.heading("tgl", text="📅 Tanggal Lahir")
        self.table.heading("alamat", text="📍 Alamat")

        # COLUMN
        self.table.column("id", width=60, anchor="center")
        self.table.column("nis", width=120, anchor="center")
        self.table.column("nama", width=200)
        self.table.column("jk", width=70, anchor="center")
        self.table.column("kelas", width=140, anchor="center")
        self.table.column("tgl", width=130, anchor="center")
        self.table.column("alamat", width=250)

        # ZEBRA ROW
        self.table.tag_configure(
            "oddrow",
            background="#1E293B"
        )
        self.table.tag_configure(
            "evenrow",
            background="#273549"
        )

        # SCROLLBAR
        scrollbar = ttk.Scrollbar(
            table_frame,
            orient="vertical",
            command=self.table.yview
        )
        self.table.configure(yscrollcommand=scrollbar.set)

        self.table.pack(
            side="left",
            fill="both",
            expand=True,
            padx=(10, 0),
            pady=10
        )
        scrollbar.pack(
            side="right",
            fill="y",
            padx=(0, 10),
            pady=10
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
                SELECT id_kelas, nama_kelas
                FROM kelas
                ORDER BY nama_kelas
            """)

            data = cursor.fetchall()
            conn.close()

            self.kelas_dict.clear()
            list_kelas = []

            for row in data:
                self.kelas_dict[row[1]] = row[0]
                list_kelas.append(row[1])

            if list_kelas:
                self.combo_kelas.configure(values=list_kelas)
                self.combo_kelas.set(list_kelas[0])
            else:
                self.combo_kelas.configure(values=["Tidak ada kelas"])
                self.combo_kelas.set("Tidak ada kelas")

        except Exception as e:
            messagebox.showerror("Error", str(e))

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
                LEFT JOIN kelas k ON s.id_kelas = k.id_kelas
                ORDER BY s.nama_siswa
            """)

            data = cursor.fetchall()
            conn.close()

            for index, row in enumerate(data):
                tag = "evenrow" if index % 2 == 0 else "oddrow"
                self.table.insert("", "end", values=row, tags=(tag,))

        except Exception as e:
            messagebox.showerror("Error", str(e))

    # ==========================
    # TAMBAH
    # ==========================

    def tambah_siswa(self):
        try:
            if self.combo_kelas.get() == "Tidak ada kelas" or self.combo_kelas.get() == "Pilih Kelas":
                messagebox.showwarning("Peringatan", "Silakan pilih kelas terlebih dahulu!")
                return

            if not self.entry_nis.get():
                messagebox.showwarning("Peringatan", "Silakan masukkan NIS!")
                return

            if not self.entry_nama.get():
                messagebox.showwarning("Peringatan", "Silakan masukkan nama siswa!")
                return

            nama_kelas = self.combo_kelas.get()
            id_kelas = self.kelas_dict[nama_kelas]

            conn = connect_db()
            cursor = conn.cursor()

            cursor.execute("""
                INSERT INTO siswa
                (id_kelas, nis, nama_siswa, jenis_kelamin, tanggal_lahir, alamat)
                VALUES (?,?,?,?,?,?)
            """, (
                id_kelas,
                self.entry_nis.get().strip(),
                self.entry_nama.get().strip(),
                self.combo_jk.get(),
                self.entry_tgl.get().strip(),
                self.entry_alamat.get().strip()
            ))

            conn.commit()
            conn.close()

            messagebox.showinfo("Sukses", "Data siswa berhasil ditambahkan!")
            self.load_data()
            self.reset_form()

        except Exception as e:
            messagebox.showerror("Error", str(e))

    # ==========================
    # PILIH DATA
    # ==========================

    def pilih_data(self, event):
        selected = self.table.focus()
        data = self.table.item(selected, "values")

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
        self.entry_tgl.insert(0, data[5] if data[5] else "")

        self.entry_alamat.delete(0, "end")
        self.entry_alamat.insert(0, data[6] if data[6] else "")

    # ==========================
    # EDIT
    # ==========================

    def edit_siswa(self):
        if not self.id_siswa:
            messagebox.showwarning("Peringatan", "Pilih data yang akan diedit!")
            return

        try:
            if self.combo_kelas.get() == "Tidak ada kelas" or self.combo_kelas.get() == "Pilih Kelas":
                messagebox.showwarning("Peringatan", "Silakan pilih kelas terlebih dahulu!")
                return

            nama_kelas = self.combo_kelas.get()
            id_kelas = self.kelas_dict[nama_kelas]

            conn = connect_db()
            cursor = conn.cursor()

            cursor.execute("""
                UPDATE siswa SET
                    id_kelas=?,
                    nis=?,
                    nama_siswa=?,
                    jenis_kelamin=?,
                    tanggal_lahir=?,
                    alamat=?
                WHERE id_siswa=?
            """, (
                id_kelas,
                self.entry_nis.get().strip(),
                self.entry_nama.get().strip(),
                self.combo_jk.get(),
                self.entry_tgl.get().strip(),
                self.entry_alamat.get().strip(),
                self.id_siswa
            ))

            conn.commit()
            conn.close()

            messagebox.showinfo("Sukses", "Data siswa berhasil diperbarui!")
            self.load_data()
            self.reset_form()

        except Exception as e:
            messagebox.showerror("Error", str(e))

    # ==========================
    # HAPUS
    # ==========================

    def hapus_siswa(self):
        if not self.id_siswa:
            messagebox.showwarning("Peringatan", "Pilih data yang akan dihapus!")
            return

        if messagebox.askyesno("Konfirmasi", "Yakin ingin menghapus data siswa ini?"):
            try:
                conn = connect_db()
                cursor = conn.cursor()

                cursor.execute(
                    "DELETE FROM siswa WHERE id_siswa=?",
                    (self.id_siswa,)
                )

                conn.commit()
                conn.close()

                messagebox.showinfo("Sukses", "Data siswa berhasil dihapus!")
                self.load_data()
                self.reset_form()

            except Exception as e:
                messagebox.showerror("Error", str(e))

    # ==========================
    # CARI
    # ==========================

    def cari_siswa(self):
        keyword = self.entry_search.get().strip()

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
                LEFT JOIN kelas k ON s.id_kelas = k.id_kelas
                WHERE s.nama_siswa LIKE ?
                ORDER BY s.nama_siswa
            """, (f"%{keyword}%",))

            data = cursor.fetchall()
            conn.close()

            for index, row in enumerate(data):
                tag = "evenrow" if index % 2 == 0 else "oddrow"
                self.table.insert("", "end", values=row, tags=(tag,))

            if len(data) == 0:
                messagebox.showinfo("Info", "Data tidak ditemukan!")

        except Exception as e:
            messagebox.showerror("Error", str(e))

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
            first_kelas = list(self.kelas_dict.keys())[0]
            self.combo_kelas.set(first_kelas)
        else:
            self.combo_kelas.set("Tidak ada kelas")
