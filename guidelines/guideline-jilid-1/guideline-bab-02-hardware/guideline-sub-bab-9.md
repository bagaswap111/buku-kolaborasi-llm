# [Jilid 1] Bab 2.9: NPU (Neural Processing Unit) — Masa Depan AI PC
> **Tipe Konten:** Prospektif — Teknologi Baru + Analisis
> **Target Pembaca:** Pengguna yang mempertimbangkan laptop AI PC untuk LLM lokal

---

## 1. TUJUAN SUB-BAB
Pembaca memahami:
- Arsitektur NPU dan perannya dalam ekosistem AI PC
- Perbandingan NPU Intel (Core Ultra), Qualcomm (Snapdragon X Elite), AMD (Ryzen AI)
- Kapan NPU berguna untuk LLM — dan kapan GPU tetap diperlukan

---

## 2. KERANGKA KONTEN (WAJIB DITULIS)

### A. Apa Itu NPU? (1 paragraf)
- NPU = Neural Processing Unit — akselerator AI dedicated di SoC
- Berbeda dari GPU: NPU dirancang untuk inferensi low-power, throughput menengah
- Arsitektur: dataflow systolic array untuk matriks INT8/INT4, efisiensi 10-20 TOPS/W
- Muncul di: Intel Core Ultra (Meteor Lake/Lunar Lake), Snapdragon X Elite, AMD Ryzen AI (Strix Point)

### B. Generasi NPU 2024-2026 (1 paragraf + tabel)
- Intel Meteor Lake: NPU 11 TOPS (AI Boost)
- Intel Lunar Lake: NPU 40-48 TOPS (Copilot+ ready)
- Qualcomm Snapdragon X Elite: Hexagon NPU 45 TOPS
- AMD Ryzen AI 300 (Strix Point): XDNA 2 NPU 50 TOPS
- Apple Neural Engine (ANE): 16-core di M4, ~38 TOPS

### C. NPU untuk LLM Inference — Realitas vs Hype (2 paragraf)
- NPU bisa menjalankan LLM (Llama-3.1-8B INT4) tapi sangat lambat: ~3.5 detik/token (Intel NPU)
- Dibandingkan GPU laptop: iGPU Intel Arc ~20 t/s, NPU ~0.3 t/s — GPU 66x lebih cepat
- Framework NITRO: NPU inference untuk transformers — 10x speedup vs vanilla OpenVINO
- llm.npu: hybrid NPU-CPU-GPU — 22.4x prefill speedup via prompt chunking + outlier detection
- T-MAC: CPU via table lookup mencapai 12.6 t/s di Snapdragon X Elite — mengalahkan NPU (10.4 t/s)

### D. Arsitektur Heterogen — CPU + GPU + NPU (1 paragraf)
- Agent.xpu: scheduling cerdas antara iGPU + NPU untuk agent workloads — 1.2-2.4x throughput vs iGPU-only
- NPU cocok untuk: prefill ringan, wake-word detection, background agent, continuous listening
- GPU/CPU untuk: LLM decoding berat, rendering, creative generation
- Intel Core Ultra: OpenVINO mengelola pemilihan hardware otomatis

### E. Matriks Komparasi NPU (1 paragraf + tabel)
- TOPS (INT8): metrik kasar, tidak selalu linear dengan performa LLM
- Memory bandwidth: NPU berbagi bandwidth dengan CPU/iGPU via shared memory
- Software stack: Qualcomm QNN vs Intel OpenVINO vs AMD Vitis AI

### F. Masa Depan (1 paragraf)
- Microsoft Copilot+: syarat minimal NPU 40 TOPS — mendorong adopsi massal
- 2026: NPU 100+ TOPS (Intel Panther Lake, AMD下一代)
- NPU belum bisa menggantikan GPU untuk LLM lokal; perannya sebagai co-processor untuk offload tugas ringan
- Model frontier 2026 (DeepSeek V4 Pro 1.6T, Mistral Large 3 675B, GPT-5.5, Claude Fable 5) sama sekali tidak feasible di NPU — membutuhkan GPU HBM atau Apple Silicon unified memory dengan bandwidth >500 GB/s
- Prediksi: NPU + iGPU hybrid akan cukup untuk SLM (3B-8B) dalam 2-3 tahun

---

## 3. TABEL WAJIB

### Tabel A: Spesifikasi NPU di AI PC (2024-2026)

