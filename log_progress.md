# Progress Log — Buku Kolaborasi LLM

> File ini mencatat semua perubahan signifikan yang dibuat ke dalam repositori.
> Setiap entri mencantumkan timestamp realtime, deskripsi perubahan, dan file yang terpengaruh.

---

## 2026-06-17

### 12:00 WIB — Inisialisasi Guideline System
- Membuat direktori `guidelines/` sebagai pusat panduan penulisan untuk peneliti dan agen AI
- Membuat 2 file contoh guideline untuk review penulis:
  - `guidelines/jilid-1/bab-01-model/sub-bab-4.md` — Deep Dive Kuantisasi
  - `guidelines/jilid-2/bab-06-home/sub-bab-1.md` — Karakteristik Sistem Home Assistant
- Membuat `log_progress.md` untuk pelacakan perubahan realtime

### 20:55 WIB — Update Referensi ke Link Valid
- Mengganti referensi teks di kedua file guideline dengan link DOI/arXiv/URL yang valid dan dapat diklik:
  - `guidelines/jilid-1/bab-01-model/sub-bab-4.md` — menambahkan 2 referensi baru (Open LLM Leaderboard, QLoRA paper)
  - `guidelines/jilid-2/bab-06-home/sub-bab-1.md` — menambahkan 4 referensi baru (Piper, Whisper, WireGuard, OpenWrt)

### 21:45 WIB — SOP Referensi Diperketat (5 Paper 5 Tahun Terakhir + DOI)
- Semua referensi paper diganti dengan format BibTeX lengkap (author, title, year, DOI/arXiv, venue)
- Setiap guideline WAJIB memiliki minimal **5 paper jurnal/konferensi** dari 5 tahun terakhir (2021-2026)
- Semua paper diverifikasi via web search untuk memastikan validitas (tidak ada halusinasi)
- Ditambahkan anotasi "Kaitan" yang menjelaskan relevansi spesifik setiap paper terhadap konten sub-bab
- Ditambahkan SOP Referensi di setiap guideline sebagai reminder wajib

**sub-bab 1.4 (Kuantisasi):** GPTQ (ICLR 2023), AWQ (MLSys 2024), SpQR (ICLR 2024), QLoRA (NeurIPS 2023), SmoothQuant (ICML 2023)

**sub-bab 6.1 (Home Assistant):** On-Device LLM Home (arXiv 2025), Harmony Smart Home (arXiv 2024), SLM Survey (arXiv 2024), Demystifying SLM Edge (ACL 2025), Edge LLM Review (arXiv 2024)

### Struktur Guideline yang Ditetapkan
Setiap file guideline berisi 7 seksi wajib:
1. **Tujuan Sub-Bab** — target kompetensi pembaca setelah membaca
2. **Kerangka Konten** — poin detail yang harus ditulis (paragraf per paragraf)
3. **Tabel Wajib** — spesifikasi kolom, baris, dan data (minimal 2 tabel)
4. **Diagram/Gambar Wajib** — deskripsi Mermaid/screenshot, path di `assets/`
5. **Tutorial / Hands-on** — langkah teknis dan command yang harus didokumentasikan
6. **Studi Kasus** — skenario dunia nyata dengan analisis
7. **Referensi Wajib** — minimal 5 paper (5 tahun terakhir) + DOI + BibTeX + dokumentasi pendukung

### SOP Referensi yang Ditetapkan
1. Minimal **5 paper jurnal/konferensi** dari 5 tahun terakhir (2021-2026)
2. Setiap paper harus memiliki DOI atau arXiv ID yang valid
3. Metadata BibTeX lengkap (author, title, year, venue, doi, url)
4. Sertakan anotasi "Kaitan" yang menjelaskan relevansi paper terhadap konten sub-bab
5. Data tabel WAJIB diverifikasi terhadap angka di paper asli
6. Paper non-teknis (dokumentasi, GitHub) diperbolehkan sebagai referensi pendukung tambahan


