# [Jilid 1] Bab 1.4: Deep Dive Kuantisasi
> **Tipe Konten:** Teknis — Teori + Komparasi + Praktik
> **Target Pembaca:** Pengguna menengah yang ingin memahami trade-off kuantisasi

---

## 1. TUJUAN SUB-BAB
Setelah membaca, pembaca harus bisa:
- Menjelaskan perbedaan Q4_K_M, Q5_0, Q8_0, dan FP16 dalam hal perplexity vs kecepatan
- Memilih tingkat kuantisasi yang tepat berdasarkan hardware dan use case
- Melakukan konversi model ke GGUF/EXL2 secara mandiri

---

## 2. KERANGKA KONTEN (WAJIB DITULIS)

### A. Konsep Dasar Kuantisasi (1 paragraf pembuka)
- Definisi: reduksi presisi bobot (FP32 -> INT4/INT8)
- Analogi: "menyimpan foto JPEG vs RAW — lebih kecil, kualitas turun sedikit"
- Sebutkan angka: FP32 (32-bit) -> INT4 (4-bit) = 8x lebih kecil

### B. Metode Pembulatan Bit (2-3 paragraf)
- **Round-to-Nearest (RTN):** metode paling sederhana, minim komputasi
- **Quantization-Aware Training (QAT):** fine-tuning dengan simulasi kuantisasi di forward pass
- **GPTQ / AWQ:** kuantisasi pasca-training berbasis optimalisasi bobot, populer untuk EXL2
- **GGUF (llama.cpp):** pendekatan layer-wise dengan berbagai level (q2_k hingga q8_0)

### C. Level Kuantisasi GGUF (wajib jelaskan masing-masing minimal 2 kalimat)
- q2_k, q3_k_m, q4_0, q4_k_m, q5_0, q5_k_m, q6_k, q8_0
- Arti suffix: `_k` = k-quants (heterogen), `_m` = medium, `_s` = small
- Kasus nyata: Q4_K_M adalah "sweet spot" untuk sebagian besar pengguna

### D. EXL2 vs GGUF (1 paragraf komparasi naratif)
- EXL2: eksklusif untuk ExLlamaV2, butuh GPU, throughput lebih tinggi
- GGUF: lintas platform (CPU + GPU hybrid, Apple Silicon, ARM)

### E. Dampak Kuantisasi pada Output (1 paragraf + tabel)
- Perplexity meningkat ~0.1-0.5 poin antara FP16 dan Q4_K_M untuk model 7B
- Halusinasi tidak selalu meningkat drastis, tapi model jadi lebih "lugu"

### F. Panduan Pemilihan (1-2 paragraf)
- 4GB VRAM -> q4_k_m (7B) atau q3_k_m (13B)
- 8GB VRAM -> q5_k_m (7B) atau q4_k_m (13B)
- 24GB VRAM -> q8_0 (13B) atau q4_k_m (70B)
- Apple Silicon 16GB -> q4_k_m (7B) dengan GPU offload 100%
- Model MoE besar seperti DeepSeek V4 Flash (284B) dan Mistral Large 3 (675B) membutuhkan kuantisasi Q2_K (~90 GB dan ~210 GB) — hanya feasible di workstation multi-GPU atau Mac Studio 192GB

---

## 3. TABEL WAJIB

### Tabel A: Perbandingan Level Kuantisasi GGUF

