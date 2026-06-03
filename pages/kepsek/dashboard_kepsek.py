import customtkinter as ctk

class DashboardKepsek(ctk.CTk):

    def __init__(self):
        super().__init__()

        self.title("Dashboard Kepala Sekolah")
        self.geometry("1200x700")

        ctk.CTkLabel(
            self,
            text="DASHBOARD KEPALA SEKOLAH",
            font=("Arial", 24, "bold")
        ).pack(pady=50)

        self.mainloop()