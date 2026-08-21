# LOG PERBAIKAN KONTEN BUKU

Repo: `buku-kolaborasi-llm`
Periode lintas konsistensi: 2026-08-16 s.d. 2026-08-21
Status: SELESAI (Fase audit & perbaikan). Sub-bab kosong 15 file belum ditulis (menunggu keputusan judul).

> Dokumen ini merangkum seluruh perbaikan yang diterapkan ke konten buku, termasuk
> temuan-temuan yang terdeteksi pada audit (ditandai "TERDETEKSI") dan tindak lanjutnya
> (diperbaiki / diverifikasi tanpa perubahan / DIBIARKAN-⚠️).

---

## Ringkasan Cakupan

| Bab | Folder | Status | Perubahan diterapkan |
|:----|:-------|:-------|:---------------------|
| 1 | `konten/jilid-1/bab-01-model/` | ✅ Diperbaiki | 5 file, 25 item |
| 2 | `konten/jilid-1/bab-02-hardware/` | ✅ Diperbaiki | 10 file, lintas konsistensi angka di sub-bab 1–10 |
| 3 | `konten/jilid-1/bab-03-software/` | ✅ Diperbaiki | 10 file, 112 edit |
| 4 | `konten/jilid-1/bab-04-otomasi-agent/` | ✅ Diperbaiki | 10 file, 10 sub-bab |
| 5 | `konten/jilid-2/bab-05-inference/` | ✅ Diperbaiki | 10 file, 98 baris |
| 6 | `konten/jilid-2/bab-06-home/` | ✅ Diperbaiki (sub-bab 1–8) | naming model, desimal, penomoran |
| 7 | `konten/jilid-2/bab-07-small/` | ✅ Diperbaiki (sub-bab 1–8) | 5 file, 35 edit |
| 8 | `konten/jilid-2/bab-08-general/` | ✅ Diperbaiki (sub-bab 1–9) | 9 file, 98 edit |
| 9 | `konten/jilid-2/bab-09-integrasi/` | ✅ Diperbaiki | 5 file, 5 sub-bab |
| 10 | `konten/jilid-2/bab-10-etika/` | ✅ Diperbaiki (sub-bab 1–5) | 5 file, 63 edit |
| Nav & index | `mkdocs.yml`, `konten/index.md`, `konten/jilid-1/index.md`, `konten/jilid-2/index.md` | ✅ Diperiksa | typo "roadma"→"roadmap"; catatan bab 09/10 |

**Total:** ±600+ edit nyata di 10 bab; seluruh perbaikan bab 2, 4, 5, 6, 1, 3 telah di-commit
(`9b62aa0`, `fcab725`, `23c3b9c`); bab 7, 8, 10 masih di working tree (belum di-commit saat log ini ditulis).

---

## BAB 1 — `konten/jilid-1/bab-01-model/`

Sumber: `logs-perbaikan/bab-01.md`. **TERDETEKSI** (dari audit awal bab 01) → perbaikan:

| File | Baris~ | Masalah | -> | Perbaikan |
|:-----|:------|:--------|:---|:----------|
| sub-bab-1.md | 22 | TERDETEKSI: "tidak hanya mengubah NLP — tetapi" (konjungsi salah, kalimat tak lengkap) | -> | "tidak hanya mengubah NLP, tetapi juga" |
| sub-bab-1.md | 33,39,81,87 | TERDETEKSI: paragraf diawali spasi kosong (rusak render) | -> | spasi awal dihapus |
| sub-bab-1.md | 43 | TERDETEKSI: "skalaibel" | -> | "skalabel" |
| sub-bab-1.md | 100 | TERDETEKSI: "tools seperti Ollama" (asing tak diberi penanda) | -> | "*tools* (perangkat lunak) seperti Ollama" |
| sub-bab-1.md | 406 | TERDETEKSI: tiga butir diklaim "dua hal" | -> | "tiga hal penting" |
| sub-bab-2.md | 123 | TERDETEKSI: "2 expert" (jumlah expert aktif V4 Pro keliru) | -> | "9 dari 256+ expert (sparsity 3,1%)" |
| sub-bab-2.md | 160 vs 376 | TERDETEKSI: ukuran Q4_K_M 8B "4.2 GB" vs "4,9 GB" | -> | diseragamkan 4,9 GB |
| sub-bab-2.md | 160 vs 283 | TERDETEKSI: ukuran Q4_K_M 70B "38 GB" vs "42 GB" | -> | diseragamkan 42 GB |
| sub-bab-2.md | 261-265 | TERDETEKSI: LayerNorm "209M (2,6%)" tak masuk akal untuk 8B | -> | 0,26M (0,003%); total dikoreksi 7,82B + persentase disesuaikan |
| sub-bab-5.md | 60 | TERDETEKSI: deret PNG mulai "Gambar 1.5-3" | -> | "Gambar 1.5-1" |
| sub-bab-6.md | 53,69,86,270,336 | TERDETEKSI: Tabel 2 muncul sebelum Tabel 1; PNG "Gambar 1.6-3" | -> | dinomori ulang (Efisiensi=Tabel 1, Perbandingan=Tabel 2); rujukan disesuaikan; PNG→"Gambar 1.6-1" |
| sub-bab-7.md | 56,78,83,117,136,141 | TERDETEKSI: "Tabel A/B" rujukan salah; PNG mulai 1.7-3; Gambar 2 sebelum 1 | -> | "Tabel 1/2", PNG→1.7-1/1.7-2, urutan mermaid ditukar |

