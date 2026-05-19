"""
widgets/sidebar.py - Sidebar simple: logo dan new chat button.
API key TIDAK ditampilkan di GUI; diambil langsung dari config.py.
(Chat history feature removed - fresh start setiap aplikasi dibuka)
"""

import customtkinter as ctk
from config import (
    BG_SIDEBAR, BORDER, TEXT_PRIMARY,
    BTN_HOVER, FONT_FAMILY,
)


class Sidebar(ctk.CTkFrame):
    def __init__(self, master, on_new_chat, **kwargs):
        super().__init__(
            master,
            width=260,
            corner_radius=0,
            fg_color=(BG_SIDEBAR, BG_SIDEBAR),
            **kwargs,
        )
        self.on_new_chat = on_new_chat
        self.grid_propagate(False)
        self._build()

    def _build(self):
        """Build sidebar dengan logo dan new chat button saja (no history)."""
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)

        # ── Top: Logo + New Chat ──────────────────────────────────────────
        top = ctk.CTkFrame(self, fg_color="transparent")
        top.grid(row=0, column=0, padx=12, pady=(16, 8), sticky="ew")
        top.grid_columnconfigure(0, weight=1)

        # Logo row
        logo_row = ctk.CTkFrame(top, fg_color="transparent")
        logo_row.pack(fill="x", pady=(0, 12))

        ctk.CTkLabel(
            logo_row, text="🏥",
            font=ctk.CTkFont(size=22),
        ).pack(side="left", padx=(4, 6))

        ctk.CTkLabel(
            logo_row, text="MedAI",
            font=ctk.CTkFont(family=FONT_FAMILY, size=16, weight="bold"),
            text_color=(TEXT_PRIMARY, TEXT_PRIMARY),
        ).pack(side="left")

        # New Chat button
        ctk.CTkButton(
            top,
            text="+ New chat",
            height=40,
            fg_color=(BTN_HOVER, BTN_HOVER),
            hover_color=("#505050", "#505050"),
            text_color=(TEXT_PRIMARY, TEXT_PRIMARY),
            font=ctk.CTkFont(family=FONT_FAMILY, size=13),
            corner_radius=8,
            anchor="w",
            command=self.on_new_chat,
        ).pack(fill="x")

        # ── Spacer ─────────────────────────────────────────────────────────
        ctk.CTkLabel(self, text="").grid(row=1, column=0)
