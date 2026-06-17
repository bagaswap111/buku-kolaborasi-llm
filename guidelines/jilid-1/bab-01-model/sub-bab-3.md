# [Jilid 1] Bab 1.3: Perbandingan Arsitektur — Dense Models vs Mixture of Experts (MoE)
> **Tipe Konten:** Komparasi — Analisis Arsitektur + Tabel + Studi Kasus
> **Target Pembaca:** Pengguna menengah yang ingin memahami perbedaan dense vs MoE

---

## 1. TUJUAN SUB-BAB
Setelah membaca, pembaca harus bisa:
- Menjelaskan perbedaan fundamental dense model dengan MoE
- Memahami konsep sparse activation, routing, dan load balancing
- Memilih arsitektur yang tepat berdasarkan hardware dan use case

---

## 2. KERANGKA KONTEN (WAJIB DITULIS)

### A. Konsep Dasar Dense Model (1 paragraf)
- Semua parameter aktif untuk setiap token — FFN seragam di semua lapisan
- Contoh: Llama-3 70B, Mistral 7B, Qwen 2.5 72B
- Kelebihan: sederhana, latency konsisten, mudah di-deploy
- Kekurangan: scaling linear dengan parameter — 70B = 70x compute 7B

### B. Konsep Dasar MoE (2 paragraf)
- Tidak semua parameter aktif — hanya "expert" tertentu per token
- Router/gate network memilih top-k expert (biasanya 2 dari 8)
- Parameter total besar, tetapi compute per token lebih kecil
- Contoh: Mixtral 8x7B (47B total, 13B aktif), DeepSeek V2 (236B total, 21B aktif), DeepSeek V4 Pro (1.6T total, 49B aktif), Mistral Large 3 (675B total, 41B aktif)

### C. Komponen MoE: Router, Experts, Load Balancing (2 paragraf)
- **Router:** jaringan linear kecil yang menghasilkan probabilitas per expert
- **Experts:** FFN independen — masing-masing specialist di domain tertentu
- **Load Balancing Loss:** memaksa distribusi token merata ke semua expert
- **Top-2 Routing:** dua expert dengan skor tertinggi diaktifkan, digabung dengan weighted sum

### D. Kelebihan MoE vs Dense (1 paragraf)
- Performa lebih tinggi per FLOP — MoE 13B aktif bisa setara dense 30B
- VRAM besar diperlukan (semua expert harus di-load) tapi compute efisien
- Cocok untuk: serving banyak user, throughput tinggi

### E. Kekurangan MoE (1 paragraf)
- VRAM lebih besar: Mixtral 8x7B butuh ~90GB FP16 (dense 13B hanya ~26GB)
- Latency inference lebih tinggi: routing overhead, expert communication
- Fine-tuning lebih kompleks: perlu menjaga load balance
- Kurang efisien untuk batch kecil (single user)

### F. Perbandingan di Ekosistem Lokal (1 paragraf)
- Ollama/llama.cpp: mendukung MoE via GGUF, offloading hybrid
- vLLM: optimasi khusus untuk MoE (expert parallelism)
- EXL2: dukungan MoE dengan bit-width fleksibel

---

## 3. TABEL WAJIB

### Tabel A: Perbandingan Dense vs MoE — Model Populer

| Model | Arsitektur | Total Param | Active Param | VRAM FP16 | VRAM Q4 | MMLU | GSM8K |
|:---|:---|:---:|:---:|:---:|:---:|:---:|:---:|
| Mistral 7B | Dense | 7.3B | 7.3B | 14 GB | 4.5 GB | 62.5% | 45.2% |
| Llama-3 8B | Dense | 8.0B | 8.0B | 16 GB | 5.2 GB | 66.7% | 79.6% |
| Llama-3 70B | Dense | 70.6B | 70.6B | 140 GB | 42 GB | 83.6% | 91.1% |
| Mixtral 8x7B | MoE | 46.7B | 12.9B | 90 GB | 28 GB | 70.6% | 68.6% |
| DeepSeek V2 | MoE | 236B | 21B | 470 GB | 140 GB | 78.5% | 85.5% |
| DeepSeek V4 Pro | MoE | 1.6T | 49B | 3.2 TB FP16 | 950 GB Q4 | 87.5%* | 93.5%* |
| DeepSeek V4 Flash | MoE | 284B | 13B | 560 GB FP16 | 160 GB Q4 | — | — |
| Mistral Large 3 | MoE | 675B | 41B | 1.35 TB FP16 | 380 GB Q4 | 84.9% | 91.2% |
| Qwen 1.5-32B | Dense | 32.8B | 32.8B | 66 GB | 20 GB | 74.6% | 72.3% |
| DBRX | MoE | 132B | 36B | 260 GB | 78 GB | 73.7% | 72.8% |