**Verifikasi:** tidak ada sisa teks lama (4.2 GB, 38 GB, 209M, skalaibel, Tabel A/B, Gambar 1.x-3/4).

---

## BAB 2 — `konten/jilid-1/bab-02-hardware/`

Sumber: `log_progress.md` (2026-08-19 s.d. 2026-08-20) + logs-perbaikan. Sudah di-commit di `9b62aa0` / `fcab725`.

**TERDETEKSI & diperbaiki:**

- **Terminologi/format lintas 10 file:** nama model dinormalkan di prosa/tabel (blok kode & ID HF dipertahankan): `Qwen-2.5-14B`→`Qwen 2.5 (14B)`, `DeepSeek-Coder-33B`→`DeepSeek Coder (33B)`, `Llama-3.1-70B`→`Llama 3.1 (70B)`, `Llama-3-8B`→`Llama 3 (8B)`; "— tetapi"→", tetapi" (5 instance).
- **sub-bab-7 (Budgeting GPU/Listrik):** epigraf Rp 461 ribu (konsisten harga tarif), tabel dinomori ulang, tarif listrik diskalakan ke Rp 1.600/kWh, skenario GPU dikoreksi (M2 Ultra 90 W, ~1,24 jt), desimal titik→koma di 17 baris, ref [5] dikoreksi → Niu et al., AAAI 2026 (diverifikasi).
- **sub-bab-8 (Pendinginan/Throttling):** klaim fiktif "scheduler RL CRAC -20%" → fakta Lu & Wang (TAWS, +40,9% @41 °C); 4 referensi dikoreksi + diverifikasi (TAPAS DOI, SIGEnergy EIR, SoCC 2024, OSDI 2024).
- **sub-bab-9 (NPU):** 0,3 t/s diatribusikan ke Meteor Lake (bukan Lunar Lake); 11 desimal koma; "dua kali lebih cepat" (10,4/5); NITRO/llm.npu/Agent.xpu refs dikoreksi + throughput 1,2–4,9×.
- **sub-bab-10 (Budgeting):** seluruh biaya disinkronkan ke Rp 1.600/kWh & 8 jam/hari (1,6 jt / 280 rb / 700 rb/thn; TCO 30/33/24 jt); Tutorial 2 memakai Rp 130.000/M agar break-even 8 bulan reproducible; rasio 4–480×; refs [1]–[4] dikoreksi penulisnya.

**Catatan terbuka:** konsistensi t/s M4 Pro (40 t/s di sub-bab-1/3/5/7/10 vs 60 t/s di sub-bab-9) — perlu keputusan penulis untuk diseragamkan.

---

## BAB 3 — `konten/jilid-1/bab-03-software/`

Sumber: `logs-perbaikan/bab-03.md`. Sudah di-commit di `23c3b9c`. **Total 112 edit di 10 file.**

Pola perbaikan per file (ringkas):

- **PUEBI/prefiks serapan:** `di-unload`→`diunload`, `di-hash`→`dihash`, `di-offload`→`dioffload`, `men-deploy`→`mendeploy`, `men-download`→`mengunduh`, `men-scroll`→`menggulir`, `di-klik`→`diklik`, `di-embed`→`diembed`, `ter-amortisasi`→`teramortisasi`, `di-upgrade`→`diupgrade`, `di-load`→`dimuat` (beberapa tempat), dsb.
- **Koma sebelum "tetapi":** "valid — tetapi"→"valid, tetapi", "koheren — tetapi"→"koheren, tetapi", dsb (7+ tempat).
- **Penomoran tabel:** `### Tabel A/B/C`→`### Tabel 1/2/3` berurutan kemunculan (sub-bab 2, 3, 5, 7, 8, 9, 10) + seluruh rujukan prosa disesuaikan.
- **Diagram→Gambar:** `### Diagram 1`→`### Gambar 1` (sub-bab 4, 5, 6) + rujukan "Diagram kedua"→"Gambar 2".
- **Tutorial→Langkah:** `### Tutorial A/B/C/D`→`### Langkah 1/2/3/4`; `## 8. Tutorial / Hands-On`→`## 8. Praktikum / Hands-On` (sub-bab 7–10).
- **Nama model:** `DeepSeek V4`→`DeepSeek V4 Flash` (2×), `Qwen2.5-14B`→`Qwen 2.5 (14B)`, `Llama-3-8B-Instruct`→`Llama 3 (8B)`.
- **Desimal koma di tabel** (sub-bab 1, 8, 9); `5.2GB`→`5,2 GB`.
- **Fakta:** sub-bab-7 "delapan dari sembilan"→"tujuh dari delapan" (konsisten tabel).
- **Klaim tanpa sumber 2025/2026** → nota "⚠️ Tidak dapat diverifikasi dari sumber tersedia — verifikasi sebelum terbit." (4×: Ministral 3 Des 2025, GPT-5.5 rilis, model frontier 2026, dsb).

**VERIFIKASI (tanpa perubahan):** nilai parameter (tokens/s, VRAM, T=0.8), ID Hugging Face, output benchmark, caption PNG yang benar, H1/H2.

---

## BAB 4 — `konten/jilid-1/bab-04-otomasi-agent/`

