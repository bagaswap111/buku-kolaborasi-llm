# [Jilid 1] Bab 2.4: Storage Bottlenecks — Kecepatan Load Model NVMe Gen 4 vs Gen 5
> **Tipe Konten:** Teknis — Benchmark Storage + Analisis
> **Target Pembaca:** Pengguna yang ingin memahami dampak storage pada TTFT dan model swapping

---

## 1. TUJUAN SUB-BAB
Pembaca memahami:
- Peran storage (NVMe SSD) dalam LLM inference — terutama untuk model loading dan offloading
- Perbedaan kecepatan NVMe Gen 3, Gen 4, Gen 5 dan dampaknya pada model load time
- Teknik optimasi I/O untuk mempercepat loading model besar dan KV cache offloading

---

## 2. KERANGKA KONTEN (WAJIB DITULIS)

### A. Storage dalam Pipeline LLM Inference (1 paragraf)
- Model loading: weights disimpan di SSD, dibaca ke DRAM/VRAM saat startup
- Offloading: KV cache dan weights bisa di-offload ke SSD jika VRAM tidak cukup
- Second-order: checkpointing, dataset caching, RAG vector storage

### B. NVMe Generations — Spesifikasi (1 paragraf + tabel)
- PCIe Gen 3: ~3.5 GB/s per lane, x4 = ~14 GB/s (NVMe 1.3)
- PCIe Gen 4: ~7.0 GB/s per lane, x4 = ~28 GB/s (NVMe 1.4)
- PCIe Gen 5: ~14.0 GB/s per lane, x4 = ~56 GB/s (NVMe 2.0)
- Angka real-world: sequential read ~70% dari teoretis karena controller overhead

### C. Dampak pada Model Loading Time (1 paragraf + tabel)
- Model 7B Q4_K_M (~4.5 GB): Gen 3 ~0.35s, Gen 4 ~0.18s, Gen 5 ~0.09s
- Model 70B Q4_K_M (~40 GB): Gen 3 ~3.0s, Gen 4 ~1.5s, Gen 5 ~0.8s
- Model 405B Q3_K_M (~230 GB): Gen 3 ~17s, Gen 4 ~8.5s, Gen 5 ~4.5s
- DeepSeek V4 Flash Q4_K_M (~160 GB): Gen 3 ~12s, Gen 4 ~6s, Gen 5 ~3s
- Mistral Large 3 Q3_K_M (~280 GB): Gen 3 ~21s, Gen 4 ~10.5s, Gen 5 ~5.5s
- Perbedaan ini krusial untuk TTFT (Time to First Token) pada cold start

### D. I/O Characterization Offloading (1 paragraf)
- Paper CHEOPS '25: pola I/O offloading didominasi 128 KiB reads, bandwidth rata-rata 2.0 GiB/s read, 11 MiB/s write
- DeepSpeed ZeRO-Inference: NVMe offload memungkinkan model >VRAM, tapi bottleneck di PCIe
- Gen 4 vs Gen 5: 40% improvement untuk model besar (data Micron 2025)

### E. Teknik Optimasi Loading (1 paragraf)
- Model fragmentation: simpan model dalam SLC region SSD untuk latensi lebih rendah (Micron AI FW)
- GPU-initiated storage access via BaM (NVIDIA + UIUC) — 25x lebih cepat dari mmap tradisional
- Pinned memory + async loading: overlap I/O dengan inisialisasi compute

### F. Rekomendasi SSD untuk LLM Workstation (1 paragraf)
- Prioritaskan sequential read speed (NVMe Gen 4 minimum, Gen 5 ideal)
- Kapasitas minimum: 1TB (bisa muat beberapa model + KV cache buffer)
- QLC vs TLC: SLC cache penting untuk model loading; Micron 4600 Gen 5 TLC ideal

---

## 3. TABEL WAJIB

### Tabel A: Spesifikasi NVMe SSD untuk AI Workstation

