import customtkinter as ctk
from .chat_bubble import ChatBubble
from .typing_indicator import TypingIndicator
from config import (
    BG_MAIN, BG_INPUT, BG_HOVER, BORDER,
    TEXT_PRIMARY, TEXT_MUTED, BTN_HOVER,
    FONT_FAMILY,
)


SUGGESTIONS = [
    ("🤒", "Demam & sakit kepala",      "Saya demam 38°C sejak kemarin disertai sakit kepala berdenyut"),
    ("🤢", "Mual & gangguan pencernaan", "Saya mual, perut kembung, dan tidak nafsu makan sejak 2 hari"),
    ("😮‍💨", "Sesak & batuk",             "Saya batuk kering 1 minggu dan kadang sesak napas ringan"),
    ("🦴", "Nyeri sendi & otot",         "Sendi lutut dan pinggang saya nyeri terutama pagi hari"),
]


class ChatPanel(ctk.CTkFrame):
    def __init__(self, master, on_send, on_reset, **kwargs):
        super().__init__(master, corner_radius=0, fg_color=(BG_MAIN, BG_MAIN), **kwargs)
        self.on_send        = on_send
        self.on_reset       = on_reset
        self._typing_widget = None
        self._row_counter   = 0
        self._in_welcome    = True
        self._build()

    #Layout 
    def _build(self):
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        # Welcome frame
        self._welcome_frame = ctk.CTkFrame(self, fg_color="transparent")
        self._welcome_frame.grid(row=0, column=0, sticky="nsew")
        self._welcome_frame.grid_rowconfigure(0, weight=1)
        self._welcome_frame.grid_rowconfigure(2, weight=1)
        self._welcome_frame.grid_columnconfigure(0, weight=1)
        self._build_welcome()

        # Scroll frame (chat mode)
        self._scroll_frame = ctk.CTkScrollableFrame(
            self,
            corner_radius=0,
            fg_color="transparent",
            scrollbar_button_color=(BORDER, BORDER),
        )
        self._scroll_frame.grid_columnconfigure(0, weight=1)

        # Bottom bar (row=1): berisi input bar ATAU reset button
        self._bottom_bar = ctk.CTkFrame(self, fg_color="transparent", corner_radius=0)
        self._bottom_bar.grid(row=1, column=0, sticky="ew", padx=0, pady=(0, 16))
        self._bottom_bar.grid_columnconfigure(0, weight=1)

        self._build_input_bar()
        self._build_reset_bar()

        # Default: tampilkan input bar
        self._input_bar.grid(row=0, column=0, sticky="ew")
        self._reset_bar.grid_forget()

    def _build_welcome(self):
        f = self._welcome_frame
        ctk.CTkLabel(f, text="").grid(row=0, column=0)

        center = ctk.CTkFrame(f, fg_color="transparent")
        center.grid(row=1, column=0, pady=0)

        ctk.CTkLabel(
            center,
            text="Apa yang ingin Anda konsultasikan?",
            font=ctk.CTkFont(family=FONT_FAMILY, size=26, weight="bold"),
            text_color=(TEXT_PRIMARY, TEXT_PRIMARY),
        ).pack(pady=(0, 32))

        chips_frame = ctk.CTkFrame(center, fg_color="transparent")
        chips_frame.pack()

        for i, (icon, label, prompt) in enumerate(SUGGESTIONS):
            row, col = divmod(i, 2)
            btn = ctk.CTkButton(
                chips_frame,
                text=f"{icon}  {label}",
                width=240, height=52,
                fg_color=(BTN_HOVER, BTN_HOVER),
                hover_color=("#505050", "#505050"),
                text_color=(TEXT_PRIMARY, TEXT_PRIMARY),
                font=ctk.CTkFont(family=FONT_FAMILY, size=13),
                corner_radius=12,
                border_width=1,
                border_color=(BORDER, BORDER),
                anchor="w",
                command=lambda p=prompt: self._suggestion_clicked(p),
            )
            btn.grid(row=row, column=col, padx=6, pady=6)

        ctk.CTkLabel(f, text="").grid(row=2, column=0)

    def _build_input_bar(self):
        self._input_bar = ctk.CTkFrame(self._bottom_bar, fg_color="transparent")
        self._input_bar.grid_columnconfigure(0, weight=1)

        inner = ctk.CTkFrame(self._input_bar, fg_color="transparent")
        inner.grid(row=0, column=0, sticky="ew", padx=180)
        inner.grid_columnconfigure(0, weight=1)

        input_container = ctk.CTkFrame(
            inner,
            fg_color=(BG_INPUT, BG_INPUT),
            corner_radius=16,
            border_width=1,
            border_color=(BORDER, BORDER),
        )
        input_container.grid(row=0, column=0, sticky="ew")
        input_container.grid_columnconfigure(0, weight=1)

        self._input_box = ctk.CTkTextbox(
            input_container,
            height=52,
            font=ctk.CTkFont(family=FONT_FAMILY, size=14),
            fg_color="transparent",
            border_width=0,
            corner_radius=0,
            wrap="word",
            text_color=TEXT_PRIMARY,
            scrollbar_button_color=(BG_INPUT, BG_INPUT),
            scrollbar_button_hover_color=(BG_INPUT, BG_INPUT),
        )
        self._input_box.grid(row=0, column=0, padx=(16, 4), pady=(8, 8), sticky="ew")

        self._tk_box = self._input_box._textbox

        self._ph    = "Ceritakan gejala Anda..."
        self._is_ph = True
        self._set_ph()
        self._rebind()

        self._send_btn = ctk.CTkButton(
            input_container,
            text="↑",
            width=36, height=36,
            font=ctk.CTkFont(family=FONT_FAMILY, size=18, weight="bold"),
            fg_color=("#FFFFFF", "#FFFFFF"),
            hover_color=("#DDDDDD", "#DDDDDD"),
            text_color=("#000000", "#000000"),
            corner_radius=8,
            command=self._do_send,
        )
        self._send_btn.grid(row=0, column=1, padx=(0, 8), pady=8)

        ctk.CTkLabel(
            inner,
            text="MedAI dapat membuat kesalahan. Selalu konfirmasi ke dokter.",
            font=ctk.CTkFont(family=FONT_FAMILY, size=11),
            text_color=(TEXT_MUTED, TEXT_MUTED),
        ).grid(row=1, column=0, pady=(6, 0))

    def _build_reset_bar(self):
        """Bar bawah berisi tombol 'Mencari Diagnosa Lain'."""
        self._reset_bar = ctk.CTkFrame(self._bottom_bar, fg_color="transparent")
        self._reset_bar.grid_columnconfigure(0, weight=1)

        inner = ctk.CTkFrame(self._reset_bar, fg_color="transparent")
        inner.grid(row=0, column=0)

        ctk.CTkButton(
            inner,
            text="🔄  Mencari Diagnosa Lain",
            width=260, height=48,
            fg_color=("#10A37F", "#10A37F"),
            hover_color=("#0D8F6F", "#0D8F6F"),
            text_color=("#FFFFFF", "#FFFFFF"),
            font=ctk.CTkFont(family=FONT_FAMILY, size=14, weight="bold"),
            corner_radius=12,
            command=self._do_reset,
        ).pack()

        ctk.CTkLabel(
            inner,
            text="MedAI dapat membuat kesalahan. Selalu konfirmasi ke dokter.",
            font=ctk.CTkFont(family=FONT_FAMILY, size=11),
            text_color=(TEXT_MUTED, TEXT_MUTED),
        ).pack(pady=(8, 0))

    #Binding 
    def _rebind(self):
        self._tk_box.bind("<FocusIn>",      self._clear_ph,    add=False)
        self._tk_box.bind("<FocusOut>",     self._restore_ph,  add=False)
        self._tk_box.bind("<Return>",       self._on_enter,    add=False)
        self._tk_box.bind("<Shift-Return>", lambda e: "break", add=False)

    #Placeholder
    def _set_ph(self):
        self._tk_box.configure(state="normal")
        self._tk_box.delete("1.0", "end")
        self._tk_box.insert("1.0", self._ph)
        self._input_box.configure(text_color=(TEXT_MUTED, TEXT_MUTED))
        self._is_ph = True

    def _clear_ph(self, _=None):
        if self._is_ph:
            self._tk_box.delete("1.0", "end")
            self._input_box.configure(text_color=(TEXT_PRIMARY, TEXT_PRIMARY))
            self._is_ph = False

    def _restore_ph(self, _=None):
        raw = self._tk_box.get("1.0", "end").strip()
        if not raw:
            self._set_ph()
            self._rebind()

    #Send
    def _on_enter(self, event):
        if event.state & 0x1:
            return
        self._do_send()
        return "break"

    def _do_send(self):
        if self._is_ph:
            return
        text = self._tk_box.get("1.0", "end").strip()
        if not text:
            return
        self._tk_box.delete("1.0", "end")
        self._is_ph = False
        self.on_send(text)

    def _suggestion_clicked(self, prompt: str):
        self._clear_ph()
        self._tk_box.insert("1.0", prompt)
        self._input_box.configure(text_color=(TEXT_PRIMARY, TEXT_PRIMARY))
        self._is_ph = False
        self._do_send()

    def _do_reset(self):
        self.on_reset()

    #Switch welcome -> chat
    def _switch_to_chat(self):
        if self._in_welcome:
            self._welcome_frame.grid_forget()
            self._scroll_frame.grid(row=0, column=0, sticky="nsew")
            self._in_welcome = False

    #Public API 
    def add_user_bubble(self, text: str):
        self._switch_to_chat()
        b = ChatBubble(self._scroll_frame, text, is_user=True)
        b.grid(row=self._row_counter, column=0, padx=0, pady=(2, 0), sticky="ew")
        self._row_counter += 1
        self._scroll_bottom()

    def add_bot_bubble(self, text: str):
        self._switch_to_chat()
        b = ChatBubble(self._scroll_frame, text, is_user=False)
        b.grid(row=self._row_counter, column=0, padx=0, pady=(2, 0), sticky="ew")
        self._row_counter += 1
        self._scroll_bottom()

    def show_typing(self):
        self._switch_to_chat()
        self._typing_widget = TypingIndicator(self._scroll_frame)
        self._typing_widget.grid(row=self._row_counter, column=0,
                                 padx=0, pady=(2, 0), sticky="ew")
        self._row_counter += 1
        self._scroll_bottom()

    def hide_typing(self):
        if self._typing_widget:
            self._typing_widget.destroy()
            self._typing_widget = None

    def show_reset_button(self):
        """Sembunyikan input bar, tampilkan tombol reset."""
        self._input_bar.grid_forget()
        self._reset_bar.grid(row=0, column=0, sticky="ew")

    def set_input_enabled(self, enabled: bool):
        """Disable input saat menunggu respons API."""
        if enabled:
            pass  # input akan disembunyikan oleh show_reset_button()
        else:
            self._tk_box.delete("1.0", "end")
            self._input_box.configure(state="disabled")
            self._send_btn.configure(state="disabled")

    def clear_chat(self):
        """Reset ke welcome screen."""
        for w in self._scroll_frame.winfo_children():
            w.destroy()
        self._row_counter   = 0
        self._typing_widget = None

        # Sembunyikan chat, tampilkan welcome
        self._scroll_frame.grid_forget()
        self._welcome_frame.grid(row=0, column=0, sticky="nsew")
        self._in_welcome = True

        # Kembalikan input bar, sembunyikan reset bar
        self._reset_bar.grid_forget()
        self._input_bar.grid(row=0, column=0, sticky="ew")

        # Reset input box
        self._input_box.configure(state="normal")
        self._set_ph()
        self._send_btn.configure(state="normal")
        self._rebind()

    def _scroll_bottom(self):
        self.after(120, lambda: self._scroll_frame._parent_canvas.yview_moveto(1.0))