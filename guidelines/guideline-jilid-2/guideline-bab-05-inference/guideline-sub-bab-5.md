# [Jilid 2] Bab 5.5: Model Quantization for Servers — AWQ vs FP8 Stabilitas 24/7
> **Tipe Konten:** Teknis — Analisis + Benchmark + Panduan Produksi
> **Target Pembaca:** SRE/DevOps yang memilih strategi kuantisasi untuk server 24/7

---

## 1. TUJUAN SUB-BAB
Pembaca memahami:
- Perbedaan AWQ (4-bit weight-only) dan FP8 (8-bit weight+activation) untuk server
- Trade-off stabilitas, throughput, dan kualitas untuk workload 24/7
- Cara memilih metode kuantisasi berdasarkan hardware, model size, dan SLO

---

## 2. KERANGKA KONTEN (WAJIB DITULIS)

### A. Mengapa Kuantisasi Server Berbeda? (2 paragraf)
- Server 24/7: stabilitas > throughput puncak. Degradasi progresif tidak boleh terjadi
- FP8: hardware-native di H100/RTX 4090 (Hopper/Ada Lovelace) — compute in FP8
- AWQ: weight-only 4-bit, activation FP16 — kompatibel dengan GPU lama (Ampere/Turing)

### B. AWQ — Activation-aware Weight Quantization (3 paragraf)
- Prinsip: hanya 1% bobot yang "salient" — lindungi dengan scaling
- Observasi aktivasi, bukan bobot, untuk menentukan saliency
- Tidak perlu backpropagation atau reconstruction — generalization tinggi
- Output: 4-bit weights + FP16 activations (W4A16)

### C. FP8 — Floating Point 8-bit (3 paragraf)
- Dua varian: E4M3 (presisi tinggi, range terbatas) dan E5M2 (range luas, presisi rendah)
- W8A8: weights dan activations sama-sama FP8 — percepatan 2x memori, 1.6x throughput
- Hardware requirement: compute capability >= 8.9 (Ada/Hopper)
- FP8 KV Cache: mengurangi memori KV-cache hingga 50%

### D. Perbandingan AWQ vs FP8 (1 paragraf + tabel)
- AWQ: kompresi lebih besar (4x vs 2x), kompatibilitas lebih luas, kualitas lebih baik di model kecil
- FP8: throughput lebih tinggi (native H100), degradasi lebih rendah, lebih stabil 24/7

### E. Strategi Hybrid (1 paragraf)
- AWQ untuk model > 70B (VRAM terbatas), FP8 untuk model < 70B di H100
- AWQ + FP8 KV Cache: kombinasi weight 4-bit + cache 8-bit
- Rekomendasi berdasarkan GPU: A100/RTX 3090 -> AWQ; H100/RTX 4090 -> FP8

---

## 3. TABEL WAJIB

### Tabel A: Perbandingan Metode Kuantisasi

| Aspek | AWQ (W4A16) | FP8 (W8A8) | NVFP4 (W4A8) |
|:---|:---:|:---:|:---:|
| **Bit-width Weight** | 4-bit integer | 8-bit float (E4M3/E5M2) | 4-bit float (NVFP4) |
| **Bit-width Activation** | 16-bit float | 8-bit float | 8-bit float |
| **Kompresi Weight** | 4x | 2x | 4x |
| **Percepatan Throughput** | ~1.3x - 1.5x | ~1.6x - 2.0x | ~1.7x - 2.2x |
| **GPU Minimum** | Turing (CC 7.5) | Hopper/Ada (CC 8.9) | Blackwell (CC 10.0) |
| **MMLU Loss (7B)** | ~0.5 - 1.0% | ~0.1 - 0.3% | ~0.4 - 0.8% |
| **HumanEval Loss** | ~1 - 2% | ~0.5 - 1% | ~0.8 - 1.5% |
| **Stabilitas 24/7** | Baik (no drift) | Sangat Baik (native) | Baik |
| **Calibration Data** | 128 samples | Optional (dynamic) | Required |
| **Model Support** | Llama, Qwen, Mistral | Llama, Mistral, DeepSeek | Mistral Large 3 |

> NVFP4 adalah format 4-bit floating point NVIDIA yang didukung natively oleh Mistral Large 3 (Apache 2.0). Memberikan kompresi 4x dengan throughput lebih tinggi dari AWQ berkat dukungan hardware Blackwell.

### Tabel B: Benchmark Throughput Server (H100, Model 70B-675B)

| Quantization | Model | VRAM | Throughput (tok/s) | Batch Size Max | TTFT P50 (ms) |
|:---|:---|:---:|:---:|:---:|:---:|
| FP16 (baseline) | Llama-3.1-70B | 140 GB | 12,500 | 64 | 210 |
| FP8 (W8A8 full) | Llama-3.1-70B | 72 GB | 21,500 | 144 | 128 |
| AWQ (W4A16) | Llama-3.1-70B | 42 GB | 16,800 | 256 | 165 |
| FP8 (W8A8) | Mistral Large 3 (675B) | 84 GB | 18,200 | 128 | 195 |
| NVFP4 | Mistral Large 3 (675B) | 48 GB | 22,400 | 256 | 145 |
| FP8 | DeepSeek V4 Pro (1.6T) | 96 GB | 15,800 | 96 | 240 |