Sumber: `logs-perbaikan/bab-04.md`. Sudah di-commit. **TERDETEKSI & diperbaiki per sub-bab:**

- **sub-bab-1:** istilah asing dimiringkan (*guideline*, *pipeline*); "Tabel 1 di seksi tabel nanti"→"seksi 2"; paragraf panjang dipecah; klaim SWE-bench 95%→[Sumber?]; "sangkur (pengaman)"→"sekering (pengaman arus)" (istilah salah konteks); "silahkan"→"silakan"; "menyinambungkan"→"menyambungkan"; bug `SimpleAgent`: tambah `import ollama`, `__init__(self, llm="llama3.1:8b")`, `think()` memakai `ollama.chat()`+parse+fallback.
- **sub-bab-2:** "penterjemah"→"penerjemah"; desimal titik→koma di tabel BFCL; bug parsing tool calls (`message.get("tool_calls",[])` + `json.loads`); "Tutorial B"→"Langkah 2"; "(90,6%) [Sumber?]".
- **sub-bab-3:** koma sebelum "tetapi"/"melainkan" (4×); "2-3 contoh"→"dua-tiga contoh"; "[Sumber?]" pada hybrid CSA/HCA; duplikasi nomor gambar; desimal koma; "di-parse"→"diparse"; referensi Kojima dipindah ke Paper Jurnal + DOI.
- **sub-bab-4:** "Menginstall"→"Menginstal", "mengkonfigurasi"→"mengonfigurasi"; rujukan tabel benar; "ter-*pull*"→"diunduh"; "di-refactor"→"diubah"; "lima *prompt*"; nama model Qwen 2.5 Coder (7B)/Llama 3.1 (8B); desimal koma; ref [4] arXiv 2603.00007→⚠️ verifikasi.
- **sub-bab-5:** desimal koma Tabel 1; "Tabel 3 pada seksi 3"; "di-hardcode"→"dihardcode"; "Tutorial 1"→"Langkah 1"; BUG `NAVIGATE` tanpa implementasi → dihapus dari daftar action + dikomentari sebagai ekstensi; paragraf duplikat dihapus; "[Sumber?]"×2; "ter-*commit*"→"tercatat".
- **sub-bab-6:** "menganalisa"→"menganalisis" (7×); koma; "Lima Lapisan Strategi" menambah butir ke-4; "dua-lima kata"; "Tutorial 1"→"Langkah 1"; "Tutorial / Hands-On"→"Praktikum"; penomoran tabel diverifikasi.
- **sub-bab-7:** "Menginstall"→"Menginstal"; penomoran tabel diurutkan (TTS/Whisper/latency); desimal koma; koma sebelum "tetapi"; WER Bhs. Indonesia→[Sumber?]; "analisa"→"analisis"; "Tutorial / Hands-On"→"Praktikum".
- **sub-bab-8:** selisih akurasi "4-6%"→"4,4–6,1%"; "me-mount"→"memount"; Tabel A/B/C→1/2/3; Tutorial A/B/C→Langkah; mermaid inline→blok; refs arXiv 2026→⚠️.
- **sub-bab-9:** rujukan tabel/tutorial dinormalisasi (Tabel 3/K Langkah); Claude Fable 5 (keliru dipakai model "kecil")→DeepSeek V4 Flash/Qwen 2.5 (7B) sebagai Editor/Writer; nama model dibenerkan; mermaid inline; desimal koma; "didebug"; "[Sumber?]" untuk nilai kualitas +40%; ref JATIR dipindah + [Sumber?]; DIBIARKAN-⚠️ (tidak memakai "Qwen 3.6" di tablet).
- **sub-bab-10:** pipeline 7 tahap vs kode 4 tahap — catatan penjelas ditambahkan; "di-debug"→"didebug"; klausa privasi vs Otter.ai dijelaskan; Tabel A/B/C→1/2/3; "[Sumber?]" akurasi diarization; nama model; "diparse"; "2025-06-16"→"2026-06-16" (anakronisme); mermaid inline; Tutorial→Langkah + judul "macOS + launchd"→"Linux — cron/inotifywait" (diselaraskan dengan isi); "di-sinkronkan"→"disinkronkan"; ref [5]→⚠️.

---

## BAB 5 — `konten/jilid-2/bab-05-inference/`

Sumber: `log_progress.md` (2026-08-19). Sudah di-commit di `9b62aa0`. **10 file, 98 baris diubah.**

- **Tabel A/B/C→Tabel 1/2/3** di sub-bab-7/8/9/10 (header + semua rujukan prosa).
- **"— tetapi"→", tetapi"** (13 instance).
- **Nama model dinormalkan** (prosa/header/alt-text tabel; blok kode & HF ID dipertahankan): `Llama-3.1-8B`→`Llama 3.1 (8B)`, `Llama-3.1-70B`→`Llama 3.1 (70B)`, `Llama-3.1-405B`→`Llama 3.1 (405B)`, `Llama-3.2-3B`→`Llama 3.2 (3B)`, `Llama-3-8B`→`Llama 3 (8B)`, `Qwen-2.5-32B`→`Qwen 2.5 (32B)`, `Mistral-7B`→`Mistral 7B`, `Llama-3.1-8B-Instruct`→`Llama 3.1 (8B)`.
- **Desimal koma di tabel** — diverifikasi 0 sisa.
- **Verifikasi:** 0 sisa `— tetapi`/`Tabel A/B/C`/nama model ber-hyphen di luar code fence; `Meta-Llama` (HF ID) tetap utuh.

