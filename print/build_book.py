#!/usr/bin/env python3
"""Build layout buku cetak HTML dari konten/ (urutan: mkdocs nav / manifest, gaya: DESIGN.md).

Usage:
    python print/build_book.py [--konten PATH] [--only jilid-1|jilid-2]

Output:
    print/preview/jilid-1.html
    print/preview/jilid-2.html

Stdlib only. Konten tidak disunting (hanya format, nomor Tabel/Gambar, break halaman).
"""
from __future__ import annotations

import argparse
import html as html_mod
import re
import shutil
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
KONTEN_CANDIDATES = [
    HERE.parent / "konten",
    Path(r"D:\17. Development\buku-kolaborasi-llm\konten"),
]

BOOK_TITLE = "The Local LLM Bible"
BOOK_SUBTITLE = "Strategic Guide to Private AI"
BOOK_TAGLINE = "Panduan Komprehensif Ekosistem LLM Lokal"
BOOK_EDITION = "2026"
BOOK_SLOGAN = "AI lokal, data Anda, infrastruktur di tangan Anda."
BOOK_AUTHOR = "Bagaskoro Saputro dkk."
BOOK_REPO = "github.com/bagaswap111/buku-kolaborasi-llm"

BOOK_ICON_SVG = (
    '<svg width="22" height="22" viewBox="0 0 24 24" fill="none" '
    'stroke="#4F46E5" stroke-width="1.8" stroke-linecap="round" '
    'stroke-linejoin="round" aria-hidden="true">'
    '<path d="M4 19.5A2.5 2.5 0 0 1 6.5 17H20"/>'
    '<path d="M6.5 2H20v20H6.5A2.5 2.5 0 0 1 4 19.5v-15A2.5 2.5 0 0 1 6.5 2z"/>'
    "</svg>"
)

NAV_ENTRY_RE = re.compile(r'^(\s*)-\s+(?:"([^"]+)"|([^:#]+?)):\s*(\S+\.md)\s*$')
NAV_GROUP_RE = re.compile(r'^(\s*)-\s+"([^"]+)":\s*$')
NAV_BARE_RE = re.compile(r"^(\s*)-\s+(.+?)\s*$")

FENCE_RE = re.compile(r"^```([\w+#.-]*)\s*$")
HEADING_RE = re.compile(r"^(#{1,6})\s+(.*?)\s*#*\s*$")
HR_RE = re.compile(r"^(-{3,}|\*{3,}|_{3,})$")
TABLE_SEP_RE = re.compile(r"^\s*\|?\s*:?-{1,}:?\s*(\|\s*:?-{1,}:?\s*)+\|?\s*$")
LIST_ITEM_RE = re.compile(r"^(\s*)([-*+]|\d+[.)])\s+(.*)$")
IMAGE_ONLY_RE = re.compile(r"^!\[([^\]]*)\]\(([^)]+)\)$")
IMG_MD_RE = re.compile(r"!\[([^\]]*)\]\(([^)]+)\)")
LINK_MD_RE = re.compile(r"\[([^\]]+)\]\(([^)]+)\)")
ITALIC_CAPTION_RE = re.compile(r"^\*(Gambar|Diagram)\s+([0-9][0-9.Xx-]*)\s*(.*)$")
MEDIA_LABEL_RE = re.compile(r"^(Tabel|Gambar|Diagram)\s+([0-9][0-9.Xx-]*)(\s*[:\u2014-].*|\s+.*)?$")
CALLOUT_RE = re.compile(r"^\*\*([^*]+):\*\*\s*(.*)$")
EMOJI_RE = re.compile(
    "[\U0001F000-\U0001FAFF\u2600-\u27BF\u2B00-\u2BFF\uFE0F\u200D\u20E3]"
)
SLUG_RE = re.compile(r"[^a-z0-9]+")
MD_TARGET_RE = re.compile(r"^(?:(jilid-[12])/)?(bab-\d+[^/]*)/(sub-bab-(\d+))\.md$")


def esc(s: str) -> str:
    return html_mod.escape(s, quote=True)


def slugify(text: str) -> str:
    text = EMOJI_RE.sub("", text).lower()
    text = SLUG_RE.sub("-", text).strip("-")
    return text or "bagian"


def find_konten(arg: str | None) -> Path:
    if arg:
        p = Path(arg)
        if not p.is_dir():
            sys.exit(f"ERROR: folder konten tidak ditemukan: {p}")
        return p.resolve()
    for c in KONTEN_CANDIDATES:
        if c.is_dir():
            return c.resolve()
    sys.exit("ERROR: folder konten/ tidak ditemukan (gunakan --konten PATH)")


def parse_nav(text: str) -> list[tuple[int, str, str | None]]:
    entries: list[tuple[int, str, str | None]] = []
    in_nav = False
    nav_indent: int | None = None
    for line in text.splitlines():
        if not in_nav:
            if re.match(r"^nav:\s*$", line):
                in_nav = True
            continue
        if not line.strip() or line.lstrip().startswith("#"):
            if entries:
                break
            continue
        if line.strip() == "---":
            break
        indent = len(line) - len(line.lstrip())
        if nav_indent is None:
            nav_indent = indent
        if indent < nav_indent:
            break
        m = NAV_ENTRY_RE.match(line)
        if m:
            entries.append((indent, (m.group(2) or m.group(3) or "").strip(), m.group(4)))
            continue
        m = NAV_GROUP_RE.match(line)
        if m:
            entries.append((indent, m.group(2).strip(), None))
            continue
        m = NAV_BARE_RE.match(line)
        if m:
            entries.append((indent, m.group(2).strip().rstrip(":").strip('"'), None))
    return entries


