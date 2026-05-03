"""
widgets/sidebar.py - Sidebar ChatGPT-style: logo, new chat, riwayat.
API key TIDAK ditampilkan di GUI; diambil langsung dari config.py.
"""

import customtkinter as ctk
from config import (
    BG_SIDEBAR, BORDER, TEXT_PRIMARY, TEXT_MUTED,
    BTN_HOVER, ACCENT_GREEN, ACCENT_RED, FONT_FAMILY,
)


class Sidebar(ctk.CTkFrame):
    def __init__(self, master, on_new_chat, on_clear_chat, **kwargs):
        super().__init__(
            master,
            width=260,
            corner_radius=0,
            fg_color=(BG_SIDEBAR, BG_SIDEBAR),
            **kwargs,
        )
        self.on_new_chat   = on_new_chat
        self.on_clear_chat = on_clear_chat
        self.grid_propagate(False)
        self._history_items = []
        self._build()

    def _build(self):
        self.grid_rowconfigure(2, weight=1)
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

        # New Chat button (mirip ChatGPT)
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

        # ── Divider ───────────────────────────────────────────────────────
        ctk.CTkFrame(self, height=1, fg_color=(BORDER, BORDER)).grid(
            row=1, column=0, padx=0, pady=0, sticky="ew"
        )

        # ── History scroll area ───────────────────────────────────────────
        self._hist_frame = ctk.CTkScrollableFrame(
            self,
            fg_color="transparent",
            scrollbar_button_color=(BORDER, BORDER),
        )
        self._hist_frame.grid(row=2, column=0, sticky="nsew", padx=0, pady=0)
        self._hist_frame.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(
            self._hist_frame,
            text="Riwayat",
            font=ctk.CTkFont(family=FONT_FAMILY, size=11),
            text_color=(TEXT_MUTED, TEXT_MUTED),
            anchor="w",
        ).grid(row=0, column=0, padx=14, pady=(10, 4), sticky="w")

        self._hist_row = 1

        # ── Divider ───────────────────────────────────────────────────────
        ctk.CTkFrame(self, height=1, fg_color=(BORDER, BORDER)).grid(
            row=3, column=0, padx=0, sticky="ew"
        )

        # ── Footer: Hapus riwayat ─────────────────────────────────────────
        ctk.CTkButton(
            self,
            text="🗑  Hapus semua riwayat",
            height=40,
            fg_color="transparent",
            hover_color=("#3A1A1A", "#3A1A1A"),
            text_color=(ACCENT_RED, ACCENT_RED),
            font=ctk.CTkFont(family=FONT_FAMILY, size=12),
            corner_radius=0,
            anchor="w",
            command=self.on_clear_chat,
        ).grid(row=4, column=0, padx=0, pady=0, sticky="ew")

    # ── Public ────────────────────────────────────────────────────────────
    def add_history_item(self, label: str):
        """Tambah item ke panel riwayat."""
        short = label[:32] + "…" if len(label) > 32 else label
        btn = ctk.CTkButton(
            self._hist_frame,
            text=f"💬  {short}",
            height=36,
            fg_color="transparent",
            hover_color=(BTN_HOVER, BTN_HOVER),
            text_color=(TEXT_PRIMARY, TEXT_PRIMARY),
            font=ctk.CTkFont(family=FONT_FAMILY, size=12),
            corner_radius=6,
            anchor="w",
        )
        btn.grid(row=self._hist_row, column=0, padx=6, pady=2, sticky="ew")
        self._hist_row += 1
        self._history_items.append(btn)

    def clear_history_ui(self):
        for btn in self._history_items:
            btn.destroy()
        self._history_items.clear()
        self._hist_row = 1
