#!/usr/bin/env python3
"""Generate print/manifest.md from mkdocs.yml nav (urutan baca buku cetak).

Usage: python print/generate_manifest.py
Stdlib only — tidak perlu PyYAML. Hanya mem-parse blok nav sederhana.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
MKDOCS = ROOT / "mkdocs.yml"
OUT = Path(__file__).resolve().parent / "manifest.md"

NAV_RE = re.compile(r"^nav:\s*$")
# - "quoted key": path.md   |  - unquoted: path.md  |  - "group":  (tanpa path)
ENTRY_RE = re.compile(r'^(\s*)-\s+(?:"([^"]+)"|([^:#]+?)):\s*(\S+\.md)\s*$')
GROUP_RE = re.compile(r'^(\s*)-\s+"([^"]+)":\s*$')
BARE_RE = re.compile(r"^(\s*)-\s+(.+?)\s*$")


def parse_nav(text: str) -> list[tuple[int, str, str | None]]:
    """Return list of (indent, title, path|None) terurut sesuai file."""
    lines = text.splitlines()
    in_nav = False
    nav_indent: int | None = None
    entries: list[tuple[int, str, str | None]] = []

    for line in lines:
        if not in_nav:
            if NAV_RE.match(line):
                in_nav = True
                nav_indent = None
            continue
        if not line.strip() or line.lstrip().startswith("#"):
            if entries:
                break
            continue
        if line.strip() == "---":
            break
        indent = len(line) - len(line.lstrip())
        if nav_indent is None:
            if indent == 0 and entries:
                break
            nav_indent = indent
        if indent < nav_indent:
            break

        m = ENTRY_RE.match(line)
        if m:
            title = (m.group(2) or m.group(3) or "").strip()
            entries.append((indent, title, m.group(4)))
            continue
        m = GROUP_RE.match(line)
        if m:
            entries.append((indent, m.group(2).strip(), None))
            continue
        m = BARE_RE.match(line)
        if m:
            entries.append((indent, m.group(2).strip().rstrip(":").strip('"'), None))

    return entries


def build_markdown(entries: list[tuple[int, str, str | None]]) -> str:
    base = min((i for i, _, p in entries if p), default=0)
    out = [
        "# Manifest Buku Cetak — Urutan Baca",
        "",
        "> **Dibuat otomatis** dari `nav:` di `mkdocs.yml` — jangan edit manual.",
        "> Regenerate: `python print/generate_manifest.py`",
        "",
        "Format: `judul` → `path` relatif terhadap folder `konten/`.",
        "",
    ]
    total = sum(1 for _, _, p in entries if p)
    for indent, title, path in entries:
        level = max(1, (indent - base) // 2 + 1)
        if path:
            out.append(f"{'  ' * (level - 1)}- **{title}** → `{path}`")
        else:
            out.append("")
            out.append(f"{'  ' * (level - 1)}- ## {title}")
    out += ["", f"**Total file:** {total}", ""]
    return "\n".join(out)


def main() -> int:
    if not MKDOCS.exists():
        print(f"ERROR: {MKDOCS} tidak ditemukan", file=sys.stderr)
        return 1
    entries = parse_nav(MKDOCS.read_text(encoding="utf-8"))
    files = [(t, p) for _, t, p in entries if p]
    if not files:
        print("ERROR: nav kosong / gagal parse", file=sys.stderr)
        return 1
    missing = [p for _, p in files if not (ROOT / "konten" / p).exists()]
    OUT.write_text(build_markdown(entries), encoding="utf-8")
    print(f"OK: {OUT.relative_to(ROOT)} ({len(files)} file)")
    if missing:
        print("WARNING: path tidak ada di konten/:")
        for p in missing:
            print(f"  - {p}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
