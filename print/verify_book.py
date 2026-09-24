import re
from pathlib import Path

ROOT = Path(r"C:\Users\bagas\AppData\Roaming\Open Design\namespaces\release-stable-win\data\projects\7edb36e4-0c2f-40a8-a492-052922993752\print")
issues = []

KNOWN_DANGLING = {
    "Diagram",  # bab-04/sub-bab-5: heading section "## 7. Diagram:" tanpa nomor
    "Gambar",   # bab-08/sub-bab-1: label yatim Gambar 3 (media tidak ada di repo)
}

# typo konten immutable (bintang tak-pasangan) — dibiarkan, dilaporkan build
KNOWN_TYPO_CTX = (
    "umum)**",              # bab-08/sub-bab-5:179 closing ** tanpa pasangan
    "Rp 1.08M**",           # bab-08/sub-bab-9:208 stray ** di sel tabel
    "fine-tuning* bukan",   # bab-10/sub-bab-3:208 **fine-tuning* (bintang kurang)
)


def strip_code(t: str) -> str:
    t = re.sub(r"(?s)<pre[^>]*>.*?</pre>", " ", t)
    t = re.sub(r"<code>[^<]*</code>", " ", t)
    t = re.sub(r"<t[dh][^>]*>\*+</t[dh]>", " ", t)  # sel rating bintang literal
    t = re.sub(r"\{\{query\}\}", " ", t)  # template prompt sah
    return t


for name in ("jilid-1", "jilid-2"):
    p = ROOT / "preview" / f"{name}.html"
    t = p.read_text(encoding="utf-8")
    print(f"== {name} size={p.stat().st_size // 1024}KB")

    for tag in ("section", "div", "figure", "table", "ul", "ol", "blockquote", "aside", "nav", "main", "figcaption"):
        o = len(re.findall(rf"<{tag}[\s>]", t))
        c = len(re.findall(rf"</{tag}>", t))
        if o != c:
            issues.append(f"{name}: <{tag}> {o} vs </{tag}> {c}")

    hrefs = set(re.findall(r'href="#([^"]+)"', t))
    ids = set(re.findall(r'id="([^"]+)"', t))
    missing = sorted(h for h in hrefs if h not in ids)
    if missing:
        issues.append(f"{name}: anchor hilang: {missing[:10]}")

    tc = strip_code(t)

    for pat, label in [
        (r"\]\(", "sisa link md"),
        (r"!\[", "sisa image md"),
        (r"(?<!\*)\*\*(?!\*)", "sisa bold md"),
        (r"(?<!\*)\*\*\*[^<\n]{1,80}\*\*\*", "sisa triple-star"),
        (r"(?m)^#{1,6} ", "sisa heading md"),
        (r"\x00", "placeholder NUL"),
        (r"(?<![\w.])Tabel\s+\d+\s*:", "referensi/label Tabel pola lama"),
    ]:
        found = list(re.finditer(pat, tc))
        if not found:
            continue
        if pat.startswith("(?<!\\*)\\*\\*(?!\\*)"):
            # sisa bold: buang yang konteksnya typo konten yang diketahui
            kept = []
            for m in found:
                ctx = tc[max(0, m.start() - 40) : m.end() + 40]
                if any(k in ctx for k in KNOWN_TYPO_CTX):
                    continue
                kept.append(m)
            if kept:
                issues.append(f"{name}: {label}: {len(kept)} ex={[m.group(0) for m in kept[:4]]}")
            continue
        m = [g if isinstance(g, str) else g[0] for g in re.findall(pat, tc)]
        if m:
            issues.append(f"{name}: {label}: {len(m)} ex={m[:4]}")

    # referensi Gambar/Diagram pola lama (kecuali 2 cacat konten yang diketahui)
    dangling = []
    for m in re.finditer(r"(?<![\w.])(Gambar|Diagram)\s+(\d+)(?!\.?\d)", tc):
        s = max(0, m.start() - 30)
        ctx = tc[s : m.end() + 30]
        if m.group(1) in KNOWN_DANGLING:
            dangling.append(re.sub(r"\s+", " ", ctx)[:90])
        else:
            issues.append(f"{name}: referensi pola lama: {m.group(0)} ctx={ctx[:80]!r}")
    if dangling:
        print(f"  (diketahui) referensi konten menggantung: {len(dangling)}")
        for d in dangling[:4]:
            print("    ", d)

    if "\x00" in t:
        issues.append(f"{name}: NUL asli di file")

    strong_star = [
        s
        for s in re.findall(r"<strong>[^<]*\*[^<]*</strong>", t)
        if not any(k in s for k in KNOWN_TYPO_CTX)
    ]
    if strong_star:
        issues.append(f"{name}: strong mengandung bintang: {len(strong_star)} ex={strong_star[:3]}")

    stray_em = re.findall(r"<em>[^<]*\*\*[^<]*</em>", t)
    if stray_em:
        issues.append(f"{name}: em mengandung bold-star: {len(stray_em)} ex={stray_em[:2]}")

    for src in re.findall(r'<img[^>]+src="([^"]+)"', t):
        if src.startswith("http"):
            issues.append(f"{name}: hotlink {src}")
        elif src.startswith("../assets/images/"):
            if not (ROOT / src[3:]).is_file():
                issues.append(f"{name}: gambar hilang {src}")

    if 'src="../assets/mermaid.min.js"' not in t:
        issues.append(f"{name}: tag script mermaid hilang")

    for w in ("Lorem ipsum", "TBD:", "FIXME"):
        if w in tc:
            issues.append(f"{name}: placeholder '{w}'")

    n_sub = len(re.findall(r'<section class="subbab"', t))
    n_div = len(re.findall(r'<section class="chapter-divider"', t))
    n_mer = len(re.findall(r'class="mermaid"', t))
    n_fig = len(re.findall(r"<figcaption>", t))
    n_tbl = len(re.findall(r'<div class="table-wrap', t))
    n_lbl = len(re.findall(r'class="table-label"', t))
    print(
        f"  subbab={n_sub} divider={n_div} mermaid={n_mer} figcap={n_fig} "
        f"tabel={n_tbl} label={n_lbl}"
    )

    # contoh nomor bab pertama jilid
    if name == "jilid-1":
        ex_t = re.findall(r"Tabel 1\.\d+:", tc)
        ex_g = re.findall(r"Gambar 1\.\d+-\d+", tc)
    else:
        ex_t = re.findall(r"Tabel 5\.\d+:", tc)
        ex_g = re.findall(r"Gambar 5\.\d+-\d+", tc)
    print(f"  contoh nomor: {ex_t[:3]} | {ex_g[:3]}")

    # sample junction hasil
    j = re.findall(r"<strong>[^<]*<em>[^<]*</em>[^<]*</strong>", tc)
    print(f"  strong+em terproses: {len(j)} ex={j[:2]}")

if not (ROOT / "assets" / "mermaid.min.js").is_file():
    issues.append("assets/mermaid.min.js hilang")
if not (ROOT / "assets" / "paged.polyfill.js").is_file():
    issues.append("assets/paged.polyfill.js hilang")

t = (ROOT / "index.html").read_text(encoding="utf-8")
for href in re.findall(r'href="(preview/[^"]+)"', t):
    if not (ROOT / href).is_file():
        issues.append(f"index.html: link rusak {href}")

if issues:
    print("ISSUES:")
    for x in issues:
        print(" -", x)
else:
    print("ALL STATIC CHECKS PASSED")