| Platform | NPU Name | INT8 TOPS | Copilot+? | Arsitektur | Software Stack | Harga Laptop Mulai |
|:---|---:|---:|:---|:---|---:|
| **Intel Core Ultra 7 155H** | Intel AI Boost | 11 | Tidak (TPM <40) | Meteor Lake | OpenVINO | ~Rp 12 jt |
| **Intel Core Ultra 9 288V** | Intel AI Boost | 48 | Ya | Lunar Lake | OpenVINO | ~Rp 25 jt |
| **Qualcomm Snapdragon X Elite** | Hexagon NPU | 45 | Ya | Custom ARM | QNN / NPE | ~Rp 18 jt |
| **Qualcomm Snapdragon X Plus** | Hexagon NPU | 45 | Ya | Custom ARM | QNN / NPE | ~Rp 15 jt |
| **AMD Ryzen AI 9 HX 370** | XDNA 2 | 50 | Ya | Strix Point | Vitis AI / Ryzen AI SW | ~Rp 22 jt |
| **Apple M4** | Neural Engine 16c | ~38 | Tidak (macOS) | Apple Silicon | CoreML / ANE | ~Rp 18 jt |
| **Apple M4 Pro** | Neural Engine 16c | ~38 | Tidak (macOS) | Apple Silicon | CoreML / ANE | ~Rp 25 jt |

### Tabel B: Benchmark LLM Inference NPU vs GPU Laptop

| Device | Framework | Model | Tokens/s | Daya | TOPS | Efisiensi (t/s/W) |
|:---|---:|---:|---:|---:|---:|---:|
| **Intel NPU (Meteor Lake)** | NITRO/OpenVINO | Llama-3-8B INT4 | ~0.3 t/s | 15W (NPU) | 11 | 0.02 |
| **Intel NPU + CPU hybrid** | Agent.xpu | Llama-3-8B W8A16 | ~5 t/s | 28W (total) | 11 | 0.18 |
| **Intel Arc iGPU (Lunar Lake)** | OpenVINO | Llama-3-8B INT4 | ~22 t/s | 35W (iGPU) | 67 (GPU) | 0.63 |
| **Snapdragon X Elite NPU** | QNN | Llama-2-7B INT4 | ~10.4 t/s | 12W (NPU) | 45 | 0.87 |
| **Snapdragon CPU (T-MAC)** | T-MAC (2 core) | Llama-2-7B W4 | ~12.6 t/s | 8W (CPU) | - | 1.58 |
| **AMD Ryzen AI NPU** | Vitis AI | Llama-3-8B INT4 | ~5 t/s | 20W (NPU) | 50 | 0.25 |
| **Apple M4 GPU (MLX)** | MLX | Llama-3.1-8B 4bit | ~60 t/s | ~30W (GPU) | - | 2.00 |
| **RTX 4090 Laptop** | CUDA/llama.cpp | Llama-3.1-8B Q4 | ~80 t/s | ~120W (GPU) | - | 0.67 |

### Tabel C: Komparasi Software Stack NPU

| Aspek | Intel OpenVINO | Qualcomm QNN | AMD Vitis AI | Apple CoreML |
|:---|:---|:---|:---|:---|
| **Model Format** | IR (Intermediate Rep) | QNN C++/C API | XIR / ONNX | .mlpackage |
| **LLM Support** | Ya (via optimum-intel) | Terbatas (NITRO) | Eksperimental | Ya (via MLX) |
| **Kemudahan Setup** | Sedang | Sulit | Sulit | Mudah |
| **Quantization** | INT8, INT4 | INT8 | INT8, INT4 | FP16, INT8 |
| **Dynamic Shapes** | Terbatas | Tidak | Tidak | Ya (via ANE) |
| **Open Source** | Ya | Tidak | Sebagian | Tidak |
| **Kematangan** | Tinggi (2024.6+) | Rendah | Rendah | Tinggi |

---

## 4. DIAGRAM/GAMBAR WAJIB

### Diagram 1: Arsitektur Heterogen SoC AI PC (Mermaid)
- **File:** `assets/diagrams/j1-b2-s9-soc-heterogen.mmd`
- **Isi:** Diagram blok SoC: CPU (P-core + E-core) ↔ Shared Memory ← NPU (systolic array) ← iGPU (Xe-core/Adreno). Garis warna menunjukkan alur data untuk inferensi hybrid.

### Gambar 2: Grafik Perbandingan TOPS NPU per Generasi
- **File:** `assets/images/jilid1/j1-b2-s9-npu-tops-evolution.png`
- **Isi:** Bar chart evolusi TOPS NPU: Meteor Lake 11 → Lunar Lake 48 → Panther Lake (prediksi 100+) sepanjang sumbu waktu 2023-2026

---

## 5. TUTORIAL / HANDS-ON (WAJIB)

### Tutorial A: Jalankan LLM di NPU Intel dengan NITRO