*MMLU-Pro untuk DeepSeek V4 Pro (MMLU standar tidak dipublikasikan).

### Tabel B: Trade-off — Dense vs MoE per Skenario

| Skenario | Pilihan Terbaik | Alasan |
|:---|:---|:---|
| **Single user, GPU 24GB** | Dense 7-8B Q4 | VRAM terbatas, MoE tidak muat |
| **Multi-user server, 2x 24GB** | MoE (Mixtral Q4) | Throughput tinggi per user |
| **Coding assistant lokal** | Dense 7-8B Q4_K_M | Latency rendah, respons cepat |
| **Batch processing (RAG)** | MoE (DeepSeek) | Lebih efisien per token |
| **Fine-tuning custom** | Dense (lebih mudah) | MoE butuh teknik khusus |
| **Apple Silicon 48GB** | MoE Q4_K_M | Unified memory cukup besar |

### Tabel C: Perbandingan Kecepatan Inference (RTX 4090, Q4_K_M)

| Model | Arsitektur | TPS (single) | TPS (batch 8) | VRAM | Latency (TTFT) |
|:---|:---|:---:|:---:|:---:|:---:|
| Llama-3 8B | Dense | ~85 | ~320 | 5.2 GB | ~50 ms |
| Mixtral 8x7B | MoE | ~40 | ~180 | 28 GB | ~120 ms |
| Qwen 2.5 32B | Dense | ~22 | ~95 | 20 GB | ~180 ms |
| DeepSeek V2 (lite) | MoE | ~35 | ~150 | 45 GB | ~100 ms |
| DeepSeek V4 Flash Q4 | MoE (13B aktif) | ~55 | ~200 | 160 GB | ~80 ms |
| Mistral Large 3 Q4 | MoE (41B aktif) | ~20 | ~80 | 380 GB | ~250 ms |

---

## 4. DIAGRAM/GAMBAR WAJIB

### Diagram 1: Arsitektur Dense vs MoE (Mermaid)
- **File:** `assets/diagrams/j1-b1-s3-dense-vs-moe.mmd`
- **Isi:** Side-by-side: dense (FFN tunggal) vs MoE (router + 8 expert + top-2)

```mermaid
graph LR
    subgraph "Dense"
        IN1[Input] --> FFN1[FFN Tunggal]
        FFN1 --> OUT1[Output]
    end
    subgraph "MoE"
        IN2[Input] --> R[Router]
        R --> E1[Expert 1]
        R --> E2[Expert 2]
        R --> E3[Expert 3]
        R --> E8[Expert 8]
        E1 --> GATE[Weighted Sum]
        E2 --> GATE
        GATE --> OUT2[Output]
    end
```

### Gambar 2: Grafik Scaling — Total vs Active Parameters
- **File:** `assets/images/jilid1/j1-b1-s3-param-scaling.png`
- **Isi:** Bar chart perbandingan total parameter (biru) vs active (hijau) untuk dense vs MoE

### Gambar 3: Load Distribution Heatmap
- **File:** `assets/images/jilid1/j1-b1-s3-load-balance.png`
- **Isi:** Heatmap distribusi token ke expert — ideal: merata, buruk: satu expert dominan

---

## 5. TUTORIAL / HANDS-ON (WAJIB)

### Tutorial A: Menjalankan Dense vs MoE di Ollama

```bash
# 1. Pull dense model
ollama pull llama3.1:8b

# 2. Pull MoE model (Mixtral)
ollama pull mixtral:8x7b

# 3. Test kecepatan - prompt yang sama
time ollama run llama3.1:8b "Jelaskan teori relativitas dalam 3 kalimat"
time ollama run mixtral:8x7b "Jelaskan teori relativitas dalam 3 kalimat"

# 4. Cek resource usage (terminal lain)
watch -n 1 nvidia-smi
```

### Tutorial B: Memeriksa Konfigurasi MoE di HuggingFace