---

## BAB 6 — `konten/jilid-2/bab-06-home/`

Sumber: `log_progress.md` + commit `23c3b9c`. **TERDETEKSI & diperbaiki (sub-bab 1–8):**

- **Nama model dinormalkan** lintas file: `Llama-3.1-70B`→`Llama 3.1 (70B)`, `Llama-3.3-70B`→`Llama 3.3 (70B)`, sebutan umum Qwen 2.5 (14B) dsb. di sub-bab 1, 2, 4, 6, 8.
- **Desimal titik→koma** di sub-bab 2 & 4; konsistensi kata "Tabel 4".
- **sub-bab-1:** koreksi "6 GB"→"32 GB" (VRAM/cluster), "Celcius"→"Celsius", "Llama-3.1-70B"→"Llama 3.1 (70B)".
- **sub-bab-6:** koreksi resolusi 3840×2160, "MPU6050"→"MPU-6050".
- **sub-bab-10 (isi, bila ada):** [Sumber?] pada klaim DeepSeek V4 Pro; penomoran tabel; desimal koma.

> Catatan: sesi perbaikan bab-06 menyebut "sub-bab 6.10" dan "3 acik konten → 10 sub-bab lengkap"; yang terlintas di log_progress tidak semuanya terwakili — lihat commit `23c3b9c` untuk daftar persisnya.

---

## BAB 7 — `konten/jilid-2/bab-07-small/`

Sumber: `logs-perbaikan/bab-07.md`. **TERDETEKSI & diperbaiki (sub-bab 1–8; sub-bab 9/10 kosong — tidak disentuh):**

- **sub-bab-1:** "99.5%"→"99,5%"; "~3.6 jam"→"~3,6 jam"; nama model hyphen→spasi (`Qwen 3.6 (27B)`, `Qwen 2.5 Coder (14B)`, `Ministral 3 (14B)`, `Llama 3.1 (70B)`, `Qwen 3 (32B)`).
- **sub-bab-2:** 7 desimal koma (112,5 GB/s; 1,6-1,7× dsb.); 11 pola nama model (Llama 3.1 (8B/70B), Qwen 2.5 (14B), DeepSeek Coder (67B), Mixtral 8x22B dsb.); "Tutorial A/B/C"→"Langkah 1/2/3" + rujukan; klaim NVLink 40-60%→[Sumber?].
- **sub-bab-3:** "— tetapi"→", tetapi"; nama model dibenerkan.
- **sub-bab-4:** "~1.5 MB"→"~1,5 MB", "~2.2/2.3/1.5 GB"→koma.
- **sub-bab-8:** nama model Tabel 4 (24–64 GB) dinormalkan.

**Catatan:** rujukan "Bab 7.1 Tutorial 3" dipertahankan (menunjuk penomoran Tutorial yang memang dipakai sub-bab-1). "menganalisa"/"Menginstall" tidak ditemukan.

---

## BAB 8 — `konten/jilid-2/bab-08-general/`

Sumber: `logs-perbaikan/bab-08.md`. **TERDETEKSI & diperbaiki (sub-bab 1–9; sub-bab-10 kosong — tidak disentuh):** **9 file, 98 edit.**

- **Penomoran Tabel/Gambar:** berurutan di semua file; "Diagram N"→"Gambar N" (sub-bab 4, 5, 6); rujukan silang diselaraskan; "Tutorial A/B/C"→"Langkah 1/2/3" (sub-bab 1, 2, 3, 5, 6, 8, 9) + "seksi 2/3"→seksi aktual.
- **Desimal koma:** 99,999%/99,9% (sub-bab 1, 8), 2,0 TB/s, Rp 1,5k/kWh, TCO, S/T 0,5/0,25 FTE, 71,5%/72,3%, Rp 4,2jt dsb.
- **Kata:** "menganalisa"→"menganalisis", "dipatikan"→"dimatikan", "Litelllm"→"LiteLLM", "devam"→"dewan", kata "jurnal" nyasar dihapus.
- **Penanda tanpa sumber [Sumber?]: 3×** (downtime 43 menit sub-bab-1; Claude Fable 5 sub-bab-5; Qwen3.7-Max sub-bab-7).
- **Referensi 2026 ⚠️: 17×** — "Tidak dapat diverifikasi dari sumber tersedia — verifikasi sebelum terbit." (termasuk SafeGPT & Mökander yang label tahunnya tak konsisten dengan arXiv ID).

**Catatan penulis:** klaim "43 menit downtime/tahun" (sub-bab-1) tidak cocok five-nines (31.536.000 × 0,0001% = 31,5 mnt) — diberi [Sumber?] dan perlu dicek sebelum terbit.

**DIBIARKAN:** sub-bab-10.md (0 byte), blok kode/mermaid, desimal sah (Bab 8.2, PCIe 4.0, 8.192, ribuan, DOI), struktur H1/H2, keterangan gambar gaya "Gambar 8.1-1" (konvensi buku).

---

## BAB 9 — `konten/jilid-2/bab-09-integrasi/`

Sumber: `logs-perbaikan/bab-09.md`. **TERDETEKSI & diperbaiki (5 sub-bab; sub-bab 6–10 kosong — tidak disentuh):**

