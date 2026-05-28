import customtkinter as ctk
from tkinter import messagebox
import threading

from database.koneksi import connect_db

from pages.dashboard_admin import DashboardAdmin
from pages.dashboard_guru import DashboardGuru
from pages.dashboard_kepsek import DashboardKepsek


# =========================================================
# TEMA
# =========================================================

COLORS = {
    "bg_dark": "#0F1117",
    "bg_card": "#1A1D27",
    "bg_input": "#252836",
    "bg_input_hover": "#2E3247",
    "accent": "#4F6EF7",
    "accent_hover": "#6B85FF",
    "accent_glow": "#3A52C4",
    "text_primary": "#F0F2FF",
    "text_secondary": "#8B92B8",
    "text_muted": "#555B7A",
    "border": "#2A2F47",
    "border_focus": "#4F6EF7",
    "success": "#22C55E",
    "error": "#EF4444",
    "divider": "#1E2235",
}

FONTS = {
    "title": ("Segoe UI", 28, "bold"),
    "subtitle": ("Segoe UI", 12),
    "label": ("Segoe UI", 11, "bold"),
    "body": ("Segoe UI", 11),
    "small": ("Segoe UI", 10),
    "btn": ("Segoe UI", 13, "bold"),
}


# =========================================================
# MODERN ENTRY
# =========================================================

class ModernEntry(ctk.CTkFrame):

    def __init__(
        self,
        master,
        label: str,
        placeholder: str,
        icon: str = "○",
        show: str = ""
    ):

        super().__init__(
            master,
            fg_color=COLORS["bg_input"],
            corner_radius=12,
            border_width=1,
            border_color=COLORS["border"]
        )

        self.show_char = show

        self.grid_columnconfigure(1, weight=1)

        # ICON

        self.lbl_icon = ctk.CTkLabel(
            self,
            text=icon,
            font=("Segoe UI", 16),
            text_color=COLORS["text_muted"],
            width=36
        )

        self.lbl_icon.grid(
            row=0,
            column=0,
            padx=(12, 0),
            pady=14
        )

        # CONTAINER

        mid = ctk.CTkFrame(
            self,
            fg_color="transparent"
        )

        mid.grid(
            row=0,
            column=1,
            sticky="ew",
            padx=(4, 0)
        )

        mid.grid_columnconfigure(0, weight=1)

        # LABEL

        self.lbl_float = ctk.CTkLabel(
            mid,
            text=label,
            font=FONTS["small"],
            text_color=COLORS["text_muted"],
            anchor="w"
        )

        self.lbl_float.grid(
            row=0,
            column=0,
            sticky="w"
        )

        # ENTRY

        self.entry = ctk.CTkEntry(
            mid,
            placeholder_text=placeholder,
            placeholder_text_color=COLORS["text_muted"],
            fg_color="transparent",
            border_width=0,
            text_color=COLORS["text_primary"],
            font=FONTS["body"],
            show=show,
            height=28
        )

        self.entry.grid(
            row=1,
            column=0,
            sticky="ew",
            pady=(0, 6)
        )

        # BIND

        self.entry.bind("<FocusIn>", self._on_focus)
        self.entry.bind("<FocusOut>", self._on_blur)

        # TOGGLE PASSWORD

        if show:

            self.btn_toggle = ctk.CTkButton(
                self,
                text="●",
                width=36,
                height=36,
                fg_color="transparent",
                hover_color=COLORS["bg_input_hover"],
                text_color=COLORS["text_muted"],
                font=("Segoe UI", 12),
                corner_radius=8,
                command=self._toggle_show
            )

            self.btn_toggle.grid(
                row=0,
                column=2,
                padx=(0, 8)
            )

            self._hidden = True

    def _on_focus(self, event=None):

        self.configure(
            border_color=COLORS["border_focus"]
        )

        self.lbl_icon.configure(
            text_color=COLORS["accent"]
        )

        self.lbl_float.configure(
            text_color=COLORS["accent"]
        )

    def _on_blur(self, event=None):

        self.configure(
            border_color=COLORS["border"]
        )

        self.lbl_icon.configure(
            text_color=COLORS["text_muted"]
        )

        self.lbl_float.configure(
            text_color=COLORS["text_muted"]
        )

    def _toggle_show(self):

        if self._hidden:

            self.entry.configure(show="")
            self.btn_toggle.configure(text="○")

            self._hidden = False

        else:

            self.entry.configure(show=self.show_char)
            self.btn_toggle.configure(text="●")

            self._hidden = True

    def get(self):

        return self.entry.get()

    def set_error(self, is_error=True):

        color = COLORS["error"] if is_error else COLORS["border"]

        self.configure(border_color=color)


