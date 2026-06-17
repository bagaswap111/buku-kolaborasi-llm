# [Jilid 2] Bab 5.6: Distributed Inference — Satu Model Besar di Dua Komputer (Ray/SkyPilot)
> **Tipe Konten:** Arsitektural — Desain Sistem + Tutorial + Studi Kasus
> **Target Pembaca:** Engineer yang ingin menjalankan model > 70B di cluster multi-node

---

## 1. TUJUAN SUB-BAB
Pembaca memahami:
- Teknik tensor parallelism, pipeline parallelism, dan sequence parallelism
- Cara setup Ray cluster untuk distributed inference dengan vLLM
- Kapan menggunakan SkyPilot untuk deploy ke cloud multi-region

---

## 2. KERANGKA KONTEN (WAJIB DITULIS)

### A. Mengapa Distributed Inference? (2 paragraf)
- Model > 70B tidak muat di satu GPU (Llama-3.1-405B = 810 GB FP16 = 10x H100)
- Memory wall: VRAM per GPU terbatas, bandwidth jadi bottleneck
- Distributed = satu model dipecah ke beberapa GPU/node

### B. Tensor Parallelism (TP) (2 paragraf)
- Satu layer dipecah per dimensi (row/column) ke beberapa GPU
- Setiap forward pass butuh all-reduce antar GPU
- NCCL sebagai backbone komunikasi — sensitive terhadap interconnect speed (NVLink > PCIe > Ethernet)
- TP paling efektif dalam satu node (NVLink bandwidth tinggi)

### C. Pipeline Parallelism (PP) (2 paragraf)
- Layer dibagi per stage — GPU 1 proses layer 1-16, GPU 2 proses layer 17-32
- Bubble overhead: GPU menganggur menunggu data dari stage sebelumnya
- Micro-batching untuk mengurangi bubble (1F1B scheduling)
- PP > TP ketika interconnect antar-node lambat

### D. Sequence Parallelism (1 paragraf)
- Satu sequence panjang dipecah ke beberapa GPU
- Berguna untuk long-context inference (128K+ token)
- Ring attention: komunikasi point-to-point antar GPU

### E. Ray dan SkyPilot (1 paragraf)
- Ray: distributed runtime untuk cluster management, fault tolerance, auto-scaling
- SkyPilot: framework untuk deploy ke multi-cloud (AWS, GCP, Azure) dengan cost optimization
- vLLM menggunakan Ray untuk multi-node deployment

---

## 3. TABEL WAJIB

### Tabel A: Strategi Parallelism — Perbandingan

| Aspek | Tensor Parallelism (TP) | Pipeline Parallelism (PP) | Sequence Parallelism (SP) |
|:---|:---:|:---:|:---:|
| **Granularitas** | Per-layer/operasi | Per-layer group | Per-sequence chunk |
| **Komunikasi** | All-reduce (setiap step) | Point-to-point (batch boundary) | Ring attention |
| **Interconnect Need** | Sangat Tinggi (NVLink) | Rendah (Ethernet OK) | Sedang (RDMA baik) |
| **Bubble Overhead** | 0% | ~10-30% (tergantung micro-batch) | 0% |
| **Efektif dalam 1 Node** | Ya (NVLink) | Tidak perlu | Ya |
| **Efektif Multi-Node** | Kurang (bottleneck network) | Ya | Ya |
| **Memory Reduction** | ~1/N per GPU | ~1/N per GPU | ~1/N untuk KV cache |

### Tabel B: Benchmark Distributed — Llama-3.1-405B

| Konfigurasi | Total GPUs | TP | PP | Throughput (tok/s) | Speedup Efficiency |
|:---|:---:|:---:|:---:|:---:|:---:|
| 8x H100 (1 node) | 8 | 8 | 1 | 4,200 | 100% |
| 16x H100 (2 node, NVLink) | 16 | 8 | 2 | 7,800 | 93% |
| 16x H100 (2 node, Ethernet) | 16 | 4 | 4 | 6,200 | 74% |
| 32x H100 (4 node, Ethernet) | 32 | 4 | 8 | 11,500 | 68% |
| 64x H100 (8 node, Ethernet) | 64 | 4 | 16 | 18,000 | 54% |

### Tabel C: Estimasi VRAM Model Distributed