---


## 22:30 WIB — Batch Generation Seluruh Guideline (85 File)

### Ringkasan Total
- **85 file guideline** berhasil dibuat di direktori `guidelines/`
- **Total konten:** 26.703 baris (~314 baris/file rata-rata)
- **7 seksi wajib** terpenuhi di semua file (validasi otomatis: 0 error)

### Rincian per Bab

| Bab | Path | File | Topik Cakupan |
|:---|:---|---:|:---|
| **1** | `guidelines/jilid-1/bab-01-model/` | 10 | Arsitektur & Seleksi Model |
| **2** | `guidelines/jilid-1/bab-02-hardware/` | 10 | GPU, CPU, NPU, Budgeting |
| **3** | `guidelines/jilid-1/bab-03-software/` | 10 | Ollama, LM Studio, Open WebUI, dll |
| **4** | `guidelines/jilid-1/bab-04-otomasi-agent/` | 10 | Agent, Function Calling, Multi-Agent |
| **5** | `guidelines/jilid-2/bab-05-inference/` | 10 | vLLM, TGI, Batching, Distributed |
| **6** | `guidelines/jilid-2/bab-06-home/` | 8 | Home Assistant, RAG, Parental |
| **7** | `guidelines/jilid-2/bab-07-small/` | 8 | Small Office, OAuth, GPU Sharing |
| **8** | `guidelines/jilid-2/bab-08-general/` | 9 | K8s, DLP, Audit, Failover |
| **9** | `guidelines/jilid-2/bab-09-integrasi/` | 5 | n8n, Dify, Flowise, Vector DB |
| **10** | `guidelines/jilid-2/bab-10-etika/` | 5 | Halusinasi, Copyright, Green AI |

### Proses Pembuatan
- Dibagi dalam 2 batch paralel (masing-masing 5 task agent)
- Batch 1: bab-01 s.d bab-05 (49 file)
- Batch 2: bab-06 s.d bab-10 (36 file)
- Setiap agen diberi blueprint topik, format template, dan SOP referensi
- Semua paper diverifikasi via web search sebelum ditulis (0 referensi palsu)
- File `log_progress.md`, `guidelines/jilid-1/bab-01-model/sub-bab-4.md`, dan `guidelines/jilid-2/bab-06-home/sub-bab-1.md` tidak diubah (file contoh awal)


### 23:00 WIB — Update Khusus Bab 1.1: Timeline Extended + Referensi 10 Tahun
- Timeline evolusi diperluas dari 2017 (Transformer) hingga 2026 (Qwen3.6), dengan proyeksi ke 2027
- Ditambahkan model-model baru ke timeline: DeepSeek-V3/R1 (2024-2025), Llama 4 Scout/Maverick (2025), Phi-4 (2024), Qwen3/3.5/3.6 (2025-2026), Phi-4-reasoning (2025)
- **Tabel A** (Timeline): dari 6 baris menjadi 16 baris — mencakup 2017-2026
- **Tabel B** (Hardware): ditambahkan Llama 4 Scout, DeepSeek-R1, Qwen3 MoE, Phi-4, Qwen3.6
- **Tabel C** (Benchmark): ditambahkan Qwen2.5, Phi-4, DeepSeek-V3/R1, Llama 4, Qwen3, Qwen3.6
- **Referensi diperluas**: dari 5 paper menjadi **14 paper** (2017-2026) — termasuk Transformer (2017), GPT-2 (2019), DeepSeek-V3/R1 (2024-2025), Phi-4 (2024), Qwen2.5/3/3.5 (2024-2026), Llama 4
- Ditambahkan seksi baru 2.H (Qwen3.5/3.6 — 2026) dan 2.I (Proyeksi 2027)
- Tutorial diperbarui dengan model dari setiap era (GPT-2 s.d. Qwen3)
- Studi Kasus diperluas dari 2019 ke 2026
- Semua paper diverifikasi via web search — judul, penulis, tahun, DOI/arXiv valid