- **sub-bab-1:** "per *query*" miring; lisensi n8n "fair-code (SSPL)"→"fair-code (SUL)" (SSPL=Milvus/Mongo); "non-Developer"→"non-developer"; penomoran tabel 2,3,1→1,2,3; desimal koma (1,6T/80,6%/67,9%/95,0%); artefak "---" ganda→satu; "6000+/1500+"→"6.000+/1.500+"; "$19.99"→"$19,99/bulan"; "0.5-1 detik"→"0,5-1"; Tutorial A-D→Langkah 1-4; "(20 Agen)"→"(3 Agen)"; Rupiah VPS + [Sumber?]; rujukan Tabel 1→3; refs 2026→⚠️ (arXiv 2604.00001 dsb.).
- **sub-bab-2:** "men-deploy"→"mendeploy"; "---" ganda; "*rerank*"; desimal koma tabel performa; "per *query*"; "pakah"→"apakah"; anakronisme "GPT-4"→"GPT-5.5"; Tutorial A-C→Langkah 1-3; "di-embed"→"diembed".
- **sub-bab-3:** "Men-deploy"→"Mendeploy"; istilah asing miring; tabel dinomori ulang 1-3 + rujukan; "$0.01"→"$0,01/query" dsb.; klaim "embedding 8192 dimensi"→"8.192 token — dimensi mengikuti model 2048/1024" + [Sumber?]; "4x"→"4×"; desimal koma; markdown splitter (0,85) vs semantic (0,87) dikoreksi; Tutorial→Langkah; GPT-4o→GPT-5.5 (fast/reasoning) dla node produksi 2026.
- **sub-bab-4:** klaim "latensi naik 30-50%" vs tabel (+140-150%) → dikoreksi; "*trade-off*"; desimal koma; ambang skala Milvus "100K-5M">5M"→"100K-10M/>10M"; Rp 5jt→Rp 5 juta; "Gambar 2" tanpa file→label dihapus; "---" ganda; Qdrant "±5-10 juta vektor"; "175-2.2M *chunks*"; DIBIARKAN-⚠️ (klaim e-commerce 50M+).
- **sub-bab-5:** penomoran tabel komponen/SLA/NL2SQL; GPT-4o→GPT-5.5 (API) di komponen; label biaya "GPT-4o"→"Biaya LLM (API cloud)" — DIBIARKAN-⚠️ alternatif tanpa mengarang harga; "2x GPU"→"2×"; desimal koma persentase NL2SQL (18 nilai); "63,5% menyamai"→"melampaui ... keduanya 62,7%"; "Mrkdwn"→"mrkdwn"; "Gambar 2" tanpa file→label dihapus; bug `len(data)` dari string JSON→`json.loads`; `import json` ditambahkan (insight_extractor.py); "di-serialisasi"→"diserialisasi"; klaim 92%/78%→[Sumber?].

---

## BAB 10 — `konten/jilid-2/bab-10-etika/`

Sumber: `logs-perbaikan/bab-10.md`. **TERDETEKSI & diperbaiki (5 sub-bab; sub-bab 6–10 kosong — tidak disentuh):** **5 file, 63 edit.**

- **Penomoran & rujukan:** Tabel A/A1/B/C→Tabel 1/2/3/4 berurutan; Gambar dikoreksi urutannya; semua rujukan silang ("Tabel B di Seksi 5", "(lihat Tabel A)") disesuaikan; "14 model"→"15 model" (sub-bab-5).
- **PUEBI:** koma sebelum "tetapi" (±12 tempat); desimal titik→koma di seluruh sel tabel (<0,9 / 80,6% / ~1,4M / +0,2 dst.); *dashboard* / *break-even* dimiringkan.
- **Terminologi:** "Tutorial A-D"→"Langkah 1-4"; "Tutorial" prosa→"Langkah/Praktikum"; SWE-bench 80,6% + sitasi [6].
- **Klaim tanpa sumber → [Sumber?] (7×):** estimasi Gartner, harga OpenAI, GPT-3 "500 ton CO2", query 5-10×, siklus rilis Meta 12-15 bulan, 40% GPU idle.
- **Referensi 2026 ⚠️ (9×):** nota "Tidak dapat diverifikasi ... verifikasi sebelum terbit." (Anthropic, DeepSeek, OpenAI, Qwen; sumber tidak dihapus).

**DIBIARKAN:** Rp 1.200/Rp 1.500 (pemisah ribuan), versi/rentang (Apache 2.0, 0-1), "di-*fine-tune*" (kata asing), struktur H1/H2, sub-bab-6 s.d. 10 (kosong).

---

## NAVIGASI & INDEX

Sumber: `logs-perbaikan/bab-index.md`. Badan `mkdocs.yml` berubah → diperiksa. Sudah di-commit.

