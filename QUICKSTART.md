# 🚀 MedAI Quick Start Guide

## Prerequisites
- ✅ MySQL Server running (XAMPP)
- ✅ Python 3.8+
- ✅ All packages installed (requirements.txt)

## Starting the App

### Method 1: Simple Command
```bash
python main.py
```

### Method 2: With Virtual Environment
```bash
.venv\Scripts\activate
python main.py
```

---

## First Time Setup

### Step 1: Create Account
1. Run `python main.py`
2. Window login akan muncul
3. Klik tab **"Daftar"**
4. Masukkan username & password baru
5. Klik **"Daftar"**

### Step 2: Login
1. Klik tab **"Masuk"**
2. Masukkan credentials yang baru dibuat
3. Klik **"Masuk"**
4. MedAI akan membuka

---

## Using the App

### Chat
```
1. Ketik gejala atau pertanyaan kesehatan
2. Tekan ENTER atau klik ↑
3. AI akan menganalisis dan memberikan saran
4. Percakapan otomatis tersimpan
```

### History Management
```
📜 Lihat history di sidebar kiri
💬 Klik item untuk restore percakapan lama
✕ Klik tombol delete untuk hapus satu chat
🗑 Klik "Hapus semua riwayat" untuk clear semua
```

### Features
- ✅ Medical symptom analysis
- ✅ AI-powered responses
- ✅ Chat history persistence
- ✅ Multi-language support (Bahasa Indonesia)
- ✅ Markdown formatted responses

---

## Troubleshooting

### Error: "Module not found"
```bash
pip install -r requirements.txt
```

### Error: "Database connection failed"
- Check MySQL is running
- Default: localhost:3306, user: root, password: (empty)
- Edit config in database.py if needed

### Error: "API Key not configured"
- Edit config.py
- Check GROQ_API_KEY is set correctly

### Chat not saving?
- Make sure MySQL is connected
- Check user is logged in properly
- View PRODUCTION_STATUS.md for details

---

## Demo Account

**Username**: `admin`  
**Password**: `admin123`

This account is auto-created on first database setup.

---

## 📁 Struktur File

```
medai-ctk/
├── main.py              # Entry point
├── app.py               # Window utama aplikasi
├── login.py             # UI Login/Daftar
├── database.py          # Fungsi database MySQL
├── config.py            # Konfigurasi (API key, warna, dll)
├── requirements.txt     # Dependensi Python
├── widgets/
│   ├── __init__.py
│   ├── chat_bubble.py   # Tampilan chat bubble
│   ├── chat_panel.py    # Panel area chat
│   ├── sidebar.py       # Sidebar riwayat chat
│   └── typing_indicator.py  # Animasi sedang mengetik
└── utils/
    ├── __init__.py
    ├── api_worker.py    # Thread worker API Groq
    └── formatter.py     # Parser markdown
```

---

## ⚙️ Konfigurasi

Edit `config.py` untuk mengubah:
- `GROQ_API_KEY` - API Key (sudah tersetting)
- `GROQ_MODEL` - Nama model AI
- Warna tema
- Ukuran window
- System prompt

---

## 🎨 Dukungan

Untuk masalah, cek:
1. [DEBUG_REPORT.md](DEBUG_REPORT.md) - Bugs yang sudah diperbaiki
2. [PRODUCTION_STATUS.md](PRODUCTION_STATUS.md) - Status fitur
3. [FIX_API_GUIDE.md](FIX_API_GUIDE.md) - Troubleshooting API
4. Status koneksi database
5. MySQL service berjalan

---

**Versi**: 1.0  
**Terakhir Diupdate**: May 17, 2026  
**Status**: Production Ready ✅

```
medai-ctk/
├── main.py              # Entry point
├── app.py               # Main application window
├── login.py             # Login/Register UI
├── database.py          # MySQL database functions
├── config.py            # Configuration (API key, colors, etc)
├── requirements.txt     # Python dependencies
├── widgets/
│   ├── chat_bubble.py   # Chat message display
│   ├── chat_panel.py    # Chat area
│   ├── sidebar.py       # Chat history sidebar
│   └── typing_indicator.py  # Typing animation
└── utils/
    ├── api_worker.py    # Groq API thread worker
    └── formatter.py     # Markdown formatting
```

---

## Configuration

Edit `config.py` to customize:
- `GROQ_API_KEY` - API Key (already set)
- `GROQ_MODEL` - AI model name
- Colors and themes
- Window size
- System prompt

---

## Support

For issues, check:
1. DEBUG_REPORT.md - Known issues & fixes
2. PRODUCTION_STATUS.md - Feature status
3. Database connection status
4. MySQL service running

---

**Version**: 1.0  
**Last Updated**: May 14, 2026  
**Status**: Production Ready ✅
