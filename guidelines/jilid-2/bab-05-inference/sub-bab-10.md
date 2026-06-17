# [Jilid 2] Bab 5.10: Speculative Decoding — Akselerasi dengan Model Kecil sebagai Draft
> **Tipe Konten:** Teknis — Algoritma + Implementasi + Benchmark
> **Target Pembaca:** Engineer yang ingin mempercepat inference tanpa mengorbankan kualitas output

---

## 1. TUJUAN SUB-BAB
Pembaca memahami:
- Prinsip speculative decoding: draft model + target model verify
- Teknik tree-based speculative inference (SpecInfer) untuk coverage lebih tinggi
- Implementasi speculative decoding di vLLM dan engine modern

---

## 2. KERANGKA KONTEN (WAJIB DITULIS)

### A. Masalah Autoregressive Decoding (2 paragraf)
- Satu forward pass = satu token -> GPU underutilized (memory-bound)
- Memory bandwidth bottleneck: ~90% waktu dihabiskan loading weights, bukan komputasi
- Ide: generate K token dengan model kecil, verify dengan model besar dalam 1 forward pass

### B. Spekulasi Dasar: Draft + Verify (2 paragraf)
- Draft model (kecil, cepat): generate K token secara autoregressive
- Target model (besar): verify semua K token dalam 1 forward pass
- Jika match: terima semua K token. Jika mismatch di posisi i: terima i-1 token pertama, discard sisanya
- Acceptance rate = persentase token draft yang diterima

### C. Tree-based Speculative Inference — SpecInfer (3 paragraf)
- Masalah draft linear: satu jalur spekulasi -> acceptance rate terbatas
- Solusi: token tree — multiple draft paths (branching)
- Tree-based parallel decoding: verify seluruh tree dalam 1 forward pass
- SpecInfer menggunakan LLM sebagai verifier, bukan incremental decoder
- Speedup: 1.5-2.8x distributed, 2.6-3.5x offloading

### D. Variasi Speculative Decoding (2 paragraf)
- **Medusa:** Multiple decoding heads (bukan model terpisah) — 2.2-2.8x speedup
- **Self-speculative:** Layer skipping — model yang sama sebagai draft
- **Eagle:** Dua model LLM dengan speculative verification
- **Lookahead Decoding:** N-gram based speculation

### E. Implementasi di Engine (1 paragraf)
- vLLM: speculative decoding via `--speculative-model` flag
- TGI: speculative decoding dengan draft model
- Aphrodite: mendukung berbagai metode speculative decoding

---

## 3. TABEL WAJIB

### Tabel A: Perbandingan Metode Speculative Decoding

| Metode | Draft Source | Speedup | Training Required | Output Distribution | Kompleksitas Deploy |
|:---|:---|:---:|:---:|:---:|:---:|
| **Vanilla SpecDec** (Leviathan) | Model kecil terpisah | 2-3x | Tidak | Identik (lossless) | Rendah (2 model) |
| **SpecInfer** (Miao) | Token tree (multiple SSM) | 1.5-3.5x | Tidak | Identik (lossless) | Sedang (tree verify) |
| **Medusa-1** (Cai) | Multiple heads (satu model) | 2.2x | Ya (heads only) | Hampir identik | Rendah (no 2nd model) |
| **Medusa-2** | Multiple heads (joint FT) | 2.3-2.8x | Ya (full model) | Mendekati | Rendah |
| **Self-Speculative** | Layer skipping | 1.5-2x | Tidak | Identik | Sangat Rendah |
| **Lookahead Decoding** | N-gram | 1.5-1.8x | Tidak | Identik | Rendah |

### Tabel B: Benchmark Speculative Decoding (Llama-2-7B Target, Llama-7B Draft, A100)

| Konfigurasi | Tokens/Step Rata | Throughput (tok/s) | Speedup | Acceptance Rate |
|:---|:---:|:---:|:---:|:---:|
| Baseline (no spec) | 1.0 | 1,250 | 1.0x | - |
| Vanilla (K=4) | 2.8 | 2,750 | 2.2x | 70% |
| Vanilla (K=8) | 3.5 | 3,125 | 2.5x | 44% |
| SpecInfer (tree K=4) | 3.2 | 3,400 | 2.7x | 80% |
| SpecInfer (tree K=8) | 4.8 | 4,000 | 3.2x | 60% |
| Medusa-1 (heads=4) | 3.0 | 3,000 | 2.4x | 75% |

### Tabel C: Trade-off Draft Model Size vs Speedup

| Draft Model | Target Model | Ratio Params | Speedup | VRAM Tambahan |
|:---|:---|:---:|:---:|:---:|
| Llama-7B (7B) | Llama-70B (70B) | 10% | 2.5x | 14 GB |
| Llama-7B (7B) | Llama-405B (405B) | 1.7% | 3.8x | 14 GB |
| TinyLlama (1.1B) | Llama-13B (13B) | 8.5% | 2.1x | 2.2 GB |
| Gemma-2B (2B) | Llama-70B (70B) | 2.9% | 3.2x | 4 GB |
| SmolLM-360M (0.36B) | Llama-8B (8B) | 4.5% | 2.0x | 0.7 GB |