| File | Baris~ | Masalah | -> | Perbaikan |
|:-----|:------|:--------|:---|:----------|
| konten/jilid-1/index.md | 11 | Typo "roadma 2026" | -> | "roadmap 2026" |
| konten/jilid-1/index.md | 12 | Deskripsi bab 02 | -> | OK, sesuai isi — tanpa perubahan |
| konten/jilid-2/index.md | 12-16 | Rencana tambah sub-bab 9-10 bab 06-10 | -> | DIBIARKAN — file sub-bab-9/10 bab 06-10 kosong (0 byte), judul belum pasti; deskripsi tidak salah; nav belum ditambah (menunggu konten ditulis). |
| konten/index.md | 39 | "Setiap bab terdiri dari 5-10 sub-bab" | -> | Pernyataan tetap benar — tanpa perubahan |
| konten/index.md | 35 | Bab 09-10 kini 10 sub-bab | -> | Ditambahkan catatan di bawah tabel Jilid 2 ("Bab 09 dan 10 kini masing-masing terdiri dari 10 sub-bab — yang baru masih dalam penyusunan"). |
| mkdocs.yml | 42, 65-165 | Integritas YAML (tag kustom superfences) | -> | `yaml.compose` → VALID; secara `safe_load` memang menolak tag `!!python/name:pymdownx.superfences.fence_code_format` (bukan error sintaks). Struktur nav & path divalidasi. |

---

## RINGKASAN STATUS TINDAK LANJUT

| Kategori | Jumlah |
|:---------|:------:|
| Item TERDETEKSI audit di 11 unit | ±90+ temuan |
| Item diperbaiki (edit nyata) | ±600+ |
| Item diverifikasi tanpa perubahan | ±40+ |
| Item DIBIARKAN-⚠️ (butuh keputusan/verifikasi penulis) | ±12 |
| Referensi 2025-akhir/2026 ditandai ⚠️ (tidak diverifikasi dari sumber) | ±30 |
| Klaim anekdotal diberi [Sumber?] | ±25 |

### Pekerjaan tertunda (menunggu penulis)
1. **Menulis 15 sub-bab kosong** (bab-06 s.d. bab-10) — tidak ada guideline; judul belum diputuskan. (Sementara DILEWATI.)
2. ~~Seragamkan t/s M4 Pro~~ → **SELESAI 2026-08-21**: gaya kanon ~40 t/s (7B Q4) & ~20 t/s (14B Q4), M4 Max ~70/73 t/s; ~45 t/s pada bab-04 sb-4 dipertahankan + catatan *tool-loop* agen (lihat SESI 2026-08-21).
3. ~~Klaim downtime 43 menit~~ → **SELESAI**: angka dihapus dari prosa (rilis terbaru tidak menyebut 43 mnt) — rujukan prosa diturunkan ke rentang yang didukung sumber [2][4].
4. ~~Rp 1.500/kWh~~ → **SELESAI 2026-08-21**: seluruh prosa/tabel/kode diseragamkan ke kanon Rp 1.600/kWh (lihat SESI 2026-08-21). Sisa "1.500" hanya non-tarif (Token Usage, harga pensil, clock 1500 MHz) + rentang PLN (1.444-1.700, 1.500-1.700, dsb.).
5. Evaluasi nota ⚠️ referensi 2026 (konflik arXiv ID DeepSeek-V4 & Ministral 3, LISA 2403.12345, dsb.) sebelum terbit — sebagian klaim sudah dipilah di SESI 2026-08-21 (terverifikasi vs fiktif-2026), evaluasi formal sebelum terbit tetap terbuka.
---

## GELOMBANG TERAKHIR (sesi lanjutan)

### Perlakuannya
Setelah push/commit sebelumnya, verifikasi menyeluruh menemukan sisa pola di file yang tidak tersentuh agen awal (bab-01 sb 3/8/9/10, bab-04 seluruh, bab-06, bab-09) + bab-07/08/10 hasil terapkan ulang yang masih menyisakan beberapa referensi. Dibereskan dengan skrip per-baris aman (fence dipertahankan).

| Item | Jumlah | Detail |
|:-----|:------:|:-------|
| `Tabel A/B/C` heading+referensi → `Tabel 1/2/3` | 10 baris | bab-01 sb-3 (Tabel A→1, B→2, C→3) |
| `### Tutorial A/B/C` & `### Tutorial N` → `### Langkah N` | ~70 baris | bab-01 sb-1/7/8/9/10, bab-02 sb-8/9/10, bab-05 sb-2, bab-06 sb-5-8, bab-07 sb-1/3/4/5/8, bab-09 sb-4/5 |
| `## N. Tutorial / Hands-On` → `## N. Praktikum / Hands-On` | 23 baris | semua sub-bab terkait |
| Referensi prosa `Tutorial A-D` → `Langkah N` | ~50 baris | disinkronkan dengan heading per file |
| `— tetapi` → `, tetapi` (PUEBI) | 36 baris | bab-01 sb 2-10, bab-04 sb 2/5/7/8/10, bab-06 sb 1/3/4/5/8, bab-09 sb 1/2/4/5 |
| Duplikat nomor Tabel | 1 file | bab-02 sb-4: Tabel 3 (CHEOPS) → **Tabel 2**, referensi disesuaikan |
| despacing `model N` / `Model N` → konsisten | beberapa | bab-07 sb-1 dll. (Qwen 3.6 (27B), Ministral 3 (14B)) |

