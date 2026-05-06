"""
MedAI — Asisten Prediksi Penyakit
Entry point utama aplikasi.
"""

import login
from app import MedAIApp


def on_login_success(username: str):
    """Dipanggil oleh LoginApp setelah login berhasil."""
    main_app = MedAIApp()
    # Opsional: kirim username ke MedAIApp jika dibutuhkan
    # main_app.set_user(username)
    main_app.mainloop()


if __name__ == "__main__":
    login_app = login.LoginApp(on_success=on_login_success)
    login_app.mainloop()