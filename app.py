import customtkinter as ctk
from config import (
    WINDOW_WIDTH, WINDOW_HEIGHT,
    SYSTEM_PROMPT, GROQ_API_KEY,
    BG_MAIN, FONT_FAMILY,
    ACCENT_RED, TEXT_PRIMARY,
)
from widgets import ChatPanel
from utils import GroqWorker

ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("dark-blue")


class MedAIApp(ctk.CTk):
    def __init__(self, username: str):
        super().__init__()
        self.title("MedAI — Asisten Prediksi Penyakit")
        self.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}")
        self.minsize(700, 500)

        self._api_key = GROQ_API_KEY
        self._history = [{"role": "system", "content": SYSTEM_PROMPT}]
        self._worker  = None
        self._username = username or "demo_user"

        self._build()
        self.protocol("WM_DELETE_WINDOW", self.on_closing)

    def _build(self):
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self._chat = ChatPanel(
            self,
            on_send=self._handle_send,
            on_reset=self._new_chat,
        )
        self._chat.grid(row=0, column=0, sticky="nsew")

    #Handlers 
    def _handle_send(self, text: str):
        if not self._api_key or self._api_key.startswith("gsk_XXX"):
            self._chat.add_bot_bubble(
                "⚠️ **API Key belum dikonfigurasi.**\n\n"
                "Buka file `config.py` dan isi variabel `GROQ_API_KEY` "
                "dengan key dari https://console.groq.com"
            )
            return

        self._chat.add_user_bubble(text)
        self._history.append({"role": "user", "content": text})

        self._chat.show_typing()
        self._chat.set_input_enabled(False)

        self._worker = GroqWorker(
            api_key   = self._api_key,
            messages  = list(self._history),
            on_result = lambda t: self.after(0, self._apply_result, t),
            on_error  = lambda e: self.after(0, self._apply_error, e),
        )
        self._worker.start()

    def _apply_result(self, text: str):
        self._chat.hide_typing()
        self._history.append({"role": "assistant", "content": text})
        self._chat.add_bot_bubble(text)
        self._chat.show_reset_button()

    def _apply_error(self, msg: str):
        self._chat.hide_typing()
        self._chat.add_bot_bubble(
            f"❌ **Terjadi kesalahan:**\n\n{msg}\n\n"
            "Periksa API Key di `config.py` atau koneksi internet Anda."
        )
        self._chat.show_reset_button()

    def _new_chat(self):
        self._chat.clear_chat()
        self._history = [{"role": "system", "content": SYSTEM_PROMPT}]

    def on_closing(self):
        if self._worker and self._worker.is_alive():
            pass
        self.destroy()