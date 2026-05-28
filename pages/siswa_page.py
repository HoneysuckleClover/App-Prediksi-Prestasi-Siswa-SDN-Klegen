import customtkinter as ctk
from tkinter import ttk, messagebox
from database.koneksi import connect_db


class SiswaPage(ctk.CTk):

    def __init__(self):
        super().__init__()

        # =========================
        # WINDOW
        # =========================

        self.title("Data Siswa")
        self.geometry("1250x720")
        self.state("zoomed")

        # =========================
        # TITLE
        # =========================

        title = ctk.CTkLabel(
            self,
            text="MANAJEMEN DATA SISWA",
            font=("Arial", 32, "bold")
        )
        title.pack(pady=20)

        # =========================
        # FRAME FORM
        # =========================

        form_frame = ctk.CTkFrame(
            self,
            width=350,
            height=650,
            corner_radius=20
        )

        form_frame.place(x=20, y=80)

        # =========================
        # FORM INPUT
        # =========================

        # NIS
        ctk.CTkLabel(
            form_frame,
            text="NIS",
            font=("Arial", 18)
        ).place(x=25, y=20)

        self.entry_nis = ctk.CTkEntry(
            form_frame,
            width=280,
            height=40
        )

        self.entry_nis.place(x=25, y=55)

        # Nama
        ctk.CTkLabel(
            form_frame,
            text="Nama",
            font=("Arial", 18)
        ).place(x=25, y=115)

        self.entry_nama = ctk.CTkEntry(
            form_frame,
            width=280,
            height=40
        )

        self.entry_nama.place(x=25, y=150)

        # Jenis Kelamin
        ctk.CTkLabel(
            form_frame,
            text="Jenis Kelamin",
            font=("Arial", 18)
        ).place(x=25, y=210)

        self.combo_jk = ctk.CTkComboBox(
            form_frame,
            values=["L", "P"],
            width=280,
            height=40
        )

        self.combo_jk.place(x=25, y=245)

        # Kelas
        ctk.CTkLabel(
            form_frame,
            text="Kelas",
            font=("Arial", 18)
        ).place(x=25, y=305)

        self.entry_kelas = ctk.CTkEntry(
            form_frame,
            width=280,
            height=40
        )

        self.entry_kelas.place(x=25, y=340)

        # Tanggal Lahir
        ctk.CTkLabel(
            form_frame,
            text="Tanggal Lahir",
            font=("Arial", 18)
        ).place(x=25, y=400)

        self.entry_ttl = ctk.CTkEntry(
            form_frame,
            placeholder_text="YYYY-MM-DD",
            width=280,
            height=40
        )

        self.entry_ttl.place(x=25, y=435)

        # Alamat
        ctk.CTkLabel(
            form_frame,
            text="Alamat",
            font=("Arial", 18)
        ).place(x=25, y=495)

        self.entry_alamat = ctk.CTkEntry(
            form_frame,
            width=280,
            height=40
        )

        self.entry_alamat.place(x=25, y=530)

        # =========================
        # BUTTON
        # =========================

        button_frame = ctk.CTkFrame(
            form_frame,
            fg_color="transparent"
        )

        button_frame.place(x=20, y=590)

        # Tambah
        self.btn_tambah = ctk.CTkButton(
            button_frame,
            text="Tambah",
            width=85,
            height=40,
            command=self.tambah_siswa
        )

        self.btn_tambah.grid(
            row=0,
            column=0,
            padx=5
        )

        # Update
        self.btn_update = ctk.CTkButton(
            button_frame,
            text="Update",
            width=85,
            height=40,
            fg_color="orange",
            hover_color="#cc8400",
            command=self.update_siswa
        )

        self.btn_update.grid(
            row=0,
            column=1,
            padx=5
        )

        # Hapus
        self.btn_hapus = ctk.CTkButton(
            button_frame,
            text="Hapus",
            width=85,
            height=40,
            fg_color="red",
            hover_color="darkred",
            command=self.hapus_siswa
        )

        self.btn_hapus.grid(
            row=0,
            column=2,
            padx=5
        )

        # =========================
        # STYLE TABLE
        # =========================

        style = ttk.Style()

        style.theme_use("default")

        style.configure(
            "Treeview",
            rowheight=35,
            font=("Arial", 11)
        )

        style.configure(
            "Treeview.Heading",
            font=("Arial", 11, "bold")
        )

        # =========================
        # FRAME TABLE
        # =========================

        table_frame = ctk.CTkFrame(
            self,
            width=820,
            height=650,
            corner_radius=20
        )

        table_frame.place(x=400, y=80)

        # =========================
        # TABLE
        # =========================

        self.table = ttk.Treeview(
            table_frame,
            columns=(
                "id",
                "nis",
                "nama",
                "jk",
                "kelas",
                "ttl",
                "alamat"
            ),
            show="headings"
        )

        # Heading
        self.table.heading("id", text="ID")
        self.table.heading("nis", text="NIS")
        self.table.heading("nama", text="Nama")
        self.table.heading("jk", text="JK")
        self.table.heading("kelas", text="Kelas")
        self.table.heading("ttl", text="Tanggal Lahir")
        self.table.heading("alamat", text="Alamat")

        # Width Kolom
        self.table.column("id", width=50, anchor="center")
        self.table.column("nis", width=90, anchor="center")
        self.table.column("nama", width=170)
        self.table.column("jk", width=70, anchor="center")
        self.table.column("kelas", width=80, anchor="center")
        self.table.column("ttl", width=130, anchor="center")
        self.table.column("alamat", width=180)

        self.table.place(
            x=10,
            y=10,
            width=780,
            height=620
        )

        # =========================
        # SCROLLBAR
        # =========================

        scroll_y = ttk.Scrollbar(
            table_frame,
            orient="vertical",
            command=self.table.yview
        )

        self.table.configure(
            yscrollcommand=scroll_y.set
        )

        scroll_y.place(
            x=790,
            y=10,
            height=620
        )

        # =========================
        # EVENT TABLE
        # =========================

        self.table.bind(
            "<<TreeviewSelect>>",
            self.pilih_data
        )

        self.selected_id = None

        self.load_data()

    # =========================
    # LOAD DATA
    # =========================

    def load_data(self):

        for item in self.table.get_children():
            self.table.delete(item)

        conn = connect_db()

        if conn:

            cursor = conn.cursor()

            query = "SELECT * FROM siswa"

            cursor.execute(query)

            rows = cursor.fetchall()

            for row in rows:
                self.table.insert("", "end", values=row)

            cursor.close()
            conn.close()

    # =========================
    # TAMBAH DATA
    # =========================

    def tambah_siswa(self):

        conn = connect_db()

        if conn:

            cursor = conn.cursor()

            query = """
                INSERT INTO siswa
                (
                    nis,
                    nama_siswa,
                    jenis_kelamin,
                    kelas,
                    tanggal_lahir,
                    alamat
                )
                VALUES (%s,%s,%s,%s,%s,%s)
            """

            values = (
                self.entry_nis.get(),
                self.entry_nama.get(),
                self.combo_jk.get(),
                self.entry_kelas.get(),
                self.entry_ttl.get(),
                self.entry_alamat.get()
            )

            cursor.execute(query, values)

            conn.commit()

            messagebox.showinfo(
                "Sukses",
                "Data siswa berhasil ditambahkan"
            )

            cursor.close()
            conn.close()

            self.load_data()
            self.clear_form()

    # =========================
    # PILIH DATA
    # =========================

    def pilih_data(self, event):

        selected = self.table.focus()

        data = self.table.item(selected)

        values = data["values"]

        if values:

            self.selected_id = values[0]

            self.entry_nis.delete(0, "end")
            self.entry_nis.insert(0, values[1])

            self.entry_nama.delete(0, "end")
            self.entry_nama.insert(0, values[2])

            self.combo_jk.set(values[3])

            self.entry_kelas.delete(0, "end")
            self.entry_kelas.insert(0, values[4])

            self.entry_ttl.delete(0, "end")
            self.entry_ttl.insert(0, values[5])

            self.entry_alamat.delete(0, "end")
            self.entry_alamat.insert(0, values[6])

    # =========================
    # UPDATE DATA
    # =========================

    def update_siswa(self):

        if not self.selected_id:
            return

        conn = connect_db()

        if conn:

            cursor = conn.cursor()

            query = """
                UPDATE siswa
                SET
                    nis=%s,
                    nama_siswa=%s,
                    jenis_kelamin=%s,
                    kelas=%s,
                    tanggal_lahir=%s,
                    alamat=%s
                WHERE id_siswa=%s
            """

            values = (
                self.entry_nis.get(),
                self.entry_nama.get(),
                self.combo_jk.get(),
                self.entry_kelas.get(),
                self.entry_ttl.get(),
                self.entry_alamat.get(),
                self.selected_id
            )

            cursor.execute(query, values)

            conn.commit()

            messagebox.showinfo(
                "Sukses",
                "Data siswa berhasil diupdate"
            )

            cursor.close()
            conn.close()

            self.load_data()
            self.clear_form()

    # =========================
    # HAPUS DATA
    # =========================

    def hapus_siswa(self):

        if not self.selected_id:
            return

        jawab = messagebox.askyesno(
            "Konfirmasi",
            "Yakin ingin menghapus data?"
        )

        if jawab:

            conn = connect_db()

            if conn:

                cursor = conn.cursor()

                query = """
                    DELETE FROM siswa
                    WHERE id_siswa=%s
                """

                cursor.execute(
                    query,
                    (self.selected_id,)
                )

                conn.commit()

                messagebox.showinfo(
                    "Sukses",
                    "Data siswa berhasil dihapus"
                )

                cursor.close()
                conn.close()

                self.load_data()
                self.clear_form()

    # =========================
    # CLEAR FORM
    # =========================

    def clear_form(self):

        self.entry_nis.delete(0, "end")
        self.entry_nama.delete(0, "end")

        self.combo_jk.set("")

        self.entry_kelas.delete(0, "end")
        self.entry_ttl.delete(0, "end")
        self.entry_alamat.delete(0, "end")

        self.selected_id = None


# =========================
# MAIN
# =========================

if __name__ == "__main__":
    app = SiswaPage()
    app.mainloop()