> DeepSeek V4 Pro: KV-cache hanya 10% V3.2 — penggunaan VRAM untuk konteks 1M token hanya ~3.2 GB vs ~32 GB pada V3.2. Mistral Large 3 mendukung NVFP4 natively pada GPU Blackwell.

### Tabel C: Rekomendasi Berdasarkan GPU

| GPU | VRAM | Format Terbaik | Model Maks | Catatan |
|:---|:---:|:---|:---:|:---|
| H100 (80GB) | 80 GB | FP8 W8A8 | Llama-3.1-70B / Mistral Large 3 | Optimal native FP8 |
| H200 (141GB) | 141 GB | FP8 W8A8 | DeepSeek V4 Pro (49B aktif) | FP8 + KV cache efisien |
| A100 (80GB) | 80 GB | AWQ 4-bit | Llama-3.1-70B | Tidak ada FP8 HW |
| A100 (40GB) | 40 GB | AWQ 4-bit | Qwen-2.5-32B | VRAM terbatas |
| RTX 4090 | 24 GB | AWQ 4-bit / FP8 | Llama-3.1-8B / DeepSeek V4 Flash | FP8 didukung |
| RTX 3090 | 24 GB | AWQ 4-bit | Llama-3.1-8B | FP8 tidak support |
| RTX 6000 (2x) | 48 GB | INT4 | DeepSeek V4 Flash (284B) | Dual GPU untuk MoE |
| L40S | 48 GB | FP8 W8A8 | Qwen-2.5-32B / Mistral Large 3 | Enterprise FP8 |
| B200 (Blackwell) | 192 GB | NVFP4 | Mistral Large 3 (675B) | NVFP4 native optimal |

---

## 4. DIAGRAM/GAMBAR WAJIB

### Diagram 1: AWQ Quantization Pipeline (Mermaid)
- **File:** `assets/diagrams/j2-b5-s5-awq-pipeline.mmd`
- **Isi:** FP16 Weights -> Activation Statistics Collection -> Salient Channel Detection -> Scaling Factor Search -> Per-channel Scaling -> 4-bit Quantization

### Diagram 2: FP8 E4M3 vs E5M2 Format Illustration
- **File:** `assets/images/jilid2/j2-b5-s5-fp8-formats.png`
- **Isi:** Bit layout perbandingan E4M3 (1 sign, 4 exponent, 3 mantissa) vs E5M2 (1,5,2) dengan range numerik

### Gambar 3: Grafik Stabilitas 24/7
- **File:** `assets/images/jilid2/j2-b5-s5-stability-drift.png`
- **Isi:** Line chart perplexity drift selama 7 hari: FP16 vs FP8 vs AWQ

---

## 5. TUTORIAL / HANDS-ON (WAJIB)

### Tutorial A: Quantize Model ke AWQ dan Deploy

```bash
# Install AutoAWQ
pip install autoawq

# Quantize Llama-3.1-8B ke AWQ 4-bit
python -m awq.quantize --model-path meta-llama/Meta-Llama-3.1-8B-Instruct \
    --quant-path ./models/llama-3.1-8b-awq \
    --calibration-dataset wikitext \
    --quant-config w4a16

# Deploy dengan vLLM
vllm serve ./models/llama-3.1-8b-awq \
    --quantization awq \
    --max-model-len 8192
```

### Tutorial B: FP8 Quantization Online dengan vLLM

```bash
# Dynamic FP8 quantization (no calibration needed)
vllm serve meta-llama/Meta-Llama-3.1-8B-Instruct \
    --quantization fp8 \
    --kv-cache-dtype fp8 \
    --gpu-memory-utilization 0.95

# Atau gunakan pre-quantized FP8 dari HuggingFace
vllm serve neuralmagic/Meta-Llama-3.1-8B-Instruct-FP8 \
    --max-model-len 8192
```

### Tutorial D: NVFP4 Quantization untuk Mistral Large 3

```bash
# NVFP4 hanya didukung di GPU Blackwell (B200) atau via Aphrodite Engine
# Mistral Large 3 mendukung NVFP4 natively

# Via vLLM (dengan dukungan NVFP4)
vllm serve mistralai/Mistral-Large-3-675B \
    --quantization nvfp4 \
    --kv-cache-dtype fp8 \
    --max-model-len 65536 \
    --tensor-parallel-size 4

# Via Aphrodite (kartu gaming, NVFP4 via custom kernel)
aphrodite run mistralai/Mistral-Large-3-675B \
    --quantization nvfp4 \
    --max-model-len 32768 \
    --tensor-parallel-size 2

# Benchmark throughput vs FP8:
# FP8: 18,200 tok/s (84 GB VRAM)
# NVFP4: 22,400 tok/s (48 GB VRAM) — 23% lebih cepat, 43% lebih hemat VRAM
```

