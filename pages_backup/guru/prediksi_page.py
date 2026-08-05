import customtkinter as ctk
from tkinter import ttk, messagebox
import joblib
import os
from datetime import date
from database.koneksi_sqlite import connect_db


class PrediksiPage(ctk.CTkFrame):

    def __init__(self, parent):
        super().__init__(parent)

        self.configure(fg_color="#0F172A")
        self.data_siswa = {}

        # =========================
        # LOAD MODEL 
        # =========================
        try:
            BASE_DIR = os.path.abspath(
                os.path.join(os.path.dirname(__file__), "..", "..")
            )
            
            MODEL_PATH = os.path.join(
                BASE_DIR, 
                "models", 
                "model_logistic.pkl"
            )

            self.model = joblib.load(MODEL_PATH)
            
            print("FITUR MODEL =", self.model.n_features_in_)
            print("INTERCEPT =", self.model.intercept_)
            print("KOEFISIEN =", self.model.coef_)
                
        except Exception as e:
            messagebox.showerror("Error Model", f"Gagal load model:\n{e}")
            self.model = None

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
            text="🎯 PREDIKSI PRESTASI SISWA",
            font=("Segoe UI", 28, "bold"),
            text_color="white"
        ).pack(anchor="w")

        ctk.CTkLabel(
            header_frame,
            text="Prediksi prestasi siswa berdasarkan data nilai, kehadiran, motivasi, dan disiplin",
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
        
        for i in range(3):
            form_frame.grid_columnconfigure(i, weight=1)

        # Row 0: Nama Siswa
        ctk.CTkLabel(
            form_frame,
            text="👤 Pilih Siswa",
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
            width=250,
            height=35,
            corner_radius=8
        )
        self.combo_siswa.grid(row=0, column=1, padx=10, pady=(15, 10), sticky="w")

        ctk.CTkButton(
            form_frame,
            text="🔮 Prediksi",
            width=150,
            height=40,
            fg_color="#8B5CF6",
            hover_color="#7C3AED",
            corner_radius=10,
            font=("Segoe UI", 13, "bold"),
            command=self.prediksi
        ).grid(row=0, column=2, padx=15, pady=(15, 10))

        # ==================================
        # HASIL PREDIKSI CARD
        # ==================================

        hasil_frame = ctk.CTkFrame(
            main_scroll,
            fg_color="#1E293B",
            corner_radius=15,
            border_width=1,
            border_color="#334155"
        )
        hasil_frame.pack(fill="x", pady=(0, 15))

        # Header hasil
        ctk.CTkLabel(
            hasil_frame,
            text="📊 Hasil Prediksi",
            text_color="#60A5FA",
            font=("Segoe UI", 14, "bold")
        ).pack(anchor="w", padx=20, pady=(15, 5))

        # Separator
        ctk.CTkFrame(
            hasil_frame,
            fg_color="#334155",
            height=2
        ).pack(fill="x", padx=20, pady=5)

        # Container hasil
        hasil_content = ctk.CTkFrame(
            hasil_frame,
            fg_color="transparent"
        )
        hasil_content.pack(fill="x", padx=20, pady=15)

        # Status prediksi
        status_frame = ctk.CTkFrame(
            hasil_content,
            fg_color="#1E293B"
        )
        status_frame.pack(side="left", expand=True, fill="both")

        ctk.CTkLabel(
            status_frame,
            text="Status",
            text_color="#94A3B8",
            font=("Segoe UI", 12)
        ).pack()

        self.lbl_status = ctk.CTkLabel(
            status_frame,
            text="❓ Belum Ada Prediksi",
            font=("Segoe UI", 18, "bold"),
            text_color="#94A3B8"
        )
        self.lbl_status.pack(pady=5)

        # Probabilitas
        prob_frame = ctk.CTkFrame(
            hasil_content,
            fg_color="#1E293B"
        )
        prob_frame.pack(side="left", expand=True, fill="both")

        ctk.CTkLabel(
            prob_frame,
            text="Probabilitas",
            text_color="#94A3B8",
            font=("Segoe UI", 12)
        ).pack()

        self.lbl_prob = ctk.CTkLabel(
            prob_frame,
            text="0%",
            font=("Segoe UI", 18, "bold"),
            text_color="#60A5FA"
        )
        self.lbl_prob.pack(pady=5)

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

        # HEADING
        self.table.heading("id_prediksi", text="ID")
        self.table.heading("nama_siswa", text="👤 Nama Siswa")
        self.table.heading("probabilitas", text="📊 Probabilitas")
        self.table.heading("hasil", text="🎯 Hasil Prediksi")
        self.table.heading("tanggal", text="📅 Tanggal")

        # COLUMN
        self.table.column("id_prediksi", width=70, anchor="center")
        self.table.column("nama_siswa", width=280)
        self.table.column("probabilitas", width=150, anchor="center")
        self.table.column("hasil", width=180, anchor="center")
        self.table.column("tanggal", width=150, anchor="center")

        # ZEBRA ROW
        self.table.tag_configure(
            "oddrow",
            background="#1E293B"
        )
        self.table.tag_configure(
            "evenrow",
            background="#273549"
        )

        # Color tags untuk hasil
        self.table.tag_configure(
            "berprestasi",
            foreground="#4ADE80"
        )
        self.table.tag_configure(
            "berisiko",
            foreground="#F87171"
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

        self.load_siswa()
        self.load_data()

    # =================================
    # LOAD DATA
    # =================================

    def load_data(self):
        for item in self.table.get_children():
            self.table.delete(item)

        try:
            conn = connect_db()
            cursor = conn.cursor()

            cursor.execute("""
                SELECT
                    hp.id_prediksi,
                    s.nama_siswa,
                    hp.probabilitas,
                    hp.hasil,
                    hp.tanggal_prediksi
                FROM hasil_prediksi hp
                JOIN siswa s ON hp.id_siswa = s.id_siswa
                ORDER BY hp.id_prediksi DESC
            """)

            rows = cursor.fetchall()
            conn.close()

            for index, row in enumerate(rows):
                tag = "evenrow" if index % 2 == 0 else "oddrow"
                
                # Format probabilitas
                prob = row[2]
                prob_text = f"{float(prob):.1f}%" if prob is not None else "0%"
                
                # Tambah tag warna berdasarkan hasil
                if "Berisiko" in row[3]:
                    tag += " berisiko"
                elif "Tidak Berisiko" in row[3]:
                    tag += " berprestasi"
                
                values = list(row)
                values[2] = prob_text
                
                self.table.insert("", "end", values=values, tags=(tag,))

        except Exception as e:
            print(f"Error loading data: {e}")
            messagebox.showerror("Error", str(e))

    # =================================
    # LOAD SISWA
    # =================================

    def load_siswa(self):
        try:
            conn = connect_db()
            cursor = conn.cursor()

            cursor.execute("""
                SELECT id_siswa, nama_siswa
                FROM siswa
                ORDER BY nama_siswa
            """)

            rows = cursor.fetchall()
            conn.close()

            self.data_siswa = {}
            daftar_nama = []

            for row in rows:
                self.data_siswa[row[1]] = row[0]
                daftar_nama.append(row[1])

            self.combo_siswa.configure(values=daftar_nama)

            if daftar_nama:
                self.combo_siswa.set(daftar_nama[0])

        except Exception as e:
            messagebox.showerror("Error Load Data", str(e))

    # =================================
    # PREDIKSI
    # =================================

    def prediksi(self):
        print("DEBUG: tombol prediksi ditekan")

        if self.model is None:
            messagebox.showerror("Error", "Model tidak berhasil dimuat!")
            return

        nama_siswa = self.combo_siswa.get()

        if nama_siswa not in self.data_siswa or nama_siswa == "Pilih Siswa":
            messagebox.showwarning(
                "Peringatan",
                "Pilih siswa terlebih dahulu!"
            )
            return

        id_siswa = self.data_siswa[nama_siswa]

        try:
            conn = connect_db()
            cursor = conn.cursor()

            # =====================
            # NILAI
            # =====================
            cursor.execute("""
                SELECT rata_nilai
                FROM nilai
                WHERE id_siswa=?
                ORDER BY id_nilai DESC
                LIMIT 1
            """, (id_siswa,))
            nilai = cursor.fetchone()

            # =====================
            # KEHADIRAN
            # =====================
            cursor.execute("""
                SELECT hadir, sakit, izin, alpha
                FROM kehadiran
                WHERE id_siswa=?
                ORDER BY id_kehadiran DESC
                LIMIT 1
            """, (id_siswa,))
            kehadiran = cursor.fetchone()

            # =====================
            # MOTIVASI
            # =====================
            cursor.execute("""
                SELECT skor_motivasi
                FROM motivasi
                WHERE id_siswa=?
                ORDER BY id_motivasi DESC
                LIMIT 1
            """, (id_siswa,))
            motivasi = cursor.fetchone()

            # =====================
            # DISIPLIN
            # =====================
            cursor.execute("""
                SELECT skor_disiplin
                FROM disiplin_belajar
                WHERE id_siswa=?
                ORDER BY id_disiplin DESC
                LIMIT 1
            """, (id_siswa,))
            disiplin = cursor.fetchone()

            conn.close()

            # =====================
            # CEK DATA
            # =====================
            if not nilai or not kehadiran or not motivasi or not disiplin:
                messagebox.showwarning(
                    "Data Tidak Lengkap",
                    "Data siswa belum lengkap!\n\n"
                    "Pastikan siswa memiliki data:\n"
                    "✅ Nilai\n"
                    "✅ Kehadiran\n"
                    "✅ Motivasi\n"
                    "✅ Disiplin"
                )
                return

            # =====================
            # FITUR MODEL
            # =====================
            fitur = [[
                float(nilai[0]),        # rata_nilai
                int(kehadiran[0]),      # hadir
                int(kehadiran[1]),      # sakit
                int(kehadiran[2]),      # izin
                int(kehadiran[3]),      # alpha
                int(motivasi[0]),       # skor_motivasi
                int(disiplin[0])        # skor_disiplin
            ]]

            # =====================
            # PREDIKSI
            # =====================
            hasil = self.model.predict(fitur)[0]
            probabilitas = self.model.predict_proba(fitur)[0][1] * 100

            # =====================
            # UPDATE UI
            # =====================
            if hasil == 1:
                status = "⚠️ Berisiko"
                warna = "#F87171"
            else:
                status = "✅ Tidak Berisiko"
                warna = "#4ADE80"

            self.lbl_status.configure(
                text=status,
                text_color=warna
            )
            self.lbl_prob.configure(
                text=f"{probabilitas:.1f}%",
                text_color="#60A5FA"
            )

            # =====================
            # SIMPAN HASIL
            # =====================
            conn = connect_db()
            cursor = conn.cursor()

            cursor.execute("""
                INSERT INTO hasil_prediksi
                (id_siswa, probabilitas, hasil, tanggal_prediksi)
                VALUES (?,?,?,?)
            """, (
                id_siswa,
                round(probabilitas, 2),
                "Berisiko" if hasil == 1 else "Tidak Berisiko",
                date.today()
            ))

            conn.commit()
            conn.close()

            # =====================
            # REFRESH TABLE
            # =====================
            self.load_data()

            messagebox.showinfo("Sukses", "Prediksi berhasil dilakukan!")

        except Exception as e:
            print("ERROR:", e)
            messagebox.showerror("Error", str(e))

    # =================================
    # CARI DATA
    # =================================

    def cari_data(self):
        keyword = self.entry_search.get().strip()

        for item in self.table.get_children():
            self.table.delete(item)

        try:
            conn = connect_db()
            cursor = conn.cursor()

            cursor.execute("""
                SELECT
                    hp.id_prediksi,
                    s.nama_siswa,
                    hp.probabilitas,
                    hp.hasil,
                    hp.tanggal_prediksi
                FROM hasil_prediksi hp
                JOIN siswa s ON hp.id_siswa = s.id_siswa
                WHERE s.nama_siswa LIKE ?
                ORDER BY hp.id_prediksi DESC
            """, (f"%{keyword}%",))

            rows = cursor.fetchall()
            conn.close()

            for index, row in enumerate(rows):
                tag = "evenrow" if index % 2 == 0 else "oddrow"
                
                prob = row[2]
                prob_text = f"{float(prob):.1f}%" if prob is not None else "0%"
                
                if "Berisiko" in row[3]:
                    tag += " berisiko"
                elif "Tidak Berisiko" in row[3]:
                    tag += " berprestasi"
                
                values = list(row)
                values[2] = prob_text
                
                self.table.insert("", "end", values=values, tags=(tag,))

            if len(rows) == 0:
                messagebox.showinfo("Info", "Data tidak ditemukan!")

        except Exception as e:
            messagebox.showerror("Error", str(e))