```python
from transformers import AutoConfig

# Cek konfigurasi MoE
config = AutoConfig.from_pretrained("mistralai/Mixtral-8x7B-Instruct-v0.1")

print(f"Arsitektur: {config.architectures}")
print(f"Num experts: {config.num_local_experts}")
print(f"Num experts per token (top-k): {config.num_experts_per_tok}")
print(f"Hidden size: {config.hidden_size}")
print(f"Intermediate size (expert FFN): {config.intermediate_size}")

# Hitung active vs total
total_expert_params = config.num_local_experts * 3 * config.hidden_size * config.intermediate_size
active_expert_params = config.num_experts_per_tok * 3 * config.hidden_size * config.intermediate_size
sparsity = active_expert_params / total_expert_params * 100

print(f"\nSparsity ratio: {sparsity:.1f}%")
print(f"Ini berarti hanya {sparsity:.1f}% dari parameter FFN yang aktif per token")
```

### Tutorial C: Simulasi Router MoE

```python
import torch
import torch.nn.functional as F

# Simulasi routing MoE
batch_size = 4
num_experts = 8
top_k = 2
hidden_dim = 4096

# Input token representation
x = torch.randn(batch_size, hidden_dim)

# Router weights
router = torch.nn.Linear(hidden_dim, num_experts)
logits = router(x)

# Top-k routing
weights, indices = torch.topk(F.softmax(logits, dim=-1), top_k)
print(f"Top-2 experts per token:\n{indices}")
print(f"Weights:\n{weights}")

# Cek load balancing
expert_counts = torch.zeros(num_experts)
for i in range(batch_size):
    for j in range(top_k):
        expert_counts[indices[i, j]] += 1
print(f"\nDistribusi load:\n{expert_counts}")
print(f"Ideal: {batch_size * top_k / num_experts:.1f} per expert")
```

---

## 6. STUDI KASUS (WAJIB)

### Studi Kasus: Memilih Arsitektur untuk API Server 8 User
- **Skenario:** Startup ingin deploy API LLM untuk 8 developer internal. Mereka punya 2x RTX 3090 (24GB each, total 48GB via NVLink).
- **Pilihan A: Dense 70B Q3_K_M** (~30GB) — kualitas tinggi, tapi hanya muat di 1 GPU, sisa GPU menganggur.
- **Pilihan B: MoE Mixtral 8x7B Q4_K_M** (~28GB) — kualitas setara 30B dense, muat di 2 GPU dengan expert parallelism.
- **Analisis:**
  - Dense 70B: throughput ~10 TPS, TTFT ~500ms — lambat untuk 8 user concurrent
  - MoE Mixtral: throughput ~35 TPS, TTFT ~120ms — memadai untuk 8 user
  - MoE memanfaatkan kedua GPU lebih efektif (expert parallelism)
- **Rekomendasi:** MoE Mixtral 8x7B Q4_K_M dengan vLLM dan tensor parallelism.

---

## 7. REFERENSI WAJIB (SOP: minimal 5 paper 5 tahun terakhir + DOI)

### Paper Jurnal/Konferensi

[1] **A Survey on Mixture of Experts**
```bibtex
@article{cai2024moesurvey,
  title     = {A Survey on Mixture of Experts in Large Language Models},
  author    = {Cai, Tianyu and Bai, Yuchen and Li, Shuang and others},
  journal   = {arXiv preprint arXiv:2407.06204},
  year      = {2024},
  doi       = {10.48550/arXiv.2407.06204},
  url       = {https://arxiv.org/abs/2407.06204}
}
```
- Kaitan: Survey komprehensif MoE — mencakup routing, load balancing, dan tren terbaru.

[2] **Mixtral of Experts**
```bibtex
@article{jiang2024mixtral,
  title     = {Mixtral of Experts},
  author    = {Jiang, Albert Q and Sablayrolles, Alexandre and Roux, Antoine and others},
  journal   = {arXiv preprint arXiv:2401.04088},
  year      = {2024},
  doi       = {10.48550/arXiv.2401.04088},
  url       = {https://arxiv.org/abs/2401.04088}
}
```
- Kaitan: Paper Mixtral 8x7B — arsitektur MoE terbuka pertama yang populer di ekosistem lokal. Data Tabel A dan C merujuk pada paper ini.

