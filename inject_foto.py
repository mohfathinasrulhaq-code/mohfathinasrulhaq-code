"""
Cara pakai:
1. Simpan teks base64 fotomu ke file bernama foto_base64.txt (satu file, isinya hanya base64).
2. Taruh file ini, profile-banner.svg, dan foto_base64.txt dalam satu folder.
3. Jalankan:  python inject_foto.py
"""
import re, sys

raw = open("foto_base64.txt", encoding="utf-8").read().strip()
raw = re.sub(r"^data:image/[a-z]+;base64,", "", raw)   # buang prefix kalau ada
b64 = re.sub(r"\s+", "", raw)                          # buang spasi / baris baru

if b64.startswith("iVBOR"):
    mime = "image/png"
elif b64.startswith("/9j/"):
    mime = "image/jpeg"
elif b64.startswith("UklGR"):
    mime = "image/webp"
else:
    sys.exit("Format gambar tidak dikenali. Pastikan isinya base64 PNG/JPEG/WEBP.")

svg = open("profile-banner.svg", encoding="utf-8").read()
svg = re.sub(r'href="data:image/[a-z]+;base64,[^"]*"',
             f'href="data:{mime};base64,{b64}"', svg, count=1)
open("profile-banner.svg", "w", encoding="utf-8").write(svg)
print(f"Selesai: foto {mime} ({len(b64)//1024} KB base64) dimasukkan ke profile-banner.svg")
