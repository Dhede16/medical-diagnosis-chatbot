"""
Login App — CustomTkinter + MySQL (XAMPP)
Jalankan: python login_app.py
Install : pip install customtkinter mysql-connector-python
"""

from typing import Any, cast
from database import setup_database, get_conn, sha, DB_CONFIG, DB_NAME
from config import C 
import customtkinter as ctk
import mysql.connector
from mysql.connector import Error
import hashlib
import threading


# ─── App ──────────────────────────────────────────────────────────────────────
class LoginApp(ctk.CTk):
    def __init__(self, on_success=None):
        """
        on_success : callable | None
            Jika diberikan, akan dipanggil dengan argumen (username: str)
            setelah login berhasil, kemudian window login ditutup otomatis.
        """
        super().__init__()
        self._on_success = on_success  # callback ke main

        self.title("CareBot — Login")
        self.geometry("420x580")
        self.minsize(380, 520)
        self.resizable(True, True)
        self.configure(fg_color=C["bg"])

        # Centre window
        self.update_idletasks()
        x = (self.winfo_screenwidth()  - 420) // 2
        y = (self.winfo_screenheight() - 580) // 2
        self.geometry(f"+{x}+{y}")

        self._tab = "login"          # "login" | "register"
        self._show_pw_login    = False
        self._show_pw_register = False

        self._build_ui()
        self._init_db()

    # ── Build UI ─────────────────────────────────────────────────────────────
    def _build_ui(self):
        # Outer padding frame
        self.outer = ctk.CTkFrame(self, fg_color=C["bg"])
        self.outer.pack(fill="both", expand=True, padx=32, pady=32)

        # ── Logo row
        logo_row = ctk.CTkFrame(self.outer, fg_color="transparent")
        logo_row.pack(fill="x", pady=(0, 22))

        logo_box = ctk.CTkFrame(logo_row, width=42, height=42,
                                fg_color=C["accent"], corner_radius=10)
        logo_box.pack(side="left", anchor="center")
        logo_box.pack_propagate(False)
        ctk.CTkLabel(logo_box, text="✦", font=("Helvetica", 20, "bold"),
                     text_color="white").pack(expand=True)

        ctk.CTkLabel(logo_row, text="  ChatApp",
                     font=("Helvetica", 20, "bold"),
                     text_color=C["text"]).pack(side="left", anchor="center")

        # ── Card frame
        self.card = ctk.CTkFrame(self.outer, fg_color=C["card"],
                                 corner_radius=14,
                                 border_width=1, border_color=C["border"])
        self.card.pack(fill="both", expand=True)

        inner = ctk.CTkFrame(self.card, fg_color="transparent")
        inner.pack(fill="both", expand=True, padx=28, pady=24)

        # ── Title
        self.lbl_title = ctk.CTkLabel(inner, text="Masuk ke akun Anda",
                                      font=("Helvetica", 17, "bold"),
                                      text_color=C["text"])
        self.lbl_title.pack(pady=(0, 2))

        self.lbl_sub = ctk.CTkLabel(inner, text="Selamat datang kembali",
                                    font=("Helvetica", 12),
                                    text_color=C["text_muted"])
        self.lbl_sub.pack(pady=(0, 16))

        # ── Tab bar
        tab_frame = ctk.CTkFrame(inner, fg_color=C["input"], corner_radius=8)
        tab_frame.pack(fill="x", pady=(0, 18))
        tab_frame.columnconfigure(0, weight=1)
        tab_frame.columnconfigure(1, weight=1)

        self.tab_login = ctk.CTkButton(
            tab_frame, text="Masuk", corner_radius=6,
            fg_color=C["card"], hover_color=C["input_hover"],
            text_color=C["text"], font=("Helvetica", 13, "bold"),
            command=lambda: self._switch("login"))
        self.tab_login.grid(row=0, column=0, padx=3, pady=3, sticky="ew")

        self.tab_reg = ctk.CTkButton(
            tab_frame, text="Daftar", corner_radius=6,
            fg_color="transparent", hover_color=C["input_hover"],
            text_color=C["text_muted"], font=("Helvetica", 13),
            command=lambda: self._switch("register"))
        self.tab_reg.grid(row=0, column=1, padx=3, pady=3, sticky="ew")

        # ── Alert label
        self.alert_var = ctk.StringVar(value="")
        self.alert_lbl = ctk.CTkLabel(inner, textvariable=self.alert_var,
                                      font=("Helvetica", 12),
                                      text_color=C["error"],
                                      wraplength=320, justify="left")
        self.alert_lbl.pack(fill="x", pady=(0, 6))
        self.alert_lbl.pack_forget()   # hidden initially

        # ── Login Panel
        self.panel_login = ctk.CTkFrame(inner, fg_color="transparent")
        self._build_login_panel(self.panel_login)
        self.panel_login.pack(fill="both", expand=True)

        # ── Register Panel (hidden)
        self.panel_reg = ctk.CTkFrame(inner, fg_color="transparent")
        self._build_register_panel(self.panel_reg)

        # ── DB status bar at bottom
        self.status_var = ctk.StringVar(value="⏳ Menghubungkan ke database…")
        self.status_lbl = ctk.CTkLabel(self.outer, textvariable=self.status_var,
                                       font=("Helvetica", 11),
                                       text_color=C["text_muted"])
        self.status_lbl.pack(pady=(10, 0))

    def _field_label(self, parent, text):
        ctk.CTkLabel(parent, text=text, font=("Helvetica", 12, "bold"),
                     text_color=C["text_muted"], anchor="w").pack(fill="x", pady=(8, 2))

    def _entry(self, parent, placeholder, show=""):
        e = ctk.CTkEntry(parent, placeholder_text=placeholder,
                         fg_color=C["input"], border_color=C["border"],
                         border_width=1, corner_radius=8,
                         text_color=C["text"],
                         placeholder_text_color=C["text_muted"],
                         font=("Helvetica", 13),
                         height=40, show=show)
        e.pack(fill="x")
        return e

    def _pw_row(self, parent, placeholder, on_toggle):
        """Password entry + show/hide button in a row."""
        row = ctk.CTkFrame(parent, fg_color="transparent")
        row.pack(fill="x")
        row.columnconfigure(0, weight=1)

        entry = ctk.CTkEntry(row, placeholder_text=placeholder,
                             fg_color=C["input"], border_color=C["border"],
                             border_width=1, corner_radius=8,
                             text_color=C["text"],
                             placeholder_text_color=C["text_muted"],
                             font=("Helvetica", 13),
                             height=40, show="●")
        entry.grid(row=0, column=0, sticky="ew")

        toggle = ctk.CTkButton(row, text="👁", width=40, height=40,
                               fg_color=C["input"], hover_color=C["input_hover"],
                               corner_radius=8, border_width=1,
                               border_color=C["border"],
                               text_color=C["text_muted"],
                               font=("Helvetica", 14),
                               command=lambda: on_toggle(entry, toggle))
        toggle.grid(row=0, column=1, padx=(6, 0))
        return entry

    # ── Login panel ──────────────────────────────────────────────────────────
    def _build_login_panel(self, parent):
        self._field_label(parent, "Username")
        self.ent_lu = self._entry(parent, "Masukkan username")

        self._field_label(parent, "Password")
        self.ent_lp = self._pw_row(parent, "Masukkan password",
                                   self._toggle_login_pw)

        self.btn_login = ctk.CTkButton(
            parent, text="Masuk", height=42, corner_radius=8,
            fg_color=C["accent"], hover_color=C["accent_hov"],
            text_color="white", font=("Helvetica", 14, "bold"),
            command=self._do_login)
        self.btn_login.pack(fill="x", pady=(18, 0))

        # Enter key
        self.ent_lu.bind("<Return>", lambda e: self._do_login())
        self.ent_lp.bind("<Return>", lambda e: self._do_login())

    # ── Register panel ───────────────────────────────────────────────────────
    def _build_register_panel(self, parent):
        self._field_label(parent, "Username")
        self.ent_ru = self._entry(parent, "Buat username baru")

        self._field_label(parent, "Password")
        self.ent_rp = self._pw_row(parent, "Minimal 6 karakter",
                                   self._toggle_reg_pw)

        self.btn_reg = ctk.CTkButton(
            parent, text="Buat Akun", height=42, corner_radius=8,
            fg_color=C["accent"], hover_color=C["accent_hov"],
            text_color="white", font=("Helvetica", 14, "bold"),
            command=self._do_register)
        self.btn_reg.pack(fill="x", pady=(18, 0))

        self.ent_ru.bind("<Return>", lambda e: self._do_register())
        self.ent_rp.bind("<Return>", lambda e: self._do_register())

    # ── Toggle password visibility ───────────────────────────────────────────
    def _toggle_login_pw(self, entry, btn):
        self._show_pw_login = not self._show_pw_login
        entry.configure(show="" if self._show_pw_login else "●")
        btn.configure(text="🙈" if self._show_pw_login else "👁")

    def _toggle_reg_pw(self, entry, btn):
        self._show_pw_register = not self._show_pw_register
        entry.configure(show="" if self._show_pw_register else "●")
        btn.configure(text="🙈" if self._show_pw_register else "👁")

    # ── Tab switch ───────────────────────────────────────────────────────────
    def _switch(self, tab):
        self._tab = tab
        self._hide_alert()

        if tab == "login":
            self.panel_reg.pack_forget()
            self.panel_login.pack(fill="both", expand=True)
            self.lbl_title.configure(text="Masuk ke akun Anda")
            self.lbl_sub.configure(text="Selamat datang kembali")
            self.tab_login.configure(fg_color=C["card"],
                                     text_color=C["text"],
                                     font=("Helvetica", 13, "bold"))
            self.tab_reg.configure(fg_color="transparent",
                                   text_color=C["text_muted"],
                                   font=("Helvetica", 13))
        else:
            self.panel_login.pack_forget()
            self.panel_reg.pack(fill="both", expand=True)
            self.lbl_title.configure(text="Buat akun baru")
            self.lbl_sub.configure(text="Bergabung sekarang, gratis")
            self.tab_reg.configure(fg_color=C["card"],
                                   text_color=C["text"],
                                   font=("Helvetica", 13, "bold"))
            self.tab_login.configure(fg_color="transparent",
                                     text_color=C["text_muted"],
                                     font=("Helvetica", 13))

    # ── Alert helpers ─────────────────────────────────────────────────────────
    def _show_alert(self, msg, color=None):
        self.alert_var.set(msg)
        self.alert_lbl.configure(text_color=color or C["error"])
        self.alert_lbl.pack(fill="x", pady=(0, 6), before=self.panel_login
                            if self._tab == "login" else self.panel_reg)

    def _hide_alert(self):
        self.alert_lbl.pack_forget()

    # ── Success dialog ────────────────────────────────────────────────────────
    def _show_success(self, title, msg):
        dlg = ctk.CTkToplevel(self)
        dlg.title("Berhasil")
        dlg.geometry("320x220")
        dlg.resizable(False, False)
        dlg.configure(fg_color=C["card"])
        dlg.grab_set()

        # Centre on parent
        self.update_idletasks()
        px = self.winfo_x() + (self.winfo_width()  - 320) // 2
        py = self.winfo_y() + (self.winfo_height() - 220) // 2
        dlg.geometry(f"+{px}+{py}")

        ctk.CTkLabel(dlg, text="✅", font=("Helvetica", 40)).pack(pady=(24, 4))
        ctk.CTkLabel(dlg, text=title,
                     font=("Helvetica", 15, "bold"),
                     text_color=C["text"]).pack()
        ctk.CTkLabel(dlg, text=msg,
                     font=("Helvetica", 12),
                     text_color=C["text_muted"],
                     wraplength=260).pack(pady=(4, 16))
        ctk.CTkButton(dlg, text="OK", width=100, height=36,
                      fg_color=C["accent"], hover_color=C["accent_hov"],
                      corner_radius=8, font=("Helvetica", 13, "bold"),
                      command=dlg.destroy).pack()

    # ── DB init (background thread) ───────────────────────────────────────────
    def _init_db(self):
        def task():
            ok, msg = setup_database()
            if ok:
                self.after(0, lambda: self.status_var.set("✅ Database terhubung — " + DB_NAME))
            else:
                self.after(0, lambda: self.status_var.set("❌ DB Error: " + msg))
                self.after(0, lambda: self._show_alert(
                    "Gagal koneksi database. Pastikan XAMPP MySQL berjalan.", C["error"]))
        threading.Thread(target=task, daemon=True).start()

    # ── Login action ──────────────────────────────────────────────────────────
    def _do_login(self):
        self._hide_alert()
        username = self.ent_lu.get().strip()
        password = self.ent_lp.get()

        if not username or not password:
            self._show_alert("Username dan password wajib diisi.")
            return

        self.btn_login.configure(state="disabled", text="⏳ Memproses…")

        def task():
            try:
                conn = get_conn()
                cur  = conn.cursor(dictionary=True)
                cur.execute(
                    "SELECT * FROM users WHERE username=%s AND password=%s",
                    (username, sha(password))
                )
                user = cast(dict[str, Any] | None, cur.fetchone())
                cur.close(); conn.close()

                if user:
                    uname = str(user['username'])
                    if self._on_success:
                        # Ada callback → tutup window login, buka window berikutnya
                        self.after(0, lambda u=uname: self._handle_success(u))
                    else:
                        # Tidak ada callback → tampilkan dialog sukses seperti semula
                        self.after(0, lambda: self._show_success(
                            "Login Berhasil! 🎉",
                            f"Selamat datang, {uname}!"))
                    self.after(0, self._reset_login_btn)
                else:
                    self.after(0, lambda: self._show_alert("Username atau password salah."))
                    self.after(0, self._reset_login_btn)

            except Error as e:
                self.after(0, lambda: self._show_alert(f"DB Error: {e}"))
                self.after(0, self._reset_login_btn)

        threading.Thread(target=task, daemon=True).start()

    def _reset_login_btn(self):
        self.btn_login.configure(state="normal", text="Masuk")

    def _handle_success(self, username: str):
        """Tutup window login lalu jalankan callback on_success."""
        self.destroy()                   # tutup LoginApp
        if self._on_success:
            self._on_success(username)   # buka window berikutnya

    # ── Register action ───────────────────────────────────────────────────────
    def _do_register(self):
        self._hide_alert()
        username = self.ent_ru.get().strip()
        password = self.ent_rp.get()

        if not username or not password:
            self._show_alert("Username dan password wajib diisi.")
            return
        if len(password) < 6:
            self._show_alert("Password minimal 6 karakter.")
            return

        self.btn_reg.configure(state="disabled", text="⏳ Memproses…")

        def task():
            try:
                conn = get_conn()
                cur  = conn.cursor()
                cur.execute(
                    "INSERT INTO users (username,password) VALUES (%s,%s)",
                    (username, sha(password))
                )
                conn.commit()
                cur.close(); conn.close()
                self.after(0, lambda: self._show_success(
                    "Akun Dibuat! ✅",
                    "Silakan masuk menggunakan akun baru Anda."))
                self.after(0, self._reset_reg_btn)

            except mysql.connector.IntegrityError:
                self.after(0, lambda: self._show_alert("Username sudah digunakan."))
                self.after(0, self._reset_reg_btn)
            except Error as e:
                self.after(0, lambda: self._show_alert(f"DB Error: {e}"))
                self.after(0, self._reset_reg_btn)

        threading.Thread(target=task, daemon=True).start()

    def _reset_reg_btn(self):
        self.btn_reg.configure(state="normal", text="Buat Akun")


# ─── Entry Point ──────────────────────────────────────────────────────────────
if __name__ == "__main__":
    app = LoginApp()
    app.mainloop()