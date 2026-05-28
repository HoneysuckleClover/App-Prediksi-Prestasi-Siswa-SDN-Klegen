import customtkinter as ctk

from pages.prediksi_page import PrediksiPage


class DashboardKepsek(ctk.CTk):

    def __init__(self):
        super().__init__()

        self.title("Dashboard Kepala Sekolah")
        self.geometry("700x400")

        ctk.CTkLabel(
            self,
            text="DASHBOARD KEPALA SEKOLAH",
            font=("Arial", 24, "bold")
        ).pack(pady=40)

        ctk.CTkButton(
            self,
            text="Lihat Prediksi Risiko",
            width=300,
            height=50,
            command=self.open_prediksi
        ).pack(pady=30)

    def open_prediksi(self):
        app = PrediksiPage()
        app.mainloop()


if __name__ == "__main__":
    app = DashboardKepsek()
    app.mainloop()