| Model | FP16 Total | TP=8 (1 node) | TP=4, PP=2 | Rekomendasi Node |
|:---|:---:|:---:|:---:|:---|
| Llama-3.1-70B | 140 GB | 17.5 GB/GPU | 35 GB/GPU | 1 node (8x H100) |
| Llama-3.1-405B | 810 GB | 101 GB/GPU | 202 GB/GPU | 2+ node (16x H100) |
| Mixtral-8x22B | 280 GB | 35 GB/GPU | 70 GB/GPU | 1 node (8x H100) |
| DeepSeek-V3 | 671 GB (FP8) | 84 GB/GPU | 168 GB/GPU | 1 node (8x H100) |

---

## 4. DIAGRAM/GAMBAR WAJIB

### Diagram 1: Tensor Parallelism vs Pipeline Parallelism (Mermaid)
- **File:** `assets/diagrams/j2-b5-s6-parallelism-strategies.mmd`
- **Isi:** Ilustrasi TP (satu layer dipecah horizontal ke 2 GPU dengan all-reduce) vs PP (layer 1-12 di GPU 1, layer 13-24 di GPU 2)

### Gambar 2: Arsitektur Ray Cluster untuk vLLM Multi-Node
- **File:** `assets/images/jilid2/j2-b5-s6-ray-cluster.png`
- **Isi:** Diagram: Ray Head Node + Worker Nodes -> vLLM Scheduler -> TP Workers -> NCCL Communication

### Gambar 3: Scaling Efficiency Chart
- **File:** `assets/images/jilid2/j2-b5-s6-scaling-efficiency.png`
- **Isi:** Line chart: jumlah GPU (x) vs speedup (y), menunjukkan diminishing returns setelah 32 GPU

---

## 5. TUTORIAL / HANDS-ON (WAJIB)

### Tutorial A: Multi-Node vLLM dengan Ray

```bash
# Install Ray dan vLLM di semua node
pip install ray vllm

# Node 1 (Head)
ray start --head --port=6379 --num-gpus=8

# Node 2 (Worker)
ray start --address=<HEAD_NODE_IP>:6379 --num-gpus=8

# Jalankan vLLM di head node dengan TP=4, PP=2
vllm serve meta-llama/Meta-Llama-3.1-405B-Instruct \
    --tensor-parallel-size 4 \
    --pipeline-parallel-size 2 \
    --distributed-executor-backend ray \
    --max-model-len 4096

# Verifikasi cluster
ray status
# Seharusnya menampilkan 16 GPU total
```

### Tutorial B: Deploy Multi-Cloud dengan SkyPilot

```yaml
# skypilot.yaml
name: distributed-vllm
resources:
  accelerators: H100:8
  cloud: gcp

num_nodes: 2

setup: |
  pip install vllm ray

run: |
  if [ $SKYPILOT_NODE_RANK == 0 ]; then
    ray start --head --port=6379 --num-gpus=8
    vllm serve meta-llama/Meta-Llama-3.1-405B-Instruct \
        --tensor-parallel-size 4 \
        --pipeline-parallel-size 2 \
        --distributed-executor-backend ray
  else
    ray start --address=$SKYPILOT_NODE_IP:6379 --num-gpus=8
    sleep infinity
  fi
```

```bash
# Deploy ke cloud
sky launch -c mycluster skypilot.yaml

# Scale down saat tidak dipakai
sky down mycluster
```

### Tutorial C: Monitor Komunikasi NCCL

```bash
# NCCL debug untuk troubleshooting bottleneck
export NCCL_DEBUG=INFO
export NCCL_DEBUG_SUBSYS=GRAPH
export NCCL_IB_DISABLE=0  # Enable InfiniBand
export NCCL_SOCKET_IFNAME=eth0  # Interface untuk komunikasi

# Profiling komunikasi
nsys profile -o nccl_trace python -m vllm.entrypoints.openai.api_server \
    --model meta-llama/Meta-Llama-3.1-70B \
    --tensor-parallel-size 8

# Cek NCCL ring latency
python -c "
import torch
import torch.distributed as dist
dist.init_process_group('nccl')
tensor = torch.randn(1024, device='cuda')
# Benchmark all-reduce
start = torch.cuda.Event(enable_timing=True)
end = torch.cuda.Event(enable_timing=True)
start.record()
for _ in range(100):
    dist.all_reduce(tensor)
end.record()
torch.cuda.synchronize()
print(f'All-reduce 100x: {start.elapsed_time(end):.2f} ms')
"
```