def build_book_structure(entries: list[tuple[int, str, str | None]]) -> dict:
    book: dict = {"beranda": None, "jilid": []}
    jilid: dict | None = None
    chapter: dict | None = None
    base = min((i for i, _, p in entries if p), default=0)
    for indent, title, path in entries:
        level = max(1, (indent - base) // 2 + 1)
        if level == 1 and path:
            book["beranda"] = path
        elif level == 1:
            jilid = {"title": title, "overview": None, "chapters": []}
            book["jilid"].append(jilid)
        elif level == 2 and path and jilid:
            jilid["overview"] = path
        elif level == 2 and jilid:
            m = re.match(r"Bab\s+(\d+)", title)
            chapter = {
                "num": m.group(1) if m else str(len(jilid["chapters"]) + 1).zfill(2),
                "title": title,
                "files": [],
            }
            jilid["chapters"].append(chapter)
        elif level >= 3 and path and chapter:
            chapter["files"].append({"title": title, "path": path})
    return book


def sub_key(path: str) -> int:
    m = re.search(r"sub-bab-(\d+)", path)
    return m and int(m.group(1)) or 0


TABLE_HEAD_RE = re.compile(r"^#{1,3}\s+Tabel\s+([0-9][0-9.Xx-]*)")


def block_has_media_before_heading(lines: list[str], start: int) -> bool:
    """True bila ada media (mermaid/gambar) sebelum heading berikutnya."""
    i, n = start, len(lines)
    while i < n:
        s = lines[i].strip()
        if not s:
            i += 1
            continue
        if HEADING_RE.match(s):
            return False
        fm = FENCE_RE.match(s)
        if fm:
            j = i + 1
            while j < n and not lines[j].strip().startswith("```"):
                j += 1
            if fm.group(1) == "mermaid":
                return True
            i = j + 1
            continue
        if IMAGE_ONLY_RE.match(s):
            return True
        i += 1
    return False


def first_heading(path: Path) -> str | None:
    try:
        for line in path.read_text(encoding="utf-8").splitlines():
            if line.startswith("# "):
                return line[2:].strip()
    except OSError:
        return None
    return None


def add_extras(book: dict, konten: Path) -> list[str]:
    """Tambahkan file sub-bab yang ada di disk tapi belum ada di nav/manifest."""
    extras: list[str] = []
    for idx, jilid in enumerate(book["jilid"], start=1):
        jdir = konten / f"jilid-{idx}"
        if not jdir.is_dir():
            continue
        known = {f["path"].replace("\\", "/") for ch in jilid["chapters"] for f in ch["files"]}
        for bab_dir in sorted(jdir.glob("bab-*")):
            if not bab_dir.is_dir():
                continue
            chapter = None
            for ch in jilid["chapters"]:
                if ch["files"] and ch["files"][0]["path"].split("/")[1] == bab_dir.name:
                    chapter = ch
                    break
            if chapter is None:
                continue
            chapter["folder"] = bab_dir.name
            for f in sorted(bab_dir.glob("sub-bab-*.md"), key=lambda p: sub_key(p.name)):
                rel = f"{jdir.name}/{bab_dir.name}/{f.name}"
                if rel not in known:
                    h = first_heading(f) or f.stem.replace("-", " ")
                    h = re.sub(r"^Bab\s+\d+(?:\.\d+)*\s*:?\s*", "", h, flags=re.I)
                    chapter["files"].append({"title": h, "path": rel})
                    extras.append(rel)
        for ch in jilid["chapters"]:
            ch["files"].sort(key=lambda f: sub_key(f["path"]))
    return extras


class Renderer:
    def __init__(self, konten: Path, images_out: Path, jilid_name: str):
        self.konten = konten
        self.images_out = images_out
        self.jilid_name = jilid_name
        self.bab: int | None = None
        self.sub: int | None = None
        self.fig_seq = 0
        self.pending_fig: tuple[str, str, str] | None = None  # (kind, orig_num, rest)
        self.id_prefix = "hal"
        self.slug_used: set[str] = set()
        self.uid = 0
        self.stats = {
            "tabel": 0,
            "gambar": 0,
            "mermaid": 0,
            "img_ok": 0,
            "img_missing": 0,
            "ref": 0,
        }
        self.missing_images: list[str] = []
        self.warnings: list[str] = []
        self.table_map: dict[str, str] = {}
        self.fig_heading_map: dict[str, str] = {}
        self.chapter_table_maps: dict[int, dict[str, str]] = {}

    # ---------- util ----------

    def next_uid(self, kind: str) -> str:
        self.uid += 1
        return f"{kind}-{self.uid}"

    def make_id(self, text: str) -> str:
        base = f"{self.id_prefix}-{slugify(text)}"
        sid = base
        n = 2
        while sid in self.slug_used:
            sid = f"{base}-{n}"
            n += 1
        self.slug_used.add(sid)
        return sid

    def new_file_state(self, bab: int | None, sub: int | None, id_prefix: str):
        self.bab = bab
        self.sub = sub
        self.fig_seq = 0
        self.pending_fig = None
        self.id_prefix = id_prefix
        self.slug_used = set()
        self.table_map = {}
        self.fig_heading_map = {}

    # ---------- gambar ----------

    def resolve_image(self, src: str, md_path: Path) -> Path | None:
        raw = src.split()[0].strip("<>")
        base = (md_path.parent / raw).resolve()
        if base.is_file():
            return base
        name = Path(raw).name
        sub_folder = md_path.stem  # sub-bab-N
        hits = list((self.konten / "assets" / "images").rglob(name))
        if len(hits) == 1:
            return hits[0]
        if hits:
            prefer = [h for h in hits if sub_folder in h.parts]
            if len(prefer) == 1:
                return prefer[0]
            return prefer[0] if prefer else hits[0]
        return None

    def image_url(self, resolved: Path) -> str:
        root = (self.konten / "assets" / "images").resolve()
        try:
            rel = resolved.relative_to(root)
            return "../assets/images/" + rel.as_posix()
        except ValueError:
            dst = self.images_out / "_imported" / resolved.name
            dst.parent.mkdir(parents=True, exist_ok=True)
            if not dst.is_file():
                shutil.copy2(resolved, dst)
            return "../assets/images/_imported/" + resolved.name

    # ---------- inline ----------

    def inline(self, text: str, refs: bool = False) -> str:
        stash: list[str] = []

        def put(html: str) -> str:
            stash.append(html)
            return f"\x00{len(stash) - 1}\x00"

        t = esc(text)

        for m in list(re.finditer(r"`([^`]+)`", t)):
            t = t.replace(m.group(0), put(f"<code>{m.group(1)}</code>"))

        for m in list(IMG_MD_RE.finditer(t)):
            alt, src = m.group(1), m.group(2)
            t = t.replace(m.group(0), put(f'<img src="{esc(src)}" alt="{alt}">'))

        def link_sub(m: re.Match) -> str:
            label, href = m.group(1), m.group(2)
            md = MD_TARGET_RE.match(href)
            if md:
                jilid_part, folder, _fname, subn = md.groups()
                bab_m = re.match(r"bab-(\d+)", folder)
                if bab_m and (jilid_part is None or jilid_part == self.jilid_name):
                    anchor = f"#subbab-{int(bab_m.group(1))}-{int(subn)}"
                    return put(f'<a href="{anchor}">{label}</a>')
                return put(label)
            if href.startswith("#"):
                return put(f'<a href="{href}">{label}</a>')
            if refs and href.startswith("http") and href not in label:
                return put(f'<a href="{href}">{label}</a> <span class="ref-url">({href})</span>')
            if href.startswith("http"):
                return put(f'<a href="{href}">{label}</a>')
            if href.endswith(".md"):
                return put(label)
            return put(f'<a href="{href}">{label}</a>')

        for m in list(LINK_MD_RE.finditer(t)):
            t = t.replace(m.group(0), link_sub(m))

        # junction markdown: **teks *italic*** dan ***A* + *B***
        def j1_sub(m: re.Match) -> str:
            inner = m.group(1) + f"<em>{m.group(2)}</em>"
            return put(f"<strong>{inner}</strong>")

        t = re.sub(r"(?<!\*)\*\*([^*\n]*)\*([^*\n]+)\*\*\*(?!\*)", j1_sub, t)
        # ***term1* ... *term***  -> <strong><em>term1</em> ... <em>term</em></strong>
        t = re.sub(
            r"(?<!\*)\*\*\*([^*\n]+)\*(?!\*)",
            lambda m: f"<strong><em>{m.group(1)}</em>",
            t,
        )
        t = re.sub(
            r"(?<!\*)\*([^*\n]+)\*\*\*(?!\*)",
            lambda m: f"<em>{m.group(1)}</em></strong>",
            t,
        )

        def bold_sub(m: re.Match) -> str:
            inner = re.sub(
                r"(?<!\*)\*([^*\n]+)\*(?!\*)",
                lambda im: put(f"<em>{im.group(1)}</em>"),
                m.group(1),
            )
            return put(f"<strong>{inner}</strong>")

        t = re.sub(
            r"(?<!\*)\*\*\*([^*\n]+?)\*\*\*(?!\*)",
            lambda m: put(f"<strong><em>{m.group(1)}</em></strong>"),
            t,
        )
        t = re.sub(r"(?<!\*)\*\*(?!\*)(.+?)(?<!\*)\*\*(?!\*)", bold_sub, t)
        # fallback: bold yang ditutup junction *** (multi-italic)
        t = re.sub(r"(?<!\*)\*\*(?!\*)([^<]+?)(?<!\*)\*{2,3}(?!\*)", bold_sub, t)
        t = re.sub(r"(?<!\*)\*([^*\n]+)\*(?!\*)", lambda m: put(f"<em>{m.group(1)}</em>"), t)

        def restore(m: re.Match) -> str:
            return stash[int(m.group(1))]

        out = t
        for _ in range(50):
            nxt = re.sub(r"\x00(\d+)\x00", restore, out)
            if nxt == out:
                break
            out = nxt
        return re.sub(r"\x00\d+\x00", "", out)

    # ---------- label media ----------

    def media_label(self, text: str) -> str:
        m = MEDIA_LABEL_RE.match(text.strip())
        if not m:
            return f'<p class="table-label">{self.inline(text)}</p>'
        kind, num, rest = m.group(1), m.group(2) or "", m.group(3) or ""
        if kind == "Tabel":
            new = self.table_map.get(num)
            if new:
                label = f"Tabel {new}"
                self.stats["tabel"] += 1
                suffix = rest if rest.startswith(":") else (f" {rest}" if rest else "")
                text = f"{label}{suffix}"
        return f'<p class="table-label" data-od-id="{self.next_uid("label")}">{self.inline(text)}</p>'

    def fig_number(self, orig: str) -> str:
        if self.bab and self.sub:
            self.fig_seq += 1
            self.stats["gambar"] += 1
            return f"{self.bab}.{self.sub}-{self.fig_seq}"
        return orig

    def make_figcaption(self) -> str:
        if not self.pending_fig:
            return ""
        kind, orig, rest = self.pending_fig
        self.pending_fig = None
        num = self.fig_number(orig)
        if orig and num != orig:
            self.fig_heading_map[orig] = num
        rest = rest or ""
        if rest and not rest.startswith((":", "\u2014", "-", " ")):
            rest = " " + rest
        return (
            f'<figcaption><span class="fig-num">{kind} {num}</span>'
            f"{self.inline(rest)}</figcaption>"
        )

    def take_italic_caption(self, text: str) -> str | None:
        m = ITALIC_CAPTION_RE.match(text.strip())
        if not m:
            return None
        kind, _num, rest = m.group(1), m.group(2), m.group(3)
        self.fig_seq += 1
        self.stats["gambar"] += 1
        num = f"{self.bab}.{self.sub}-{self.fig_seq}" if self.bab and self.sub else _num
        rest = rest.strip()
        sep = rest if rest.startswith(("\u2014", ":", "-")) else (f" {rest}" if rest else "")
        return (
            f'<figcaption><span class="fig-num">{kind} {num}</span>'
            f"{self.inline(sep) if sep.startswith(' ') else esc(sep)}</figcaption>"
        )

    # ---------- blok ----------

    def render_fence(self, lang: str, code: str) -> str:
        if lang == "mermaid":
            self.stats["mermaid"] += 1
            cap = self.make_figcaption() if self.pending_fig else ""
            fid = self.next_uid("diagram")
            return (
                f'<figure class="fig-diagram" data-od-id="{fid}">'
                f'<div class="mermaid">{esc(code)}</div>{cap}</figure>'
            )
        lang_s = esc(lang) if lang else ""
        label = f'<div class="code-lang">{lang_s}</div>' if lang else ""
        return (
            f'<div class="code-block" data-od-id="{self.next_uid("kode")}">'
            f"{label}<pre><code>{esc(code)}</code></pre></div>"
        )

    def render_table(self, rows: list[str]) -> str:
        def split_cells(line: str) -> list[str]:
            line = line.strip()
            if line.startswith("|"):
                line = line[1:]
            if line.endswith("|"):
                line = line[:-1]
            return [c.strip() for c in re.split(r"(?<!\\)\|", line)]

        header = split_cells(rows[0])
        seps = split_cells(rows[1])
        aligns = []
        for s in seps:
            s2 = s.replace(" ", "")
            if s2.startswith(":") and s2.endswith(":"):
                aligns.append("c")
            elif s2.endswith(":"):
                aligns.append("c")  # DESIGN §2: :---: → kolom angka rata kanan
            else:
                aligns.append("l")
        wide = " wide" if len(header) >= 6 else ""

        thead = "<tr>" + "".join(
            f'<th class="align-{aligns[i] if i < len(aligns) else "l"}">{self.inline(c)}</th>'
            for i, c in enumerate(header)
        ) + "</tr>"
        body_rows = []
        for r in rows[2:]:
            if not r.strip():
                continue
            cs = split_cells(r)
            tds = "".join(
                f'<td class="align-{aligns[i] if i < len(aligns) else "l"}">{self.inline(c)}</td>'
                for i, c in enumerate(cs)
            )
            body_rows.append(f"<tr>{tds}</tr>")
        tid = self.next_uid("tabel")
        return (
            f'<div class="table-wrap{wide}" data-od-id="{tid}">'
            f"<table><thead>{thead}</thead><tbody>{''.join(body_rows)}</tbody></table></div>"
        )

    def render_blockquote(self, lines: list[str]) -> str:
        stripped = [re.sub(r"^>\s?", "", ln) for ln in lines]
        paras: list[str] = []
        buf: list[str] = []
        for ln in stripped:
            if ln.strip():
                buf.append(ln.strip())
            else:
                if buf:
                    paras.append(" ".join(buf))
                    buf = []
        if buf:
            paras.append(" ".join(buf))
        if not paras:
            return ""
        m = CALLOUT_RE.match(paras[0])
        if m:
            label, rest = m.group(1), m.group(2)
            first = f"<strong>{esc(label)}:</strong> {self.inline(rest)}" if rest else f"<strong>{esc(label)}:</strong>"
            body = [first] + [self.inline(p) for p in paras[1:]]
            return (
                f'<aside class="callout" data-od-id="{self.next_uid("catatan")}">'
                + "".join(f"<p>{b}</p>" for b in body)
                + "</aside>"
            )
        body = "".join(f"<p>{self.inline(p)}</p>" for p in paras)
        return f'<blockquote class="epigraph">{body}</blockquote>'

    def render_list(self, block: list[str]) -> str:
        items: list[tuple[int, bool, str]] = []  # (indent, ordered, text)
        for ln in block:
            m = LIST_ITEM_RE.match(ln.rstrip())
            if m:
                ind = len(m.group(1).expandtabs(4))
                ordered = m.group(2)[0].isdigit()
                items.append((ind, ordered, m.group(3)))
            elif items and ln.strip():
                ind = len(ln) - len(ln.lstrip())
                if ind >= items[-1][0] + 2:
                    items[-1] = (items[-1][0], items[-1][1], items[-1][2] + " " + ln.strip())
        if not items:
            return ""
        root_ordered = items[0][1]
        root_tag = "ol" if root_ordered else "ul"
        out = [f"<{root_tag}>"]
        i = 0
        while i < len(items):
            ind, ordered, text = items[i]
            if ind == 0:
                children: list[str] = []
                j = i + 1
                while j < len(items) and items[j][0] > 0:
                    children.append(items[j][2])
                    j += 1
                inner = self.inline(text)
                if children:
                    tag = "ol" if ordered else "ul"
                    inner += f"<{tag}>" + "".join(f"<li>{self.inline(c)}</li>" for c in children) + f"</{tag}>"
                out.append(f"<li>{inner}</li>")
                i = j
            else:
                i += 1
        out.append(f"</{root_tag}>")
        return "".join(out)

    # ---------- file ----------

    def render_file(self, md_path: Path) -> str:
        text = md_path.read_text(encoding="utf-8")
        lines = text.splitlines()
        out: list[str] = []
        i = 0
        n = len(lines)
        first_h1 = True
        opened = False

        while i < n:
            line = lines[i]
            s = line.strip()

            if not s:
                i += 1
                continue

            m = FENCE_RE.match(s)
            if m:
                lang = m.group(1)
                j = i + 1
                buf: list[str] = []
                while j < n and not lines[j].strip().startswith("```"):
                    buf.append(lines[j])
                    j += 1
                out.append(self.render_fence(lang, "\n".join(buf)))
                i = j + 1
                continue

            m = HEADING_RE.match(s)
            if m:
                level = len(m.group(1))
                raw = EMOJI_RE.sub("", m.group(2)).strip()
                ml = MEDIA_LABEL_RE.match(raw)
                if ml and ml.group(1) in ("Gambar", "Diagram") and level <= 3:
                    if block_has_media_before_heading(lines, i + 1):
                        self.pending_fig = ("Gambar", ml.group(2), ml.group(3) or "")
                    else:
                        self.warnings.append(
                            f"{md_path.name}: label media yatim (tanpa media) -> {raw}"
                        )
                        out.append(f'<p class="table-label">{self.inline(raw)}</p>')
                    i += 1
                    continue
                if ml and ml.group(1) == "Tabel" and level <= 3:
                    out.append(self.media_label(raw))
                    i += 1
                    continue
                if level == 1 and first_h1:
                    first_h1 = False
                    opened = True
                    num = f"{self.bab}.{self.sub}" if self.bab and self.sub else ""
                    hid = self.id_prefix
                    num_html = f'<span class="opener-num">{esc(num)}</span>' if num else ""
                    out.append(
                        f'<div class="opener-block">{num_html}'
                        f'<h1 id="{esc(hid)}" data-od-id="{esc(hid)}">{self.inline(raw)}</h1>'
                        f'<hr class="opener-rule"></div>'
                    )
                    i += 1
                    continue
                if level == 1:
                    first_h1 = False
                hid = self.make_id(raw)
                tag = f"h{min(level, 4)}"
                out.append(f'<{tag} id="{esc(hid)}" data-od-id="{esc(hid)}">{self.inline(raw)}</{tag}>')
                i += 1
                continue

            if HR_RE.match(s) and "|" not in s:
                out.append('<hr class="md-hr-center">')
                i += 1
                continue

            if s.startswith(">"):
                j = i
                buf = []
                while j < n and (lines[j].strip().startswith(">") or (
                    lines[j].strip() == "" and j + 1 < n and lines[j + 1].strip().startswith(">")
                )):
                    buf.append(lines[j])
                    j += 1
                out.append(self.render_blockquote(buf))
                i = j
                continue

            if "|" in s and i + 1 < n and TABLE_SEP_RE.match(lines[i + 1]) and "|" in lines[i + 1]:
                rows = [lines[i], lines[i + 1]]
                j = i + 2
                while j < n and "|" in lines[j] and lines[j].strip() and not HR_RE.match(lines[j].strip()):
                    rows.append(lines[j])
                    j += 1
                out.append(self.render_table(rows))
                i = j
                continue

            if LIST_ITEM_RE.match(line):
                j = i
                buf = []
                while j < n and (LIST_ITEM_RE.match(lines[j]) or (
                    lines[j].strip() and lines[j][:1] in (" ", "\t") and buf
                    and not lines[j].strip().startswith(("#", "```", "|", ">"))
                    and not HR_RE.match(lines[j].strip())
                ) or (not lines[j].strip() and j + 1 < n and LIST_ITEM_RE.match(lines[j + 1]))):
                    buf.append(lines[j])
                    j += 1
                out.append(self.render_list(buf))
                i = j
                continue

            # paragraf
            buf = []
            j = i
            while j < n and lines[j].strip() and not HEADING_RE.match(lines[j].strip()) \
                    and not FENCE_RE.match(lines[j].strip()) \
                    and not lines[j].strip().startswith(">") \
                    and not LIST_ITEM_RE.match(lines[j]) \
                    and not HR_RE.match(lines[j].strip()) \
                    and not ("|" in lines[j] and j + 1 < n and TABLE_SEP_RE.match(lines[j + 1])):
                buf.append(lines[j].strip())
                j += 1
            para = " ".join(buf)
            img = IMAGE_ONLY_RE.match(para)
            if img:
                alt, src = img.group(1), img.group(2)
                resolved = self.resolve_image(src, md_path)
                cap = None
                # lookahead: caption italic setelah blok gambar
                k = j
                while k < n and not lines[k].strip():
                    k += 1
                if k < n:
                    cap = self.take_italic_caption(lines[k].strip())
                    if cap is not None:
                        self.pending_fig = None
                        j = k + 1
                if cap is None and self.pending_fig:
                    cap = self.make_figcaption()
                if resolved:
                    self.stats["img_ok"] += 1
                    url = self.image_url(resolved)
                    img_html = f'<img src="{esc(url)}" alt="{esc(alt)}" loading="eager">'
                else:
                    self.stats["img_missing"] += 1
                    self.missing_images.append(src)
                    img_html = (
                        f'<div class="image-missing">Gambar tidak ditemukan dalam proyek: '
                        f"<code>{esc(src)}</code></div>"
                    )
                out.append(
                    f'<figure data-od-id="{self.next_uid("gambar")}">{img_html}{cap or ""}</figure>'
                )
                i = j
                continue

            refs = bool(re.match(r"^\[\d+\]", para))
            cls = ' class="referensi-block"' if refs else ""
            if refs:
                out.append(f"<p{cls}>{self.inline(para, refs=True)}</p>")
            else:
                out.append(f"<p>{self.inline(para)}</p>")
            i = j

        # flush caption yang belum terpakai (seharusnya jarang: lookahead sudah jamin media)
        if self.pending_fig:
            kind, num, rest = self.pending_fig
            self.pending_fig = None
            self.warnings.append(f"{md_path.name}: label media tanpa media di akhir file -> {kind} {num}")
            out.append(
                f'<p class="table-label">{self.inline(f"{kind} {num}{rest}")}</p>'
            )
        body = "".join(out)
        if not opened:
            body = f'<div class="opener-block"><h1 id="{esc(self.id_prefix)}">{esc(md_path.stem)}</h1></div>' + body
        return body

    # ---------- renumber referensi silang dalam teks ----------

    def renumber_prose(self, html: str, source: str) -> str:
        """Renumber rujukan 'Tabel N' / 'Gambar N' / 'Diagram N' di teks biasa.

        Blok <pre>/<code> dilewati (contoh literal). Mermaid ikut direnumber.
        """
        if not (self.table_map or self.fig_heading_map):
            return html

        blocks: list[str] = []

        def stash_code(m: re.Match) -> str:
            blocks.append(m.group(0))
            return f"\x00CB{len(blocks) - 1}\x00"

        t = re.sub(r"(?s)<pre[^>]*>.*?</pre>|<code>[^<]*</code>", stash_code, html)
        count = 0
        unresolved: list[str] = []

        def cross(m: re.Match) -> str:
            nonlocal count
            num, prep, word, sec = m.group(1), m.group(2), m.group(3), int(m.group(4))
            target = self.chapter_table_maps.get(sec, {}).get(num) or self.table_map.get(num)
            if target:
                count += 1
                return f"Tabel {target} {prep} {word} {sec}"
            unresolved.append(f"Tabel {num} (seksi {sec})")
            return m.group(0)

        t = re.sub(r"\bTabel\s+(\d+)\s+(di|pada)\s+([Ss]eksi)\s+(\d+)", cross, t)

        def tbl(m: re.Match) -> str:
            nonlocal count
            num = m.group(1)
            target = self.table_map.get(num)
            if target:
                count += 1
                return f"Tabel {target}"
            unresolved.append(f"Tabel {num}")
            return m.group(0)

        t = re.sub(r"(?<![\w.])Tabel\s+(\d+)(?!\.?\d)", tbl, t)

        def fig(m: re.Match) -> str:
            nonlocal count
            kind, num = m.group(1), m.group(2)
            target = self.fig_heading_map.get(num)
            if target:
                count += 1
                return f"Gambar {target}"
            unresolved.append(f"{kind} {num}")
            return m.group(0)

        t = re.sub(r"(?<![\w.])(Gambar|Diagram)\s+(\d+)(?!\.?\d)", fig, t)

        def unstash(m: re.Match) -> str:
            return blocks[int(m.group(1))]

        for _ in range(20):
            nxt = re.sub(r"\x00CB(\d+)\x00", unstash, t)
            if nxt == t:
                break
            t = nxt

        self.stats["ref"] += count
        for u in unresolved:
            self.warnings.append(f"{source}: referensi tak-terpetakan -> {u}")
        return t

def render_md_file(renderer: Renderer, path: Path) -> str:
    return renderer.render_file(path)


# ---------- bagian depan ----------


def title_page_html(jilid_title: str) -> str:
    return f"""
<section class="title-page" data-od-id="halaman-judul">
  <div class="title-mark">{BOOK_ICON_SVG}<span>Edisi {BOOK_EDITION}</span></div>
  <div class="title-main">
    <h1>{esc(BOOK_TITLE)}</h1>
    <p class="title-sub">{esc(BOOK_SUBTITLE)}<br>{esc(BOOK_TAGLINE)}</p>
    <hr class="title-rule">
    <p class="title-meta">
      {esc(BOOK_AUTHOR)}<br>
      {esc(jilid_title)}
    </p>
    <p class="title-meta slogan">&ldquo;{esc(BOOK_SLOGAN)}&rdquo;</p>
  </div>
  <div class="title-foot">
    Trim UNESCO 155 &times; 230 mm &middot; &copy; {BOOK_EDITION} {esc(BOOK_AUTHOR)}<br>
    {esc(BOOK_REPO)}
  </div>
</section>"""


def copyright_page_html() -> str:
    return f"""
<section class="frontmatter copyright-block" data-od-id="halaman-kredit">
  <p><strong>{esc(BOOK_TITLE)} &mdash; {esc(BOOK_SUBTITLE)}</strong><br>
  {esc(BOOK_TAGLINE)}</p>
  <p>Edisi {BOOK_EDITION}<br>
  Penyunting: Bagaskoro Saputro (Project Leader) dan tim penulis bab<br>
  &copy; {BOOK_EDITION} {esc(BOOK_AUTHOR)}. Buku kolaborasi open-source.</p>
  <p>Repo: <a href="https://github.com/bagaswap111/buku-kolaborasi-llm">{esc(BOOK_REPO)}</a><br>
  Slogan: &ldquo;{esc(BOOK_SLOGAN)}&rdquo;</p>
  <p>Konten bab ditulis dalam Bahasa Indonesia. Layout cetak mengikuti kontrak
  desain internal (trim UNESCO 155 &times; 230 mm, margin dalam 20 mm).</p>
</section>"""


def toc_html(book: dict, jilid: dict, include_beranda: bool) -> str:
    items = []
    if include_beranda and book.get("beranda"):
        items.append('<li><a href="#tentang-buku">Tentang Buku Ini</a></li>')
    if jilid.get("overview"):
        items.append(
            f'<li><a href="#overview-{slugify(jilid["title"])[:20]}">Overview {esc(jilid["title"].split("—")[0].strip())}</a></li>'
        )
    for ch in jilid["chapters"]:
        items.append(
            f'<li class="toc-chapter"><a href="#bab-{esc(ch["num"])}">'
            f'<span class="toc-num">{esc(ch["num"])}</span> {esc(ch["title"])}</a></li>'
        )
        for f in ch["files"]:
            m = re.search(r"sub-bab-(\d+)", f["path"])
            subn = m.group(1) if m else ""
            bab_m = re.search(r"bab-(\d+)", f["path"])
            babn = bab_m.group(1) if bab_m else ""
            num = f"{int(babn)}.{subn}" if babn and subn else ""
            title = f["title"]
            items.append(
                f'<li class="toc-sub"><a href="#subbab-{int(babn) if babn else 0}-{int(subn) if subn else 0}">'
                f"{esc(title)}</a></li>"
            )
    return (
        '<nav class="toc" data-od-id="daftar-isi"><h1>Daftar Isi</h1>'
        f'<ul class="toc-list">{"".join(items)}</ul></nav>'
    )


def divider_html(jilid_title: str, ch: dict, subs: list[dict]) -> str:
    num = esc(ch["num"])
    eyebrow = esc(jilid_title.split("—")[0].strip())
    lis = []
    for s in subs:
        lis.append(f'<li><span class="num">{esc(s["num"])}</span>{esc(s["title"])}</li>')
    return f"""
<section class="chapter-divider" id="bab-{num}" data-od-id="bab-{num}">
  <p class="divider-eyebrow">{eyebrow}</p>
  <span class="opener-num">{num}</span>
  <h1>{esc(ch["title"])}</h1>
  <hr class="divider-rule">
  <ul class="divider-toc">{''.join(lis)}</ul>
</section>"""


# ---------- pembungkus HTML ----------

BOOT_JS = """
(function () {
  var loader = document.getElementById('od-loader');
  var finished = false;
  var pagedStarted = false;
  function finish() {
    if (finished) return;
    finished = true;
    if (loader) {
      loader.classList.add('od-hidden');
      setTimeout(function () { if (loader.parentNode) loader.parentNode.removeChild(loader); }, 400);
    }
    if (window.__odPagedRendered) {
      document.documentElement.classList.remove('od-flow');
    }
  }
  window.PagedConfig = window.PagedConfig || {};
  window.PagedConfig.auto = false;
  var prevAfter = window.PagedConfig.after;
  window.PagedConfig.after = function (flow) {
    window.__odPagedRendered = true;
    if (typeof prevAfter === 'function') { try { prevAfter(flow); } catch (e) {} }
    finish();
  };

  function fallbackMermaid() {
    var nodes = document.querySelectorAll('.mermaid');
    for (var i = 0; i < nodes.length; i++) {
      var pre = document.createElement('pre');
      pre.className = 'mermaid-fallback';
      pre.textContent = '[Diagram tidak dapat dirender - sumber teks:]\\n' + nodes[i].textContent;
      nodes[i].parentNode.replaceChild(pre, nodes[i]);
    }
  }

  function renderMermaid() {
    var nodes = Array.prototype.slice.call(document.querySelectorAll('.mermaid'));
    if (!nodes.length || !window.mermaid) return Promise.resolve();
    try {
      mermaid.initialize({
        startOnLoad: false,
        theme: 'base',
        securityLevel: 'loose',
        fontFamily: 'Inter, Helvetica, sans-serif',
        themeVariables: {
          primaryColor: '#F4F4F8',
          primaryTextColor: '#1A1A2E',
          primaryBorderColor: '#4F46E5',
          lineColor: '#4A4A5A',
          secondaryColor: '#FFFFFF',
          tertiaryColor: '#F4F4F8',
          background: '#FFFFFF',
          mainBkg: '#F4F4F8',
          nodeBorder: '#4F46E5',
          clusterBkg: '#FAFAFC',
          clusterBorder: '#D8D8E0',
          titleColor: '#1A1A2E',
          edgeLabelBackground: '#F4F4F8',
          fontSize: '13px'
        }
      });
    } catch (e) {}
    var chain = Promise.resolve();
    nodes.forEach(function (node) {
      chain = chain.then(function () {
        try {
          if (mermaid.run) {
            return mermaid.run({ nodes: [node] }).catch(function () {
              var pre = document.createElement('pre');
              pre.className = 'mermaid-fallback';
              pre.textContent = '[Diagram gagal dirender - sumber teks:]\\n' + node.textContent;
              if (node.parentNode) node.parentNode.replaceChild(pre, node);
            });
          }
          return new Promise(function (resolve) {
            try { mermaid.init(undefined, node, function () { resolve(); }); }
            catch (e) {
              var pre = document.createElement('pre');
              pre.className = 'mermaid-fallback';
              pre.textContent = '[Diagram gagal dirender - sumber teks:]\\n' + node.textContent;
              if (node.parentNode) node.parentNode.replaceChild(pre, node);
              resolve();
            }
          });
        } catch (e) {
          var pre = document.createElement('pre');
          pre.className = 'mermaid-fallback';
          pre.textContent = '[Diagram gagal dirender - sumber teks:]\\n' + node.textContent;
          if (node.parentNode) node.parentNode.replaceChild(pre, node);
        }
      });
    });
    return chain;
  }

  function waitForImages() {
    var imgs = Array.prototype.slice.call(document.images || []);
    return Promise.all(imgs.map(function (img) {
      if (img.complete) return Promise.resolve();
      return new Promise(function (resolve) {
        img.addEventListener('load', resolve, { once: true });
        img.addEventListener('error', resolve, { once: true });
      });
    }));
  }

  function startPaged() {
    var s = document.createElement('script');
    s.src = '../assets/paged.polyfill.js';
    s.onload = function () {
      pagedStarted = true;
      try {
        if (window.Paged && Paged.PagedHtml) {
          var result = new Paged.PagedHtml().render();
          if (result && typeof result.then === 'function') {
            result.catch(function () { finish(); });
          }
          setTimeout(finish, 120000);
        } else {
          finish();
        }
      } catch (e) {
        finish();
      }
    };
    s.onerror = function () { finish(); };
    document.head.appendChild(s);
  }

  var ready = renderMermaid();
  if (document.fonts && document.fonts.ready) {
    ready = ready.then(function () { return document.fonts.ready; });
  }
  ready = ready.then(waitForImages);
  ready = ready.then(function () {
    if (loader && loader.parentNode && !(window.Paged && Paged.PagedHtml)) {
      /* loader dilepas sebelum Paged mengekstrak konten */
    }
    if (loader && loader.parentNode) {
      loader.parentNode.removeChild(loader);
      loader = null;
    }
    startPaged();
  });
  ready.catch(function () { fallbackMermaid(); if (loader && loader.parentNode) loader.parentNode.removeChild(loader); startPaged(); });
  setTimeout(finish, 240000);
})();
"""

LOADER_HTML = """
<div id="od-loader" role="status" aria-live="polite">
  <div class="od-spinner" aria-hidden="true"></div>
  <div class="od-loader-title">Menyiapkan buku cetak</div>
  <div class="od-loader-sub">Merender diagram dan mengatur halaman. Tunggu hingga selesai sebelum mencetak (Ctrl+P).</div>
</div>"""


def wrap_html(title: str, body: str, css: str, od_id: str) -> str:
    return f"""<!doctype html>
<html lang="id">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(title)}</title>
<style>
{css}
</style>
</head>
<body>
{LOADER_HTML}
<main class="book" data-od-id="{esc(od_id)}">
{body}
</main>
<script src="../assets/mermaid.min.js"></script>
<script>
{BOOT_JS}
</script>
</body>
</html>
"""


def load_css() -> str:
    css = (HERE / "book.css").read_text(encoding="utf-8")
    imp = '@import url("assets/fonts/fonts-face.css");'
    faces = HERE / "assets" / "fonts" / "fonts-face.css"
    if imp in css and faces.is_file():
        css = css.replace(imp, faces.read_text(encoding="utf-8"))
    css = css.replace('url("assets/', 'url("../assets/').replace("url('assets/", "url('../assets/")
    return css


# ---------- perakitan ----------


def ensure_assets(konten: Path) -> None:
    assets = HERE / "assets"
    assets.mkdir(parents=True, exist_ok=True)
    (assets / "fonts").mkdir(exist_ok=True)
    src_mermaid = konten / "assets" / "javascripts" / "mermaid.min.js"
    dst_mermaid = assets / "mermaid.min.js"
    if src_mermaid.is_file() and not dst_mermaid.is_file():
        shutil.copy2(src_mermaid, dst_mermaid)
    src_images = konten / "assets" / "images"
    dst_images = assets / "images"
    if src_images.is_dir():
        shutil.copytree(src_images, dst_images, dirs_exist_ok=True)


def build_jilid(book: dict, jilid: dict, konten: Path, css: str, include_beranda: bool) -> tuple[str, Renderer]:
    renderer = Renderer(konten, HERE / "assets" / "images", jilid.get("_name", ""))
    parts: list[str] = [title_page_html(jilid["title"]), copyright_page_html()]
    parts.append(toc_html(book, jilid, include_beranda))

    if include_beranda and book.get("beranda"):
        p = konten / book["beranda"]
        if p.is_file():
            renderer.new_file_state(None, None, "tentang")
            parts.append(f'<section class="front-section" data-od-id="tentang-buku" id="tentang-buku">'
                         f"{renderer.render_file(p)}</section>")

    if jilid.get("overview"):
        p = konten / jilid["overview"]
        if p.is_file():
            oid = f"overview-{slugify(jilid['title'])[:20]}"
            renderer.new_file_state(None, None, oid)
            parts.append(f'<section class="front-section" data-od-id="{oid}" id="{oid}">'
                         f"{renderer.render_file(p)}</section>")

    for ch in jilid["chapters"]:
        bab_m = re.match(r"(\d+)", ch["num"])
        bab = int(bab_m.group(1)) if bab_m else None
        subs = []
        for f in ch["files"]:
            sm = re.search(r"sub-bab-(\d+)", f["path"])
            fm = re.search(r"bab-(\d+)", f["path"])
            subn = int(sm.group(1)) if sm else 0
            babn = int(fm.group(1)) if fm else (bab or 0)
            num = f"{babn}.{subn}"
            title = re.sub(r"^(Bab\s+)?\d+(?:\.\d+)*\s*:?\s*", "", f["title"], flags=re.I) or f["title"]
            subs.append({"num": num, "title": title})
        parts.append(divider_html(jilid["title"], ch, subs))

        # prescan peta nomor Tabel seluruh bab (untuk label + referensi silang)
        renderer.chapter_table_maps = {}
        seq = 0
        for f in ch["files"]:
            p = konten / f["path"]
            if not p.is_file():
                continue
            sm = re.search(r"sub-bab-(\d+)", f["path"])
            subn = int(sm.group(1)) if sm else 0
            lines = p.read_text(encoding="utf-8").splitlines()
            file_map: dict[str, str] = {}
            in_fence = False
            for line in lines:
                s = line.strip()
                if FENCE_RE.match(s):
                    in_fence = not in_fence
                    continue
                if in_fence:
                    continue
                hm = TABLE_HEAD_RE.match(s)
                if hm:
                    seq += 1
                    file_map[hm.group(1)] = f"{bab}.{seq}" if bab else str(seq)
            renderer.chapter_table_maps[subn] = file_map

        for f, meta in zip(ch["files"], subs):
            p = konten / f["path"]
            if not p.is_file():
                continue
            sm = re.search(r"sub-bab-(\d+)", f["path"])
            fm = re.search(r"bab-(\d+)", f["path"])
            subn = int(sm.group(1)) if sm else 0
            babn = int(fm.group(1)) if fm else (bab or 0)
            idp = f"subbab-{babn}-{subn}"
            renderer.new_file_state(babn, subn, idp)
            renderer.table_map = renderer.chapter_table_maps.get(subn, {})
            inner = renderer.render_file(p)
            inner = renderer.renumber_prose(inner, f["path"])
            parts.append(
                f'<section class="subbab" id="{idp}" data-od-id="{idp}">{inner}</section>'
            )

    body = "\n".join(parts)
    jilid_num = "1" if "Jilid 1" in jilid["title"] else "2"
    title = f"{BOOK_TITLE} - Jilid {jilid_num}"
    return wrap_html(title, body, css, f"buku-jilid-{jilid_num}"), renderer


def main() -> int:
    ap = argparse.ArgumentParser(description="Build layout buku cetak HTML")
    ap.add_argument("--konten", help="path folder konten/")
    ap.add_argument("--only", choices=["jilid-1", "jilid-2"], help="build satu jilid saja")
    args = ap.parse_args()

    konten = find_konten(args.konten)
    mkdocs = konten.parent / "mkdocs.yml"
    if not mkdocs.is_file():
        sys.exit(f"ERROR: {mkdocs} tidak ditemukan (sumber urutan baca)")
    entries = parse_nav(mkdocs.read_text(encoding="utf-8"))
    if not entries:
        sys.exit("ERROR: nav kosong / gagal parse mkdocs.yml")

    book = build_book_structure(entries)
    extras = add_extras(book, konten)
    ensure_assets(konten)
    css = load_css()

    preview = HERE / "preview"
    preview.mkdir(exist_ok=True)

    # nama jilid internal untuk pencocokan link
    targets = [args.only] if args.only else ["jilid-1", "jilid-2"]
    ok = True
    for idx, jilid in enumerate(book["jilid"], start=1):
        name = f"jilid-{idx}"
        if name not in targets:
            continue
        jilid["_name"] = name
        include_beranda = name == "jilid-1"
        html_out, renderer = build_jilid(book, jilid, konten, css, include_beranda)
        out_path = preview / f"{name}.html"
        out_path.write_text(html_out, encoding="utf-8")

        # scan sisa markup emphasis (typo konten: bintang tak-pasangan)
        scan = re.sub(r"(?s)<pre[^>]*>.*?</pre>", " ", html_out)
        scan = re.sub(r"<code>[^<]*</code>", " ", scan)
        scan = re.sub(r"<t[dh][^>]*>\*+</t[dh]>", " ", scan)
        scan = re.sub(r"\{\{query\}\}", " ", scan)
        for m in re.finditer(r"(?<!\*)\*\*(?!\*)", scan):
            ctx = re.sub(r"\s+", " ", scan[max(0, m.start() - 60) : m.end() + 60])
            renderer.warnings.append(f"{name}: sisa '**' (typo konten?) -> ...{ctx}...")
        for m in re.finditer(r"<strong>[^<]*\*[^<]*</strong>", scan):
            renderer.warnings.append(
                f"{name}: strong mengandung '*' (typo konten?) -> {m.group(0)[:90]}"
            )

        size = out_path.stat().st_size
        print(
            f"OK: {out_path.relative_to(HERE.parent)} "
            f"({size // 1024} KB | tabel +{renderer.stats['tabel']} | "
            f"gambar +{renderer.stats['gambar']} | mermaid {renderer.stats['mermaid']} | "
            f"ref +{renderer.stats['ref']} | "
            f"img ok {renderer.stats['img_ok']} | img hilang {renderer.stats['img_missing']})"
        )
        if renderer.missing_images:
            ok = False
            for mi in renderer.missing_images:
                print(f"  GAMBAR TIDAK ADA: {mi}")
        if renderer.warnings:
            cap = 25
            for w in renderer.warnings[:cap]:
                print(f"  WARN: {w}")
            if len(renderer.warnings) > cap:
                print(f"  WARN: ... +{len(renderer.warnings) - cap} peringatan lain")

    if extras:
        print(f"INFO: {len(extras)} sub-bab di luar manifest ikut disertakan:")
        for e in extras:
            print(f"  + {e}")
    print("Selesai." if ok else "Selesai DENGAN gambar yang tidak ditemukan (lihat di atas).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