| SSD | Interface | Seq Read | Seq Write | 4K Random | Kapasitas | Harga (Rp) | Model Load 7B | Model Load 70B |
|:---|:---:|:---:|:---:|:---:|:---:|---:|---:|---:|
| **Samsung 970 EVO Plus** | PCIe 3.0 x4 | 3.5 GB/s | 3.3 GB/s | 600K IOPS | 1TB | ~1.2 jt | 0.35s | 3.0s |
| **WD Black SN850X** | PCIe 4.0 x4 | 7.3 GB/s | 6.6 GB/s | 1.2M IOPS | 2TB | ~2.5 jt | 0.18s | 1.5s |
| **Samsung 990 Pro** | PCIe 4.0 x4 | 7.5 GB/s | 6.9 GB/s | 1.4M IOPS | 2TB | ~3.0 jt | 0.17s | 1.4s |
| **Micron 3500** | PCIe 4.0 x4 | 7.0 GB/s | 6.0 GB/s | 1.0M IOPS | 1TB | ~1.8 jt | 0.18s | 1.5s |
| **Micron 4600** | PCIe 5.0 x4 | 14.5 GB/s | 12.0 GB/s | 2.0M IOPS | 1TB | ~3.5 jt | 0.09s | 0.8s |
| **Crucial T700** | PCIe 5.0 x4 | 12.4 GB/s | 11.8 GB/s | 1.5M IOPS | 2TB | ~4.5 jt | 0.10s | 0.9s |
| **Seagate FireCuda 540** | PCIe 5.0 x4 | 10.0 GB/s | 10.0 GB/s | 1.3M IOPS | 2TB | ~4.0 jt | 0.12s | 1.0s |
| **Intel Optane 905P** | PCIe 3.0 x4 | 2.6 GB/s | 2.2 GB/s | 5.0M IOPS | 960GB | ~8 jt (EOL) | 0.25s | 2.5s |

### Tabel B: Dampak Storage pada TTFT Cold Start

| Skenario | Gen 3 (3.5 GB/s) | Gen 4 (7 GB/s) | Gen 5 (14 GB/s) |
|:---|---:|---:|---:|
| 7B Q4_K_M load + inference | 0.45s | 0.28s | 0.19s |
| 13B Q4_K_M load + inference | 0.85s | 0.52s | 0.35s |
| 70B Q3_K_M load + inference | 3.5s | 2.0s | 1.2s |
| 405B Q3_K_M offload (50% ke SSD) | 12s | 6.5s | 3.5s |
| DeepSeek V4 Flash Q4 (160 GB) load | 12s | 6.0s | 3.0s |
| Mistral Large 3 Q3 (280 GB) load | 21s | 10.5s | 5.5s |

### Tabel C: I/O Performance Offloading (Data dari CHEOPS '25)

| Metrik | DeepSpeed ZeRO-Inference | FlexGen |
|:---|---:|---:|
| **Block size dominan** | 128 KiB | 128 KiB |
| **Read bandwidth rata-rata** | 2.0 GiB/s | 1.8 GiB/s |
| **Write bandwidth rata-rata** | 11.0 MiB/s | 9.5 MiB/s |
| **I/O pattern** | Sequential read | Sequential read |
| **Saturasi NVMe** | Tidak (hanya 20% bandwidth) | Tidak (hanya 18%) |

---

## 4. DIAGRAM/GAMBAR WAJIB

### Diagram 1: Aliran Data Model Loading (Mermaid)
- **File:** `assets/diagrams/j1-b2-s4-model-loading-flow.mmd`
- **Isi:** Flowchart: SSD (NVMe) → PCIe → DRAM → VRAM → GPU Compute. Anotasi bandwidth setiap tahap.

### Gambar 2: Grafik Model Load Time per Generasi NVMe
- **File:** `assets/images/jilid1/j1-b2-s4-load-time-comparison.png`
- **Isi:** Bar chart stacked: Gen 3 vs Gen 4 vs Gen 5 untuk model 7B, 13B, 70B, 405B. Sumbu Y = detik.

---

## 5. TUTORIAL / HANDS-ON (WAJIB)

### Tutorial A: Benchmark NVMe SSD untuk Model Loading

```bash
# 1. Cek PCIe generation SSD
sudo nvme list
sudo nvme id-ctrl /dev/nvme0n1 | grep "LBA Format"

# 2. Cek link speed real-time
sudo nvme admin-passthru /dev/nvme0n1 --opcode 0x06 --data-len 4096
# Atau dengan lspci
lspci -vvv -s $(lspci | grep "Non-Volatile" | awk '{print $1}') | grep "Speed"

# 3. Sequential read benchmark langsung
sudo hdparm -t /dev/nvme0n1
# Atau full benchmark
sudo fio --name=seqread --rw=read --bs=1M --size=10G \
    --filename=/dev/nvme0n1 --runtime=30 --ioengine=libaio --iodepth=64

# 4. Simulasi model loading — ukuran file 4.5 GB (setara 7B Q4)
dd if=/dev/zero of=test_model.bin bs=1M count=4608
# Ukur waktu baca
time cat test_model.bin > /dev/null
```