# =========================================================
# LOGIN PAGE
# =========================================================

class LoginPage(ctk.CTk):

    def __init__(self):
        super().__init__()

        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        self.title("Sistem Informasi Sekolah")

        self.geometry("480x620")
        self.resizable(False, False)

        self.configure(
            fg_color=COLORS["bg_dark"]
        )

        self.after(10, self._center_window)

        self._build_ui()

        self.bind(
            "<Return>",
            lambda _: self.login()
        )

    # =====================================================

    def _center_window(self):

        self.update_idletasks()

        w = 480
        h = 620

        sw = self.winfo_screenwidth()
        sh = self.winfo_screenheight()

        x = (sw - w) // 2
        y = (sh - h) // 2

        self.geometry(f"{w}x{h}+{x}+{y}")

    # =====================================================

    def _build_ui(self):

        self._draw_background()

        # CARD

        card = ctk.CTkFrame(
            self,
            width=400,
            height=540,
            fg_color=COLORS["bg_card"],
            corner_radius=24,
            border_width=1,
            border_color=COLORS["border"]
        )

        card.place(
            relx=0.5,
            rely=0.5,
            anchor="center"
        )

        card.pack_propagate(False)

        self._build_header(card)
        self._build_form(card)
        self._build_footer(card)

    # =====================================================

    def _draw_background(self):

        dot = ctk.CTkLabel(
            self,
            text="",
            width=180,
            height=180,
            fg_color=COLORS["accent_glow"],
            corner_radius=90
        )

        dot.place(x=-60, y=-60)

        dot2 = ctk.CTkLabel(
            self,
            text="",
            width=120,
            height=120,
            fg_color="#1A1040",
            corner_radius=60
        )

        dot2.place(x=380, y=500)

    # =====================================================

    def _build_header(self, parent):

        header = ctk.CTkFrame(
            parent,
            fg_color="transparent"
        )

        header.pack(
            pady=(36, 28),
            padx=32,
            fill="x"
        )

        logo = ctk.CTkFrame(
            header,
            width=52,
            height=52,
            fg_color=COLORS["accent"],
            corner_radius=16
        )

        logo.pack(anchor="center")
        logo.pack_propagate(False)

        ctk.CTkLabel(
            logo,
            text="✦",
            font=("Segoe UI", 22, "bold"),
            text_color="white"
        ).place(
            relx=0.5,
            rely=0.5,
            anchor="center"
        )

        ctk.CTkLabel(
            header,
            text="Selamat Datang",
            font=FONTS["title"],
            text_color=COLORS["text_primary"]
        ).pack(
            pady=(14, 4)
        )

        ctk.CTkLabel(
            header,
            text="Login Sistem Informasi Sekolah",
            font=FONTS["subtitle"],
            text_color=COLORS["text_secondary"]
        ).pack()

    # =====================================================

    def _build_form(self, parent):

        form = ctk.CTkFrame(
            parent,
            fg_color="transparent"
        )

        form.pack(
            padx=32,
            fill="x"
        )

        # USERNAME

        self.field_username = ModernEntry(
            form,
            label="Username",
            placeholder="Masukkan username",
            icon="⊙"
        )

        self.field_username.pack(
            fill="x",
            pady=(0, 14)
        )

        # PASSWORD

        self.field_password = ModernEntry(
            form,
            label="Password",
            placeholder="Masukkan password",
            icon="◈",
            show="●"
        )

        self.field_password.pack(
            fill="x",
            pady=(0, 18)
        )

        # BUTTON LOGIN

        self.btn_login = ctk.CTkButton(
            form,
            text="Masuk",
            height=50,
            font=FONTS["btn"],
            corner_radius=12,
            fg_color=COLORS["accent"],
            hover_color=COLORS["accent_hover"],
            command=self.login
        )

        self.btn_login.pack(fill="x")

    # =====================================================

    def _build_footer(self, parent):

        footer = ctk.CTkFrame(
            parent,
            fg_color="transparent"
        )

        footer.pack(
            side="bottom",
            pady=24,
            padx=32,
            fill="x"
        )

        ctk.CTkFrame(
            footer,
            fg_color=COLORS["divider"],
            height=1
        ).pack(
            fill="x",
            pady=(0, 16)
        )

        ctk.CTkLabel(
            footer,
            text="© 2025 Sistem Informasi Sekolah",
            font=FONTS["small"],
            text_color=COLORS["text_muted"]
        ).pack()

    # =====================================================

    def _set_loading(self, loading):

        if loading:

            self.btn_login.configure(
                text="Memproses...",
                state="disabled"
            )

        else:

            self.btn_login.configure(
                text="Masuk",
                state="normal"
            )

    # =====================================================

    def login(self):

        username = self.field_username.get().strip()
        password = self.field_password.get()

        if not username:

            messagebox.showwarning(
                "Peringatan",
                "Username tidak boleh kosong"
            )

            return

        if not password:

            messagebox.showwarning(
                "Peringatan",
                "Password tidak boleh kosong"
            )

            return

        self._set_loading(True)

        threading.Thread(
            target=self._do_login,
            args=(username, password),
            daemon=True
        ).start()

    # =====================================================

    def _do_login(self, username, password):

        conn = connect_db()

        if not conn:

            self.after(
                0,
                lambda: self._db_error()
            )

            return

        try:

            cursor = conn.cursor()

            query = """
                SELECT id_user, nama, role
                FROM users
                WHERE username=%s
                AND password=%s
            """

            cursor.execute(
                query,
                (username, password)
            )

            user = cursor.fetchone()

        except Exception as e:

            self.after(
                0,
                lambda: self._query_error(str(e))
            )

            return

        finally:

            cursor.close()
            conn.close()

        if user:

            id_user, nama, role = user

            self.after(
                0,
                lambda: self._login_success(
                    id_user,
                    nama,
                    role
                )
            )

        else:

            self.after(
                0,
                self._login_failed
            )

    # =====================================================

    def _login_success(self, id_user, nama, role):

        self._set_loading(False)

        dashboard_map = {
            "admin": DashboardAdmin,
            "guru": DashboardGuru,
            "kepala_sekolah": DashboardKepsek
        }

        DashboardClass = dashboard_map.get(role)

        if DashboardClass:

            messagebox.showinfo(
                "Berhasil",
                f"Selamat datang, {nama}"
            )

            self.after(
                300,
                lambda: self._open_dashboard(
                    DashboardClass,
                    id_user,
                    nama
                )
            )

        else:

            messagebox.showerror(
                "Error",
                f"Role '{role}' tidak dikenali"
            )

    # =====================================================

    def _login_failed(self):

        self._set_loading(False)

        messagebox.showerror(
            "Login Gagal",
            "Username atau password salah"
        )

        self.field_password.entry.delete(0, "end")

    # =====================================================

    def _db_error(self):

        self._set_loading(False)

        messagebox.showerror(
            "Database",
            "Koneksi database gagal"
        )

    # =====================================================

    def _query_error(self, detail):

        self._set_loading(False)

        messagebox.showerror(
            "Error",
            detail
        )

    # =====================================================

    def _open_dashboard(self, DashboardClass, id_user, nama):

        self.destroy()

        app = DashboardClass(id_user, nama)
        app.mainloop()


# =========================================================
# MAIN
# =========================================================

if __name__ == "__main__":

    app = LoginPage()
    app.mainloop()