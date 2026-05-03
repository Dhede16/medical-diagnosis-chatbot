# 🏥 MedAI — Asisten Prediksi Penyakit

Aplikasi desktop chat berbasis **CustomTkinter** yang menggunakan **Groq API** (LLaMA 3.3 70B) untuk menganalisis gejala penyakit dan memberikan kemungkinan diagnosis awal dalam Bahasa Indonesia.

> ⚠️ **Disclaimer:** MedAI **bukan** pengganti diagnosis medis resmi. Selalu konsultasikan kondisi kesehatan Anda kepada dokter atau tenaga medis profesional.

---

## ✨ Fitur

| Fitur | Keterangan |
|---|---|
| 💬 Chat real-time | Antarmuka percakapan dengan gelembung chat |
| 🤖 LLaMA 3.3 70B | Model bahasa canggih via Groq API (gratis) |
| 🌓 Mode terang/gelap | Toggle tema langsung dari sidebar |
| 🔐 API Key aman | Masking dengan opsi show/hide |
| 🗑 Hapus riwayat | Reset percakapan kapan saja |
| ⌨️ Animasi mengetik | Indikator saat bot sedang memproses |
| 📝 Markdown support | **Bold**, heading, bullet dirender dengan benar |

---

## 🖼 Tampilan

```
┌─────────────────────────────────────────────────────────────┐
│  Sidebar (220px)  │         Panel Chat (flex)               │
│                   │  ┌─────────────────────────────────┐   │
│  🏥 MedAI         │  │  Konsultasi Gejala  ● Online    │   │
│  ─────────────    │  ├─────────────────────────────────┤   │
│  Groq API Key     │  │                                  │   │
│  [••••••••••]     │  │   🏥 Selamat datang di MedAI!   │   │
│  👁 Tampilkan key │  │                                  │   │
│  [✅ Simpan]      │  │              👤 Demam 3 hari    │   │
│  ✅ Terhubung     │  │   🏥 ● ● ●  (loading...)       │   │
│                   │  │                                  │   │
│  Model aktif      │  ├─────────────────────────────────┤   │
│  llama-3.3-70b    │  │ [input teks...      ] [ Kirim ] │   │
│                   │  └─────────────────────────────────┘   │
│  🌓 Mode Terang   │                                         │
│  [🗑 Hapus Chat]  │                                         │
└─────────────────────────────────────────────────────────────┘
```

---

## 🚀 Instalasi & Menjalankan

### 1. Clone repo
```bash
git clone https://github.com/username/medai-ctk.git
cd medai-ctk
```

### 2. Buat virtual environment (opsional tapi disarankan)
```bash
python -m venv venv

# Windows
venv\Scripts\activate

# macOS / Linux
source venv/bin/activate
```

### 3. Install dependensi
```bash
pip install -r requirements.txt
```

### 4. Dapatkan Groq API Key (GRATIS)
1. Buka [https://console.groq.com](https://console.groq.com)
2. Buat akun atau login
3. Masuk ke **API Keys** → **Create API Key**
4. Salin key yang dihasilkan (format: `gsk_xxxxxxxxxxxx`)

### 5. Jalankan aplikasi
```bash
python main.py
```

### 6. Masukkan API Key di sidebar
- Tempel API Key di kolom "Groq API Key"
- Klik **Simpan & Hubungkan**
- Status berubah menjadi ✅ Terhubung

---

## 📁 Struktur Proyek

```
medai-ctk/
│
├── main.py              # Entry point
├── app.py               # Window utama (MedAIApp)
├── config.py            # Konstanta warna, font, prompt
├── requirements.txt
├── README.md
│
├── widgets/
│   ├── __init__.py
│   ├── chat_bubble.py      # Gelembung pesan user/bot
│   ├── typing_indicator.py # Animasi "sedang mengetik"
│   ├── sidebar.py          # Panel kiri (API key, tema, dll)
│   └── chat_panel.py       # Panel kanan (chat + input)
│
└── utils/
    ├── __init__.py
    ├── api_worker.py       # Thread request ke Groq API
    └── formatter.py        # Parser markdown sederhana
```

---

## ⚙️ Konfigurasi

Edit `config.py` untuk mengubah:

| Variabel | Default | Keterangan |
|---|---|---|
| `GROQ_MODEL` | `llama-3.3-70b-versatile` | Model yang digunakan |
| `GROQ_TEMP` | `0.4` | Kreativitas respons (0–1) |
| `GROQ_MAX_TOK` | `1024` | Maksimum token respons |
| `WINDOW_WIDTH` | `960` | Lebar jendela awal |
| `WINDOW_HEIGHT` | `720` | Tinggi jendela awal |
| `SYSTEM_PROMPT` | *(lihat config.py)* | Instruksi kepribadian bot |

---

## 🛠 Persyaratan Sistem

- Python **3.10+**
- OS: Windows 10/11, macOS 11+, Ubuntu 20.04+
- Koneksi internet (untuk Groq API)
- Dependensi: `customtkinter>=5.2.0` (tidak ada library lain selain stdlib)

---

## 📝 Lisensi

MIT License — bebas digunakan dan dimodifikasi.
