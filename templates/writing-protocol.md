# PROTOKOL PENULISAN KONTEN BUKU (WAJIB DIPATUHI SEMUA PENULIS/AGEN)

> Dokumen ini adalah **standar tunggal** untuk menulis file konten di `konten/`.
> Baca **seluruhnya** sebelum menulis. Setiap pelanggaran akan direvisi kembali.

---

## 1. PETA SUMBER

| Sumber | Lokasi | Fungsi |
|:---|:---|:---|
| Guideline wajib | `guidelines/guideline-jilid-{1,2}/guideline-bab-XX-*/guideline-sub-bab-N.md` | **Satu-satunya sumber kebenaran** konten: kerangka, tabel, diagram, tutorial, studi kasus, referensi |
| Acuan gaya | `konten/jilid-1/bab-01-model/sub-bab-1.md`, `sub-bab-2.md`, `sub-bab-3.md` | Contoh standar mutu: struktur naratif, kedalaman, dan format |
| Template | `templates/chapter-template.md`, `templates/table-style.md` | Format markdown, tabel, mermaid |
| Output | `konten/jilid-{1,2}/bab-XX-*/sub-bab-N.md` | File yang ditulis |

---

## 2. PERSYARATAN SEBELUM MENULIS (WAJIB)

1. **Baca guideline sub-bab** yang bersangkutan secara lengkap — jangan pernah menebak isi guideline.
2. **Baca minimal 1 file acuan gaya** (`konten/jilid-1/bab-01-model/sub-bab-1.md`) untuk meniru kedalaman, gaya bahasa, dan ritme naratifnya.
3. Jika terdapat data di guideline yang kurang lengkap, **lakukan web search untuk verifikasi** angka/model/dokumentasi terbaru (maksimal ±10 tahun, ideal 5 tahun terakhir). Catat sumbernya.
4. Semua angka, spesifikasi, dan klaim yang ditulis **harus dapat dipertanggungjawabkan** — bersumber dari guideline, dokumentasi resmi, paper (DOI/arXiv), atau hasil verifikasi web.
5. **Dilarang membuat angka asal-asalan.** Jika data tidak ditemukan, tulis deskripsi kualitatif + beri catatan "estimasi" dengan dasar pemikiran yang jelas.

---

## 3. STRUKTUR FILE KONTEN (WAJIB — 18 SEKSI MAKSIMAL, DIURUTKAN)

Setiap file konten mengikuti struktur berikut. Penomoran seksi **dimulai dari 1** dan berjalan berurutan tanpa lompatan:

```markdown
# Bab X.N: [Judul dari mkdocs.yml / guideline]

> [Epigraf/narasi pembuka 2-4 kalimat yang "mengajak masuk ke dunia topik" —
> bahasa menarik, tidak basi, menimbulkan rasa ingin tahu. 1 paragraf.]

---

## 1. Tujuan Sub-Bab
[Bullet list target kompetensi pembaca (4-6 poin) — TULIS ULANG dari guideline, perluas bahasanya.]

---

## 2. [Seksi teori pertama — judul sesuaikan topik]
### Sub-judul naratif A
### Sub-judul naratif B
[Panjang paragraf BEBAS — tidak ada batas maksimum. Aturan satu-satunya: setiap paragraf membawa informasi baru dan mengalir. Vary: paragraf pendek (1-2 kalimat) untuk efek/simpulan, paragraf panjang (5-8 kalimat) untuk pembahasan mendalam. Bahasa mengalir: analogi hidup → konsep → detail teknis → implikasi praktis.]

## 3. [Seksi teori berikutnya]
...
[Catatan: seksi teori boleh banyak (hingga 10), sesuaikan kerangka guideline. Namun PENOMORAN berurutan 2,3,4,...]

---

**ATURAN MEDIA INLINE (WAJIB):**
Tabel, diagram mermaid, dan gambar statis TIDAK BOLEH dikumpulkan di seksi akhir ("Tabel Wajib", "Diagram & Visualisasi"). Setiap media diletakkan INLINE, tepat di seksi teori yang membahasnya, dengan pola berikut:

```markdown
## 2. [Seksi teori — judul sesuaikan topik]

[Paragraf teori yang memunculkan kebutuhan data komparasi...]

### Tabel 1: [Judul tabel]
[1 kalimat narasi pengantar sebelum tabel — jelaskan apa yang dilihat pembaca.]

|[Header]|[Header]|[Header]|
|:---|:---:|:---|
|[data]|[data]|[data]|
[dst — SEMUA tabel wajib konsisten: header separator wajib ada, kolom selaras, tidak ada pipa terputus]