### 23:45 WIB — Update Besar Bab 1.1: Integrasi Model Terbaru (Mistral Large 3, GPT-5.5, DeepSeek V4, Qwen3.7, Claude Fable 5)
- **Kerangka Konten diperluas**: dari 9 seksi (A-I) menjadi 11 seksi (A-K):
  - **Seksi H (baru)**: Mistral Large 3 (Dec 2025) — 675B MoE granular, Apache 2.0, open-source Eropa
  - **Seksi I** (ex-H): Qwen3.5/3.6 (Feb-Apr 2026) — tidak berubah
  - **Seksi J (baru)**: Era Frontier Baru (Apr-Jun 2026) — GPT-5.5, DeepSeek V4 Pro/Flash, Qwen3.7-Max, Claude Fable 5
  - **Seksi K** (ex-I): Proyeksi 2027 — ditambahkan poin open vs closed
- **Tabel A (Timeline)**: +7 baris baru:
  - Mistral Large 3 (Dec 2025): 675B/41B aktif, granular MoE + Vision
  - GPT-5.5/5.5 Pro (Apr 2026): proprietary, 1M context, reasoning effort
  - DeepSeek-V4 Pro (Apr 2026): 1.6T/49B aktif, CSA/HCA hybrid attn, MIT
  - DeepSeek-V4 Flash (Apr 2026): 284B/13B aktif, MIT
  - Qwen3.7-Max (May 2026): ~1T+ est., proprietary, agent-centric
  - Claude Fable 5 (Jun 2026): Mythos-class, 1M context, safety classifiers
- **Tabel B (Hardware)**: +6 baris: Mistral Large 3, DeepSeek V4 Flash/Pro, Ministral 3 14B/3B
- **Tabel C (Benchmark)**: +6 baris: Mistral Large 3, DeepSeek V4 Pro, GPT-5.5, Qwen3.7-Max, Claude Fable 5
- **Diagram Mermaid**: diperbarui dengan 2025-2026 entries
- **Tutorial A**: ditambahkan Mistral Large 3 (via API) dan DeepSeek V4 Flash (via Ollama)
- **Tutorial C (Python)**: diperbarui dengan Mistral L3 dan DS V4 Pro
- **Studi Kasus**: diperpanjang hingga H1 2026 dengan DeepSeek V4 Flash
- **Referensi**: +4 paper baru (DeepSeek V4 tech report, Mistral Large 3 blog, GPT-5.5 System Card, Claude Fable 5 blog, Ministral 3 arXiv) + 2 referensi pendukung (Qwen3.7 blog, DeepSeek V4 API docs)
- Total referensi: 14 paper → 19 paper + 7 referensi pendukung = 26 referensi
- Update SOP Referensi: ditambahkan aturan untuk model proprietary (gunakan system card/blog sebagai sumber)
- Semua informasi diverifikasi via web search (Hugging Face, arXiv, blog resmi, system card)

### 00:30 WIB — Integrasi Model Terbaru ke Seluruh 85 Guideline File
- **Batch paralel (5 agent)** memperbarui 85 file guideline dengan model-model terbaru:

**Bab 01 — Model (10 file):**
- Semua sub-bab diperbarui dengan Mistral Large 3 (anatomi 675B MoE granular) di tabel perbandingan, DeepSeek V4 Pro/Flash di tutorial dan studi kasus, Claude Fable 5 di benchmarking, GPT-5.5 di section reasoning
- sub-bab-1.md: skip (sudah diupdate sebelumnya — 582 baris, 11 seksi, 27 referensi)
- sub-bab-5.md: + Mistral Large 3 ke Tabel A perbandingan model

