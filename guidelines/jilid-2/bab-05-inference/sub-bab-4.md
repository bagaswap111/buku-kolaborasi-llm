# [Jilid 2] Bab 5.4: Continuous Batching — Melayani 10 User Tanpa Terasa Lambat
> **Tipe Konten:** Teknis — Konsep + Implementasi + Benchmark
> **Target Pembaca:** System engineer yang ingin memahami mekanisme scheduling di inference engine

---

## 1. TUJUAN SUB-BAB
Pembaca memahami:
- Perbedaan static batching vs continuous batching (iteration-level scheduling)
- Mekanisme selective batching untuk menangani variasi panjang sequence
- Dampak continuous batching terhadap latency dan throughput di berbagai engine

---

## 2. KERANGKA KONTEN (WAJIB DITULIS)

### A. Masalah Static Batching (2 paragraf)
- Batch tradisional: semua request harus selesai sebelum batch berikutnya
- Head-of-line blocking: request pendek menunggu request panjang
- GPU utilization drop drastis saat request dalam batch selesai tidak bersamaan
- Kutip data: static batching hanya mencapai 20-40% GPU utilization (Yu et al.)

### B. Iteration-Level Scheduling / Continuous Batching (3 paragraf)
- Konsep dari paper Orca (OSDI 2022)
- Scheduler bekerja per-iteration (satu token generation step), bukan per-request
- Setiap iterasi: generate 1 token untuk semua active request -> cek selesai -> tambah request baru
- Batch composition berubah setiap step — request bisa join/leave kapan saja

### C. Selective Batching (2 paragraf)
- Tantangan: di iteration-level, tiap request punya panjang sequence berbeda
- Attention operation: tidak bisa di-batch karena shape tensor berbeda
- Solusi: batch hanya untuk feed-forward + LayerNorm; attention diproses per-request
- Selective batching hanya berdampak kecil pada efisiensi karena attention tidak punya parameter (Yu et al.)

### D. Implementasi di Berbagai Engine (1 paragraf)
- vLLM: continuous batching + PagedAttention
- TGI: iteration-level scheduling dengan dynamic batching
- Aphrodite: fork dari vLLM dengan continuous batching
- TensorRT-LLM: in-flight batching (istilah NVIDIA untuk continuous batching)

### E. Dampak pada User Experience (1 paragraf)
- 10 user concurrent: tanpa continuous batching -> yang ke-10 menunggu ~50 detik
- Dengan continuous batching: semua user mulai mendapat token dalam < 2 detik
- Trade-off: throughput naik drastis, latency per-request sedikit naik (tapi lebih predictably)

---

## 3. TABEL WAJIB

### Tabel A: Static vs Continuous Batching (7B Model, A100 80GB)

| Metrik | Static Batching | Continuous Batching | Improvement |
|:---|:---:|:---:|:---:|
| GPU Utilization | 28% | 85% | 3x |
| Throughput (req/s) | 4.2 | 28.5 | 6.8x |
| TTFT P50 (ms) | 180 | 210 | -17% |
| Latency P99 (ms) | 12,500 | 2,800 | 4.5x lebih baik |
| Max Batch Size | 8 | 64 | 8x |
| VRAM Waste | ~50% | ~4% | 12.5x lebih baik |

### Tabel B: Pengaruh Concurrent Users (vLLM, Llama-3.1-8B)

| Concurrent Users | Mean TTFT (ms) | Mean Latency (ms) | Throughput (tok/s) | Queue Time (ms) |
|:---|:---:|:---:|:---:|:---:|
| 1 | 85 | 450 | 1,250 | 0 |
| 5 | 120 | 580 | 4,800 | 35 |
| 10 | 165 | 720 | 7,200 | 95 |
| 20 | 250 | 1,100 | 10,500 | 180 |
| 50 | 480 | 2,400 | 14,200 | 380 |

### Tabel C: Perbandingan Engine — Continuous Batching Support

