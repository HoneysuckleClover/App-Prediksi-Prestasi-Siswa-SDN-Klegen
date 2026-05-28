import customtkinter as ctk
from tkinter import ttk, messagebox
import mysql.connector
import os

from datetime import datetime

from reportlab.platypus import (
    SimpleDocTemplate,
    Table,
    TableStyle,
    Paragraph,
    Spacer
)

from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.pagesizes import letter


class RiwayatPrediksiPage(ctk.CTk):

    def __init__(self):
        super().__init__()

        self.title("Riwayat dan Hasil Prediksi")
        self.geometry("1000x600")

        # =========================
        # TITLE
        # =========================

        ctk.CTkLabel(
            self,
            text="RIWAYAT dan HASIL PREDIKSI SISWA",
            font=("Arial", 24, "bold")
        ).pack(pady=20)

        # =========================
        # BUTTON EXPORT PDF
        # =========================

        ctk.CTkButton(
            self,
            text="Export PDF",
            width=200,
            command=self.export_pdf
        ).pack(pady=10)

        # =========================
        # FRAME TABLE
        # =========================

        table_frame = ctk.CTkFrame(self)

        table_frame.pack(
            fill="both",
            expand=True,
            padx=20,
            pady=10
        )

        # =========================
        # SCROLLBAR
        # =========================

        scrollbar_y = ttk.Scrollbar(
            table_frame,
            orient="vertical"
        )

        scrollbar_x = ttk.Scrollbar(
            table_frame,
            orient="horizontal"
        )

        # =========================
        # TABLE
        # =========================

        self.table = ttk.Treeview(
            table_frame,
            columns=(
                "id",
                "nama",
                "probabilitas",
                "hasil",
                "tanggal"
            ),
            show="headings",
            yscrollcommand=scrollbar_y.set,
            xscrollcommand=scrollbar_x.set
        )

        # =========================
        # TABLE HEADING
        # =========================

        self.table.heading("id", text="ID")
        self.table.heading("nama", text="Nama Siswa")
        self.table.heading("probabilitas", text="Probabilitas")
        self.table.heading("hasil", text="Hasil Prediksi")
        self.table.heading("tanggal", text="Tanggal Prediksi")

        # =========================
        # COLUMN WIDTH
        # =========================

        self.table.column("id", width=70, anchor="center")
        self.table.column("nama", width=220, anchor="center")
        self.table.column("probabilitas", width=140, anchor="center")
        self.table.column("hasil", width=180, anchor="center")
        self.table.column("tanggal", width=220, anchor="center")

        # =========================
        # PACK TABLE
        # =========================

        self.table.pack(
            side="left",
            fill="both",
            expand=True
        )

        # =========================
        # CONFIG SCROLLBAR
        # =========================

        scrollbar_y.config(command=self.table.yview)
        scrollbar_y.pack(side="right", fill="y")

        scrollbar_x.config(command=self.table.xview)
        scrollbar_x.pack(side="bottom", fill="x")

        # =========================
        # LOAD DATA
        # =========================

        self.load_data()

    # =========================
    # DATABASE CONNECTION
    # =========================

    def connect_db(self):

        return mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="db_deteksi_prestasi"
        )

    # =========================
    # LOAD DATA
    # =========================

    def load_data(self):

        try:

            conn = self.connect_db()

            cursor = conn.cursor()

            query = """
                SELECT
                    hasil_prediksi.id_prediksi,
                    siswa.nama_siswa,
                    hasil_prediksi.probabilitas,
                    hasil_prediksi.hasil,
                    hasil_prediksi.tanggal_prediksi

                FROM hasil_prediksi

                JOIN siswa
                ON hasil_prediksi.id_siswa = siswa.id_siswa

                ORDER BY hasil_prediksi.id_prediksi DESC
            """

            cursor.execute(query)

            rows = cursor.fetchall()

            # =========================
            # HAPUS DATA LAMA
            # =========================

            for item in self.table.get_children():
                self.table.delete(item)

            # =========================
            # INSERT DATA
            # =========================

            for row in rows:

                data = (
                    row[0],
                    row[1],
                    f"{float(row[2]):.2f}",
                    row[3],
                    str(row[4])
                )

                self.table.insert("", "end", values=data)

            cursor.close()
            conn.close()

        except Exception as e:

            messagebox.showerror(
                "Error Load Data",
                str(e)
            )

    # =========================
    # EXPORT PDF
    # =========================

    def export_pdf(self):

        try:

            conn = self.connect_db()

            cursor = conn.cursor()

            query = """
                SELECT
                    siswa.nama_siswa,
                    hasil_prediksi.probabilitas,
                    hasil_prediksi.hasil,
                    hasil_prediksi.tanggal_prediksi

                FROM hasil_prediksi

                JOIN siswa
                ON hasil_prediksi.id_siswa = siswa.id_siswa

                ORDER BY hasil_prediksi.id_prediksi DESC
            """

            cursor.execute(query)

            rows = cursor.fetchall()

            # =========================
            # VALIDASI DATA
            # =========================

            if not rows:

                messagebox.showwarning(
                    "Warning",
                    "Data prediksi masih kosong!"
                )

                return

            # =========================
            # FOLDER DOWNLOAD WINDOWS
            # =========================

            download_folder = os.path.join(
                os.path.expanduser("~"),
                "Downloads"
            )

            # =========================
            # NAMA FILE PDF
            # =========================

            tanggal = datetime.now().strftime(
                "%Y-%m-%d_%H-%M-%S"
            )

            nama_file = (
                f"laporan_prediksi_{tanggal}.pdf"
            )

            file_path = os.path.join(
                download_folder,
                nama_file
            )

            # =========================
            # PDF DOCUMENT
            # =========================

            pdf = SimpleDocTemplate(
                file_path,
                pagesize=letter
            )

            elements = []

            styles = getSampleStyleSheet()

            title = Paragraph(
                "LAPORAN HASIL PREDIKSI SISWA",
                styles["Title"]
            )

            elements.append(title)

            elements.append(Spacer(1, 20))

            # =========================
            # TABLE DATA PDF
            # =========================

            data = [
                [
                    "No",
                    "Nama Siswa",
                    "Probabilitas",
                    "Hasil Prediksi",
                    "Tanggal"
                ]
            ]

            no = 1

            for row in rows:

                data.append([
                    no,
                    row[0],
                    f"{float(row[1]):.2f}",
                    row[2],
                    str(row[3])
                ])

                no += 1

            table = Table(
                data,
                colWidths=[40, 180, 100, 120, 170]
            )

            # =========================
            # STYLE TABLE
            # =========================

            style = TableStyle([

                ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),

                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),

                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),

                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),

                ('BACKGROUND', (0, 1), (-1, -1), colors.beige),

                ('GRID', (0, 0), (-1, -1), 1, colors.black)
            ])

            table.setStyle(style)

            elements.append(table)

            # =========================
            # BUILD PDF
            # =========================

            pdf.build(elements)

            cursor.close()
            conn.close()

            # =========================
            # SUCCESS MESSAGE
            # =========================

            messagebox.showinfo(
                "Sukses",
                f"PDF berhasil disimpan di:\n\n{file_path}"
            )

            # =========================
            # AUTO OPEN PDF
            # =========================

            os.startfile(file_path)

            print("PDF berhasil dibuat:", file_path)

        except Exception as e:

            messagebox.showerror(
                "Error Export PDF",
                str(e)
            )

            print("ERROR PDF:", e)


if __name__ == "__main__":

    app = RiwayatPrediksiPage()
    app.mainloop()