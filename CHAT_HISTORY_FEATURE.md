# 📚 Fitur Chat History - ChatGPT Style

## 🎯 Overview
Fitur chat history yang sudah ditingkatkan menyerupai ChatGPT dengan **grouping berdasarkan tanggal** dan **collapsible sections** untuk organisasi yang lebih baik.

---

## ✨ Fitur Utama

### 1. **Date-Based Grouping**
Chat history secara otomatis diorganisir dalam kategori waktu:

| Kategori | Deskripsi |
|----------|-----------|
| 🔵 **Today** | Chat yang dikirim hari ini |
| 🟡 **Yesterday** | Chat dari kemarin |
| 🟢 **This Week** | Chat dari minggu ini (2-7 hari lalu) |
| 🟠 **Last Month** | Chat dari bulan terakhir (8-30 hari lalu) |
| ⚫ **Older** | Chat yang lebih dari 30 hari lalu |

### 2. **Collapsible Sections**
- Setiap grup tanggal bisa **diklik** untuk expand/collapse
- Header menampilkan simbol:
  - `▼` = Grup **terbuka** (sedang menampilkan chat)
  - `▶` = Grup **tertutup** (chat tersembunyi)
- Membantu menjaga sidebar tetap rapi dan tidak ramai

### 3. **Chat Management**
Setiap chat dalam grup memiliki:
- **Judul**: 30 karakter pertama dari pesan (otomatis dipotong)
- **Tombol klik**: Buka chat history yang dipilih
- **Tombol hapus (✕)**: Hapus satu chat (muncul saat hover)

### 4. **Quick Actions**
- **+ New chat**: Buat percakapan baru
- **🗑 Hapus semua riwayat**: Clear semua history sekaligus

---

## 🔄 Cara Kerja

### Ketika Aplikasi Dibuka:
```
1. Ambil semua chat dari database user
2. Kategorikan berdasarkan created_at timestamp
3. Susun dalam grup dengan header collapsible
4. Tampilkan di sidebar dengan expand state default
```

### Ketika User Klik Chat:
```
1. Load percakapan lengkap dari database
2. Tampilkan semua messages di chat area
3. User bisa lanjut percakapan atau read-only viewing
```

### Ketika User Hapus Chat:
```
1. Delete dari database
2. Refresh sidebar otomatis
3. Grup yang kosong tidak ditampilkan
```

---

## 📁 Struktur Database

Chat disimpan di tabel `history_chat`:

```sql
CREATE TABLE history_chat (
    id              INT AUTO_INCREMENT PRIMARY KEY,
    username        VARCHAR(50) NOT NULL,
    title           VARCHAR(255) NOT NULL,      -- Judul (dari msg pertama)
    preview         TEXT,                        -- Preview singkat
    messages        LONGTEXT NOT NULL,           -- Chat lengkap (JSON)
    created_at      TIMESTAMP DEFAULT NOW(),    -- Waktu dibuat
    updated_at      TIMESTAMP ON UPDATE NOW(),  -- Waktu update terakhir
    FOREIGN KEY (username) REFERENCES users(username)
);
```

---

## 💻 Implementasi Teknis

### File yang Dimodifikasi:
- **`widgets/sidebar.py`** - Sidebar dengan date grouping

### Class Baru:
```python
class DateGroup:
    """Tracking group tanggal dan state collapse/expand"""
    label          # Nama grup (Today, Yesterday, dll)
    chats          # List chat dalam grup
    collapsed      # Boolean state
    frame          # UI element untuk grup
    header_btn     # Tombol header
    content_frame  # Container chat items
    items          # List chat items dalam grup
```

### Method Utama:

#### `_categorize_chat_by_date(created_at_str: str) -> str`
```python
# Parse timestamp dari database
# Return: "Today" | "Yesterday" | "This Week" | "Last Month" | "Older"
```

#### `_group_chats_by_date(chat_list: list) -> dict`
```python
# Group chat list berdasarkan date category
# Return: {"Today": [...], "Yesterday": [...], ...}
```

#### `load_history_from_db(username: str)`
```python
# Load history dari DB dan populate UI dengan grouping
# Otomatis clear history UI terlebih dahulu
```

