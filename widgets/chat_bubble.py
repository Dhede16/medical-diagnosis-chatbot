import tkinter.font as tkfont
import customtkinter as ctk
from utils.formatter import parse_markdown
from config import (
    TEXT_PRIMARY, TEXT_MUTED,
    USER_BUBBLE, BORDER,
    FONT_FAMILY,
)

MAX_WIDTH = 700   


class ChatBubble(ctk.CTkFrame):
    def __init__(self, master, text: str, is_user: bool, **kwargs):
        super().__init__(master, fg_color="transparent", **kwargs)
        self.is_user = is_user
        self._build(text)

    def _build(self, text: str):
        self.grid_columnconfigure(0, weight=1)

        if self.is_user:
            self._build_user(text)
        else:
            self._build_bot(text)

    #Estimasi tinggi dengan memperhitungkan word wrap
    def _estimate_height(self, text: str, font_size: int, line_height: int,
                         box_width: int, padding: int) -> int:
        try:
            f = tkfont.Font(family=FONT_FAMILY, size=font_size)
            usable_width = max(box_width - padding, 1)
            total_lines = 0

            for raw_line in text.split("\n"):
                if raw_line == "":
                    total_lines += 1
                    continue
                # Ukur berapa baris visual yang dibutuhkan baris ini
                words = raw_line.split(" ")
                current_w = 0
                visual_lines = 1
                for word in words:
                    word_w = f.measure(word + " ")
                    if current_w + word_w > usable_width and current_w > 0:
                        visual_lines += 1
                        current_w = word_w
                    else:
                        current_w += word_w
                total_lines += visual_lines

            return max(total_lines * line_height + padding, line_height * 2)
        except Exception:
            # Fallback: hitung naif jika font tidak tersedia
            lines = text.count("\n") + 1
            return max(lines * line_height + padding, line_height * 2)

    #User bubble 
    def _build_user(self, text: str):
        outer = ctk.CTkFrame(self, fg_color="transparent")
        outer.grid(row=0, column=0, sticky="ew", padx=40, pady=(6, 6))
        outer.grid_columnconfigure(0, weight=1)

        tb = ctk.CTkTextbox(
            outer,
            wrap="word",
            activate_scrollbars=False,
            fg_color=(USER_BUBBLE, USER_BUBBLE),
            border_width=0,
            corner_radius=18,
            text_color=TEXT_PRIMARY,
            font=ctk.CTkFont(family=FONT_FAMILY, size=14),
            cursor="arrow",
            width=MAX_WIDTH,
        )
        tb.grid(row=0, column=1, sticky="e")
        outer.grid_columnconfigure(0, weight=1)

        tb.configure(state="normal")
        self._insert_plain(tb, text)
        tb.configure(state="disabled")

        height = self._estimate_height(
            text,
            font_size=14,
            line_height=24,
            box_width=MAX_WIDTH,
            padding=24,
        )
        tb.configure(height=height)

    #Bot bubble 
    def _build_bot(self, text: str):
        outer = ctk.CTkFrame(self, fg_color="transparent")
        outer.grid(row=0, column=0, sticky="ew", padx=(16, 60), pady=(6, 6))
        outer.grid_columnconfigure(1, weight=1)

        avatar = ctk.CTkLabel(
            outer, text="🏥",
            width=32, height=32,
            fg_color=("#2A3A2A", "#1A2A1A"),
            corner_radius=16,
            font=ctk.CTkFont(size=15),
        )
        avatar.grid(row=0, column=0, padx=(0, 12), sticky="n", pady=(4, 0))

        tb = ctk.CTkTextbox(
            outer,
            wrap="word",
            activate_scrollbars=True,
            fg_color="transparent",
            border_width=0,
            corner_radius=0,
            text_color=TEXT_PRIMARY,
            font=ctk.CTkFont(family=FONT_FAMILY, size=14),
            cursor="arrow",
        )
        tb.grid(row=0, column=1, sticky="ew")

        tb.configure(state="normal")
        self._insert_formatted(tb, text)
        tb.configure(state="disabled")

        height = self._estimate_height(
            text,
            font_size=14,
            line_height=22,
            box_width=MAX_WIDTH,
            padding=20,
        )
        tb.configure(height=min(height, 500))

    #Text inserters 
    def _insert_plain(self, tb: ctk.CTkTextbox, text: str):
        """User bubble: plain text, no markdown."""
        tk_text = tb._textbox
        normal = tkfont.Font(family=FONT_FAMILY, size=14)
        tk_text.tag_configure("plain", font=normal)
        tk_text.insert("end", text, "plain")

    def _insert_formatted(self, tb: ctk.CTkTextbox, text: str):
        tk_text = tb._textbox

        normal_f  = tkfont.Font(family=FONT_FAMILY, size=14)
        bold_f    = tkfont.Font(family=FONT_FAMILY, size=14, weight="bold")
        h2_f      = tkfont.Font(family=FONT_FAMILY, size=15, weight="bold")
        h3_f      = tkfont.Font(family=FONT_FAMILY, size=14, weight="bold",
                                 underline=True)

        tk_text.tag_configure("bold",        font=bold_f)
        tk_text.tag_configure("heading2",    font=h2_f)
        tk_text.tag_configure("heading3",    font=h3_f)
        tk_text.tag_configure("bullet",      font=normal_f, foreground="#8E8EA0")
        tk_text.tag_configure("bullet_text", font=normal_f)
        tk_text.tag_configure("normal",      font=normal_f)

        for piece, tag in parse_markdown(text):
            tk_text.insert("end", piece, tag)

        content = tk_text.get("1.0", "end")
        if content.endswith("\n\n"):
            tk_text.delete("end-1c", "end")