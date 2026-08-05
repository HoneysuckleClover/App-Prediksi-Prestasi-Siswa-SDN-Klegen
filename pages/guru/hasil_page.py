import customtkinter as ctk
from tkinter import ttk, messagebox
from database.koneksi_sqlite import connect_db


class HasilPage(ctk.CTkFrame):

    def __init__(self, parent):
        super().__init__(parent)

        self.configure(fg_color="#0F172A")

        # ==================================
        # STYLE TABLE
        # ==================================

        style = ttk.Style()
        style.theme_use("clam")

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

        style.map(
            "Treeview",
            background=[("selected", "#2563EB")],
            foreground=[("selected", "white")]
        )

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
            text="🎯 HASIL PREDIKSI SISWA",
            font=("Segoe UI", 28, "bold"),
            text_color="white"
        ).pack(anchor="w")

        ctk.CTkLabel(
            header_frame,
            text="Hasil prediksi prestasi siswa",
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
        # STATISTIK CARD
        # ==================================

        stats_frame = ctk.CTkFrame(
            main_scroll,
            fg_color="transparent"
        )
        stats_frame.pack(fill="x", pady=(0, 15))

        # Card 1: Total Prediksi
        card1 = ctk.CTkFrame(
            stats_frame,
            fg_color="#1E293B",
            corner_radius=15,
            border_width=1,
            border_color="#334155"
        )
        card1.pack(side="left", fill="x", expand=True, padx=5)

        ctk.CTkLabel(
            card1,
            text="📊",
            font=("Segoe UI", 28)
        ).pack(pady=(10, 0))

        ctk.CTkLabel(
            card1,
            text="Total Prediksi",
            text_color="#94A3B8",
            font=("Segoe UI", 12)
        ).pack()

        self.label_total = ctk.CTkLabel(
            card1,
            text="0",
            text_color="white",
            font=("Segoe UI", 20, "bold")
        )
        self.label_total.pack(pady=(0, 10))

        # Card 2: Prediksi Berhasil
        card2 = ctk.CTkFrame(
            stats_frame,
            fg_color="#1E293B",
            corner_radius=15,
            border_width=1,
            border_color="#334155"
        )
        card2.pack(side="left", fill="x", expand=True, padx=5)

        ctk.CTkLabel(
            card2,
            text="✅",
            font=("Segoe UI", 28)
        ).pack(pady=(10, 0))

        ctk.CTkLabel(
            card2,
            text="Tidak Berisiko",
            text_color="#4ADE80",
            font=("Segoe UI", 12)
        ).pack()

        self.label_berhasil = ctk.CTkLabel(
            card2,
            text="0",
            text_color="#4ADE80",
            font=("Segoe UI", 20, "bold")
        )
        self.label_berhasil.pack(pady=(0, 10))

        # Card 3: Prediksi Berisiko
        card3 = ctk.CTkFrame(
            stats_frame,
            fg_color="#1E293B",
            corner_radius=15,
            border_width=1,
            border_color="#334155"
        )
        card3.pack(side="left", fill="x", expand=True, padx=5)

        ctk.CTkLabel(
            card3,
            text="⚠️",
            font=("Segoe UI", 28)
        ).pack(pady=(10, 0))

        ctk.CTkLabel(
            card3,
            text="Berisiko",
            text_color="#F87171",
            font=("Segoe UI", 12)
        ).pack()

        self.label_bimbingan = ctk.CTkLabel(
            card3,
            text="0",
            text_color="#F87171",
            font=("Segoe UI", 20, "bold")
        )
        self.label_bimbingan.pack(pady=(0, 10))

        # Card 4: Rata-rata Probabilitas
        card4 = ctk.CTkFrame(
            stats_frame,
            fg_color="#1E293B",
            corner_radius=15,
            border_width=1,
            border_color="#334155"
        )
        card4.pack(side="left", fill="x", expand=True, padx=5)

        ctk.CTkLabel(
            card4,
            text="📈",
            font=("Segoe UI", 28)
        ).pack(pady=(10, 0))

        ctk.CTkLabel(
            card4,
            text="Rata-rata Prob.",
            text_color="#60A5FA",
            font=("Segoe UI", 12)
        ).pack()

        self.label_rata = ctk.CTkLabel(
            card4,
            text="0%",
            text_color="#60A5FA",
            font=("Segoe UI", 20, "bold")
        )
        self.label_rata.pack(pady=(0, 10))

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
            "id_prediksi",
            "nama_siswa",
            "kelas",
            "probabilitas",
            "hasil",
            "tanggal"
        )

        self.table = ttk.Treeview(
            table_frame,
            columns=columns,
            show="headings",
            height=12
        )

        self.table.heading("id_prediksi", text="ID")
        self.table.heading("nama_siswa", text="👤 Nama Siswa")
        self.table.heading("kelas", text="📚 Kelas")
        self.table.heading("probabilitas", text="📊 Probabilitas")
        self.table.heading("hasil", text="🎯 Hasil Prediksi")
        self.table.heading("tanggal", text="📅 Tanggal")

        self.table.column("id_prediksi", width=70, anchor="center")
        self.table.column("nama_siswa", width=250)
        self.table.column("kelas", width=120, anchor="center")
        self.table.column("probabilitas", width=130, anchor="center")
        self.table.column("hasil", width=180, anchor="center")
        self.table.column("tanggal", width=150, anchor="center")

        self.table.tag_configure("oddrow", background="#1E293B")
        self.table.tag_configure("evenrow", background="#273549")

        self.table.tag_configure("berprestasi", foreground="#4ADE80")
        self.table.tag_configure("berisiko", foreground="#F87171")

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

        self.load_data()

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
                    hp.id_prediksi,
                    s.nama_siswa,
                    COALESCE(k.nama_kelas, '-') AS kelas,
                    hp.probabilitas,
                    hp.hasil,
                    hp.tanggal_prediksi
                FROM hasil_prediksi hp
                JOIN siswa s ON hp.id_siswa = s.id_siswa
                LEFT JOIN kelas k ON s.id_kelas = k.id_kelas
                ORDER BY hp.id_prediksi DESC
            """)

            data = cursor.fetchall()
            conn.close()

            total = len(data)
            berhasil = 0
            berisiko = 0
            total_prob = 0

            for index, row in enumerate(data):
                tag = "evenrow" if index % 2 == 0 else "oddrow"
                
                hasil = str(row[4])
                if "Tidak Berisiko" in hasil or "Berprestasi" in hasil:
                    tag += " berprestasi"
                    berhasil += 1
                else:
                    tag += " berisiko"
                    berisiko += 1
                
                prob = row[3]
                if prob is not None:
                    total_prob += float(prob)
                    prob_text = f"{float(prob):.1f}%"
                else:
                    prob_text = "0%"
                
                values = list(row)
                values[3] = prob_text
                
                self.table.insert("", "end", values=values, tags=(tag,))

            self.label_total.configure(text=str(total))
            self.label_berhasil.configure(text=str(berhasil))
            self.label_bimbingan.configure(text=str(berisiko))
            
            rata = total_prob / total if total > 0 else 0
            self.label_rata.configure(text=f"{rata:.1f}%")

        except Exception as e:
            messagebox.showerror("Error", f"Gagal load data:\n{str(e)}")

    # ==================================
    # CARI DATA
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
                    hp.id_prediksi,
                    s.nama_siswa,
                    COALESCE(k.nama_kelas, '-') AS kelas,
                    hp.probabilitas,
                    hp.hasil,
                    hp.tanggal_prediksi
                FROM hasil_prediksi hp
                JOIN siswa s ON hp.id_siswa = s.id_siswa
                LEFT JOIN kelas k ON s.id_kelas = k.id_kelas
                WHERE s.nama_siswa LIKE ?
                ORDER BY hp.id_prediksi DESC
            """, (f"%{keyword}%",))

            data = cursor.fetchall()
            conn.close()

            total = len(data)
            berhasil = 0
            berisiko = 0
            total_prob = 0

            for index, row in enumerate(data):
                tag = "evenrow" if index % 2 == 0 else "oddrow"
                
                hasil = str(row[4])
                if "Tidak Berisiko" in hasil or "Berprestasi" in hasil:
                    tag += " berprestasi"
                    berhasil += 1
                else:
                    tag += " berisiko"
                    berisiko += 1
                
                prob = row[3]
                if prob is not None:
                    total_prob += float(prob)
                    prob_text = f"{float(prob):.1f}%"
                else:
                    prob_text = "0%"
                
                values = list(row)
                values[3] = prob_text
                
                self.table.insert("", "end", values=values, tags=(tag,))

            self.label_total.configure(text=str(total))
            self.label_berhasil.configure(text=str(berhasil))
            self.label_bimbingan.configure(text=str(berisiko))
            
            rata = total_prob / total if total > 0 else 0
            self.label_rata.configure(text=f"{rata:.1f}%")

            if total == 0:
                messagebox.showinfo("Info", "Data tidak ditemukan!")

        except Exception as e:
            messagebox.showerror("Error", str(e))