```bash
# 1. Install OpenVINO 2024.6+
pip install openvino openvino_genai

# 2. Clone NITRO
git clone https://github.com/abdelfattah-lab/nitro
cd nitro

# 3. Download model Llama-3.2-3B INT4
optimum-cli export openvino -m meta-llama/Llama-3.2-3B-Instruct \
    --weight-format int4 Llama-3.2-3B-INT4

# 4. Jalankan di NPU
python nitro/run_npu.py \
    --model_path ./Llama-3.2-3B-INT4 \
    --device NPU \
    --prompt "Saya adalah asisten AI"

# 5. Bandingkan dengan CPU
python nitro/run_npu.py \
    --model_path ./Llama-3.2-3B-INT4 \
    --device CPU \
    --prompt "Saya adalah asisten AI"
```

### Tutorial B: Hybrid NPU + CPU + GPU dengan Agent.xpu

```bash
# 1. Install Agent.xpu (Intel Core Ultra required)
pip install agent-xpu openvino

# 2. Optimasi model untuk heterogen compute
python -c "
from agent_xpu import HeterogeneousScheduler
from transformers import AutoTokenizer

model_id = 'meta-llama/Llama-3.2-3B-Instruct'

# Scheduler otomatis: prefill di NPU, decode di iGPU
scheduler = HeterogeneousScheduler(
    model_id=model_id,
    prefill_device='NPU',  # NPU untuk prefill ringan
    decode_device='GPU',   # iGPU untuk decode
    precision='int4'
)

tokenizer = AutoTokenizer.from_pretrained(model_id)
inputs = tokenizer('Jelaskan cara kerja NPU', return_tensors='pt')
outputs = scheduler.generate(**inputs, max_new_tokens=100)
print(tokenizer.decode(outputs[0]))
"
```

### Tutorial C: Test T-MAC di Snapdragon X Elite

```bash
# 1. Clone T-MAC
git clone https://github.com/microsoft/T-MAC
cd T-MAC
pip install -r requirements.txt

# 2. Benchmark Llama-2-7B 4-bit via CPU T-MAC
python tools/bench_e2e.py \
    --model llama-2-7b-4bit \
    --num_threads 4 \
    --prompt_len 1024 \
    --gen_len 1024

# Output: ~18-22 t/s (Snapdragon X Elite, 4 core)
# Bandingkan: NPU via QNN hanya ~10.4 t/s
```

---

## 6. STUDI KASUS (WAJIB)

### Studi Kasus: Memilih Laptop AI PC untuk LLM Lokal
- **Skenario:** Mahasiswa AI butuh laptop untuk coding assistant lokal (Llama-3.1-8B) dengan budget Rp 20-25 jt
- **Opsi A:** Intel Core Ultra 9 288V (Lunar Lake) — NPU 48 TOPS + Arc iGPU + 32GB RAM
- **Opsi B:** Snapdragon X Elite — NPU 45 TOPS + Adreno iGPU + 32GB RAM
- **Opsi C:** MacBook Pro M4 Pro — GPU 20-core + 24GB unified memory + Neural Engine
- **Analisis:**
  - NPU di opsi A/B sangat lambat untuk LLM (~0.3-10 t/s) — tidak cukup untuk real-time
  - iGPU Lunar Lake/Adreno: ~20 t/s untuk 7B model — cukup untuk basic use
  - MacBook M4 Pro + MLX: ~60 t/s — 3x lebih cepat dari opsi A/B untuk LLM
- **Rekomendasi:** Jika prioritas utama adalah LLM lokal, MacBook M4 Pro masih unggul jauh. Laptop AI PC (Intel/Qualcomm) NPU-nya belum matang untuk LLM — GPU tetap backbone. NPU berguna untuk background AI tasks (Windows Studio Effects, voice transcription).

---

## 7. REFERENSI WAJIB (SOP: minimal 5 paper 5 tahun terakhir + DOI)

### Paper Jurnal/Konferensi

[1] **NITRO: LLM Inference on Intel Laptop NPUs**
```
@article{abdelfattah2024nitro,
  title     = {{NITRO}: {LLM} Inference on {Intel} Laptop {NPUs}},
  author    = {Abdelfattah, Mohamed and others},
  journal   = {arXiv preprint arXiv:2412.11053},
  year      = {2024},
  doi       = {10.48550/arXiv.2412.11053},
  url       = {https://arxiv.org/abs/2412.11053}
}
```
- Kaitan: Framework NPU inference pertama untuk Intel Core Ultra — 10x speedup vs vanilla OpenVINO. Data benchmark NPU Intel di Tabel B merujuk paper ini.

