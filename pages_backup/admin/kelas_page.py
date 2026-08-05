import customtkinter as ctk
from tkinter import ttk, messagebox
from database.koneksi_sqlite import connect_db


class KelasPage(ctk.CTkFrame):

    def __init__(self, parent=None):
        super().__init__(parent)

        self.configure(fg_color="#0F172A")

        self.id_kelas = None
        self.user_dict = {}

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
            text="🏫 DATA KELAS",
            font=("Segoe UI", 28, "bold"),
            text_color="white"
        ).pack(anchor="w")

        ctk.CTkLabel(
            header_frame,
            text="Kelola data kelas dan wali kelas",
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

        # Row 0: Guru/Wali Kelas & Nama Kelas
        ctk.CTkLabel(
            form_frame,
            text="👨‍🏫 Guru/Wali Kelas",
            text_color="white",
            font=("Segoe UI", 12, "bold")
        ).grid(row=0, column=0, padx=15, pady=(15, 10), sticky="w")

        self.combo_user = ctk.CTkOptionMenu(
            form_frame,
            values=["Pilih Guru"],
            fg_color="#334155",
            button_color="#1E293B",
            button_hover_color="#475569",
            text_color="white",
            dropdown_fg_color="#1E293B",
            dropdown_text_color="white",
            dropdown_hover_color="#334155",
            width=200,
            height=35,
            corner_radius=8
        )
        self.combo_user.grid(row=0, column=1, padx=10, pady=(15, 10), sticky="w")

        ctk.CTkLabel(
            form_frame,
            text="📚 Nama Kelas",
            text_color="white",
            font=("Segoe UI", 12, "bold")
        ).grid(row=0, column=2, padx=15, pady=(15, 10), sticky="w")

        self.entry_kelas = ctk.CTkEntry(
            form_frame,
            width=200,
            height=35,
            fg_color="#334155",
            border_color="#475569",
            border_width=2,
            text_color="white",
            corner_radius=8,
            font=("Segoe UI", 11),
            placeholder_text="Contoh: VI-A"
        )
        self.entry_kelas.grid(row=0, column=3, padx=10, pady=(15, 10), sticky="w")

        # Row 1: Tahun Ajaran & Semester
        ctk.CTkLabel(
            form_frame,
            text="📅 Tahun Ajaran",
            text_color="white",
            font=("Segoe UI", 12, "bold")
        ).grid(row=1, column=0, padx=15, pady=(10, 15), sticky="w")

        self.entry_tahun = ctk.CTkEntry(
            form_frame,
            width=200,
            height=35,
            fg_color="#334155",
            border_color="#475569",
            border_width=2,
            text_color="white",
            corner_radius=8,
            font=("Segoe UI", 11),
            placeholder_text="2025/2026"
        )
        self.entry_tahun.grid(row=1, column=1, padx=10, pady=(10, 15), sticky="w")

        ctk.CTkLabel(
            form_frame,
            text="📋 Semester",
            text_color="white",
            font=("Segoe UI", 12, "bold")
        ).grid(row=1, column=2, padx=15, pady=(10, 15), sticky="w")

        self.combo_semester = ctk.CTkOptionMenu(
            form_frame,
            values=["Ganjil", "Genap"],
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
        self.combo_semester.grid(row=1, column=3, padx=10, pady=(10, 15), sticky="w")

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
            command=self.tambah_kelas,
            **button_style
        ).pack(side="left", padx=5)

        ctk.CTkButton(
            btn_frame,
            text="✏️ Edit",
            fg_color="#3B82F6",
            hover_color="#2563EB",
            command=self.edit_kelas,
            **button_style
        ).pack(side="left", padx=5)

        ctk.CTkButton(
            btn_frame,
            text="🗑️ Hapus",
            fg_color="#EF4444",
            hover_color="#DC2626",
            command=self.hapus_kelas,
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
            placeholder_text="🔍 Cari Nama Kelas...",
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
            command=self.cari_data
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
            "guru",
            "kelas",
            "tahun",
            "semester"
        )

        self.table = ttk.Treeview(
            table_frame,
            columns=columns,
            show="headings",
            height=12
        )

        # HEADING
        self.table.heading("id", text="ID")
        self.table.heading("guru", text="👨‍🏫 Wali Kelas")
        self.table.heading("kelas", text="📚 Nama Kelas")
        self.table.heading("tahun", text="📅 Tahun Ajaran")
        self.table.heading("semester", text="📋 Semester")

        # COLUMN
        self.table.column("id", width=70, anchor="center")
        self.table.column("guru", width=250)
        self.table.column("kelas", width=180, anchor="center")
        self.table.column("tahun", width=150, anchor="center")
        self.table.column("semester", width=120, anchor="center")

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

        self.load_guru()
        self.load_data()

    # ======================
    # LOAD GURU
    # ======================

    def load_guru(self):
        try:
            conn = connect_db()
            cursor = conn.cursor()

            cursor.execute("""
                SELECT id_user, nama
                FROM users
                WHERE role='guru'
                ORDER BY nama
            """)

            data = cursor.fetchall()
            conn.close()

            list_guru = []
            self.user_dict.clear()

            for row in data:
                self.user_dict[row[1]] = row[0]
                list_guru.append(row[1])

            if list_guru:
                self.combo_user.configure(values=list_guru)
                self.combo_user.set(list_guru[0])
            else:
                self.combo_user.configure(values=["Tidak ada guru"])
                self.combo_user.set("Tidak ada guru")

        except Exception as e:
            messagebox.showerror("Error", str(e))

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
                    k.id_kelas,
                    u.nama,
                    k.nama_kelas,
                    k.tahun_ajaran,
                    k.semester
                FROM kelas k
                LEFT JOIN users u ON k.id_user = u.id_user
                ORDER BY k.nama_kelas
            """)

            data = cursor.fetchall()
            conn.close()

            for index, row in enumerate(data):
                tag = "evenrow" if index % 2 == 0 else "oddrow"
                self.table.insert("", "end", values=row, tags=(tag,))

        except Exception as e:
            messagebox.showerror("Error", str(e))

    # ======================
    # TAMBAH
    # ======================

    def tambah_kelas(self):
        try:
            guru = self.combo_user.get()
            
            if guru == "Tidak ada guru" or guru == "Pilih Guru":
                messagebox.showwarning("Peringatan", "Silakan pilih guru terlebih dahulu!")
                return

            if not self.entry_kelas.get():
                messagebox.showwarning("Peringatan", "Silakan masukkan nama kelas!")
                return

            if not self.entry_tahun.get():
                messagebox.showwarning("Peringatan", "Silakan masukkan tahun ajaran!")
                return

            id_user = self.user_dict[guru]

            conn = connect_db()
            cursor = conn.cursor()

            cursor.execute("""
                INSERT INTO kelas
                (id_user, nama_kelas, tahun_ajaran, semester)
                VALUES (?,?,?,?)
            """, (
                id_user,
                self.entry_kelas.get().strip(),
                self.entry_tahun.get().strip(),
                self.combo_semester.get()
            ))

            conn.commit()
            conn.close()

            messagebox.showinfo("Sukses", "Data kelas berhasil ditambahkan!")
            self.load_data()
            self.reset_form()

        except Exception as e:
            messagebox.showerror("Error", str(e))

    # ======================
    # PILIH DATA
    # ======================

    def pilih_data(self, event):
        selected = self.table.focus()
        data = self.table.item(selected, "values")

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
            messagebox.showwarning("Peringatan", "Pilih data yang akan diedit!")
            return

        try:
            guru = self.combo_user.get()
            
            if guru == "Tidak ada guru" or guru == "Pilih Guru":
                messagebox.showwarning("Peringatan", "Silakan pilih guru terlebih dahulu!")
                return

            if not self.entry_kelas.get():
                messagebox.showwarning("Peringatan", "Silakan masukkan nama kelas!")
                return

            id_user = self.user_dict[guru]

            conn = connect_db()
            cursor = conn.cursor()

            cursor.execute("""
                UPDATE kelas SET
                    id_user=?,
                    nama_kelas=?,
                    tahun_ajaran=?,
                    semester=?
                WHERE id_kelas=?
            """, (
                id_user,
                self.entry_kelas.get().strip(),
                self.entry_tahun.get().strip(),
                self.combo_semester.get(),
                self.id_kelas
            ))

            conn.commit()
            conn.close()

            messagebox.showinfo("Sukses", "Data kelas berhasil diupdate!")
            self.load_data()
            self.reset_form()

        except Exception as e:
            messagebox.showerror("Error", str(e))

    # ======================
    # HAPUS
    # ======================

    def hapus_kelas(self):
        if not self.id_kelas:
            messagebox.showwarning("Peringatan", "Pilih data yang akan dihapus!")
            return

        if messagebox.askyesno("Konfirmasi", "Yakin ingin menghapus data kelas ini?"):
            try:
                conn = connect_db()
                cursor = conn.cursor()

                cursor.execute(
                    "DELETE FROM kelas WHERE id_kelas=?",
                    (self.id_kelas,)
                )

                conn.commit()
                conn.close()

                messagebox.showinfo("Sukses", "Data kelas berhasil dihapus!")
                self.load_data()
                self.reset_form()

            except Exception as e:
                messagebox.showerror("Error", str(e))

    # ======================
    # CARI DATA
    # ======================

    def cari_data(self):
        keyword = self.entry_search.get().strip()

        for row in self.table.get_children():
            self.table.delete(row)

        try:
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
                LEFT JOIN users u ON k.id_user = u.id_user
                WHERE k.nama_kelas LIKE ?
                ORDER BY k.nama_kelas
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

    # ======================
    # RESET
    # ======================

    def reset_form(self):
        self.id_kelas = None
        
        if self.user_dict:
            first_guru = list(self.user_dict.keys())[0]
            self.combo_user.set(first_guru)
        else:
            self.combo_user.set("Tidak ada guru")

        self.entry_kelas.delete(0, "end")
        self.entry_tahun.delete(0, "end")
        self.combo_semester.set("Ganjil")