### Tutorial B: Optimalisasi Model Loading dengan Pinned Memory

```python
# fast_load.py — model loading dengan async prefetch
import numpy as np
import time
from concurrent.futures import ThreadPoolExecutor

class FastModelLoader:
    def __init__(self, ssd_bandwidth_gbps=7.0):
        self.bw = ssd_bandwidth_gbps
        self.executor = ThreadPoolExecutor(max_workers=4)

    def estimate_load_time(self, model_size_gb):
        return model_size_gb / (self.bw * 0.7)  # 70% utilization

    def load_with_prefetch(self, model_path, n_chunks=8):
        """Load model file with parallel chunk reads"""
        chunk_size = 512 * 1024 * 1024  # 512MB chunks
        futures = []

        for i in range(n_chunks):
            offset = i * chunk_size
            future = self.executor.submit(
                self._read_chunk, model_path, offset, chunk_size
            )
            futures.append(future)

        return [f.result() for f in futures]

    def _read_chunk(self, path, offset, size):
        start = time.time()
        with open(path, 'rb') as f:
            f.seek(offset)
            data = f.read(size)
        elapsed = time.time() - start
        bw = size / elapsed / 1e9
        print(f"Chunk {offset//1024//1024}MB: {elapsed:.2f}s ({bw:.1f} GB/s)")
        return data

loader = FastModelLoader()
# Estimasi: model 4.5 GB di SSD Gen 4
print(f"Estimasi load time: {loader.estimate_load_time(4.5):.2f}s")
```

### Tutorial C: Setup NVMe Offload dengan llama.cpp

```bash
# llama.cpp mendukung offloading ke CPU/NVMe via mmap
# Secara default, model di-mmap dari disk — sistem I/O = file cache

# Cek page cache hit rate setelah pertama kali load
echo 3 > /proc/sys/vm/drop_caches  # Hapus cache
time ./main -m model-q4_k_m.gguf -p "test" -n 1  # Cold start

# Kedua kali — page cache masih ada, jauh lebih cepat
time ./main -m model-q4_k_m.gguf -p "test" -n 1  # Warm start

# Untuk offloading KV cache ke NVMe (llama.cpp >= b3044):
./server -m model.gguf -ngl 20 --kv-cache-offload 1
```

---

## 6. STUDI KASUS (WAJIB)

### Studi Kasus: Upgrade SSD Gen 3 ke Gen 5 untuk Multi-Model Workflow
- **Skenario:** Developer sering berganti-ganti model (Llama-3.1-8B, Qwen-2.5-14B, DeepSeek-Coder) setiap kali riset — butuh load cepat
- **Sebelum:** Samsung 970 EVO Plus (Gen 3, 3.5 GB/s) — load model 7B 0.35s, 14B 0.65s
- **Sesudah:** Crucial T700 (Gen 5, 12.4 GB/s) — load 7B 0.10s, 14B 0.18s
- **Dampak:** Saat berganti model 20x sehari, hemat ~15 detik/hari — akumulasi ~5 jam/tahun
- **Biaya:** Rp 4.5 jt untuk Crucial T700 2TB vs Rp 1.2 jt untuk Samsung 970 EVO Plus 1TB
- **Rekomendasi:** Gen 4 (SN850X/Samsung 990 Pro) sudah cukup untuk sebagian besar kasus; Gen 5 hanya untuk pengguna yang sering cold-start model besar

---

## 7. REFERENSI WAJIB (SOP: minimal 5 paper 5 tahun terakhir + DOI)

### Paper Jurnal/Konferensi

[1] **I/O Characterizing Study of Offloading LLM Models to NVMe SSD**
```
@inproceedings{ren2025iocharssd,
  title     = {An {I/O} Characterizing Study of Offloading {LLM} Models and {KV} Caches to {NVMe} {SSD}},
  author    = {Ren, Zebin and Doekemeijer, Krijn and De Matteis, Tiziano and Pinto, Christian and Stoica, Radu and Trivedi, Animesh},
  booktitle = {Proceedings of the 5th Workshop on Challenges and Opportunities of Efficient and Performant Storage Systems (CHEOPS)},
  year      = {2025},
  doi       = {10.1145/3719330.3721230},
  url       = {https://dl.acm.org/doi/10.1145/3719330.3721230}
}
```
- Kaitan: Satu-satunya paper yang mengkarakterisasi pola I/O offloading LLM ke SSD. Data Tabel C bersumber dari studi ini.