### Verifikasi pasca-gelombang terakhir
- Fence ``` ganjil: **0**.
- Sisa pola terlarang: **0 hits**.
- Penomoran Tabel per file berurutan 1..N: **semua OK**.
- 116 gambar embed, **0 missing**.
- `mkdocs build`: **sukses** (3.9 s).

Status pekerjaan tertunda (penulis) pasca-gelombang terakhir: 15 sub-bab kosong, evaluasi ⚠️ referensi 2026 — lihat seksi terbaru berikut.

---

## SESI 2026-08-21 — Konsistensi Angka & Penyelesaian Penanda [Sumber?] (47 edit di 28 file)

### A. Tarif listrik kanonik Rp 1.600/kWh (lanjutan dari gelombang sebelumnya)

Addendum `bab-06-home/sub-bab-8.md` (Seksi 8):

- **Tabel 1** (Listrik/tahun): 1.800.000→**1.920.000**, 2.400.000→**2.560.000**; Total Tahun 1: 29.300.000→**29.420.000**, 47.900.000→**48.060.000**; Tahun 2: 31.600.000→**31.840.000**, 50.800.000→**51.120.000**; Tahun 3: 33.900.000→**34.260.000**, 53.700.000→**54.180.000**; TCO bersih ~25.800.000→**~26.160.000**, ~40.200.000→**~40.680.000**. Asumsi baris 78 & 90 1.500→1.600. Caption Gambar 6.8-1 "bertambah Rp 4,6jt"→**4,8jt**. Analisis prosa disesuaikan (29,4jt/48,1jt; 34,3jt; ~26,2jt); kalimat "Satu-satunya argumen kuat untuk cloud…" dipulihkan setelah tak sengaja terhapus.
- **Tabel 2** semua baris: RTX 3090 ~130rb/1,56jt→**~140rb/~1,68jt**; 4090 ~144rb/1,73jt→**~156rb/~1,87jt**; Mac Mini ~25rb/300rb→**~27rb/~327rb**; Mac Studio ~43rb/516rb→**~47rb/~561rb**; NUC ~11rb/130rb→**~12rb/~140rb**; 2×4090 ~252rb/3,02jt→**~273rb/~3,27jt**. Caption 6.8-2 (140-273rb / 12-27rb) & analisis (~140-156rb) disesuaikan. Paragraf Mac Mini M4 Pro dikoreksi **idle 7W+load 65W→15W/85W** (sinkron Tabel 2). Semua kode: `"1500"`→`"1600"` (default, 3 skenario), `TARIF=1600`, template sensor `kwh * 1600`. Studi kasus Seksi 9: listrik 2,4jt→**2,56jt/thn**, 52,2jt→**52,7jt/3thn**, penghematan 37,8jt→**37,3jt**; break-even bulan ke-20 terverifikasi tetap valid (45/(2,5-0,255)≈20).

Addendum `bab-07-small/sub-bab-8.md`:

- **Tabel 4 Listrik (24/7)**: 1.500.000/2.000.000/3.000.000→**1.600.000/2.133.000/3.200.000**; Total Opex Bulanan 4,6/6,8/9,6→**4,7/6,9/9,8jt** (sempat salah tulis 10,3 → dikoreksi; verifikasi 3,2+0,5+0,2+1,0+0,5+4,44=9,84). Narasi "±Rp 9,6 juta"→**±Rp 9,8 juta**; komentar & prosa skrip 1.500→1.600; kode skrip `* 1500`→`* 1600` (ketidaksinkronan komentar-kode ditemukan & diperbaiki). Catatan B-3 (rentang PLN 1.500-1.700) dibiarkan; "Rp 1-3 juta/bulan" tetap valid (1,6-3,2jt).

Addendum `bab-08-general/sub-bab-9.md` (Seksi 9):

- Kalkulasi 4 kW: `1.600 × 24 × 365 × 4 = **Rp 56 juta/tahun**`; komentar `# Rp 1.500`→`# Rp 1.600`; `cost_per_kwh=1500`→`1600`. Skrip 2×H100 (2,38 kW) → **±Rp 33 jt/thn** (konsisten Tabel 1 Medium Rp 35jt + margin cooling). **Tabel 1 (15/35/60jt) diverifikasi tetap konsisten di 1.600** (Entry ~12,8jt ≈ 15jt dgn cooling; Premium 60,8jt ≈ 60jt).

**Tambahan**: `bab-04-otomasi-agent/sub-bab-4.md` intro Tabel 2 — konsistensi M4 Max: mengukur t/s dalam *tool-loop* agen (Cline/Aider: skema alat, riwayat percakapan) lebih rendah dari *inference* murni; contoh eksplisit Llama 3.1 (8B) ~70 t/s murni (Bab 2) → ~45 t/s saat dijalankan agent. Keputusan: **~45 t/s DIPERTAHANKAN** dengan catatan, bukan diseragamkan.

### B. Inventaris penanda tanpa sumber

- `[Sumber?]` = **24 item di 19 file** (bab-01: 0; bab-02: 0; bab-03: 0; bab-04: 12; bab-05: 0; bab-06: 2; bab-07: 1; bab-08: 2; bab-09: 3; bab-10: 4).
- ⚠️ = **48 item di 28 file** → kini **49 di 29 file** setelah penyeragaman anotasi ref `[4] JATIR` di bab-04 sb-9.
  - **Kategori A (13)**: blockquote `> ⚠️ Tidak dapat diverifikasi dari sumber tersedia — verifikasi sebelum terbit.` → **DIPERTAHANKAN** (penanda editorial).
  - **Kategori B (4)**: "ID placeholder — ganti dengan ID asli sebelum rilis" (bab-02 sb-1/2/5/6) → **DIPERTAHANKAN**.
  - **Kategori C (7)**: "verifikasi sebelum rilis (ID arXiv 2026)" → **DIPERTAHANKAN**.
  - **Kategori D (24)**: anotasi inline entri daftar referensi → **DIPERTAHANKAN**.
