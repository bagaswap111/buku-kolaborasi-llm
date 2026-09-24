# OPENDESIGN.md — Brief: Layout Buku Cetak

> **Entry point untuk OpenDesign / coding agent.** Baca file ini + `DESIGN.md` sebelum membuat layout.
> Sumber kebenaran urutan baca: `print/manifest.md` (di-generate dari `mkdocs.yml` — jangan tebak urutan).

---

## 1. Misi

Ubah seluruh konten Markdown di `konten/` menjadi **layout buku cetak siap ekspor PDF** menggunakan OpenDesign (artifact tipe **Document**), dengan gaya yang dikontrak oleh `DESIGN.md`.

- **Bahasa konten:** Indonesia — jangan terjemahkan, jangan sunting substansi.
- **Scope:** 2 jilid, 10 bab, ±93 file sub-bab + 2 overview + 1 beranda.
- **Output akhir:** PDF per jilid di `print/` (default), atau 1 PDF gabungan bila diminta.

## 2. Peta file

| Peran | Path | Keterangan |
|:---|:---|:---|
| Kontrak desain | `DESIGN.md` | Wajib dibaca; spesifikasi cetak, tipografi, komponen |
| Brief ini | `OPENDESIGN.md` | Aturan main layout & ekspor |
| Urutan baca | `print/manifest.md` | Daftar file terurut + judul; regenerate dengan `python print/generate_manifest.py` |
| Konten | `konten/jilid-{1,2}/bab-XX-*/sub-bab-N.md` | Sumber satu-satunya teks |
| Gambar | `konten/assets/images/<folder-bab>/sub-bab-N/*.png` | Path relatif dari file konten: `../../assets/images/...` |
| Gaya tulisan (referensi) | `templates/writing-protocol.md` | Makna struktur seksi, format caption "Tabel N"/"Gambar N" |
| Nav web (sekunder) | `mkdocs.yml` | Sumber manifest; jangan dipakai langsung untuk order cetak |

## 3. Aturan layout (WAJIB)

1. **Konten immutable.** Semua teks, angka, tabel, dan referensi dari `konten/` ditampilkan utuh. Anda hanya boleh: memformat ulang, memecah halaman, merender ulang media, dan menomori ulang Tabel/Gambar per bab.
2. **Ikuti `DESIGN.md`** untuk ukuran trim, margin, font, spacing, komponen, dan anti-patterns. Tidak ada keputusan visual di luar file itu kecuali diminta brief turunan.
3. **Urutan baca persis `print/manifest.md`:** Beranda → Overview Jilid 1 → Bab 01–04 (sub-bab 1..n) → Overview Jilid 2 → Bab 05–10 → referensi global (opsional).
4. **Mermaid → gambar.** Setiap blok ```mermaid wajib dirender ke SVG/PNG (pakai mermaid-cli / `mmdc`, atau HTML→screenshot) dan disimpan di `konten/assets/images/<folder>/sub-bab-N/` sebelum masuk layout. Blok mentah dilarang tampil di PDF.
5. **Gambar PNG** dari `konten/assets/images/` dipakai apa adanya; embed dengan path relatif yang benar; pertahankan rasio asli; ≥150 dpi cetak.
6. **Caption & penomoran:**
   - Pertahankan pola asli: `### Tabel N:` sebelum tabel, `### Gambar N:` / `Gambar X.N-i` untuk gambar.
   - Setelah digabung jadi buku: renumber per bab → `Tabel 4.2`, `Gambar 4.2-1` dst. (ikuti numbering gaya buku).
7. **Admonition** (`> **Catatan:**`, `!!!`, `<details>`) dirender statis terbuka; emoji di header → label teks.
8. **Tabel lebar:** jika melebihi measure (lebar kolom ±120 mm pada trim UNESCO), turunkan font tabel (min 7.5 pt), rotasi halaman untuk tabel ekstra lebar, atau pecah — jangan overflow margin.
9. **Referensi tetap per sub-bab** di akhir file masing-masing; jangan digabung jadi satu daftar kecuali diminta.
10. **Halaman baru per bab** (chapter opener sesuai `DESIGN.md` §5); seksi mengalir dengan break rules (hindari orphan heading).

## 4. Spesifikasi ekspor

| Item | Default |
|:---|:---|
| Page size | **UNESCO 155 × 230 mm** (portrait) — lihat `DESIGN.md` §4 untuk margin/grid |
| Format | PDF (print-ready, margins sesuai `DESIGN.md`) |
| Granularitas | 1 PDF per jilid: `print/local-llm-bible-jilid-1.pdf`, `print/local-llm-bible-jilid-2.pdf` |
| Alternatif | 1 PDF gabungan: `print/local-llm-bible-full.pdf` |
| HTML preview | `print/preview/*.html` (boleh di-commit; export PDF juga) |
| Metadata PDF | Judul = "The Local LLM Bible", Author = "Bagaskoro Saputro dkk.", © 2026 |
| Color mode | RGB (default) — konversi CMYK dilakukan prepress terpisah |

## 5. Cara menjalankan (OpenDesign)

OpenDesign lokal belum tentu terpasang di mesin ini. Pilih salah satu:

**A. Lewat coding agent (disarankan — OpenDesign mendukung OpenCode):**
```bash
# sekali saja, setelah od CLI / desktop app terpasang: https://open-design.ai
od mcp install opencode
```
Lalu di sesi agent: *"Buat layout buku cetak dari repo ini sesuai OPENDESIGN.md dan DESIGN.md, ekspor PDF per jilid ke print/."*

**B. Lewat desktop app:** buka repo ini sebagai working directory Studio → artifact type **Document** → tempel brief ringkas: `Baca OPENDESIGN.md dan DESIGN.md, layout konten/ urut print/manifest.md menjadi PDF cetak per jilid di print/.`

**C. Tanpa OpenDesign:** layout bisa dikerjakan agent biasa ke HTML/CSS print (`print/preview/`) lalu print-to-PDF — kontrak visual tetap `DESIGN.md`.

## 6. Checklist sebelum serah terima

- [ ] Semua file di `print/manifest.md` masuk layout, tidak ada bab terlewat.
- [ ] Tidak ada blok ```mermaid mentah di PDF.
- [ ] Semua embed gambar menunjuk file PNG yang ada (tidak broken).
- [ ] Nomor Tabel/Gambar berurutan per bab; tidak ada label "TBD/...".
- [ ] Tidak ada teks yang terpotong/overflow margin; heading tidak yatim.
- [ ] PDF bisa dibuka, jumlah halaman wajar (target: ±20–35 halaman/bab).
- [ ] Metadata PDF terisi.
