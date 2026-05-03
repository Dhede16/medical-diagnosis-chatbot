"""
utils/formatter.py — Konversi markdown sederhana ke format yang bisa
ditampilkan di widget CTkTextbox dengan tag warna/font.
"""

import re
from typing import List, Tuple


def parse_markdown(text: str) -> List[Tuple[str, str]]:
    """
    Memecah teks markdown menjadi list (segment, tag).
    Tag yang tersedia: 'bold', 'bullet', 'heading2', 'heading3', 'normal'.
    Return list of (text_piece, tag_name).
    """
    segments: List[Tuple[str, str]] = []
    lines = text.split("\n")

    for line in lines:
        stripped = line.strip()

        # Heading ###
        if stripped.startswith("### "):
            content = stripped[4:]
            segments.extend(_inline_bold(content, "heading3"))
            segments.append(("\n", "normal"))

        # Heading ##
        elif stripped.startswith("## "):
            content = stripped[3:]
            segments.extend(_inline_bold(content, "heading2"))
            segments.append(("\n", "normal"))

        # Bullet
        elif stripped.startswith("* ") or stripped.startswith("- "):
            segments.append(("  • ", "bullet"))
            content = stripped[2:]
            segments.extend(_inline_bold(content, "bullet_text"))
            segments.append(("\n", "normal"))

        # Normal
        else:
            segments.extend(_inline_bold(line, "normal"))
            segments.append(("\n", "normal"))

    return segments


def _inline_bold(text: str, base_tag: str) -> List[Tuple[str, str]]:
    """Pecah teks dengan **bold** menjadi segmen normal + bold."""
    parts: List[Tuple[str, str]] = []
    pattern = re.compile(r'\*\*(.+?)\*\*')
    last = 0
    for m in pattern.finditer(text):
        if m.start() > last:
            parts.append((text[last:m.start()], base_tag))
        parts.append((m.group(1), "bold"))
        last = m.end()
    if last < len(text):
        parts.append((text[last:], base_tag))
    return parts


def strip_markdown(text: str) -> str:
    """Menghapus simbol markdown untuk keperluan clipboard/export."""
    text = re.sub(r'\*\*(.+?)\*\*', r'\1', text)
    text = re.sub(r'^#{1,3}\s+', '', text, flags=re.MULTILINE)
    text = re.sub(r'^[*\-]\s+', '• ', text, flags=re.MULTILINE)
    return text
