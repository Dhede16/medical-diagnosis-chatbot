"""
utils/api_worker.py — Worker thread untuk request ke Groq API.
"""

import threading
import urllib.request
import urllib.error
import json
from config import GROQ_MODEL, GROQ_TEMP, GROQ_MAX_TOK


class GroqWorker(threading.Thread):
    """
    Thread terpisah agar UI tidak freeze saat menunggu respons API.
    Callback `on_result(text)` dan `on_error(msg)` dipanggil dari thread ini;
    pastikan update UI memakai widget.after() di sisi pemanggil.
    """

    def __init__(self, api_key: str, messages: list,
                 on_result, on_error):
        super().__init__(daemon=True)
        self.api_key  = api_key
        self.messages = messages
        self.on_result = on_result
        self.on_error  = on_error

    def run(self):
        try:
            payload = json.dumps({
                "model": GROQ_MODEL,
                "messages": self.messages,
                "temperature": GROQ_TEMP,
                "max_tokens": GROQ_MAX_TOK,
            }).encode("utf-8")

            req = urllib.request.Request(
                "https://api.groq.com/openai/v1/chat/completions",
                data=payload,
                headers={
                    "Content-Type": "application/json",
                    "Authorization": f"Bearer {self.api_key}",
                },
                method="POST",
            )
            with urllib.request.urlopen(req, timeout=30) as resp:
                data = json.loads(resp.read().decode())
                content = data["choices"][0]["message"]["content"]
                self.on_result(content)

        except urllib.error.HTTPError as e:
            body = e.read().decode()
            try:
                msg = json.loads(body).get("error", {}).get("message", body)
            except Exception:
                msg = body
            self.on_error(f"HTTP {e.code}: {msg}")
        except Exception as exc:
            self.on_error(str(exc))
