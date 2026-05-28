import customtkinter as ctk

from pages.nilai_page import NilaiPage
from pages.kehadiran_page import KehadiranPage
from pages.motivasi_page import MotivasiPage
from pages.disiplin_page import DisiplinPage
from pages.prediksi_page import PrediksiPage


class DashboardGuru(ctk.CTk):

    def __init__(self):
        super().__init__()

        self.title("Dashboard Guru")
        self.geometry("800x500")

        ctk.CTkLabel(
            self,
            text="DASHBOARD GURU",
            font=("Arial", 26, "bold")
        ).pack(pady=30)

        frame = ctk.CTkFrame(self)
        frame.pack(pady=20)

        ctk.CTkButton(
            frame,
            text="Input Nilai",
            width=220,
            command=self.open_nilai
        ).grid(row=0, column=0, padx=10, pady=10)

        ctk.CTkButton(
            frame,
            text="Input Kehadiran",
            width=220,
            command=self.open_kehadiran
        ).grid(row=0, column=1, padx=10, pady=10)

        ctk.CTkButton(
            frame,
            text="Input Motivasi",
            width=220,
            command=self.open_motivasi
        ).grid(row=1, column=0, padx=10, pady=10)

        ctk.CTkButton(
            frame,
            text="Input Disiplin",
            width=220,
            command=self.open_disiplin
        ).grid(row=1, column=1, padx=10, pady=10)

        ctk.CTkButton(
            frame,
            text="Prediksi Risiko",
            width=220,
            command=self.open_prediksi
        ).grid(row=2, column=0, padx=10, pady=10)

    def open_nilai(self):
        app = NilaiPage()
        app.mainloop()

    def open_kehadiran(self):
        app = KehadiranPage()
        app.mainloop()

    def open_motivasi(self):
        app = MotivasiPage()
        app.mainloop()

    def open_disiplin(self):
        app = DisiplinPage()
        app.mainloop()

    def open_prediksi(self):
        app = PrediksiPage()
        app.mainloop()


if __name__ == "__main__":
    app = DashboardGuru()
    app.mainloop()