| Level | Bits/Weight | Ukuran Model 7B | Ukuran Model 70B | Perplexity Loss (vs FP16) | Kecepatan Relatif | Rekomendasi |
|:---|:---:|:---:|:---:|:---:|:---:|:---|
| **Q2_K** | 2.56 bit | ~2.3 GB | ~23 GB | +0.8 ~ 1.5 | Cepat | Hanya untuk HW sangat terbatas |
| **Q3_K_M** | 3.35 bit | ~3.0 GB | ~30 GB | +0.5 ~ 0.8 | Sedang | 4GB VRAM, model >=13B |
| **Q4_0** | 4.00 bit | ~3.6 GB | ~36 GB | +0.3 ~ 0.5 | Cepat | Standar universal |
| **Q4_K_M** | 4.25 bit | ~3.8 GB | ~38 GB | +0.2 ~ 0.4 | Sedang | **SWEET SPOT** |
| **Q5_K_M** | 5.06 bit | ~4.5 GB | ~45 GB | +0.1 ~ 0.2 | Lambat | Kualitas maksimal di VRAM cukup |
| **Q6_K** | 6.00 bit | ~5.4 GB | ~54 GB | +0.05 ~ 0.1 | Lambat | Hampir lossless |
| **Q8_0** | 8.00 bit | ~7.2 GB | ~72 GB | ~0.01 | Sangat lambat | Hanya untuk >=24GB VRAM |
| **FP16** | 16.00 bit | ~14 GB | ~140 GB | 0 (baseline) | - | Referensi, tidak praktikal |

> **Data bersumber dari:** llama.cpp benchmark, Open LLM Leaderboard. Penulis WAJIB memverifikasi angka perplexity dengan model terkini (Llama-3.1-8B sebagai contoh).

### Tabel B: Trade-off Kecepatan vs Kualitas (7B Model, RTX 4090)

| Kuantisasi | Speed (t/s) | VRAM Used | Perplexity (WikiText-2) |
|:---|:---:|:---:|:---:|
| Q4_K_M | ~85 t/s | ~5.2 GB | 5.84 |
| Q5_K_M | ~72 t/s | ~6.1 GB | 5.76 |
| Q8_0 | ~55 t/s | ~8.5 GB | 5.62 |

### Tabel C: Perbandingan Tools Konversi

| Fitur | llama.cpp (GGUF) | ExLlamaV2 (EXL2) | AutoGPTQ | AWQ |
|:---|:---|:---|:---|:---|
| **Format Output** | GGUF | EXL2/Safetensors | GPTQ | AWQ |
| **CPU + GPU Hybrid** | Ya | GPU only | GPU only | GPU only |
| **Apple Silicon** | Native | - | - | - |
| **Kecepatan Loading** | *** | ***** | *** | **** |
| **Kemudahan Konversi** | ***** | ** | *** | ** |
| **Best For** | Semua platform | GPU kencang | GPU NVIDIA | GPU NVIDIA |

---

## 4. DIAGRAM/GAMBAR WAJIB

### Diagram 1: Pipeline Kuantisasi (Mermaid)
- **File:** `assets/diagrams/j1-b1-s4-pipeline-kuantisasi.mmd`
- **Isi:** Flowchart dari FP32 -> Calibration Dataset -> Quantization Algorithm -> Quantized Model
- **Node:** Original Weights -> Calibration -> RTN/GPTQ/AWQ -> GGUF/EXL2 -> Inference

### Diagram 2: Perbandingan Ukuran Model per Kuantisasi (Bar Chart)
- **File:** `assets/images/jilid1/j1-b1-s4-size-comparison.png`
- **Isi:** Bar chart 7B vs 13B vs 70B di setiap level kuantisasi (Q2-Q8)
- **Sumber data:** Dari Tabel A

### Gambar 3: Screenshot Contoh Konversi GGUF
- **File:** `assets/images/jilid1/j1-b1-s4-gguf-convert-terminal.png`
- **Isi:** Output terminal saat menjalankan `llama.cpp/convert.py`

---

## 5. TUTORIAL / HANDS-ON (WAJIB)

### Tutorial A: Konversi Model ke GGUF (llama.cpp)

```bash
# 1. Clone llama.cpp
git clone https://github.com/ggerganov/llama.cpp
cd llama.cpp

# 2. Build (Mac dengan Apple Silicon)
LLAMA_METAL=1 make -j

# 3. Convert HuggingFace model ke FP16 GGUF
python convert.py ../path-to-model/ \
    --outfile models/model-fp16.gguf \
    --outtype f16

# 4. Quantize ke Q4_K_M
./quantize models/model-fp16.gguf \
    models/model-q4_k_m.gguf \
    q4_k_m

# 5. Test inference
./main -m models/model-q4_k_m.gguf \
    -p "Saya adalah" -n 128
```