---

## 4. DIAGRAM/GAMBAR WAJIB

### Diagram 1: Alur Speculative Decoding (Mermaid)
- **File:** `assets/diagrams/j2-b5-s10-speculative-decoding.mmd`
- **Isi:** Input -> Draft Model (generate K tokens cepat) -> Target Model (verify K tokens parallel) -> Accept/Reject -> Output
- **Node:** Draft step 1..K (autoregressive), Verify step (single forward), Accept tokens

### Diagram 2: Token Tree SpecInfer
- **File:** `assets/images/jilid2/j2-b5-s10-token-tree.png`
- **Isi:** Ilustrasi token tree: root -> branch A (token "the", "a", "an") -> branch B (token "cat", "dog") -> ... -> verify semua dalam 1 forward pass

### Gambar 3: Speedup Comparison Bar Chart
- **File:** `assets/images/jilid2/j2-b5-s10-speedup-comparison.png`
- **Isi:** Bar chart speedup tiap metode (data Tabel A), dengan annotation acceptance rate

---

## 5. TUTORIAL / HANDS-ON (WAJIB)

### Tutorial A: Speculative Decoding dengan vLLM

```bash
# 1. Siapkan target model dan draft model
#    Target: meta-llama/Meta-Llama-3.1-70B-Instruct
#    Draft: meta-llama/Llama-3.2-3B-Instruct  (draft yang cocok)

# 2. Jalankan dengan speculative decoding
vllm serve meta-llama/Meta-Llama-3.1-70B-Instruct \
    --speculative-model meta-llama/Llama-3.2-3B-Instruct \
    --num-speculative-tokens 5 \
    --speculative-draft-tensor-parallel-size 1 \
    --speculative-max-model-len 4096 \
    --gpu-memory-utilization 0.90

# 3. Verifikasi speedup
curl http://localhost:8000/v1/completions \
    -H "Content-Type: application/json" \
    -d '{
        "model": "meta-llama/Meta-Llama-3.1-70B-Instruct",
        "prompt": "Jelaskan speculative decoding dalam 3 paragraf",
        "max_tokens": 200,
        "temperature": 0
    }'
```

### Tutorial B: Implementasi Speculative Decoding Manual (Python)

```python
# speculative_decoding_demo.py
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer

class SpeculativeDecoder:
    def __init__(self, target_model, draft_model, tokenizer, k=4):
        self.target = target_model
        self.draft = draft_model
        self.tokenizer = tokenizer
        self.k = k

    @torch.no_grad()
    def generate(self, prompt, max_new_tokens=128):
        input_ids = self.tokenizer(prompt, return_tensors="pt").input_ids.cuda()
        generated = input_ids.clone()

        while generated.shape[1] < input_ids.shape[1] + max_new_tokens:
            # Draft: generate K token autoregressive
            draft_input = generated
            draft_tokens = []
            for _ in range(self.k):
                logits = self.draft(draft_input).logits[:, -1, :]
                next_token = torch.argmax(logits, dim=-1, keepdim=True)
                draft_tokens.append(next_token)
                draft_input = torch.cat([draft_input, next_token], dim=-1)

            # Target: verify semua draft token
            draft_seq = torch.cat(draft_tokens, dim=-1)
            full_seq = torch.cat([generated, draft_seq], dim=-1)
            target_logits = self.target(full_seq).logits

            # Acceptance check (greedy)
            n_accepted = 0
            for i in range(self.k):
                target_token = torch.argmax(
                    target_logits[:, generated.shape[1] + i - 1, :], dim=-1
                )
                if target_token.item() == draft_tokens[i].item():
                    n_accepted += 1
                else:
                    break

            # Terima token yang match
            generated = torch.cat(
                [generated] + draft_tokens[:max(1, n_accepted)], dim=-1
            )

        return self.tokenizer.decode(generated[0])

# Contoh penggunaan
# decoder = SpeculativeDecoder(target_model, draft_model, tokenizer, k=5)
# output = decoder.generate("Apa itu speculative decoding?")
```

### Tutorial C: Monitoring Speculative Decoding Metrics

```bash
# vLLM metrics untuk speculative decoding
curl http://localhost:8000/metrics | grep spec

# Metrics penting:
# vllm:speculative_num_accepted_tokens
# vllm:speculative_num_draft_tokens
# vllm:speculative_acceptance_rate  = accepted / draft

# Hitung acceptance rate real-time
acceptance_rate = rate(
    vllm:speculative_num_accepted_tokens[5m]
) / rate(
    vllm:speculative_num_draft_tokens[5m]
)
```

