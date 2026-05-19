# 🔧 Panduan Perbaikan: API Groq Tidak Terhubung

## 📍 Diagnosis Masalah

Anda mendapat error: **HTTP 403 Forbidden (Error Code: 1010)**

Ini biasanya berarti API Key Anda tidak punya akses atau sudah expired.

---

## ✅ Solusi Langkah demi Langkah

### **Langkah 1: Periksa/Buat API Key Baru**

1. Buka browser dan pergi ke: https://console.groq.com
2. Login dengan akun Anda (atau buat akun baru jika belum punya)
3. Di sidebar, cari **"API Keys"** atau **"Settings"**
4. Klik tombol **"Create New API Key"** atau **"Generate Key"**
5. **Copy API Key** 

### **Langkah 2: Update config.py**

1. Buka file: `config.py` di folder project
2. Cari baris ini:
   ```python
   GROQ_API_KEY = "API KEY HERE"
   ```
3. Ganti dengan API Key baru Anda:
   ```python
   GROQ_API_KEY = "PASTE_KEY_ANDA_DI_SINI"
   ```
4. **SAVE file** (Ctrl+S)

### **Langkah 3: Test Koneksi API**

1. Buka **Terminal** di folder project
2. Jalankan:
   ```bash
   python test_api.py
   ```
3. Tunggu hingga selesai dan lihat hasilnya:
   - ✅ Jika berhasil → API terkoneksi!
   - ❌ Jika gagal → Lihat error message dan ikuti saran di bawah

### **Langkah 4: Restart Aplikasi**

Setelah API Key diupdate:
1. Tutup aplikasi (jika sedang berjalan)
2. Jalankan aplikasi lagi: `python main.py`

---

## 🆘 Troubleshooting

### Error: 403 Forbidden (1010)

**Penyebab mungkin:**
- ❌ API Key tidak valid atau sudah dihapus
- ❌ Akun Groq masih dalam trial dan belum diverifikasi
- ❌ Terlalu banyak failed request

**Fix:**
1. ✅ Buat API Key baru di https://console.groq.com
2. ✅ Pastikan akun Anda sudah terverifikasi
3. ✅ Tunggu 5 menit sebelum retry jika ada rate limiting

### Error: 401 Unauthorized

**Penyebab:**
- ❌ API Key salah atau berformat tidak valid
- ❌ Token corrupted atau expired

**Fix:**
1. ✅ Copy API Key lagi dari console
2. ✅ Pastikan tidak ada space atau karakter extra
3. ✅ Buat API Key baru jika perlu

### Error: Connection Timeout / Can't Connect

**Penyebab:**
- ❌ Internet connection bermasalah
- ❌ Firewall memblokir akses ke api.groq.com
- ❌ Groq API sedang down

**Fix:**
1. ✅ Periksa koneksi internet Anda
2. ✅ Coba dari jaringan lain (misalnya hotspot)
3. ✅ Check status Groq di: https://status.groq.com
4. ✅ Disable VPN/Proxy jika ada

---

## 🧪 Test Manual

Jika ingin test dari Command Line:

```bash
python test_api.py
```

---

## 📚 Dokumentasi Terkait

- [PRODUCTION_STATUS.md](PRODUCTION_STATUS.md) - Status sistem keseluruhan
- [DEBUG_REPORT.md](DEBUG_REPORT.md) - Laporan debug lengkap
- [README.md](README.md) - Panduan umum aplikasi

**Terakhir diperbarui**: May 17, 2026

Script ini akan:
- ✓ Validasi API Key
- ✓ Check model availability
- ✓ Kirim test request ke Groq
- ✓ Tampilkan detailed error jika ada

---

## 📞 Bantuan Lebih Lanjut

Jika masih tidak bisa:

1. **Check status Groq API:** https://status.groq.com
2. **Baca Groq docs:** https://console.groq.com/docs
3. **Contact Groq support:** support@groq.com

---

## ℹ️ Info Penting

- **Jangan pernah share API Key Anda** di public code atau chat
- **API Key gratis Groq**: Ada rate limit, tapi cukup untuk development
- **Model yang digunakan:** `llama-3.3-70b-versatile` (powerful & fast)

---

## 📚 Dokumentasi Terkait

- [PRODUCTION_STATUS.md](PRODUCTION_STATUS.md) - Status sistem keseluruhan
- [DEBUG_REPORT.md](DEBUG_REPORT.md) - Laporan debug lengkap
- [README.md](README.md) - Panduan umum aplikasi

---

**Terakhir diperbarui**: May 17, 2026
