# -*- coding: utf-8 -*-
"""Cek kontras token DESIGN.md dan overflow statis pada preview."""
import re, sys, pathlib

ROOT = pathlib.Path(r"C:\Users\bagas\AppData\Roaming\Open Design\namespaces\release-stable-win\data\projects\7edb36e4-0c2f-40a8-a492-052922993752")
PRINT = ROOT / "print"
fail = 0

def note(msg):
    global fail
    print(msg)
    if "FAIL" in msg:
        fail += 1

# ---------- 1. Kontras token DESIGN.md ----------
def srgb_to_lin(c):
    c = c / 255.0
    return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4

def luminance(hex_color):
    h = hex_color.lstrip("#")
    if len(h) == 3:
        h = "".join(ch * 2 for ch in h)
    r, g, b = (int(h[i:i+2], 16) for i in (0, 2, 4))
    return 0.2126 * srgb_to_lin(r) + 0.7152 * srgb_to_lin(g) + 0.0722 * srgb_to_lin(b)

def contrast(fg, bg):
    l1, l2 = luminance(fg), luminance(bg)
    lighter, darker = max(l1, l2), min(l1, l2)
    return (lighter + 0.05) / (darker + 0.05)

pairs = [
    ("ink on bg",        "#1A1A2E", "#FFFFFF", 4.5),
    ("ink-muted on bg",  "#4A4A5A", "#FFFFFF", 4.5),
    ("primary on bg",    "#4F46E5", "#FFFFFF", 4.5),
    ("ink on surface",   "#1A1A2E", "#F4F4F8", 4.5),
    ("ink-muted on surface", "#4A4A5A", "#F4F4F8", 4.5),
    ("accent on surface (label)", "#0D9488", "#F4F4F8", 3.0),
    ("warn-ink on warn-bg", "#1A1A2E", "#FEF3C7", 4.5),
    ("ink on zebra",     "#1A1A2E", "#FAFAFC", 4.5),
    ("border vs bg (nonteks)", "#D8D8E0", "#FFFFFF", 1.2),
]
print("== Kontras token ==")
for label, fg, bg, min_ratio in pairs:
    r = contrast(fg, bg)
    status = "OK" if r >= min_ratio else "FAIL"
    note(f"  [{status}] {label}: {r:.2f}:1 (min {min_ratio})")

# ---------- 2. Overflow statis ----------
print("== Overflow statis (preview) ==")
for name in ("jilid-1.html", "jilid-2.html"):
    path = PRINT / "preview" / name
    html = path.read_text(encoding="utf-8")
    # baris <pre> tanpa spasi > 90 char (kemungkinan overflow)
    long_pre = 0
    for m in re.finditer(r"<pre[^>]*>(.*?)</pre>", html, re.S):
        block = re.sub(r"<[^>]+>", "", m.group(1))
        for line in block.splitlines():
            if len(line) > 90 and " " not in line:
                long_pre += 1
    # cell tabel sangat panjang tanpa spasi
    long_cells = 0
    for m in re.finditer(r"<td[^>]*>(.*?)</td>", html, re.S):
        text = re.sub(r"<[^>]+>", "", m.group(1)).strip()
        if len(text) > 60 and " " not in text:
            long_cells += 1
    # tag gambar dengan dimensi absolut besar tanpa max-width guard di CSS
    css = (PRINT / "book.css").read_text(encoding="utf-8")
    has_img_guard = bool(re.search(r"img[^{]*\{[^}]*max-width\s*:\s*100%", css))
    note(f"  {name}: pre tanpa-spasi>90={long_pre} (info), cell tabel>60={long_cells} (info), img-guard={has_img_guard}")
    if not has_img_guard:
        note(f"  [FAIL] {name}: CSS tanpa img max-width:100%")

    # pastikan ada overflow-x:auto untuk tabel
    if not re.search(r"table[^{]*\{[^}]*overflow-x\s*:\s*auto", css):
        note(f"  [FAIL] book.css: tabel tanpa overflow-x:auto")
    else:
        note(f"  [OK] book.css: tabel overflow-x:auto")

print("== Ringkasan ==")
if fail:
    print(f"FAIL count: {fail}")
    sys.exit(1)
print("ALL EXTRA CHECKS PASSED")
sys.exit(0)
