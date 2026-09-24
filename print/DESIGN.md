# DESIGN.md — The Local LLM Bible (Edisi Cetak)

> Kontrak desain untuk OpenDesign. Setiap artefak layout buku cetak/PDF **wajib** membaca file ini.
> Skema 9 section mengikuti standar `DESIGN.md` OpenDesign.
> Ubah nilai di sini jika spesifikasi cetak berubah — jangan hard-code di template.

---

## 1. Color

Palet cetak hemat warna (indigo/teal mengikuti tema MkDocs buku ini). Untuk prepress CMYK, konversikan di tahap akhir — nilai HEX adalah sumber kebenaran layout.

| Token | HEX | Pemakaian |
|:---|:---:|:---|
| `--color-ink` | `#1A1A2E` | Teks utama, heading H1–H3 |
| `--color-ink-muted` | `#4A4A5A` | Teks sekunder, caption, nomor halaman |
| `--color-primary` | `#4F46E5` | Aksen utama: nomor bab, link, garis chapter opener |
| `--color-accent` | `#0D9488` | Aksen sekunder: label "Tabel N"/"Gambar N", callout |
| `--color-surface` | `#F4F4F8` | Latar blok kode, baris tabel bergaris-seling |
| `--color-border` | `#D8D8E0` | Garis tabel, garis pemisah header/footer |
| `--color-bg` | `#FFFFFF` | Latar halaman (putih) |
| `--color-warn-bg` | `#FEF3C7` | Latar admonition/warning (opsional, 1 warna) |
| `--color-warn-border` | `#D97706` | Border admonition/warning |

Aturan:
- Diagram/grafik boleh grayscale-friendly: gunakan `--color-primary` + `--color-accent` + abu-abu, JANGAN mengandalkan warna merah-hijau saja untuk membedakan seri data.
- Blok kode di cetak: teks `--color-ink` di atas `--color-surface`, TANPA syntax color (hemat tinta); bila proses digital-print boleh syntax highlight redup (opacity 70%).

---

## 2. Typography

| Peran | Font stack | Ukuran | Line height | Berat |
|:---|:---|:---:|:---:|:---:|
| Body | `"Source Serif 4", "Charter", "Georgia", serif` | 10.5 pt | 1.5 | 400 |
| Heading H1 (Bab) | `"Inter", "Helvetica Neue", sans-serif` | 24 pt | 1.2 | 700 |
| Heading H2 (seksi) | `"Inter", sans-serif` | 15 pt | 1.3 | 650 |
| Heading H3 (sub-judul) | `"Inter", sans-serif` | 12 pt | 1.35 | 600 |
| Caption (Tabel/Gambar) | `"Inter", sans-serif` | 8.5 pt | 1.35 | 500 |
| Code / terminal | `"JetBrains Mono", "IBM Plex Mono", monospace` | 8.5 pt | 1.45 | 400 |
| Nomor halaman / running head | `"Inter", sans-serif` | 8 pt | — | 500 |
| Referensi / sitasi | body stack | 9 pt | 1.4 | 400 |

Aturan:
- Body full **justified** dengan *hyphenation* aktif (bahasa Indonesia), `text-wrap: pretty` untuk heading.
- Istilah asing *italic* (mis. *inference*, *throughput*); istilah kunci **bold** — format dari konten sudah final, jangan diubah.
- Angka di tabel: font tabular-nums, kolom angka rata kanan (`:---:`).
- Monospace maksimal 8.5 pt; jangan menyusutkan body untuk memuat kode — pindahkan blok panjang ke halaman penuh/allow break.

---

## 3. Spacing

| Token | Nilai | Pemakaian |
|:---|:---:|:---|
| `--space-xs` | 4 pt | Jarak dalam caption & label |
| `--space-sm` | 8 pt | Antara paragraf & media |
| `--space-md` | 12 pt | Antar blok kode / tabel |
| `--space-lg` | 24 pt | Antara seksi (`##`) |
| `--space-xl` | 48 pt | Sebelum chapter opener |
| `--space-xxl` | 72 pt | Halaman baru per bab (flush) |

Aturan:
- Spasi vertikal konsisten: 8 pt body rhythm, kecuali aturan `--space-*` di atas.
- Tabel & gambar: `--space-sm` di atas, `--space-md` di bawah (ruang untuk analisis lanjutan).
- Jangan menumpuk >3 elemen media tanpa paragraf penghubung.

---

## 4. Layout

Spesifikasi cetak (default — ubah di sini bila ganti ukuran trim):

| Parameter | Nilai |
|:---|:---|
| Trim size | **UNESCO 155 × 230 mm** (portrait) — standar ukuran buku UNESCO (GMMP/SNV) |
| Margin dalam (gutter/binding) | 20 mm |
| Margin luar (fore-edge) | 15 mm |
| Margin atas | 18 mm |
| Margin bawah | 20 mm |
| Kolom | 1 kolom teks (full measure ± 120 mm) |
| Grid baseline | 12 pt |
| Bleed | 3 mm (khusus gambar yang menyentuh tepi; default: tanpa bleed) |
| Nomor halaman | Bawah tengah; bab genap/ganjil: running head kiri/kanan (nama bab · nama buku) |

Struktur halaman (urutan):
1. Halaman judul (title page) — judul, subjudul, edisi, tahun
2. Halaman kredit/copyright & daftar isi (TOC)
3. **Jilid 1** — Bab 01–04
4. **Jilid 2** — Bab 05–10
5. Sumber & koleksi referensi global (opsional)