---

## 6. STUDI KASUS (WAJIB)

### Studi Kasus: Research Lab — Menjalankan DeepSeek-V3 di Cluster 4 Node
- **Latar Belakang:** Lab riset ingin menjalankan DeepSeek-V3 (671B FP8) untuk research NLP
- **Hardware:** 4 node, masing-masing 8x H100 (80GB), total 32 GPU
- **Interconnect:** InfiniBand antar-node (400 Gbps), NVLink dalam node
- **Konfigurasi:** TP=4 (dalam node), PP=4 (antar node) — optimal untuk campuran NVLink + InfiniBand
- **Hasil:** Loading model ~15 menit, throughput ~12,000 tok/s untuk batch 128
- **Efisiensi Scaling:** 68% dari ideal (Tabel B) — bottleneck di komunikasi PP antar-node
- **Optimasi:** Ganti ke TP=8 per node + PP=2 -> efisiensi naik ke 78%

---

## 7. REFERENSI WAJIB

[1] **Alpa — Automated Model Parallelism**
```
@inproceedings{zheng2022alpa,
  title     = {{Alpa}: Automating Inter- and {Intra-Operator} Parallelism for Distributed Deep Learning},
  author    = {Zheng, Lianmin and Li, Zhuohan and Zhang, Hao and Zhuang, Yonghao and Chen, Zhifeng and Huang, Yanping and Wang, Yida and Xu, Yuanzhong and Zhuo, Danyang and Xing, Eric P. and Gonzalez, Joseph E. and Stoica, Ion},
  booktitle = {16th USENIX Symposium on Operating Systems Design and Implementation (OSDI)},
  year      = {2022},
  url       = {https://www.usenix.org/conference/osdi22/presentation/zheng-lianmin}
}
```
- Kaitan: Framework otomatis parallelism — mendasari strategi TP/PP di vLLM.

[2] **PagedAttention — Distributed Serving**
```
@inproceedings{kwon2023pagedattention,
  title     = {Efficient Memory Management for Large Language Model Serving with {PagedAttention}},
  author    = {Kwon, Woosuk and others},
  booktitle = {SOSP},
  year      = {2023},
  doi       = {10.1145/3600006.3613165}
}
```
- Kaitan: vLLM mendukung distributed execution dengan TP dan PP untuk model besar.

[3] **Megatron-LM — Model Parallelism**
```
@inproceedings{shoeybi2019megatron,
  title     = {{Megatron-LM}: Training Multi-Billion Parameter Language Models Using Model Parallelism},
  author    = {Shoeybi, Mohammad and others},
  booktitle = {Advances in Neural Information Processing Systems (NeurIPS)},
  year      = {2019},
  doi       = {10.48550/arXiv.1909.08053},
  url       = {https://arxiv.org/abs/1909.08053}
}
```
- Kaitan: Fondasi tensor parallelism yang digunakan vLLM. TP di vLLM mengadopsi algoritma Megatron.

[4] **FlexGen — Offloading-based Inference**
```
@inproceedings{sheng2023flexgen,
  title     = {{FlexGen}: High-Throughput Generative Inference of Large Language Models with a Single {GPU}},
  author    = {Sheng, Ying and others},
  booktitle = {International Conference on Machine Learning (ICML)},
  year      = {2023},
  doi       = {10.48550/arXiv.2303.06865}
}
```
- Kaitan: Alternatif distributed inference dengan CPU/disk offloading untuk GPU tunggal.

[5] **Efficient Large-Scale LLM Training and Inference — Survey**
```
@article{wan2024efficient,
  title     = {Efficient Large Language Models: A Survey},
  author    = {Wan, Zhongwei and others},
  journal   = {arXiv preprint arXiv:2312.03863},
  year      = {2024},
  doi       = {10.48550/arXiv.2312.03863}
}
```
- Kaitan: Survey komprehensif teknik parallelism — konteks distributed inference dalam ekosistem LLM.

[6] Ray Project. *Documentation*. [https://docs.ray.io](https://docs.ray.io)

[7] SkyPilot Project. *Documentation*. [https://skypilot.readthedocs.io](https://skypilot.readthedocs.io)

[8] NVIDIA. *NCCL Documentation*. [https://docs.nvidia.com/deeplearning/nccl](https://docs.nvidia.com/deeplearning/nccl)