| Engine | Nama Internal | Tahun Adopsi | Kelebihan Spesifik |
|:---|:---|:---:|:---|
| vLLM | Continuous Batching | 2023 | +PagedAttention, prefix caching |
| TGI | Dynamic Batching | 2023 | +Safety checker, watermark |
| TensorRT-LLM | In-flight Batching | 2023 | +FP8, kernel fusions maksimal |
| Aphrodite | Continuous Batching | 2024 | +Samplers kreatif, multi-quant |
| SGLang | RadixAttention + Batching | 2024 | +Prefix caching radix tree |

---

## 4. DIAGRAM/GAMBAR WAJIB

### Diagram 1: Static vs Continuous Batching Timeline (Mermaid)
- **File:** `assets/diagrams/j2-b5-s4-batching-timeline.mmd`
- **Isi:** Gantt chart perbandingan static (Request 1-4 menunggu semua selesai) vs continuous (request join/leave per step)

### Gambar 2: Grafik GPU Utilization
- **File:** `assets/images/jilid2/j2-b5-s4-gpu-utilization.png`
- **Isi:** Line chart GPU utilization over time: static (sawtooth) vs continuous (flat high)

### Gambar 3: Diagram Selective Batching
- **File:** `assets/images/jilid2/j2-b5-s4-selective-batching.png`
- **Isi:** Ilustrasi model dengan 3 request berbeda panjang — mana yang di-batch (FFN, LayerNorm) dan mana yang tidak (Attention)

---

## 5. TUTORIAL / HANDS-ON (WAJIB)

### Tutorial A: Simulasi Continuous Batching dengan Python

```python
# simulasi_continuous_batching.py
import time
import random

class ContinuousBatchSimulator:
    """Simulasi continuous batching untuk edukasi"""
    def __init__(self, max_batch=8):
        self.max_batch = max_batch
        self.active = {}  # request_id: {remaining_tokens, ...}

    def add_request(self, req_id, num_tokens):
        self.active[req_id] = {"remaining": num_tokens}

    def step(self):
        """Satu iteration = generate 1 token untuk semua active request"""
        completed = []
        for req_id, state in list(self.active.items()):
            state["remaining"] -= 1
            if state["remaining"] <= 0:
                completed.append(req_id)

        for req_id in completed:
            del self.active[req_id]

        return completed

    def run(self, request_list):
        queue = list(request_list)
        timeline = {"batch_size": [], "completed": 0, "steps": 0}

        while queue or self.active:
            # Isi batch sampai penuh
            while len(self.active) < self.max_batch and queue:
                req_id, tokens = queue.pop(0)
                self.add_request(req_id, tokens)

            # Satu step generasi
            completed = self.step()
            timeline["steps"] += 1
            timeline["batch_size"].append(len(self.active))
            timeline["completed"] += len(completed)
            time.sleep(0.01)  # simulasi GPU time

        return timeline

# Test dengan 10 user, panjang output bervariasi
requests = [(i, random.randint(50, 500)) for i in range(10)]
sim = ContinuousBatchSimulator(max_batch=8)
result = sim.run(requests)
print(f"Steps: {result['steps']}, Avg batch: {sum(result['batch_size'])/len(result['batch_size']):.1f}")
```

### Tutorial B: Benchmark Engine dengan Berbagai Concurrency

```bash
# Install locust untuk load testing
pip install locust

# Test vLLM dengan concurrency berbeda
for users in 1 5 10 20; do
    locust \
        --headless \
        --users $users \
        --spawn-rate 1 \
        --host http://localhost:8000 \
        --locustfile benchmark_locust.py \
        2>&1 | grep "TTFT\|Request/sec"
done
```

### Tutorial C: Konfigurasi Max Batch Size di vLLM

```bash
# Parameter penting untuk continuous batching:
# --max-num-seqs: max sequences dalam satu batch
# --max-num-batched-tokens: max token per batch
# --enable-chunked-prefill: pecah prefill besar menjadi chunk

vllm serve meta-llama/Meta-Llama-3.1-8B-Instruct \
    --max-num-seqs 256 \
    --max-num-batched-tokens 8192 \
    --enable-chunked-prefill \
    --gpu-memory-utilization 0.90
```