**Catatan untuk Penulis:** Pastikan output `./quantize --help` juga didokumentasikan agar pembaca tahu semua pilihan level.

### Tutorial B: Unduh Model yang Sudah Terkuantisasi

```bash
# Langsung dari HuggingFace (TheBloke / bartowski)
ollama pull llama3.1:8b
# atau
huggingface-cli download bartowski/Meta-Llama-3.1-8B-Instruct-GGUF \
    Meta-Llama-3.1-8B-Instruct-Q4_K_M.gguf
```

### Tutorial C: Verifikasi Perplexity

```bash
./perplexity -m models/model-q4_k_m.gguf \
    -f wiki.test.raw
```

---

## 6. STUDI KASUS (WAJIB)

### Studi Kasus: Memilih Kuantisasi untuk MacBook Pro M3 18GB
- **Skenario:** User ingin menjalankan Llama-3.1-8B-Instruct untuk daily coding assistant
- **Batasan:** 18GB Unified Memory, perlu ~6-8GB untuk OS dan aplikasi lain
- **Rekomendasi:** Q4_K_M (~3.8GB model + ~2GB KV-cache = ~6GB) -> sisa 12GB untuk sistem
- **Alternatif:** Q5_K_M jika pengguna rela menutup browser
- **Hasil Akhir:** Q4_K_M memberikan keseimbangan terbaik

---

## 7. REFERENSI WAJIB (SOP: minimal 5 paper 5 tahun terakhir + DOI)

### Paper Jurnal/Konferensi

**Wajib disitasi dan dijadikan acuan data di setiap sub-bab. Metadata lengkap (author, title, year, DOI/arXiv, venue) harus dicantumkan.**

[1] **GPTQ — Post-Training Quantization 4-bit**
```
@inproceedings{frantar2023gptq,
  title     = {{GPTQ}: Accurate Post-Training Quantization for Generative Pre-trained Transformers},
  author    = {Frantar, Elias and Ashkboos, Saleh and Hoefler, Torsten and Alistarh, Dan},
  booktitle = {International Conference on Learning Representations (ICLR)},
  year      = {2023},
  doi       = {10.48550/arXiv.2210.17323},
  url       = {https://arxiv.org/abs/2210.17323}
}
```
- Kaitan: Landasan algoritma kuantisasi layer-wise yang digunakan oleh GGUF/llama.cpp. Penjelasan teknis di seksi 2.B harus merujuk pada metode OPT (second-order information) dari paper ini.

[2] **AWQ — Activation-aware Weight Quantization**
```
@inproceedings{lin2024awq,
  title     = {{AWQ}: Activation-aware Weight Quantization for {LLM} Compression and Acceleration},
  author    = {Lin, Ji and Tang, Jiaming and Tang, Haotian and Yang, Shang and Chen, Wei-Ming and Wang, Wei-Chen and Xiao, Guangxuan and Dang, Xingyu and Gan, Chuang and Han, Song},
  booktitle = {Proceedings of Machine Learning and Systems (MLSys)},
  year      = {2024},
  doi       = {10.48550/arXiv.2306.00978},
  url       = {https://arxiv.org/abs/2306.00978}
}
```
- Kaitan: Metode alternatif kuantisasi yang populer untuk EXL2. Perbandingan AWQ vs GPTQ di Tabel C harus berdasar data paper ini.

[3] **SpQR — Near-Lossless Sparse-Quantized Representation**
```
@inproceedings{dettmers2024spqr,
  title     = {{SpQR}: A Sparse-Quantized Representation for Near-Lossless {LLM} Weight Compression},
  author    = {Dettmers, Tim and Svirschevski, Ruslan and Egiazarian, Vage and Kuznedelev, Denis and Frantar, Elias and Ashkboos, Saleh and Borzunov, Alexander and Hoefler, Torsten and Alistarh, Dan},
  booktitle = {International Conference on Learning Representations (ICLR)},
  year      = {2024},
  doi       = {10.48550/arXiv.2306.03078},
  url       = {https://arxiv.org/abs/2306.03078}
}
```
- Kaitan: Teknik identifikasi outlier weights — relevan untuk menjelaskan mengapa Q4_K_M mempertahankan kualitas di sub-bab 2.E.

