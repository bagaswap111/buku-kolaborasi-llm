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