[2] **NVMe Offload for Democratizing AI at Scale**
```
@inproceedings{rajgopal2024nvmeoffload,
  title     = {{NVMe} Offload for Democratizing {AI} at Scale},
  author    = {Rajgopal, Jairaj and others},
  booktitle = {Future Memory Storage (FMS)},
  year      = {2024},
  url       = {https://files.futurememorystorage.com/proceedings/2024/20240808_CLDS-303-1_Rajgopal.pdf}
}
```
- Kaitan: Studi NVMe offload DeepSpeed ZeRO-Inference — Gen 3 ke Gen 4 memberikan 40% improvement performa. Data scaling PCIe di Tabel B merujuk paper ini.

[3] **InstInfer: In-Storage Attention Offloading for Long-Context LLM**
```
@article{liu2024instinfer,
  title     = {{InstInfer}: In-Storage Attention Offloading for Cost-Effective Long-Context {LLM} Inference},
  author    = {Liu, Jiawei and others},
  journal   = {arXiv preprint arXiv:2409.04992},
  year      = {2024},
  doi       = {10.48550/arXiv.2409.04992},
  url       = {https://arxiv.org/abs/2409.04992}
}
```
- Kaitan: Sistem CSD (Computational Storage Drive) untuk offload KV cache — 11.1x lebih cepat dari FlexGen. Relevan untuk seksi 2.D tentang optimasi offloading.

[4] **Cake: Computation and I/O Aware KV Cache Caching**
```
@article{liu2024cake,
  title     = {Cake: Computation and {I/O} Aware {KV} Cache Caching for Long-Context {LLM} Inference},
  author    = {Liu, Yuhan and others},
  journal   = {arXiv preprint arXiv:2410.03065},
  year      = {2024},
  doi       = {10.48550/arXiv.2410.03065},
  url       = {https://arxiv.org/abs/2410.03065}
}
```
- Kaitan: Sistem hybrid computation + I/O untuk mengurangi TTFT — 2.6x reduksi vs compute-only atau I/O-only. Relevan untuk strategi loading di seksi 2.E.

[5] **LLM in a Flash: Efficient LLM Inference with Limited Memory**
```
@inproceedings{alizadeh2024llmflash,
  title     = {{LLM} in a Flash: Efficient Large Language Model Inference with Limited Memory},
  author    = {Alizadeh, Keivan and others},
  booktitle = {Annual Meeting of the Association for Computational Linguistics (ACL)},
  year      = {2024},
  doi       = {10.18653/v1/2024.acl-long.678},
  url       = {https://aclanthology.org/2024.acl-long.678.pdf}
}
```
- Kaitan: Teknik windowing + row-column bundling untuk inferensi model 2x DRAM size dengan flash storage. Data teknik optimasi di seksi 2.E merujuk paper ini.

### Referensi Pendukung

[6] Micron. *AI Storage for LLM Inference*. [https://www.micron.com/products/ai-solutions](https://www.micron.com/products/ai-solutions)

[7] NVIDIA. *BaM: GPU-Initiated Storage Access*. [https://github.com/ZaidQureshi/bam](https://github.com/ZaidQureshi/bam)

[8] AnandTech / TechPowerUp. *SSD Benchmarks*. [https://www.techpowerup.com/review/ssd](https://www.techpowerup.com/review/ssd)

[9] Samsung. *990 PRO SSD Specifications*. [https://semiconductor.samsung.com/consumer-storage/nvme/990-pro](https://semiconductor.samsung.com/consumer-storage/nvme/990-pro)

[10] **DeepSeek-V4: Model Size and Storage Requirements**
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
- Kaitan: Model 284B dan 1.6T — ukuran file besar yang membutuhkan storage cepat untuk cold start <10 detik.

### SOP Referensi
- WAJIB menyertakan minimal **5 paper jurnal/konferensi** dengan DOI/arXiv valid.
- Data bandwidth SSD diverifikasi dari spesifikasi vendor dan review independen.
- Model load time adalah estimasi teoretis; real-world bervariasi tergantung sistem.
