import customtkinter as ctk
from tkinter import ttk, messagebox
from database.koneksi_sqlite import connect_db


class UserPage(ctk.CTkFrame):

    def __init__(self, parent=None):
        super().__init__(parent)

        self.configure(fg_color="#0F172A")

        self.id_user = None

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
            text="👥 MANAJEMEN USER",
            font=("Segoe UI", 28, "bold"),
            text_color="white"
        ).pack(anchor="w")

        ctk.CTkLabel(
            header_frame,
            text="Kelola akun user sistem",
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

        # Row 0: Nama & Username
        ctk.CTkLabel(
            form_frame,
            text="👤 Nama Lengkap",
            text_color="white",
            font=("Segoe UI", 12, "bold")
        ).grid(row=0, column=0, padx=15, pady=(15, 10), sticky="w")

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
        self.entry_nama.grid(row=0, column=1, padx=10, pady=(15, 10), sticky="w")

        ctk.CTkLabel(
            form_frame,
            text="🔑 Username",
            text_color="white",
            font=("Segoe UI", 12, "bold")
        ).grid(row=0, column=2, padx=15, pady=(15, 10), sticky="w")

        self.entry_username = ctk.CTkEntry(
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
        self.entry_username.grid(row=0, column=3, padx=10, pady=(15, 10), sticky="w")

        # Row 1: Password & Role
        ctk.CTkLabel(
            form_frame,
            text="🔒 Password",
            text_color="white",
            font=("Segoe UI", 12, "bold")
        ).grid(row=1, column=0, padx=15, pady=(10, 10), sticky="w")

        self.entry_password = ctk.CTkEntry(
            form_frame,
            width=200,
            height=35,
            fg_color="#334155",
            border_color="#475569",
            border_width=2,
            text_color="white",
            corner_radius=8,
            font=("Segoe UI", 11),
            show="*"
        )
        self.entry_password.grid(row=1, column=1, padx=10, pady=(10, 10), sticky="w")

        ctk.CTkLabel(
            form_frame,
            text="🎯 Role",
            text_color="white",
            font=("Segoe UI", 12, "bold")
        ).grid(row=1, column=2, padx=15, pady=(10, 10), sticky="w")

        self.combo_role = ctk.CTkOptionMenu(
            form_frame,
            values=["admin", "guru", "kepala_sekolah"],
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
        self.combo_role.grid(row=1, column=3, padx=10, pady=(10, 10), sticky="w")

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
            command=self.tambah_user,
            **button_style
        ).pack(side="left", padx=5)

        ctk.CTkButton(
            btn_frame,
            text="✏️ Edit",
            fg_color="#3B82F6",
            hover_color="#2563EB",
            command=self.edit_user,
            **button_style
        ).pack(side="left", padx=5)

        ctk.CTkButton(
            btn_frame,
            text="🗑️ Hapus",
            fg_color="#EF4444",
            hover_color="#DC2626",
            command=self.hapus_user,
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
            placeholder_text="🔍 Cari Nama User...",
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
            command=self.cari_user
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
            "nama",
            "username",
            "role"
        )

        self.table = ttk.Treeview(
            table_frame,
            columns=columns,
            show="headings",
            height=12
        )

        # HEADING
        self.table.heading("id", text="ID")
        self.table.heading("nama", text="👤 Nama")
        self.table.heading("username", text="🔑 Username")
        self.table.heading("role", text="🎯 Role")

        # COLUMN
        self.table.column("id", width=70, anchor="center")
        self.table.column("nama", width=280)
        self.table.column("username", width=200)
        self.table.column("role", width=150, anchor="center")

        # ZEBRA ROW
        self.table.tag_configure(
            "oddrow",
            background="#1E293B"
        )
        self.table.tag_configure(
            "evenrow",
            background="#273549"
        )

        # Color tags for role
        self.table.tag_configure(
            "admin",
            foreground="#60A5FA"
        )
        self.table.tag_configure(
            "guru",
            foreground="#4ADE80"
        )
        self.table.tag_configure(
            "kepala_sekolah",
            foreground="#FBBF24"
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
                SELECT id_user, nama, username, role
                FROM users
                ORDER BY nama
            """)

            data = cursor.fetchall()
            conn.close()

            for index, row in enumerate(data):
                tag = "evenrow" if index % 2 == 0 else "oddrow"
                
                # Tambah tag berdasarkan role
                role_tag = ""
                if row[3] == "admin":
                    role_tag = "admin"
                elif row[3] == "guru":
                    role_tag = "guru"
                elif row[3] == "kepala_sekolah":
                    role_tag = "kepala_sekolah"
                
                if role_tag:
                    tag += f" {role_tag}"
                
                self.table.insert("", "end", values=row, tags=(tag,))

        except Exception as e:
            messagebox.showerror("Error", str(e))

    # ======================
    # TAMBAH
    # ======================

    def tambah_user(self):
        nama = self.entry_nama.get().strip()
        username = self.entry_username.get().strip()
        password = self.entry_password.get().strip()
        role = self.combo_role.get()

        if not nama or not username or not password:
            messagebox.showwarning(
                "Peringatan",
                "Semua field wajib diisi!\n\n"
                "• Nama Lengkap\n"
                "• Username\n"
                "• Password"
            )
            return

        try:
            conn = connect_db()
            cursor = conn.cursor()

            # Cek username sudah digunakan
            cursor.execute(
                "SELECT username FROM users WHERE username=?",
                (username,)
            )

            if cursor.fetchone():
                messagebox.showerror(
                    "Error",
                    f"Username '{username}' sudah digunakan!"
                )
                conn.close()
                return

            cursor.execute("""
                INSERT INTO users (nama, username, password, role)
                VALUES (?,?,?,?)
            """, (
                nama,
                username,
                password,
                role
            ))

            conn.commit()
            conn.close()

            messagebox.showinfo("Sukses", "User berhasil ditambahkan!")
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

        self.id_user = data[0]

        self.entry_nama.delete(0, "end")
        self.entry_nama.insert(0, data[1])

        self.entry_username.delete(0, "end")
        self.entry_username.insert(0, data[2])

        self.combo_role.set(data[3])
        
        # Kosongkan password untuk keamanan
        self.entry_password.delete(0, "end")

    # ======================
    # EDIT
    # ======================

    def edit_user(self):
        if not self.id_user:
            messagebox.showwarning("Peringatan", "Pilih data yang akan diedit!")
            return

        nama = self.entry_nama.get().strip()
        username = self.entry_username.get().strip()
        password = self.entry_password.get().strip()
        role = self.combo_role.get()

        if not nama or not username:
            messagebox.showwarning(
                "Peringatan",
                "Nama dan Username wajib diisi!"
            )
            return

        try:
            conn = connect_db()
            cursor = conn.cursor()

            # Cek username sudah digunakan oleh user lain
            cursor.execute("""
                SELECT username FROM users 
                WHERE username=? AND id_user!=?
            """, (username, self.id_user))

            if cursor.fetchone():
                messagebox.showerror(
                    "Error",
                    f"Username '{username}' sudah digunakan!"
                )
                conn.close()
                return

            # Jika password diisi, update password juga
            if password:
                cursor.execute("""
                    UPDATE users SET
                        nama=?,
                        username=?,
                        password=?,
                        role=?
                    WHERE id_user=?
                """, (
                    nama,
                    username,
                    password,
                    role,
                    self.id_user
                ))
            else:
                cursor.execute("""
                    UPDATE users SET
                        nama=?,
                        username=?,
                        role=?
                    WHERE id_user=?
                """, (
                    nama,
                    username,
                    role,
                    self.id_user
                ))

            conn.commit()
            conn.close()

            messagebox.showinfo("Sukses", "User berhasil diperbarui!")
            self.load_data()
            self.reset_form()

        except Exception as e:
            messagebox.showerror("Error", str(e))

    # ======================
    # HAPUS
    # ======================

    def hapus_user(self):
        if not self.id_user:
            messagebox.showwarning("Peringatan", "Pilih data yang akan dihapus!")
            return

        if messagebox.askyesno("Konfirmasi", "Yakin ingin menghapus user ini?"):
            try:
                conn = connect_db()
                cursor = conn.cursor()

                cursor.execute(
                    "DELETE FROM users WHERE id_user=?",
                    (self.id_user,)
                )

                conn.commit()
                conn.close()

                messagebox.showinfo("Sukses", "User berhasil dihapus!")
                self.load_data()
                self.reset_form()

            except Exception as e:
                messagebox.showerror("Error", str(e))

    # ======================
    # CARI
    # ======================

    def cari_user(self):
        keyword = self.entry_search.get().strip()

        for row in self.table.get_children():
            self.table.delete(row)

        try:
            conn = connect_db()
            cursor = conn.cursor()

            cursor.execute("""
                SELECT id_user, nama, username, role
                FROM users
                WHERE nama LIKE ?
                ORDER BY nama
            """, (f"%{keyword}%",))

            data = cursor.fetchall()
            conn.close()

            for index, row in enumerate(data):
                tag = "evenrow" if index % 2 == 0 else "oddrow"
                
                if row[3] == "admin":
                    tag += " admin"
                elif row[3] == "guru":
                    tag += " guru"
                elif row[3] == "kepala_sekolah":
                    tag += " kepala_sekolah"
                
                self.table.insert("", "end", values=row, tags=(tag,))

            if len(data) == 0:
                messagebox.showinfo("Info", "Data tidak ditemukan!")

        except Exception as e:
            messagebox.showerror("Error", str(e))

    # ======================
    # RESET
    # ======================

    def reset_form(self):
        self.id_user = None

        self.entry_nama.delete(0, "end")
        self.entry_username.delete(0, "end")
        self.entry_password.delete(0, "end")

        self.combo_role.set("guru")