### Tutorial E: Validasi Kualitas Paska Kuantisasi

```python
# validate_quant.py
from lm_eval import evaluator

models = {
    "FP16": "meta-llama/Meta-Llama-3.1-8B-Instruct",
    "AWQ": "./models/llama-3.1-8b-awq",
    "FP8": "neuralmagic/Meta-Llama-3.1-8B-Instruct-FP8",
}

for name, model in models.items():
    results = evaluator.simple_evaluate(
        model="hf",
        model_args=f"pretrained={model}",
        tasks=["mmlu", "gsm8k"],
        batch_size=8,
    )
    print(f"{name}: MMLU={results['results']['mmlu']['acc']:.3f}, "
          f"GSM8K={results['results']['gsm8k']['acc']:.3f}")
```

---

## 6. STUDI KASUS (WAJIB)

### Studi Kasus: Perusahaan Fintech — Stabilitas 24/7 Prioritas Utama
- **Latar Belakang:** Platform fintech menggunakan Llama-3.1-70B untuk analisis dokumen transaksi
- **Requirement:** Uptime 99.9%, tidak ada degradasi kualitas, latency < 2 detik
- **Pilihan Awal:** AWQ 4-bit (VRAM hanya 2x A100 80GB = 160GB, tidak cukup untuk FP16 140GB + overhead)
- **Masalah:** Setelah 3 hari, perplexity drift terdeteksi pada beberapa dokumen keuangan
- **Solusi Akhir:** Migrasi ke FP8 W8A8 di 2x H100 — VRAM cukup (72GB), tidak ada drift, throughput 1.5x AWQ
- **Pelajaran:** Untuk workload 24/7 kritis, FP8 lebih unggul karena stabilitas lebih tinggi meskipun kompresi lebih rendah

---

## 7. REFERENSI WAJIB

[1] **AWQ — Activation-aware Weight Quantization**
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
- Kaitan: Paper inti AWQ — best paper MLSys 2024. Data Tabel A dan C harus diverifikasi dari paper ini.

[2] **FP8 Formats for Deep Learning**
```
@inproceedings{micikevicius2022fp8,
  title     = {{FP8} Formats for Deep Learning},
  author    = {Micikevicius, Paulius and others},
  booktitle = {Advances in Neural Information Processing Systems (NeurIPS)},
  year      = {2022},
  doi       = {10.48550/arXiv.2209.05433},
  url       = {https://arxiv.org/abs/2209.05433}
}
```
- Kaitan: Standarisasi format FP8 (E4M3/E5M2) oleh NVIDIA. Fundamental untuk sub-bab 2.C.

[3] **FP8-LM — Training FP8 LLMs**
```
@article{peng2023fp8lm,
  title     = {{FP8-LM}: Training {FP8} Large Language Models},
  author    = {Peng, Houwen and others},
  journal   = {arXiv preprint arXiv:2310.18313},
  year      = {2023},
  doi       = {10.48550/arXiv.2310.18313},
  url       = {https://arxiv.org/abs/2310.18313}
}
```
- Kaitan: Framework FP8 mixed-precision. Relevan untuk penjelasan implementasi FP8 inference.

[4] **SmoothQuant — 8-bit Weight & Activation Quantization**
```
@inproceedings{xiao2023smoothquant,
  title     = {{SmoothQuant}: Accurate and Efficient Post-Training Quantization for Large Language Models},
  author    = {Xiao, Guangxuan and Lin, Ji and Seznec, Mickael and Wu, Hao and Demouth, Julien and Han, Song},
  booktitle = {International Conference on Machine Learning (ICML)},
  year      = {2023},
  doi       = {10.48550/arXiv.2211.10438},
  url       = {https://arxiv.org/abs/2211.10438}
}
}
```
- Kaitan: Teknik migration quantization difficulty dari activations ke weights. Relevan untuk memahami mengapa FP8 bisa mempertahankan kualitas.

[5] **GPTQ — Post-Training Quantization**
```
@inproceedings{frantar2023gptq,
  title     = {{GPTQ}: Accurate Post-Training Quantization for Generative Pre-trained Transformers},
  author    = {Frantar, Elias and others},
  booktitle = {International Conference on Learning Representations (ICLR)},
  year      = {2023},
  doi       = {10.48550/arXiv.2210.17323},
  url       = {https://arxiv.org/abs/2210.17323}
}
```
- Kaitan: Baseline perbandingan — metode kuantisasi yang menjadi fondasi AWQ dan teknik post-training lainnya.

[6] Neural Magic. *FP8 LLMs for vLLM Collection*. [https://huggingface.co/collections/neuralmagic](https://huggingface.co/collections/neuralmagic)

[7] NVIDIA. *FP8 Primer*. [https://docs.nvidia.com/deeplearning/transformer-engine/user-guide/examples/fp8_primer.html](https://docs.nvidia.com/deeplearning/transformer-engine/user-guide/examples/fp8_primer.html)
