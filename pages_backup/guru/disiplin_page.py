import customtkinter as ctk
from tkinter import ttk, messagebox
from database.koneksi_sqlite import connect_db


class DisiplinPage(ctk.CTkFrame):

    def __init__(self, parent):
        super().__init__(parent)

        self.configure(fg_color="#0F172A")

        self.id_disiplin = None
        self.data_siswa = {}

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
            text="📊 DATA DISIPLIN BELAJAR",
            font=("Segoe UI", 28, "bold"),
            text_color="white"
        ).pack(anchor="w")

        ctk.CTkLabel(
            header_frame,
            text="Kelola data disiplin belajar siswa",
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

        # Row 0: Nama Siswa & Semester
        ctk.CTkLabel(
            form_frame,
            text="👤 Nama Siswa",
            text_color="white",
            font=("Segoe UI", 12, "bold")
        ).grid(row=0, column=0, padx=15, pady=(15, 10), sticky="w")

        self.combo_siswa = ctk.CTkOptionMenu(
            form_frame,
            values=["Pilih Siswa"],
            fg_color="#334155",
            button_color="#1E293B",
            button_hover_color="#475569",
            text_color="white",
            dropdown_fg_color="#1E293B",
            dropdown_text_color="white",
            dropdown_hover_color="#334155",
            width=220,
            height=35,
            corner_radius=8
        )
        self.combo_siswa.grid(row=0, column=1, padx=10, pady=(15, 10), sticky="w")

        ctk.CTkLabel(
            form_frame,
            text="📅 Semester",
            text_color="white",
            font=("Segoe UI", 12, "bold")
        ).grid(row=0, column=2, padx=15, pady=(15, 10), sticky="w")

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
        self.combo_semester.grid(row=0, column=3, padx=10, pady=(15, 10), sticky="w")

        # Separator
        ctk.CTkFrame(
            form_frame,
            fg_color="#334155",
            height=2
        ).grid(row=1, column=0, columnspan=4, sticky="ew", padx=20, pady=5)

        # Header Disiplin
        ctk.CTkLabel(
            form_frame,
            text="📊 Detail Disiplin Belajar",
            text_color="#60A5FA",
            font=("Segoe UI", 14, "bold")
        ).grid(row=2, column=0, columnspan=4, padx=15, pady=(10, 5), sticky="w")

        # ==================================
        # ENTRY SKOR DISIPLIN
        # ==================================

        entry_style = {
            "width": 200,
            "height": 35,
            "fg_color": "#334155",
            "border_color": "#475569",
            "border_width": 2,
            "text_color": "white",
            "corner_radius": 8,
            "font": ("Segoe UI", 11)
        }

        ctk.CTkLabel(
            form_frame,
            text="⭐ Skor Disiplin",
            text_color="#FACC15",
            font=("Segoe UI", 12, "bold")
        ).grid(row=3, column=0, padx=15, pady=15, sticky="w")

        self.entry_skor = ctk.CTkEntry(form_frame, **entry_style)
        self.entry_skor.grid(row=3, column=1, padx=10, pady=15, sticky="w")

        # Keterangan Skor
        keterangan_frame = ctk.CTkFrame(
            form_frame,
            fg_color="transparent"
        )
        keterangan_frame.grid(row=3, column=2, columnspan=2, padx=15, pady=15, sticky="w")

        ctk.CTkLabel(
            keterangan_frame,
            text="📌 Keterangan Skor:",
            text_color="#94A3B8",
            font=("Segoe UI", 11)
        ).pack(anchor="w")

        ctk.CTkLabel(
            keterangan_frame,
            text="80-100: Sangat Baik  |  60-79: Baik  |  40-59: Cukup  |  0-39: Kurang",
            text_color="#64748B",
            font=("Segoe UI", 10)
        ).pack(anchor="w")

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
            command=self.tambah_data,
            **button_style
        ).pack(side="left", padx=5)

        ctk.CTkButton(
            btn_frame,
            text="✏️ Edit",
            fg_color="#3B82F6",
            hover_color="#2563EB",
            command=self.edit_data,
            **button_style
        ).pack(side="left", padx=5)

        ctk.CTkButton(
            btn_frame,
            text="🗑️ Hapus",
            fg_color="#EF4444",
            hover_color="#DC2626",
            command=self.hapus_data,
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
            "nama_siswa",
            "semester",
            "skor_disiplin",
            "kategori"
        )

        self.table = ttk.Treeview(
            table_frame,
            columns=columns,
            show="headings",
            height=12
        )

        # HEADING
        self.table.heading("id", text="ID")
        self.table.heading("nama_siswa", text="👤 Nama Siswa")
        self.table.heading("semester", text="📅 Semester")
        self.table.heading("skor_disiplin", text="⭐ Skor")
        self.table.heading("kategori", text="📊 Kategori")

        # COLUMN
        self.table.column("id", width=70, anchor="center")
        self.table.column("nama_siswa", width=280)
        self.table.column("semester", width=150, anchor="center")
        self.table.column("skor_disiplin", width=120, anchor="center")
        self.table.column("kategori", width=150, anchor="center")

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

        self.load_siswa()
        self.load_data()

    # ==================================
    # GET KATEGORI
    # ==================================

    def get_kategori(self, skor):
        try:
            skor = int(skor)
            if skor >= 80:
                return "Sangat Baik"
            elif skor >= 60:
                return "Baik"
            elif skor >= 40:
                return "Cukup"
            else:
                return "Kurang"
        except:
            return "-"

    # ==================================
    # LOAD SISWA
    # ==================================

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
            self.data_siswa = {}
            nama_siswa = []
            for row in data:
                self.data_siswa[row[1]] = row[0]
                nama_siswa.append(row[1])
            self.combo_siswa.configure(values=nama_siswa)
            conn.close()
        except Exception as e:
            messagebox.showerror("Error", str(e))

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
                    d.id_disiplin,
                    s.nama_siswa,
                    d.semester,
                    d.skor_disiplin
                FROM disiplin_belajar d
                JOIN siswa s ON d.id_siswa = s.id_siswa
                ORDER BY s.nama_siswa
            """)
            data = cursor.fetchall()
            conn.close()

            for index, row in enumerate(data):
                kategori = self.get_kategori(row[3])
                values = list(row) + [kategori]
                tag = "evenrow" if index % 2 == 0 else "oddrow"
                self.table.insert("", "end", values=values, tags=(tag,))

        except Exception as e:
            messagebox.showerror("Error", str(e))

    # ==================================
    # TAMBAH
    # ==================================

    def tambah_data(self):
        try:
            if self.combo_siswa.get() == "Pilih Siswa" or not self.combo_siswa.get():
                messagebox.showwarning("Peringatan", "Silakan pilih siswa terlebih dahulu!")
                return

            skor = self.entry_skor.get()
            if not skor:
                messagebox.showwarning("Peringatan", "Silakan masukkan skor disiplin!")
                return

            id_siswa = self.data_siswa[self.combo_siswa.get()]

            conn = connect_db()
            cursor = conn.cursor()

            cursor.execute("""
                INSERT INTO disiplin_belajar
                (id_siswa, semester, skor_disiplin)
                VALUES (?, ?, ?)
            """, (
                id_siswa,
                self.combo_semester.get(),
                skor
            ))

            conn.commit()
            conn.close()

            messagebox.showinfo("Sukses", "Data disiplin berhasil ditambahkan!")
            self.load_data()
            self.reset_form()

        except Exception as e:
            messagebox.showerror("Error", str(e))

    # ==================================
    # PILIH DATA
    # ==================================

    def pilih_data(self, event):
        selected = self.table.focus()
        data = self.table.item(selected, "values")
        if not data:
            return

        self.id_disiplin = data[0]
        self.combo_siswa.set(data[1])
        self.combo_semester.set(data[2])

        self.entry_skor.delete(0, "end")
        self.entry_skor.insert(0, data[3])

    # ==================================
    # EDIT
    # ==================================

    def edit_data(self):
        if not self.id_disiplin:
            messagebox.showwarning("Peringatan", "Pilih data yang akan diedit!")
            return

        try:
            skor = self.entry_skor.get()
            if not skor:
                messagebox.showwarning("Peringatan", "Silakan masukkan skor disiplin!")
                return

            id_siswa = self.data_siswa[self.combo_siswa.get()]

            conn = connect_db()
            cursor = conn.cursor()

            cursor.execute("""
                UPDATE disiplin_belajar SET
                    id_siswa=?,
                    semester=?,
                    skor_disiplin=?
                WHERE id_disiplin=?
            """, (
                id_siswa,
                self.combo_semester.get(),
                skor,
                self.id_disiplin
            ))

            conn.commit()
            conn.close()

            messagebox.showinfo("Sukses", "Data berhasil diupdate!")
            self.load_data()
            self.reset_form()

        except Exception as e:
            messagebox.showerror("Error", str(e))

    # ==================================
    # HAPUS
    # ==================================

    def hapus_data(self):
        if not self.id_disiplin:
            messagebox.showwarning("Peringatan", "Pilih data yang akan dihapus!")
            return

        if messagebox.askyesno("Konfirmasi", "Yakin ingin menghapus data ini?"):
            try:
                conn = connect_db()
                cursor = conn.cursor()
                cursor.execute(
                    "DELETE FROM disiplin_belajar WHERE id_disiplin=?",
                    (self.id_disiplin,)
                )
                conn.commit()
                conn.close()
                self.load_data()
                self.reset_form()
            except Exception as e:
                messagebox.showerror("Error", str(e))

    # ==================================
    # CARI
    # ==================================

    def cari_data(self):
        keyword = self.entry_search.get().strip()

        for row in self.table.get_children():
            self.table.delete(row)

        try:
            conn = connect_db()
            cursor = conn.cursor()
            cursor.execute("""
                SELECT
                    d.id_disiplin,
                    s.nama_siswa,
                    d.semester,
                    d.skor_disiplin
                FROM disiplin_belajar d
                JOIN siswa s ON d.id_siswa = s.id_siswa
                WHERE s.nama_siswa LIKE ?
                ORDER BY s.nama_siswa
            """, (f"%{keyword}%",))
            data = cursor.fetchall()
            conn.close()

            for index, row in enumerate(data):
                kategori = self.get_kategori(row[3])
                values = list(row) + [kategori]
                tag = "evenrow" if index % 2 == 0 else "oddrow"
                self.table.insert("", "end", values=values, tags=(tag,))

        except Exception as e:
            messagebox.showerror("Error", str(e))

    # ==================================
    # RESET
    # ==================================

    def reset_form(self):
        self.id_disiplin = None
        self.combo_siswa.set("Pilih Siswa")
        self.combo_semester.set("Ganjil")
        self.entry_skor.delete(0, "end")