- Keputusan (2026-08-21): verifikasi web untuk klaim real; klaim yang merujuk model fiktif-2026 (DeepSeek V4 Flash/Pro, Claude Fable 5, Qwen3.7-Max, GPT-5.5) dikonversi ke catatan editorial `(klaim fiktif-2026 — verifikasi sebelum terbit)` — **12 penggunaan di 11 file**.

### C. Hasil verifikasi web & penanganan per klaim (19 file [Sumber?] → 0 sisa)

**Terverifikasi & diberi sumber/angka yang benar:**

| Klaim | Hasil verifikasi | Penanganan |
|:------|:-----------------|:-----------|
| Whisper id 7,1% (bab-04 sb-7) | Cocok FLEURS large-v2; large-v3 sedikit lebih baik; small 11,8% | `[1]` Radford 2023 + kalimat "diukur pada benchmark FLEURS dalam rilis resmi Whisper [1]" |
| pyannote ~85% (bab-04 sb-10) | setara DER 12-19% pada AMI/VoxConverse, pyannote 3.1 | "setara DER 12-19% … [7]" (pyannote-audio; sitasi sempat salah [2]→dikoreksi) |
| GPT-3 ~500 tCO2 (bab-10 sb-5) | Patterson et al. 2021 (arXiv:2104.10350): 1.287 MWh, 502-552 tCO2e, ~100-123 mobil/thn | 500-550 ton + 100-123 mobil + **[14]** |
| LLM vs search 5-10× (bab-10 sb-5) | ~2,9 Wh ChatGPT vs ~0,3 Wh Google per query (≈10×; IEA Electricity 2024) | ditimpa dengan angka IEA + **[15]** |
| "40% GPU idle" (bab-10 sb-5) | **SALAH** — yang benar: Epoch AI (GPU ≈ 40% daya AI DC) & ACMETrace NSDI '24 (**49% waktu GPU direservasi idle di dalam job**) | rewrite framing ACMETrace + **[16] Hu et al., NSDI '24** (URL usenix.org diverifikasi) |
| Gartner $100rb/insiden (bab-10 sb-1) | Tidak terverifikasi; riil: Gartner 25-06-2025 — **>40% proyek agentic AI dibatalkan s.d. akhir 2027** (biaya membengkak, nilai tak jelas, kontrol risiko buruk) | rewrite proyeksi tersebut + **[17]** |
| bge-m3 1024-d/8192-token (bab-09 sb-3) | arXiv:2402.03216 | sitasi **[13]** (ref baru) |
| NVLink TP 2-GPU 40-60% (bab-07 sb-2) | ✓ ~50% *throughput* (benchmark tensor parallelism 2-GPU) | dipatok ~50% + **[10]** (komunitas) |
| GPT-4o mini Rp 15.000/1M (bab-10 sb-4) | Riil: **$0,15/1M input, $0,60/1M output** | prosa → USD + kesetaraan Rp 2.400-9.600 (kurs ±16k) + **[10]**; klaim harga model frontier → catatan fiktif-2026 |
| Meta siklus rilis 3-4/12-15 bln (bab-10 sb-3) | ✓ cocok; dari grafik: minor 2-3 bln, major ±12 bln (Llama 3 Apr 24 → Llama 4 Apr 25) | prosa disesuaikan ke fakta grafik + **[1][10]** |

**Klaim fiktif-2026 → catatan editorial `(klaim fiktif-2026 — verifikasi sebelum terbit)`:**
bab-04 sb-1 (SWE-bench 95%), sb-2 (90,6% ×2), sb-3 (hybrid CSA/HCA), sb-5 (30% tiket), sb-9 (40% kualitas); bab-06 sb-2 (KV-cache DeepSeek V4 Pro 10%); bab-08 sb-5 (Claude Fable 5 Juni 2026), sb-7 (Qwen3.7-Max Mei 2026); bab-09 sb-3 (DeepSeek V4 Embedding 2048-d), sb-5 (NL2SQL 92%/78%); bab-10 sb-4 (harga frontier).

**Lainnya:** bab-09 sb-1 — harga VPS "Rp 800rb" → `(harga asumsi editor — verifikasi tarif aktual antar-provider sebelum terbit)`; bab-06 sb-2 — resale value Mac → opsi DIPERTAHANKAN + catatan `(perkiraan umum pasar barang bekas — verifikasi harga pasar aktual sebelum terbit)` & penghapusan klausa duplikat.

### D. Catatan gambar statis (⚠️ untuk penulis)

Angka tabel biaya berubah, tetapi **PNG statis tidak dapat diregenerasi** (`scripts/` kosong, PNG tak terbaca): `sub-bab-8/{biaya-listrik-per-bulan,akumulasi-biaya-3-tahun}.png`, `sub-bab-8/tco-cloud-vs-self-hosted.png`, `sub-bab-9/{anggaran-capex-opex-tco,biaya-per-user-saas}.png`, `sub-bab-4/biaya-lokal-vs-cloud.png` — **wajib diregenerasi oleh penulis sebelum terbit**.

### E. Status akhir

- `grep '[Sumber?]'` = **0** di seluruh konten.
- ⚠️ = 49 di 29 file (48 inventaris + 1 penyeragaman ref JATIR bab-04 sb-9).
- Semua edit SESI 2026-08-21 masih di working tree (belum di-commit).