[1-2 paragraf analisis SETELAH tabel: bacakan insight penting, bukan mengulang isi tabel. Format "pro dan kontra", "kapan memilih A vs B", dst.]

[PNG statis yang memvisualkan tabel diletakkan langsung setelah analisis tabel tsb (lihat aturan Gambar Statik di bawah).]

### Gambar 1: [Judul diagram]
[1 kalimat narasi pengantar sebelum diagram.]

```mermaid
[gambar/flowchart/sequencediagram yang DIVERIFIKASI sintaksnya]
```

[Penjelasan gambar: apa yang dilihat, mengapa penting. Panjang bebas.]

## 3. [Seksi teori berikutnya]
...
```

**Aturan penempatan:**
- Tabel ditempatkan di seksi yang paling banyak membahas topik tabel tersebut (mis. tabel benchmark → seksi benchmark, bukan di akhir bab).
- Setiap seksi media diberi narasi pengantar 1 kalimat SEBELUM header `### Tabel N:` / `### Gambar N:`, dan analisis SETELAH media.
- Penomoran tabel/gambar berurutan sesuai urutan kemunculan di dokumen (Tabel 1, 2, 3...; Gambar 1, 2, 3...).
- Seksi `## Tujuan Sub-Bab` (no. 1) tidak boleh menerima media; media tidak boleh ditempatkan di seksi Praktikum/Studi Kasus/Referensi.
- DILARANG membuat seksi berjudul "Tabel Wajib", "Tabel Referensi", atau "Diagram & Visualisasi" sebagai penampung media di akhir bab.

**Aturan Mermaid:**
- Gunakan `graph TD`, `flowchart LR`, `sequenceDiagram`, `pie`, atau `graph LR` — sesederhana mungkin agar tidak rusak saat dirender.
- Id node pakai huruf/angka tanpa spasi: `A[Judul]`, `B[...]`; teks di dalam `[]`.
- Pastikan semua panah `-->` tersambung ke node yang ada; TIDAK BOLEH ada node yang didefinisikan tapi tidak direferensikan (atau sebaliknya) → akan gagal render.
- Setelah ditulis, lakukan pencermatan ulang sintaks baris per baris (agen penulis wajib memeriksa Mermaid sendiri sebelum menyimpan).

**Aturan Gambar Statik (WAJIB minimal 1 per file):**
- Setiap file konten WAJIB memiliki **minimal 1 gambar statis PNG** yang di-generate (matplotlib) dari data nyata tabel di file tersebut — bukan sekadar mermaid.
- Lokasi penyimpanan: `konten/assets/images/<nama-folder-bab>/sub-bab-N/<deskripsi>.png` (contoh: `konten/assets/images/bab-01-model/sub-bab-2/perbandingan-vram.png`).
- Embed dengan path relatif dari file konten ke `../../assets/images/...` (contoh dari `konten/jilid-1/bab-01-model/sub-bab-2.md` → `../../assets/images/bab-01-model/sub-bab-2/perbandingan-vram.png`).
- Format embed:
  ```markdown
  ![Judul Gambar](../../assets/images/<folder>/sub-bab-N/<file>.png)

  *Gambar X.N-i — keterangan singkat + insight 1-2 kalimat.*
  ```
- Gambar HANYA boleh memakai angka yang sudah ada di file (dari tabel/data guideline). JANGAN mengarang data baru hanya untuk grafik.
- Verifikasi: script matplotlib dijalankan sampai berhasil, file PNG ada (ukuran > 0), dan path relatif benar (file editor harus bisa menampilkan gambar di posisi embed).
- Gaya gambar: ikuti `templates/chart-style.md`.

---

## N+1. Praktikum / Hands-On
### Langkah 1: [Judul langkah]
[Penjelasan singkat sebelum perintah.]
```bash
# Perintah nyata — WAJIB dapat dijalankan, dengan komentar penjelasan
```

[Langkah 2 dst. Boleh berisi: instalasi, konfigurasi YAML/JSON, script Python, verifikasi, pengujian. Semua kode diberi label bahasa (bash, yaml, python, dockerfile, nginx, dll).]

## N+2. Studi Kasus: [Judul]
[1-2 paragraf latar skenario: siapa, di mana, apa masalahnya → analisis pilihan → langkah solusi → hasil & pelajaran. Gunakan runut cerita yang hidup, bukan draft teknis kering.]

---