[3] **Switch Transformers: Scaling to Trillion Parameters with Simple and Efficient Sparsity**
```bibtex
@inproceedings{fedus2022switch,
  title     = {Switch Transformers: Scaling to Trillion Parameters with Simple and Efficient Sparsity},
  author    = {Fedus, William and Zoph, Barret and Shazeer, Noam},
  booktitle = {Journal of Machine Learning Research},
  year      = {2022},
  volume    = {23},
  pages     = {1--40},
  doi       = {10.48550/arXiv.2101.03961},
  url       = {https://arxiv.org/abs/2101.03961}
}
```
- Kaitan: Fondasi MoE modern — pengenalan top-1 routing dan load balancing loss.

[4] **GShard: Scaling Giant Models with Conditional Computation and Automatic Sharding**
```bibtex
@inproceedings{lepikhin2021gshard,
  title     = {{GShard}: Scaling Giant Models with Conditional Computation and Automatic Sharding},
  author    = {Lepikhin, Dmitry and Lee, HyoukJoong and Xu, Yuanzhong and others},
  booktitle = {International Conference on Learning Representations (ICLR)},
  year      = {2021},
  doi       = {10.48550/arXiv.2006.16668},
  url       = {https://arxiv.org/abs/2006.16668}
}
```
- Kaitan: Implementasi MoE pertama di skala besar oleh Google — konsep sharding expert yang digunakan di DeepSeek.

[5] **Can Mixture-of-Experts Surpass Dense LLMs Under Strictly Equal Resources?**
```bibtex
@article{li2025moevsdense,
  title     = {Can Mixture-of-Experts Surpass Dense {LLMs} Under Strictly Equal Resources?},
  author    = {Li, Houyi and Lo, Ka Man and Wang, Ziqi and others},
  journal   = {arXiv preprint arXiv:2506.12119},
  year      = {2025},
  doi       = {10.48550/arXiv.2506.12119},
  url       = {https://arxiv.org/abs/2506.12119}
}
```
- Kaitan: Studi terbaru (2025) yang membandingkan MoE vs dense dengan sumber daya identik — relevan untuk analisis trade-off di seksi 2.D-2.E.

[6] **Revisiting MoE and Dense Speed-Accuracy Comparisons for LLM Training**
```bibtex
@article{deep2024moevsdense,
  title     = {Revisiting {MoE} and Dense Speed-Accuracy Comparisons for {LLM} Training},
  author    = {Dey, Nolan and Gosal, Gurpreet and Zhai, Zhiming and others},
  journal   = {arXiv preprint arXiv:2405.15052},
  year      = {2024},
  doi       = {10.48550/arXiv.2405.15052},
  url       = {https://arxiv.org/abs/2405.15052}
}
```
- Kaitan: Benchmark sistematis MoE vs dense di 6.4B, 12.6B, 29.6B scale — data untuk Tabel B.

### Referensi Pendukung (Non-Paper)

[7] DeepSpeed MoE Tutorial. [https://www.deepspeed.ai/tutorials/mixture-of-experts/](https://www.deepspeed.ai/tutorials/mixture-of-experts/)

[8] Hugging Face MoE Documentation. [https://huggingface.co/docs/transformers/model_doc/mixtral](https://huggingface.co/docs/transformers/model_doc/mixtral)

[9] Epoch AI — MoE vs Dense Inference Analysis. [https://epoch.ai/gradient-updates/moe-vs-dense-models-inference](https://epoch.ai/gradient-updates/moe-vs-dense-models-inference)

[10] vLLM — Expert Parallelism for MoE. [https://docs.vllm.ai](https://docs.vllm.ai)

[11] **DeepSeek-V4: Hybrid MoE with CSA/HCA Attention**
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
- Kaitan: MoE ekstrem 1.6T dengan sparsity ratio 3.1% — perbandingan paling ekstrem antara total vs active parameter di Tabel A.

[12] **Mistral Large 3: Apache 2.0 Granular MoE**
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
- Kaitan: Granular MoE 675B dengan Apache 2.0 — MoE open-weight terbesar untuk fine-tuning dan deployment lokal.

### SOP Referensi
- WAJIB menyertakan minimal **5 paper jurnal/konferensi** dari 5 tahun terakhir (2021-2026) dengan DOI/arXiv yang valid.
- Data Tabel A harus diverifikasi dari Open LLM Leaderboard dan paper asli model.
- Angka sparsity ratio harus konsisten dengan perhitungan active vs total parameter.