[2] **Fast On-device LLM Inference with NPUs (llm.npu)**
```
@inproceedings{liu2024llmnpu,
  title     = {Fast On-device {LLM} Inference with {NPUs}},
  author    = {Liu, Jiawei and others},
  booktitle = {International Conference on Mobile Systems, Applications, and Services (MobiSys)},
  year      = {2024},
  doi       = {10.48550/arXiv.2407.05858},
  url       = {https://arxiv.org/abs/2407.05858}
}
```
- Kaitan: Hybrid NPU-CPU-GPU — 22.4x prefill speedup, 30.7x energy savings. Arsitektur hybrid di seksi 2.D merujuk paper ini.

[3] **Agent.xpu: Heterogeneous Scheduling for Agentic LLM on SoC**
```
@article{kim2025agentxpu,
  title     = {Agent.xpu: Efficient Scheduling of Agentic {LLM} Workloads on Heterogeneous {SoC}},
  author    = {Kim, Sehoon and others},
  journal   = {arXiv preprint arXiv:2506.24045},
  year      = {2025},
  doi       = {10.48550/arXiv.2506.24045},
  url       = {https://arxiv.org/abs/2506.24045}
}
```
- Kaitan: 1.2-2.4x throughput NPU-iGPU hybrid vs iGPU-only. Data Tabel B tentang hybrid inference merujuk paper ini.

[4] **T-MAC: CPU Renaissance via Table Lookup for Low-Bit LLM**
```
@inproceedings{wei2024tmac,
  title     = {{T-MAC}: CPU Renaissance via Table Lookup for Low-Bit {LLM} Inference on Edge},
  author    = {Wei, Jianyu and Cao, Shijie and Cao, Ting and Ma, Lingxiao and Wang, Lei and Zhang, Yanyong and Yang, Mao},
  booktitle = {European Conference on Computer Systems (EuroSys)},
  year      = {2025},
  doi       = {10.48550/arXiv.2407.00088},
  url       = {https://arxiv.org/abs/2407.00088}
}
```
- Kaitan: CPU via T-MAC mengalahkan NPU di Snapdragon X Elite (12.6 vs 10.4 t/s). Data benchmark Tabel B — T-MAC CPU vs NPU — diverifikasi dari paper ini.

[5] **Intel Achieves Full NPU Support in MLPerf Client v0.6**
```
@article{intel2025mlperfnpu,
  title     = {Intel Achieves First, Only Full {NPU} Support in {MLPerf} Client v0.6 Benchmark},
  author    = {Intel Corporation},
  journal   = {Intel Newsroom},
  year      = {2025},
  url       = {https://newsroom.intel.com/client-computing/intel-achieves-first-only-full-npu-support-mlperf-client-v0-6-benchmark}
}
```
- Kaitan: NPU first-token latency 1.09s, throughput 18.55 t/s di Llama-2-7B — standarisasi benchmark NPU pertama. Data Tabel A tentang NPU TOPS dan performa merujuk publikasi ini.

[6] **DeepSeek-V4: Hardware Requirements for Frontier MoE**
```
@article{deepseek2026v4,
  title     = {{DeepSeek-V4}: A Hybrid {CSA/HCA} Mixture-of-Experts Language Model},
  author    = {DeepSeek-AI},
  journal   = {arXiv preprint arXiv:2604.09980},
  year      = {2026},
  doi       = {10.48550/arXiv.2604.09980},
  url       = {https://arxiv.org/abs/2604.09980}
}
```
- Kaitan: Model 1.6T parameter — contoh frontier yang sama sekali tidak bisa dijalankan di NPU, mempertegas batas kemampuan NPU vs GPU.

### Referensi Pendukung

[7] Microsoft. *Copilot+ PC Requirements*. [https://www.microsoft.com/en-us/windows/copilot-plus-pcs](https://www.microsoft.com/en-us/windows/copilot-plus-pcs)

[8] Intel. *OpenVINO NPU Guide*. [https://docs.openvino.ai](https://docs.openvino.ai)

[9] Qualcomm. *Snapdragon Neural Processing Engine SDK*. [https://developer.qualcomm.com/software/qualcomm-neural-processing-sdk](https://developer.qualcomm.com/software/qualcomm-neural-processing-sdk)

[10] AMD. *Ryzen AI Software*. [https://ryzenai.docs.amd.com](https://ryzenai.docs.amd.com)

[11] Apple. *Core ML Neural Engine*. [https://developer.apple.com/machine-learning/core-ml](https://developer.apple.com/machine-learning/core-ml)

### SOP Referensi
- WAJIB menyertakan minimal **5 paper jurnal/konferensi** dengan DOI/arXiv valid.
- Data TOPS NPU bersumber dari spesifikasi resmi vendor.
- Benchmark LLM di NPU masih sangat awal — angka dapat berubah signifikan dalam 1-2 tahun.