## N+3. Referensi
### Paper Jurnal/Konferensi
[1] Author, A. (Tahun). *Judul*. Venue. DOI: [10.xxx](url) — [SOP: minimal 5 paper 5-10 tahun terakhir, langsung dari guideline]
[[2] ... [dst]
### Referensi Pendukung (Dokumentasi/Repository)
[dst]
```

---

## 4. ATURAN KUALITAS NARATIF (PENTING)

1. **Alur baca seperti sedang diajak bertualang** — mulai dari *mengapa topik ini penting bagi pembaca* → konsep → detail → perbandingan → praktik → studi kasus → referensi. Setiap transisi ada "jembatan" kalimat.
2. **Gaya bahasa**: bahasa Indonesia teknis tetapi komunikatif; istilah asing tetap disertakan dengan *italic* (mis. *inference*, *throughput*, *quantization*); gunakan **bold** untuk istilah kunci.
3. **Kedalaman**: target **350-450+ baris per file**. TIDAK ada batasan jumlah paragraf per seksi — yang dilarang adalah seksi kering 1 kalimat tanpa substansi dan paragraf berulang. Variasikan ritme: paragraf pembuka pendek yang "menangkap", pembahasan inti yang panjang dan mendalam, satu kalimat penekanan untuk menutup.
4. **Analogi hidup**: gunakan analogi sehari-hari (dapur, lalu lintas, perpustakaan, orkestra) untuk menjelaskan konsep teknis — tetapi tetap akurat secara teknis.
5. **Tidak ada *filler***: setiap paragraf membawa informasi baru; tidak ada paragraf berulang atau basa-basi.
6. **Netral & objektif**: sebutkan kelebihan DAN kekurangan setiap teknologi; gunakan data aktual (token/s, GB, harga IDR, skor benchmark) bukan kata sifat kosong.
7. **Konsistensi internal buku**: sebutkan model/teknologi yang sama dengan istilah yang sama seperti di guideline (mis. DeepSeek V4 Flash, Mistral Large 3, Qwen3.6, GPT-5.5, Claude Fable 5). Jangan menciptakan produk fiktif baru.
8. **Dinamika naratif**: boleh memecah seksi panjang menjadi sub-judul bernomor, list, *admonition* (mis. `> **Catatan:**`), atau blok tanya-jawab — selama tidak merusak alur. Akhiri setiap seksi dengan "jembatan" menuju seksi berikutnya.

---

## 5. ATURAN TABEL (WAJIB DIPERIKSA ULANG)

- Setiap tabel WAJIB punya baris separator `|:---|:---|` setelah header.
- Kolom selaras (jumlah pipa konsisten di semua baris).
- Gunakan penjajaran `:---:` untuk kolom angka, `:---` untuk teks, `:---:` juga untuk kolom pusat.
- Nomor tabel berurutan: "Tabel 1", "Tabel 2", dst.
- Setiap tabel WAJIB didahului kalimat narasi dan diikuti analisis 1-2 paragraf.
- Sel tidak boleh ada yang kosong tanpa alasan; jika tidak ada data tulis "—" atau "N/A".

---

## 6. ATURAN REFERENSI (WAJIB)

1. Replikasi **seluruh referensi yang tercantum di guideline** (paper beserta DOI/arXiv-nya + referensi pendukung). Tidak boleh dibuang.
2. Jika mengutip data baru dari web search, tambahkan sebagai referensi pendukung dengan URL lengkap dan dapat diklik.
3. Format kutipan dalam teks bila perlu: `[1]`, `[2]`, dst — konsisten dengan daftar referensi di akhir.
4. Referensi WAJIB minimal 5 paper 5-10 tahun terakhir (2021-2026) dengan DOI/arXiv yang valid.

---

## 7. CHECKLIST SEBELUM MENYIMPAN (WAJIB DILALUI)

- [ ] Semua seksi guideline (Tujuan, Kerangka, Tabel, Diagram, Tutorial, Studi Kasus, Referensi) TERCOVER di konten.
- [ ] Minimal 2 tabel valid + minimal 1 mermaid valid + minimal 1 GAMBAR STATIS PNG (data asli dari file) per file.
- [ ] Minimal 5 paper 5-10 tahun terakhir di Referensi.
- [ ] Semua embed gambar statis menunjuk ke file PNG yang benar-benar ada (path relatif benar).
- [ ] Sintaks mermaid diperiksa baris per baris.
- [ ] Tidak ada kalimat/kata yang tercetak dobel atau *placeholder* ("...", "TBD", "Lorem").
- [ ] File tidak kurang dari 350 baris.
- [ ] Bahasa Indonesia teknis-komunikatif, alur baca nyaman.
- [ ] Data angka konsisten dengan guideline (perplexity, t/s, GB, harga, dll).