Elemen yang boleh full-width: tabel lebar, gambar, blok kode panjang. Heading tidak boleh jadi *orphan* (sisipkan minimal 2 baris teks setelah heading di halaman yang sama).

---

## 5. Components

| Komponen | Spesifikasi cetak |
|:---|:---|
| **Chapter opener** | Halaman ganjil baru; nomor bab besar (`--color-primary`, 48 pt), judul bab (H1), garis horizontal 2 pt `--color-primary`, ringkasan bab 2–3 kalimat italic |
| **Section heading (H2)** | `--color-ink`, spasi `--space-lg` di atas; boleh diberi nomor "X.Y" sesuai konten |
| **Tabel** | Header: bg `--color-surface`, teks bold; garis horizontal saja (tanpa garis vertikal); baris bergaris-seling opsional `#FAFAFC`; label "### Tabel N: …" jadi caption di ATAS tabel, analisis tetap di bawah |
| **Gambar/diagram** | Caption "Gambar N" / "Gambar X.N-i" di BAWAH gambar, 8.5 pt, `--color-ink-muted`; gambar maks 100% measure; PNG dari `konten/assets/images/` dipertahankan resolusi asli (≥150 dpi cetak, ideal ≥300 dpi) |
| **Mermaid** | TIDAK dirender langsung — ekspor dulu ke SVG/PNG, lalu perlakukan sebagai gambar biasa (lihat anti-patterns) |
| **Blok kode** | Radius 0–2 pt, padding 8 pt, bg `--color-surface`, border kiri 2 pt `--color-accent` |
| **Admonition / callout** | Kotak: bg `--color-warn-bg`, border kiri 3 pt `--color-warn-border`, label bold; jangan pakai emoji sebagai ikon — ganti dengan teks "Catatan"/"Peringatan" |
| **Referensi** | Daftar bernomor `[1]`, hanging indent 12 pt, 9 pt; tetap per sub-bab seperti sumbernya |
| **Nomor Tabel/Gambar** | "Tabel 1, 2, …" dan "Gambar 1, 2, …" per file sub-bab; saat digabung jadi 1 buku, renumber per bab ("Tabel 4.2") |
| **Link** | Cetak: URL ditulis lengkap di referensi; inline link cukup teks biasa (tanpa underline), warna `--color-primary` |

---

## 6. Motion

**Tidak berlaku untuk cetak/PDF statis.** Semua animasi web (toggle admonition, tab, hover) diabaikan; `admonition`/`details` dirender dalam kondisi terbuka sebagai kotak statis. Bila kelak ada edisi digital interaktif, kembalikan section ini.

---

## 7. Voice

- Bahasa Indonesia teknis-komunikatif; istilah asing dipertahankan dengan *italic*.
- Nada: panduan praktis yang tajam — bukan buku teks kaku, bukan blog kasual.
- Judul seksi: judul kasus kalimat, tanpa emoji (emoji di header web ditransformasi jadi label teks saat layout cetak).
- Konsistensi istilah mengikuti `templates/writing-protocol.md` (mis. "sub-bab" bukan "subbab", "kuantisasi" untuk *quantization*).
- Epigraf pembuka sub-bab dipertahankan sebagai *pull quote* italic setelah chapter opener/seksi awal.

---

## 8. Brand

| Atriben | Nilai |
|:---|:---|
| Judul buku | **The Local LLM Bible — Strategic Guide to Private AI** |
| Judul lokal | Buku Kolaborasi LLM |
| Sub-judul | Panduan Komprehensif Ekosistem LLM Lokal |
| Edisi | 2026 |
| Penulis/Penyunting | Bagaskoro Saputro (Project Leader) + tim penulis bab |
| Repo | https://github.com/bagaswap111/buku-kolaborasi-llm |
| Logo/ikon | Ikon buku (fontawesome/solid/book) — monokrom `--color-primary`, pojok kiri atas halaman judul |
| Slogan (opsional) | "AI lokal, data Anda, infrastruktur di tangan Anda." |

Identitas visual: tipografi editorial (serif body + sans heading), aksen indigo/teal, tanpa ilustrasi dekoratif — teknis dan bersih.

---

## 9. Anti-patterns

DILARANG dalam layout cetak:

1. **Mermaid code block tampil sebagai teks mentah** di PDF — wajib dirender ke gambar dulu.
2. **Mengubah isi teks/angka** konten `konten/` — layout hanya memformat, tidak menyunting substansi.
3. **Tabel terpotong** keluar margin — pecah tabel atau gunakan font lebih kecil untuk tabel, jangan overflow.
4. **Heading yatim (orphan)** tanpa 2 baris isi di halaman yang sama.
5. **Grafik PNG diregangkan** melebihi rasio aslinya; gambar blur (<150 dpi untuk cetak).
6. **Emoji sebagai ikon** di halaman cetak (ganti label teks).
7. **Syntax highlight terang-terangan** di blok kode (buang tinta, kurangi kontras cetak).
8. **Nomor Tabel/Gambar tidak berurutan** setelah penggabungan bab.
9. **Warna tunggal sebagai satu-satunya pembeda** informasi (burung-burung/bebek aman-warna).
10. **Halaman kosong tanpa alasan** atau konten "TBD/Lorem/..." yang tersisa dari template.