#### `_add_date_group(group_label: str, chats: list)`
```python
# Buat satu date group dengan header collapsible
# Populate dengan chat items
```

#### `_toggle_date_group(group: DateGroup)`
```python
# Toggle collapsed state
# Update UI (header text ▼/▶)
```

---

## 🎨 UI/UX Details

### Sidebar Layout:
```
┌─────────────────────────────────┐
│  🏥 MedAI                       │
│  ────────────────────────────── │
│  + New chat                     │
│  ────────────────────────────── │
│  Riwayat                        │
│                                 │
│  ▼ Today (3 chats)              │
│    💬 Demam dan sakit kepala    │ ✕
│    💬 Flu symptoms             │ ✕
│    💬 Sesak napas...           │ ✕
│                                 │
│  ▼ Yesterday (2 chats)          │
│    💬 Nyeri sendi               │ ✕
│    💬 Mual dan pusing...        │ ✕
│                                 │
│  ▶ This Week (5 chats)          │
│    (collapsed - hidden)         │
│                                 │
│  ────────────────────────────── │
│  🗑 Hapus semua riwayat         │
└─────────────────────────────────┘
```

### Colors:
- **Header text**: `TEXT_MUTED` (#8E8EA0) - subdued appearance
- **Chat item text**: `TEXT_PRIMARY` (#ECECEC) - bright for readability
- **Hover**: `BTN_HOVER` (#404040) - highlight on interaction
- **Delete button**: `ACCENT_RED` (#EF4444) - warning color

---

## 🔍 Logic Detail: Date Categorization

```python
today = datetime.now()
chat_date = datetime.strptime(created_at, "%Y-%m-%d %H:%M:%S")
diff_days = (today - chat_date).days

if diff_days == 0:           return "Today"
elif diff_days == 1:         return "Yesterday"
elif diff_days <= 7:         return "This Week"      # 2-7 hari
elif diff_days <= 30:        return "Last Month"     # 8-30 hari
else:                        return "Older"          # > 30 hari
```

---

## 🚀 Usage Examples

### Contoh 1: User Login dan Lihat History
```
1. Login dengan username: "admin"
2. Sidebar auto-load chat history dari database
3. Chat dikelompokkan berdasarkan tanggal
4. User bisa collapse grup yang tidak butuh
```

### Contoh 2: Open Old Chat
```
1. User klik chat di grup "This Week"
2. Chat history di-restore ke chat panel
3. Tampilkan semua messages dengan user/bot bubbles
4. User bisa lanjut percakapan
```

### Contoh 3: Delete Chat
```
1. User hover chat item
2. Tombol ✕ muncul
3. Klik ✕ → delete dari database
4. Sidebar auto-refresh
5. Jika grup jadi kosong → grup hilang dari display
```

---

## ⚙️ Configuration

Tidak ada configuration khusus untuk fitur ini. Semuanya otomatis:
- Date categorization berdasarkan **system time**
- Group sorting otomatis (Today → Yesterday → ... → Older)
- Collapse state di-reset saat reload history

---

## 🐛 Troubleshooting

### Issue: Chat tidak muncul di history
**Solusi**: Pastikan:
- Chat sudah disimpan ke database (ada di `history_chat` table)
- User login dengan username yang benar
- Database connection aktif

### Issue: Grouping salah (misalnya chat Today masuk Yesterday)
**Solusi**: 
- Check server/database timezone setting
- Pastikan `created_at` timestamp benar di database

### Issue: Delete tidak bekerja
**Solusi**:
- Check foreign key constraint di database
- Pastikan user punya privilege delete di table

---

## 📝 Future Improvements

Ide untuk upgrade di masa depan:
- [ ] Search chat history
- [ ] Pin/star important chats
- [ ] Export chat ke file
- [ ] Custom sort (oldest first, alphabetical, etc)
- [ ] Rename chat titles
- [ ] Archive old chats
- [ ] Multi-select delete

---

## 📞 Support

Untuk pertanyaan atau bug report, silakan check:
- [DEBUG_REPORT.md](DEBUG_REPORT.md)
- [README.md](README.md)

---

**Last Updated**: May 2026
**Version**: 2.0 (with Date Grouping)