---

## 6. STUDI KASUS (WAJIB)

### Studi Kasus: API Provider — Menghemat 40% Biaya GPU
- **Latar Belakang:** API provider melayani 500 req/s dengan Llama-3.1-70B di 8x H100
- **Masalah:** Biaya GPU sangat tinggi (~$200/jam), throughput terbatas memory bandwidth
- **Solusi:** Implementasi speculative decoding dengan Llama-3.2-3B sebagai draft (rasio 2.3%)
- **Konfigurasi:** num_speculative_tokens=6, greedy decoding
- **Hasil:** Throughput naik 2.8x (12,500 -> 35,000 tok/s), GPU cost per token turun 64%
- **Efek Samping:** Opsional — bisa turunkan jumlah GPU dari 8 ke 4 dengan throughput sama
- **Pelajaran:** Draft model < 5% ukuran target memberikan speedup signifikan tanpa penurunan kualitas

---

## 7. REFERENSI WAJIB

[1] **Fast Inference from Transformers via Speculative Decoding**
```
@inproceedings{leviathan2023speculative,
  title     = {Fast Inference from Transformers via Speculative Decoding},
  author    = {Leviathan, Yaniv and Kalman, Matan and Matias, Yossi},
  booktitle = {International Conference on Machine Learning (ICML)},
  year      = {2023},
  doi       = {10.48550/arXiv.2211.17192},
  url       = {https://arxiv.org/abs/2211.17192}
}
```
- Kaitan: Paper inti speculative decoding. Data Tabel A dan B harus diverifikasi dari paper ini.

[2] **SpecInfer — Tree-based Speculative Inference**
```
@inproceedings{miao2024specinfer,
  title     = {{SpecInfer}: Accelerating Generative Large Language Model Serving with Tree-based Speculative Inference and Verification},
  author    = {Miao, Xupeng and Oliaro, Gabriele and Zhang, Zhihao and Cheng, Xinhao and Wang, Zeyu and Wong, Rae Ying Yee and Chen, Zhuoming and Arfeen, Daiyaan and Abhyankar, Reyna and Jia, Zhihao},
  booktitle = {Architectural Support for Programming Languages and Operating Systems (ASPLOS)},
  year      = {2024},
  doi       = {10.48550/arXiv.2305.09781},
  url       = {https://arxiv.org/abs/2305.09781}
}
```
- Kaitan: Tree-based speculation — meningkatkan acceptance rate dengan token tree. Data speedup di Tabel A dan B.

[3] **Medusa — Simple LLM Acceleration with Multiple Decoding Heads**
```
@inproceedings{cai2024medusa,
  title     = {{MEDUSA}: Simple {LLM} Inference Acceleration Framework with Multiple Decoding Heads},
  author    = {Cai, Tianle and Li, Yuhong and Geng, Zhengyang and Peng, Hongwu and Lee, Jason D. and Chen, Deming and Dao, Tri},
  booktitle = {International Conference on Machine Learning (ICML)},
  year      = {2024},
  doi       = {10.48550/arXiv.2401.10774},
  url       = {https://arxiv.org/abs/2401.10774}
}
```
- Kaitan: Alternatif tanpa draft model terpisah. Data speedup Medusa di Tabel A.

[4] **Self-Speculative Decoding**
```
@inproceedings{zhang2024selfspec,
  title     = {Draft \& Verify: Lossless Large Language Model Acceleration via Self-Speculative Decoding},
  author    = {Zhang, Jun and others},
  booktitle = {Proceedings of the 62nd Annual Meeting of the Association for Computational Linguistics (ACL)},
  year      = {2024},
  doi       = {10.48550/arXiv.2309.08168}
}
```
- Kaitan: Self-speculative dengan layer skipping — tidak perlu draft model eksternal.

[5] **Sequoia — Scalable Speculative Decoding**
```
@inproceedings{chen2024sequoia,
  title     = {{Sequoia}: Scalable, Robust, and Hardware-aware Speculative Decoding},
  author    = {Chen, Zhuoming and May, Avner and Svirschevski, Ruslan and Huang, Yuhsun and Ryabinin, Max and Jia, Zhihao and Chen, Beidi},
  booktitle = {Advances in Neural Information Processing Systems (NeurIPS)},
  year      = {2024},
  doi       = {10.48550/arXiv.2402.12374},
  url       = {https://arxiv.org/abs/2402.12374}
}
```
- Kaitan: Speculative decoding yang scalable dan hardware-aware. Referensi untuk hyperparameter tuning draft.

[6] vLLM Speculative Decoding Docs. *Official Documentation*. [https://docs.vllm.ai](https://docs.vllm.ai)

[7] TGI Speculative Decoding. *HuggingFace Blog*. [https://huggingface.co/docs/text-generation-inference](https://huggingface.co/docs/text-generation-inference)
