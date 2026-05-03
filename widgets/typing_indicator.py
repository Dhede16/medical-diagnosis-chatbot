"""
widgets/typing_indicator.py - Typing indicator ChatGPT-style (3 titik).
"""

import customtkinter as ctk
from config import TEXT_MUTED, FONT_FAMILY


class TypingIndicator(ctk.CTkFrame):
    _STATES = ["●  ○  ○", "●  ●  ○", "●  ●  ●", "○  ●  ●", "○  ○  ●", "○  ○  ○"]

    def __init__(self, master, **kwargs):
        super().__init__(master, fg_color="transparent", **kwargs)
        self._idx = 0
        self._job = None
        self._build()

    def _build(self):
        outer = ctk.CTkFrame(self, fg_color="transparent")
        outer.grid(row=0, column=0, sticky="ew", padx=(16, 60), pady=(4, 4))
        outer.grid_columnconfigure(1, weight=1)

        avatar = ctk.CTkLabel(
            outer, text="🏥",
            width=32, height=32,
            fg_color=("#2A3A2A", "#1A2A1A"),
            corner_radius=16,
            font=ctk.CTkFont(size=15),
        )
        avatar.grid(row=0, column=0, padx=(0, 12), sticky="nw", pady=4)

        self._dot_lbl = ctk.CTkLabel(
            outer,
            text=self._STATES[0],
            font=ctk.CTkFont(family=FONT_FAMILY, size=15),
            text_color=(TEXT_MUTED, TEXT_MUTED),
            anchor="w",
        )
        self._dot_lbl.grid(row=0, column=1, sticky="w", pady=8)

        self.grid_columnconfigure(0, weight=1)
        self._animate()

    def _animate(self):
        self._idx = (self._idx + 1) % len(self._STATES)
        self._dot_lbl.configure(text=self._STATES[self._idx])
        self._job = self.after(350, self._animate)

    def stop(self):
        if self._job:
            self.after_cancel(self._job)
            self._job = None

    def destroy(self):
        self.stop()
        super().destroy()
