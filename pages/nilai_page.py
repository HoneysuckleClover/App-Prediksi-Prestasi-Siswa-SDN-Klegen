import customtkinter as ctk
from tkinter import ttk, messagebox
from database.koneksi import connect_db


class NilaiPage(ctk.CTk):

    def __init__(self):
        super().__init__()

        # =========================
        # WINDOW
        # =========================

        self.title("Data Nilai Siswa")
        self.geometry("1250x720")
        self.state("zoomed")

        # =========================
        # TITLE
        # =========================

        title = ctk.CTkLabel(
            self,
            text="MANAJEMEN DATA NILAI",
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

        form_frame.place(relx=0.02, rely=0.12)

        # =========================
        # FORM INPUT
        # =========================

        # Pilih Siswa
        ctk.CTkLabel(
            form_frame,
            text="Pilih Siswa",
            font=("Arial", 18)
        ).place(x=25, y=20)

        self.combo_siswa = ctk.CTkComboBox(
            form_frame,
            values=[],
            width=280,
            height=40
        )

        self.combo_siswa.place(x=25, y=55)

        # Semester
        ctk.CTkLabel(
            form_frame,
            text="Semester",
            font=("Arial", 18)
        ).place(x=25, y=130)

        self.entry_semester = ctk.CTkEntry(
            form_frame,
            width=280,
            height=40
        )

        self.entry_semester.place(x=25, y=165)

        # Nilai
        ctk.CTkLabel(
            form_frame,
            text="Rata-rata Nilai",
            font=("Arial", 18)
        ).place(x=25, y=240)

        self.entry_nilai = ctk.CTkEntry(
            form_frame,
            width=280,
            height=40
        )

        self.entry_nilai.place(x=25, y=275)

        # =========================
        # BUTTON
        # =========================

        button_frame = ctk.CTkFrame(
            form_frame,
            fg_color="transparent"
        )

        button_frame.place(x=20, y=360)

        # Tambah
        self.btn_tambah = ctk.CTkButton(
            button_frame,
            text="Tambah",
            width=85,
            height=40,
            command=self.tambah_nilai
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
            command=self.update_nilai
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
            command=self.hapus_nilai
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
            width=900,
            height=650,
            corner_radius=20
        )

        table_frame.place(relx=0.30, rely=0.12)

        # =========================
        # TABLE
        # =========================

        self.table = ttk.Treeview(
            table_frame,
            columns=(
                "id",
                "nama",
                "semester",
                "nilai"
            ),
            show="headings"
        )

        # Heading
        self.table.heading("id", text="ID")
        self.table.heading("nama", text="Nama Siswa")
        self.table.heading("semester", text="Semester")
        self.table.heading("nilai", text="Rata-rata")

        # Column Width
        self.table.column("id", width=70, anchor="center")
        self.table.column("nama", width=300)
        self.table.column("semester", width=150, anchor="center")
        self.table.column("nilai", width=150, anchor="center")

        self.table.place(
            x=10,
            y=10,
            width=860,
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
            x=870,
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

        self.load_siswa()
        self.load_data()

    # =========================
    # LOAD SISWA
    # =========================

    def load_siswa(self):

        conn = connect_db()

        if conn:

            cursor = conn.cursor()

            query = """
                SELECT id_siswa, nama_siswa
                FROM siswa
            """

            cursor.execute(query)

            rows = cursor.fetchall()

            self.siswa_map = {}

            siswa_list = []

            for row in rows:

                siswa_id = row[0]
                nama = row[1]

                siswa_list.append(nama)

                self.siswa_map[nama] = siswa_id

            self.combo_siswa.configure(
                values=siswa_list
            )

            cursor.close()
            conn.close()

    # =========================
    # LOAD DATA
    # =========================

    def load_data(self):

        for item in self.table.get_children():
            self.table.delete(item)

        conn = connect_db()

        if conn:

            cursor = conn.cursor()

            query = """
                SELECT
                    nilai.id_nilai,
                    siswa.nama_siswa,
                    nilai.semester,
                    nilai.rata_nilai
                FROM nilai
                JOIN siswa
                ON nilai.id_siswa = siswa.id_siswa
            """

            cursor.execute(query)

            rows = cursor.fetchall()

            for row in rows:
                self.table.insert(
                    "",
                    "end",
                    values=row
                )

            cursor.close()
            conn.close()

    # =========================
    # TAMBAH DATA
    # =========================

    def tambah_nilai(self):

        nama_siswa = self.combo_siswa.get()

        id_siswa = self.siswa_map.get(
            nama_siswa
        )

        conn = connect_db()

        if conn:

            cursor = conn.cursor()

            query = """
                INSERT INTO nilai
                (
                    id_siswa,
                    semester,
                    rata_nilai
                )
                VALUES (%s,%s,%s)
            """

            values = (
                id_siswa,
                self.entry_semester.get(),
                self.entry_nilai.get()
            )

            cursor.execute(query, values)

            conn.commit()

            messagebox.showinfo(
                "Sukses",
                "Data nilai berhasil ditambahkan"
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

            self.combo_siswa.set(values[1])

            self.entry_semester.delete(0, "end")
            self.entry_semester.insert(0, values[2])

            self.entry_nilai.delete(0, "end")
            self.entry_nilai.insert(0, values[3])

    # =========================
    # UPDATE DATA
    # =========================

    def update_nilai(self):

        if not self.selected_id:
            return

        nama_siswa = self.combo_siswa.get()

        id_siswa = self.siswa_map.get(
            nama_siswa
        )

        conn = connect_db()

        if conn:

            cursor = conn.cursor()

            query = """
                UPDATE nilai
                SET
                    id_siswa=%s,
                    semester=%s,
                    rata_nilai=%s
                WHERE id_nilai=%s
            """

            values = (
                id_siswa,
                self.entry_semester.get(),
                self.entry_nilai.get(),
                self.selected_id
            )

            cursor.execute(query, values)

            conn.commit()

            messagebox.showinfo(
                "Sukses",
                "Data nilai berhasil diupdate"
            )

            cursor.close()
            conn.close()

            self.load_data()
            self.clear_form()

    # =========================
    # HAPUS DATA
    # =========================

    def hapus_nilai(self):

        if not self.selected_id:
            return

        jawab = messagebox.askyesno(
            "Konfirmasi",
            "Yakin ingin menghapus data nilai?"
        )

        if jawab:

            conn = connect_db()

            if conn:

                cursor = conn.cursor()

                query = """
                    DELETE FROM nilai
                    WHERE id_nilai=%s
                """

                cursor.execute(
                    query,
                    (self.selected_id,)
                )

                conn.commit()

                messagebox.showinfo(
                    "Sukses",
                    "Data nilai berhasil dihapus"
                )

                cursor.close()
                conn.close()

                self.load_data()
                self.clear_form()

    # =========================
    # CLEAR FORM
    # =========================

    def clear_form(self):

        self.combo_siswa.set("")

        self.entry_semester.delete(0, "end")

        self.entry_nilai.delete(0, "end")

        self.selected_id = None


# =========================
# MAIN
# =========================

if __name__ == "__main__":
    app = NilaiPage()
    app.mainloop()