---

## 6. STUDI KASUS (WAJIB)

### Studi Kasus: Kantor dengan 15 Karyawan Menggunakan AI Assistant
- **Skenario:** Kantor kecil (15 orang) menggunakan AI untuk bantuan coding, menulis email, research
- **Masalah:** Dengan Ollama (static batching), user ke-5 harus menunggu 30+ detik
- **Solusi:** Migrasi ke vLLM dengan continuous batching + Llama-3.1-8B
- **Hasil:** Seluruh 15 user mendapat response dalam < 3 detik, throughput naik 8x
- **Korelasi Tabel B:** Pada 20 concurrent users, TTFT = 250ms — masih dalam batas acceptable
- **Pelajaran:** Continuous batching membuat pengalaman multi-user terasa seamless

---

## 7. REFERENSI WAJIB

[1] **Orca — Iteration-Level Scheduling**
```
@inproceedings{yu2022orca,
  title     = {{Orca}: A Distributed Serving System for {Transformer-Based} Generative Models},
  author    = {Yu, Gyeong-In and Jeong, Joo Seong and Kim, Geon-Woo and Kim, Soojeong and Chun, Byung-Gon},
  booktitle = {16th USENIX Symposium on Operating Systems Design and Implementation (OSDI)},
  year      = {2022},
  url       = {https://www.usenix.org/conference/osdi22/presentation/yu}
}
```
- Kaitan: Paper inti continuous batching. Data Tabel A dan B harus diverifikasi dari paper ini.

[2] **PagedAttention — Memori Management**
```
@inproceedings{kwon2023pagedattention,
  title     = {Efficient Memory Management for Large Language Model Serving with {PagedAttention}},
  author    = {Kwon, Woosuk and others},
  booktitle = {SOSP},
  year      = {2023},
  doi       = {10.1145/3600006.3613165}
}
```
- Kaitan: Continuous batching + PagedAttention = fondasi vLLM. Keduanya saling melengkapi.

[3] **Anyscale — Continuous Batching 23x Throughput**
```
@article{daniel2023continuous,
  title   = {How continuous batching enables 23x throughput in {LLM} inference},
  author  = {Daniel, Cade and Shen, Chen and Liang, Eric and Liaw, Richard},
  journal = {Anyscale Blog},
  year    = {2023},
  url     = {https://www.anyscale.com/blog/continuous-batching-llm-inference}
}
```
- Kaitan: Benchmark komprehensif continuous batching di berbagai engine. Sumber data validasi Tabel A.

[4] **Splitwise — Phase Disaggregation**
```
@inproceedings{patel2024splitwise,
  title     = {{Splitwise}: Efficient Generative {LLM} Inference Using Phase Splitting},
  author    = {Patel, Pratyush and others},
  booktitle = {International Symposium on Computer Architecture (ISCA)},
  year      = {2024},
  doi       = {10.48550/arXiv.2311.18677},
  url       = {https://arxiv.org/abs/2311.18677}
}
```
- Kaitan: Meng-upgrade continuous batching dengan memisahkan prefill dan decode phase.

[5] **TensorRT-LLM — In-Flight Batching**
```
@misc{nvidia2024tensorrtllm,
  title   = {{TensorRT-LLM}: In-Flight Batching Documentation},
  author  = {{NVIDIA}},
  year    = {2024},
  url     = {https://github.com/NVIDIA/TensorRT-LLM}
}
```
- Kaitan: Implementasi continuous batching oleh NVIDIA dengan nama "in-flight batching".

[6] vLLM Project. *Continuous Batching Documentation*. [https://docs.vllm.ai](https://docs.vllm.ai)

[7] SGLang Project. *RadixAttention*. [https://github.com/sgl-project/sglang](https://github.com/sgl-project/sglang)
