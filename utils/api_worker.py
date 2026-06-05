import threading
import json
from config import GROQ_MODEL, GROQ_TEMP, GROQ_MAX_TOK

try:
    import requests
except ImportError:
    import subprocess
    import sys
    print("[API] Installing requests library...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "requests", "-q"])
    import requests


class GroqWorker(threading.Thread):
    def __init__(self, api_key: str, messages: list,
                 on_result, on_error):
        super().__init__(daemon=True)
        self.api_key  = api_key
        self.messages = messages
        self.on_result = on_result
        self.on_error  = on_error

    def run(self):
        try:
            # Validasi API key
            if not self.api_key or self.api_key.startswith("gsk_XXX"):
                self.on_error("❌ API Key tidak valid. Silakan isi GROQ_API_KEY di config.py")
                return
            
            print(f"[API] Menghubungi Groq API dengan model: {GROQ_MODEL}")
            
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json",
            }
            
            payload = {
                "model": GROQ_MODEL,
                "messages": self.messages,
                "temperature": GROQ_TEMP,
                "max_tokens": GROQ_MAX_TOK,
            }
            
            print("[API] Request dikirim ke Groq API...")
            response = requests.post(
                "https://api.groq.com/openai/v1/chat/completions",
                headers=headers,
                json=payload,
                timeout=60
            )
            
            if response.status_code == 200:
                data = response.json()
                content = data["choices"][0]["message"]["content"]
                print(f"[API] ✓ Respons diterima dari API")
                self.on_result(content)
            else:
                # Handle error responses
                print(f"[API] HTTP Error {response.status_code}")
                try:
                    error_data = response.json()
                    error_msg = error_data.get("error", {})
                    if isinstance(error_msg, dict):
                        error_msg = error_msg.get("message", str(error_msg))
                except:
                    error_msg = response.text
                
                # Format pesan error yang informatif
                if response.status_code == 401:
                    self.on_error(f"❌ **Unauthorized (401)**: API Key tidak valid atau expired.\n\n**Solusi:**\n1. Buka https://console.groq.com\n2. Login dengan akun Anda\n3. Copy API Key dari Settings\n4. Paste ke GROQ_API_KEY di config.py\n5. Restart aplikasi")
                elif response.status_code == 403:
                    self.on_error(f"❌ **Forbidden (403)**: API Key tidak punya akses yang cukup.\n\n**Kemungkinan penyebab:**\n• API Key expired atau sudah dihapus\n• Akun Groq masih dalam mode trial\n• Terlalu banyak error request\n\n**Solusi:**\n1. Kunjungi https://console.groq.com\n2. Verify akun Anda dan upgrade jika perlu\n3. Buat API Key baru\n4. Ganti di config.py")
                elif response.status_code == 429:
                    self.on_error(f"❌ **Rate Limited (429)**: Terlalu banyak request. Tunggu sebentar sebelum mencoba lagi.")
                elif response.status_code == 500:
                    self.on_error(f"❌ **Server Error (500)**: Groq API sedang mengalami masalah. Coba lagi nanti.")
                else:
                    self.on_error(f"❌ **HTTP {response.status_code}**: {error_msg}")

        except requests.exceptions.ConnectionError as e:
            print(f"[API] Connection Error: {e}")
            self.on_error(f"❌ **Connection Error**: Tidak bisa terhubung ke Groq API.\n\nPeriksa:\n• Koneksi internet Anda\n• URL endpoint API\n• Firewall/Proxy settings")
            
        except requests.exceptions.Timeout as e:
            print(f"[API] Timeout Error: {e}")
            self.on_error(f"❌ **Timeout Error**: Request timeout (lebih dari 60 detik).\n\nGroq API mungkin sedang lambat. Coba lagi.")
            
        except json.JSONDecodeError as e:
            print(f"[API] JSON Decode Error: {e}")
            self.on_error(f"❌ **Response Error**: API mengirim respons yang tidak valid. Coba lagi.")
            
        except Exception as exc:
            print(f"[API] Unexpected Error: {exc}")
            self.on_error(f"❌ **Error**: {str(exc)}\n\nSilakan periksa log console untuk detail lebih lanjut.")