[4] **QLoRA — 4-bit Finetuning**
```
@inproceedings{dettmers2023qlora,
  title     = {{QLoRA}: Efficient Finetuning of Quantized {LLMs}},
  author    = {Dettmers, Tim and Pagnoni, Artidoro and Holtzman, Ari and Zettlemoyer, Luke},
  booktitle = {Advances in Neural Information Processing Systems (NeurIPS)},
  year      = {2023},
  doi       = {10.48550/arXiv.2305.14314},
  url       = {https://arxiv.org/abs/2305.14314}
}
```
- Kaitan: NF4 (NormalFloat) data type — menjelaskan teknik kuantisasi 4-bit yang optimal secara information-theoretic. Relevan untuk sub-bab 2.C.

[5] **SmoothQuant — 8-bit Weight & Activation Quantization**
```
@inproceedings{xiao2023smoothquant,
  title     = {{SmoothQuant}: Accurate and Efficient Post-Training Quantization for Large Language Models},
  author    = {Xiao, Guangxuan and Lin, Ji and Seznec, Mickael and Wu, Hao and Demouth, Julien and Han, Song},
  booktitle = {International Conference on Machine Learning (ICML)},
  year      = {2023},
  doi       = {10.48550/arXiv.2211.10438},
  url       = {https://arxiv.org/abs/2211.10438}
}
```
- Kaitan: Teknik migration quantization difficulty dari activations ke weights. Relevan untuk menjelaskan mengapa beberapa level kuantisasi (Q8_0) hampir lossless.

### Referensi Pendukung (Non-Paper)

[6] Ggerganov. *llama.cpp* — Inference engine untuk GGUF. [https://github.com/ggerganov/llama.cpp](https://github.com/ggerganov/llama.cpp)

[7] TheBloke. *GGUF Model Repository* — Hugging Face. [https://huggingface.co/TheBloke](https://huggingface.co/TheBloke)

[8] LMSYS. *Chatbot Arena Leaderboard*. [https://lmarena.ai](https://lmarena.ai)

[9] **DeepSeek-V4: Open-Weight MoE — Quantization Feasibility**
```bibtex
@article{deepseek2026v4,
  title     = {{DeepSeek-V4}: A Hybrid {CSA/HCA} Mixture-of-Experts Language Model},
  author    = {DeepSeek-AI},
  journal   = {arXiv preprint arXiv:2604.09980},
  year      = {2026},
  doi       = {10.48550/arXiv.2604.09980},
  url       = {https://arxiv.org/abs/2604.09980}
}
```
- Kaitan: Model 1.6T parameter — kasus ekstrem untuk kuantisasi dan panduan level Q2_K hingga Q4_K_M.

[10] **Mistral Large 3 — Apache 2.0 Granular MoE**
```bibtex
@article{mistral2025large3,
  title     = {Mistral Large 3: Granular MoE with Multimodal Capabilities},
  author    = {Mistral AI},
  journal   = {arXiv preprint arXiv:2512.01820},
  year      = {2025},
  doi       = {10.48550/arXiv.2512.01820},
  url       = {https://arxiv.org/abs/2512.01820}
}
```
- Kaitan: Model 675B parameter dengan Apache 2.0 — relevan untuk panduan kuantisasi model MoE besar.

### SOP Referensi
- WAJIB menyertakan minimal **5 paper jurnal/konferensi** dari 5 tahun terakhir (2021-2026) dengan DOI/arXiv yang valid.
- Setiap data di tabel (perplexity, speed, VRAM) WAJIB diverifikasi terhadap angka di paper asli.
- Jika ada perbedaan data antara paper dan pengukuran ulang penulis, sebutkan deviasi dan metodologi pengukuran yang digunakan.
