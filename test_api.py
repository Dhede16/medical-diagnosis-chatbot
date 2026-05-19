"""
test_api.py - Script untuk test koneksi ke Groq API
Jalankan dengan: python test_api.py
"""

import json
import sys
from config import GROQ_API_KEY, GROQ_MODEL, GROQ_TEMP, GROQ_MAX_TOK

print("=" * 60)
print("TEST GROQ API CONNECTION")
print("=" * 60)

# Check API key
if not GROQ_API_KEY or GROQ_API_KEY.startswith("gsk_XXX"):
    print("❌ ERROR: API Key tidak valid!")
    print(f"   Current: {GROQ_API_KEY[:20]}...")
    print("\nSolusi: Edit config.py dan masukkan API key yang valid dari https://console.groq.com")
    exit(1)

print(f"✓ API Key: {GROQ_API_KEY[:30]}...")
print(f"✓ Model: {GROQ_MODEL}")
print(f"✓ Temperature: {GROQ_TEMP}")
print(f"✓ Max Tokens: {GROQ_MAX_TOK}")

print("\n" + "=" * 60)
print("Mencoba install requests library...")
print("=" * 60)

try:
    import requests
    print("✓ requests library sudah terinstall")
except ImportError:
    print("Menginstall requests...")
    import subprocess
    subprocess.check_call([sys.executable, "-m", "pip", "install", "requests", "-q"])
    import requests
    print("✓ requests library berhasil diinstall")

print("\n" + "=" * 60)
print("Mengirim test request ke Groq API dengan requests library...")
print("=" * 60)

try:
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json",
    }
    
    payload = {
        "model": GROQ_MODEL,
        "messages": [
            {"role": "system", "content": "Anda adalah assistant yang membantu."},
            {"role": "user", "content": "Halo, apakah Anda bisa membantu?"}
        ],
        "temperature": GROQ_TEMP,
        "max_tokens": GROQ_MAX_TOK,
    }
    
    print(f"Headers: {headers}")
    print(f"URL: https://api.groq.com/openai/v1/chat/completions")
    print(f"Payload keys: {list(payload.keys())}")
    print("Mengirim request...")
    
    response = requests.post(
        "https://api.groq.com/openai/v1/chat/completions",
        headers=headers,
        json=payload,
        timeout=30
    )
    
    print(f"Status Code: {response.status_code}")
    
    if response.status_code == 200:
        data = response.json()
        content = data["choices"][0]["message"]["content"]
        print("\n✅ SUCCESS! API berhasil terhubung!")
        print(f"\nRespon dari API:\n{content}")
    else:
        print(f"\n❌ HTTP Error {response.status_code}")
        print(f"Response: {response.text}")
        
        if response.status_code == 401:
            print("\n💡 HINT: Masalah otentikasi (401 Unauthorized)")
            print("   - API Key mungkin invalid atau expired")
            print("   - Coba buat API Key baru di https://console.groq.com")
        elif response.status_code == 403:
            print("\n💡 HINT: Akses ditolak (403 Forbidden)")
            print("   - Akun mungkin belum terverifikasi")
            print("   - Atau API Key sudah dihapus")
            print("   - Coba cek dashboard Groq: https://console.groq.com")
        elif response.status_code == 429:
            print("\n💡 HINT: Rate limit tercapai (429)")
            print("   - Tunggu sebentar dan coba lagi")

except requests.exceptions.ConnectionError as e:
    print(f"\n❌ Connection Error: {e}")
    print("\n💡 HINT: Tidak bisa terhubung ke Groq API")
    print("   - Periksa koneksi internet")
    print("   - Coba disable VPN jika ada")
    
except requests.exceptions.Timeout as e:
    print(f"\n❌ Timeout Error: {e}")
    print("\n💡 HINT: Request timeout")
    print("   - Groq API mungkin sedang lambat")
    print("   - Coba lagi dalam beberapa saat")

except Exception as exc:
    print(f"\n❌ Unexpected Error: {exc}")
    import traceback
    traceback.print_exc()

print("\n" + "=" * 60)