**Bab 02 — Hardware (10 file):**
- Tabel kebutuhan hardware diperbarui dengan DeepSeek V4 Flash (284B, ~150GB INT4), Mistral Large 3 (675B, ~280GB FP8), Ministral 3 (3B/14B)
- sub-bab-8.md: tantangan thermal untuk DeepSeek V4 Flash & Mistral Large 3
- sub-bab-9.md: catatan frontier 2026 model tidak feasible di NPU

**Bab 03 — Software (10 file):**
- Ollama & LM Studio: `ollama pull deepseek-v4-flash`, Modelfile CSA/HCA attention flags
- Open WebUI, LocalAI, KoboldCPP: model backend diperbarui ke DeepSeek V4 Flash
- GPT4All, WebLLM, Mobile: Ministral 3 (3B/8B/14B) sebagai model CPU/edge
- CLI & Parameters: GPT-5.5 `reasoning_effort` parameter (low/medium/high/xhigh)

**Bab 04 — Otomasi Agent (10 file):**
- Function Calling BFCL tabel: +Claude Fable 5 (95.6%), GPT-5.5, DeepSeek V4 Pro, Mistral Large 3
- Coding Agents: SWE-bench tabel: +Claude Fable 5 (95.0%), DeepSeek V4 Pro (82.3%)
- Planning/Reasoning: GSM8K tabel: +DeepSeek V4 Pro (85.2%), Mistral Large 3
- Browser Agents, Multi-Agent, Daily Workflow: pipeline menggunakan DeepSeek V4 Flash/Pro

**Bab 05 — Inference (10 file):**
- vLLM, TGI, Aphrodite: Tabel throughput + DeepSeek V4 Pro, Mistral Large 3, Ministral 3
- KV-cache: catatan DeepSeek V4 hanya 10% KV cache V3.2 pada 1M context
- Quantization: NVFP4 diperkenalkan untuk Mistral Large 3 di H200/B200
- Distributed, Speculative Decoding: konfigurasi multi-node untuk model baru

**Bab 06 — Home (8 file):**
- Smart Home, RAG, Voice: Ministral 3 3B/8B untuk edge, DeepSeek V4 Flash 1M konteks
- Budgeting: Build Edge Hemat (NUC + Ministral 3 ~Rp 8-12jt), Build High-End (2xRTX 4090 + DS V4 Flash)

**Bab 07 — Small Office (8 file):**
- Tabel hardware: +DeepSeek V4 Flash, Mistral Large 3, Ministral 3, Qwen3.6-27B
- Studi kasus, tutorial, referensi diperbarui dengan model terbaru

**Bab 08 — General Office (9 file):**
- K8s, Enterprise Gateway: +DeepSeek V4 Flash, Mistral Large 3, GPT-5.5, Claude Fable 5
- DLP, Audit: Claude Fable 5 safety classifiers sebagai referensi kebijakan keamanan
- Failover, Knowledge Graph: strategi MoE model fallback, Qwen3.7-Max agent-centric

**Bab 09 — Integrasi (5 file):**
- n8n, Dify, Flowise: +7 model terbaru di tabel perbandingan, tutorial multi-agent dengan DS V4 Pro
- Vector DB: embedding dimension analysis untuk DS V4 (2048d), Mistral v3 (1024d)
- Report Gen: tabel akurasi diperbarui dengan DS V4 Pro (76.8%), GPT-5.5 (78.5%), Fable 5 (79.1%)

**Bab 10 — Etika (5 file):**
- Halusinasi: Claude Fable 5 safety classifiers, benchmark halusinasi 7 model terbaru
- Copyright: studi kasus lisensi DeepSeek V4 MIT — 5 implikasi bisnis
- Green AI: efisiensi MoE granular (DS V4 Pro 27% FLOPs), Cascade Distillation (Ministral 3: 40% hemat training)
- Local vs Cloud: tabel break-even dengan GPT-5.5 $5/$30, Fable 5 $10/$50 per M token

**Total:** ~1.500+ baris baru ditambahkan ke 85 file. Semua model diverifikasi dari sumber resmi (Hugging Face, arXiv, blog resmi, system card).
