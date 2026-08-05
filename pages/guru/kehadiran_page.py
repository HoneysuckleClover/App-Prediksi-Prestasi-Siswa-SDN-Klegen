import customtkinter as ctk
from tkinter import ttk, messagebox
from database.koneksi_sqlite import connect_db

class KehadiranPage(ctk.CTkFrame):

    def __init__(self, parent):
        super().__init__(parent)

        self.configure(fg_color="#0F172A")

        self.id_kehadiran = None
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
            text="📅 DATA KEHADIRAN SISWA",
            font=("Segoe UI", 28, "bold"),
            text_color="white"
        ).pack(anchor="w")

        ctk.CTkLabel(
            header_frame,
            text="Kelola data kehadiran siswa",
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
        
        for i in range(6):
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
            width=200,
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
            width=150,
            height=35,
            corner_radius=8
        )
        self.combo_semester.grid(row=0, column=3, padx=10, pady=(15, 10), sticky="w")

        # Separator
        ctk.CTkFrame(
            form_frame,
            fg_color="#334155",
            height=2
        ).grid(row=1, column=0, columnspan=6, sticky="ew", padx=20, pady=5)

        # Header Kehadiran
        ctk.CTkLabel(
            form_frame,
            text="📊 Detail Kehadiran",
            text_color="#60A5FA",
            font=("Segoe UI", 14, "bold")
        ).grid(row=2, column=0, columnspan=6, padx=15, pady=(10, 5), sticky="w")

        # ==================================
        # ENTRY KEHADIRAN
        # ==================================

        entry_style = {
            "width": 130,
            "height": 35,
            "fg_color": "#334155",
            "border_color": "#475569",
            "border_width": 2,
            "text_color": "white",
            "corner_radius": 8,
            "font": ("Segoe UI", 11)
        }

        # Row 3: Hadir & Sakit
        ctk.CTkLabel(
            form_frame,
            text="✅ Hadir",
            text_color="#4ADE80",
            font=("Segoe UI", 12, "bold")
        ).grid(row=3, column=0, padx=15, pady=8, sticky="w")

        self.entry_hadir = ctk.CTkEntry(form_frame, **entry_style)
        self.entry_hadir.grid(row=3, column=1, padx=10, pady=8, sticky="w")

        ctk.CTkLabel(
            form_frame,
            text="🤒 Sakit",
            text_color="#FBBF24",
            font=("Segoe UI", 12, "bold")
        ).grid(row=3, column=2, padx=15, pady=8, sticky="w")

        self.entry_sakit = ctk.CTkEntry(form_frame, **entry_style)
        self.entry_sakit.grid(row=3, column=3, padx=10, pady=8, sticky="w")

        # Row 4: Izin & Alpha
        ctk.CTkLabel(
            form_frame,
            text="📝 Izin",
            text_color="#60A5FA",
            font=("Segoe UI", 12, "bold")
        ).grid(row=4, column=0, padx=15, pady=8, sticky="w")

        self.entry_izin = ctk.CTkEntry(form_frame, **entry_style)
        self.entry_izin.grid(row=4, column=1, padx=10, pady=8, sticky="w")

        ctk.CTkLabel(
            form_frame,
            text="❌ Alpha",
            text_color="#F87171",
            font=("Segoe UI", 12, "bold")
        ).grid(row=4, column=2, padx=15, pady=8, sticky="w")

        self.entry_alpha = ctk.CTkEntry(form_frame, **entry_style)
        self.entry_alpha.grid(row=4, column=3, padx=10, pady=8, sticky="w")

        # ==================================
        # TOTAL KEHADIRAN (Auto Calculate)
        # ==================================

        ctk.CTkFrame(
            form_frame,
            fg_color="#334155",
            height=2
        ).grid(row=5, column=0, columnspan=6, sticky="ew", padx=20, pady=10)

        ctk.CTkLabel(
            form_frame,
            text="📊 Total Kehadiran",
            text_color="#FACC15",
            font=("Segoe UI", 13, "bold")
        ).grid(row=6, column=0, padx=15, pady=15, sticky="w")

        self.entry_total = ctk.CTkEntry(
            form_frame,
            width=130,
            height=40,
            fg_color="#1E293B",
            border_color="#FACC15",
            border_width=2,
            text_color="#FACC15",
            font=("Segoe UI", 14, "bold"),
            corner_radius=8
        )
        self.entry_total.grid(row=6, column=1, padx=10, pady=15, sticky="w")
        self.entry_total.configure(state="readonly")

        # Bind untuk auto calculate total
        self.entry_hadir.bind("<KeyRelease>", lambda e: self.hitung_total())
        self.entry_sakit.bind("<KeyRelease>", lambda e: self.hitung_total())
        self.entry_izin.bind("<KeyRelease>", lambda e: self.hitung_total())
        self.entry_alpha.bind("<KeyRelease>", lambda e: self.hitung_total())

        # ==================================
        # TEMPLATE FRAME
        # ==================================

        template_frame = ctk.CTkFrame(
            main_scroll,
            fg_color="transparent"
        )
        template_frame.pack(fill="x", pady=(0, 15))

        ctk.CTkButton(
            template_frame,
            text="📥 Download Template Kehadiran",
            width=200,
            height=38,
            fg_color="#8B5CF6",
            hover_color="#7C3AED",
            corner_radius=8,
            font=("Segoe UI", 12, "bold"),
            command=self.download_template
        ).pack(side="left", padx=5)

        ctk.CTkButton(
            template_frame,
            text="📤 Import Data Kehadiran",
            width=200,
            height=38,
            fg_color="#10B981",
            hover_color="#059669",
            corner_radius=8,
            font=("Segoe UI", 12, "bold"),
            command=self.import_data
        ).pack(side="left", padx=5)

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
            "hadir",
            "sakit",
            "izin",
            "alpha"
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
        self.table.heading("hadir", text="✅ Hadir")
        self.table.heading("sakit", text="🤒 Sakit")
        self.table.heading("izin", text="📝 Izin")
        self.table.heading("alpha", text="❌ Alpha")

        # COLUMN
        self.table.column("id", width=70, anchor="center")
        self.table.column("nama_siswa", width=280)
        self.table.column("semester", width=120, anchor="center")
        self.table.column("hadir", width=100, anchor="center")
        self.table.column("sakit", width=100, anchor="center")
        self.table.column("izin", width=100, anchor="center")
        self.table.column("alpha", width=100, anchor="center")

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
    # DOWNLOAD & IMPORT TEMPLATE
    # ==================================

    def download_template(self):
        from utils.import_export import ImportExportData
        importer = ImportExportData(self)
        importer.download_template("kehadiran")

    def import_data(self):
        from utils.import_export import ImportExportData
        importer = ImportExportData(self)
        importer.import_data("kehadiran")

    # ==================================
    # HITUNG TOTAL
    # ==================================

    def hitung_total(self):
        try:
            hadir = int(self.entry_hadir.get() or 0)
            sakit = int(self.entry_sakit.get() or 0)
            izin = int(self.entry_izin.get() or 0)
            alpha = int(self.entry_alpha.get() or 0)
            total = hadir + sakit + izin + alpha
            
            self.entry_total.configure(state="normal")
            self.entry_total.delete(0, "end")
            self.entry_total.insert(0, str(total))
            self.entry_total.configure(state="readonly")
        except:
            pass

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
            JOIN siswa s ON k.id_siswa = s.id_siswa
            ORDER BY s.nama_siswa
        """)
        data = cursor.fetchall()
        conn.close()

        for index, row in enumerate(data):
            tag = "evenrow" if index % 2 == 0 else "oddrow"
            self.table.insert("", "end", values=row, tags=(tag,))

    # ==================================
    # TAMBAH
    # ==================================

    def tambah_data(self):
        try:
            if self.combo_siswa.get() == "Pilih Siswa" or not self.combo_siswa.get():
                messagebox.showwarning("Peringatan", "Silakan pilih siswa terlebih dahulu!")
                return

            id_siswa = self.data_siswa[self.combo_siswa.get()]

            conn = connect_db()
            cursor = conn.cursor()

            cursor.execute("""
                INSERT INTO kehadiran
                (id_siswa, semester, hadir, sakit, izin, alpha)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (
                id_siswa,
                self.combo_semester.get(),
                self.entry_hadir.get() or 0,
                self.entry_sakit.get() or 0,
                self.entry_izin.get() or 0,
                self.entry_alpha.get() or 0
            ))

            conn.commit()
            conn.close()

            messagebox.showinfo("Sukses", "Data kehadiran berhasil ditambahkan!")
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

        self.id_kehadiran = data[0]
        self.combo_siswa.set(data[1])
        self.combo_semester.set(data[2])

        self.entry_hadir.delete(0, "end")
        self.entry_hadir.insert(0, data[3])

        self.entry_sakit.delete(0, "end")
        self.entry_sakit.insert(0, data[4])

        self.entry_izin.delete(0, "end")
        self.entry_izin.insert(0, data[5])

        self.entry_alpha.delete(0, "end")
        self.entry_alpha.insert(0, data[6])

        self.hitung_total()

    # ==================================
    # EDIT
    # ==================================

    def edit_data(self):
        if not self.id_kehadiran:
            messagebox.showwarning("Peringatan", "Pilih data yang akan diedit!")
            return

        try:
            id_siswa = self.data_siswa[self.combo_siswa.get()]

            conn = connect_db()
            cursor = conn.cursor()

            cursor.execute("""
                UPDATE kehadiran SET
                    id_siswa=?,
                    semester=?,
                    hadir=?,
                    sakit=?,
                    izin=?,
                    alpha=?
                WHERE id_kehadiran=?
            """, (
                id_siswa,
                self.combo_semester.get(),
                self.entry_hadir.get() or 0,
                self.entry_sakit.get() or 0,
                self.entry_izin.get() or 0,
                self.entry_alpha.get() or 0,
                self.id_kehadiran
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
        if not self.id_kehadiran:
            messagebox.showwarning("Peringatan", "Pilih data yang akan dihapus!")
            return

        if messagebox.askyesno("Konfirmasi", "Yakin ingin menghapus data ini?"):
            conn = connect_db()
            cursor = conn.cursor()
            cursor.execute("DELETE FROM kehadiran WHERE id_kehadiran=?", (self.id_kehadiran,))
            conn.commit()
            conn.close()
            self.load_data()
            self.reset_form()

    # ==================================
    # CARI
    # ==================================

    def cari_data(self):
        keyword = self.entry_search.get().strip()

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
            JOIN siswa s ON k.id_siswa = s.id_siswa
            WHERE s.nama_siswa LIKE ?
            ORDER BY s.nama_siswa
        """, (f"%{keyword}%",))
        data = cursor.fetchall()
        conn.close()

        for index, row in enumerate(data):
            tag = "evenrow" if index % 2 == 0 else "oddrow"
            self.table.insert("", "end", values=row, tags=(tag,))

    # ==================================
    # RESET
    # ==================================

    def reset_form(self):
        self.id_kehadiran = None
        self.combo_siswa.set("Pilih Siswa")
        self.combo_semester.set("Ganjil")

        self.entry_hadir.delete(0, "end")
        self.entry_sakit.delete(0, "end")
        self.entry_izin.delete(0, "end")
        self.entry_alpha.delete(0, "end")

        self.entry_total.configure(state="normal")
        self.entry_total.delete(0, "end")
        self.entry_total.configure(state="readonly")
