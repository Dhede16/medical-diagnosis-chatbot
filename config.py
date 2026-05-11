"""
config.py — Konstanta warna, font, dan pengaturan aplikasi MedAI.

UNTUK DEVELOPER: Isi GROQ_API_KEY di bawah sebelum distribusi.
Dapatkan key gratis di: https://console.groq.com -> API Keys
"""

# ── Groq API Key — ISI DI SINI ───────────────────────────────────────────────
GROQ_API_KEY  = "gsk_XXXXXXXXXXXXXXXXXXXXXXXX"   # <-- ganti dengan key Anda

# ── Model Groq ───────────────────────────────────────────────────────────────
GROQ_MODEL    = "llama-3.3-70b-versatile"
GROQ_TEMP     = 0.4
GROQ_MAX_TOK  = 1024

# ── Warna ChatGPT-style dark ─────────────────────────────────────────────────
BG_MAIN       = "#212121"
BG_SIDEBAR    = "#171717"
BG_INPUT      = "#2F2F2F"
BG_HOVER      = "#2A2A2A"
BORDER        = "#383838"
USER_BUBBLE   = "#2F2F2F"
TEXT_PRIMARY  = "#ECECEC"
TEXT_MUTED    = "#8E8EA0"
BTN_HOVER     = "#404040"
ACCENT_GREEN  = "#10A37F"
ACCENT_RED    = "#EF4444"

# ── Ukuran & Font ────────────────────────────────────────────────────────────
WINDOW_WIDTH   = 1100
WINDOW_HEIGHT  = 760
SIDEBAR_WIDTH  = 260
FONT_FAMILY    = "Segoe UI"

# ── System Prompt ─────────────────────────────────────────────────────────────
SYSTEM_PROMPT = """Kamu adalah asisten medis AI bernama MedAI yang membantu menganalisis gejala penyakit.

Ketika pengguna menyebutkan gejala, kamu harus:
1. **Analisis Gejala** - Ringkasan gejala yang disebutkan
2. **Kemungkinan Penyakit** - Daftar 2-4 penyakit yang paling mungkin (dari yang paling probable)
3. **Penjelasan Singkat** - Untuk setiap penyakit, jelaskan kenapa gejalanya cocok
4. **Saran Tindakan** - Apakah perlu ke dokter segera, bisa ditangani sendiri, dll.
5. **Peringatan** - Selalu ingatkan bahwa ini BUKAN diagnosis medis resmi

Gunakan bahasa Indonesia yang ramah dan mudah dipahami. Format respons dengan rapi menggunakan markdown.
Jika pengguna menanyakan hal di luar gejala/kesehatan, arahkan kembali ke topik medis dengan sopan."""

# Warna manual (mirip ChatGPT dark)
C = {
    "bg":         "#212121",
    "card":       "#2f2f2f",
    "input":      "#3c3c3c",
    "input_hover":"#444444",
    "border":     "#4a4a4a",
    "accent":     "#10a37f",
    "accent_hov": "#0d8f6f",
    "text":       "#ececec",
    "text_muted": "#9b9b9b",
    "error":      "#ef4444",
    "success":    "#10a37f",
    "tab_active": "#3c3c3c",
    "tab_inactive":"#272727",
}