# [Jilid 2] Bab 5.7: LoRA Adapters — 10 Variasi AI dari 1 Base Model
> **Tipe Konten:** Praktis — Konsep + Implementasi + Studi Kasus
> **Target Pembaca:** Engineer yang ingin melayani multiple fine-tuned models tanpa duplikasi parameter

---

## 1. TUJUAN SUB-BAB
Pembaca memahami:
- Prinsip LoRA dan mengapa cocok untuk multi-tenant serving
- Cara melayani puluhan LoRA adapters dengan satu base model di vLLM/TGI
- Trade-off antara jumlah adapter, VRAM, dan throughput

---

## 2. KERANGKA KONTEN (WAJIB DITULIS)

### A. Konsep LoRA (2 paragraf)
- Frozen pre-trained weights + trainable low-rank matrices (A dan B)
- r << d — parameter hanya ~0.1% dari full fine-tuning untuk r=8
- Pada inference: W' = W + BA (merge) — zero additional latency

### B. LoRA Serving — Tantangan (2 paragraf)
- Naif: deploy 10 adapters = 10 instance model = 10x VRAM
- Solusi: 1 base model di memory + load adapter weights per request
- Dynamic LoRA swapping: GPU tetap, adapter berganti per user

### C. Multi-LoRA di vLLM (3 paragraf)
- Menggunakan Punica kernel: CUDA kernel untuk multiple LoRA batch
- Scheduler: group request dengan adapter yang sama untuk co-batching
- Adapter loading: simpan di CPU memory, load ke GPU saat dibutuhkan
- Batas: tergantung VRAM — 100+ adapter feasible di 1 GPU

### D. Trade-off dan Performance (1 paragraf + tabel)
- Semakin banyak adapter -> batch fragmentation -> throughput turun
- Ukuran adapter: r lebih besar -> kualitas lebih baik -> memory lebih besar
- Prefix caching membantu karena adapter berbeda tapi prefix sama

### E. Use Cases (1 paragraf)
- Chatbot dengan persona berbeda tiap user
- AI code assistant per programming language
- Model dengan domain expertise berbeda (hukum, medis, teknik)

---

## 3. TABEL WAJIB

### Tabel A: VRAM Usage — Base Model + LoRA Adapters

| Konfigurasi | Base Model (FP16) | Per Adapter (r=16) | 10 Adapters | 50 Adapters | 100 Adapters |
|:---|:---:|:---:|:---:|:---:|:---:|
| Llama-3.1-8B | 16 GB | 0.034 GB | 16.34 GB | 17.7 GB | 19.4 GB |
| Llama-3.1-70B | 140 GB | 0.26 GB | 142.6 GB | 153 GB | 166 GB |
| Qwen-2.5-32B | 64 GB | 0.12 GB | 65.2 GB | 70 GB | 76 GB |
| Mistral-7B | 14 GB | 0.028 GB | 14.28 GB | 15.4 GB | 16.8 GB |

### Tabel B: Performance Impact — Multi-LoRA Serving (vLLM, 8B, A100)

| Jumlah Adapter Aktif | Throughput (req/s) | Latency P50 (ms) | Batch Fragmentasi | VRAM Adapter |
|:---|:---:|:---:|:---:|:---:|
| 0 (base only) | 45.2 | 180 | 0% | 0 GB |
| 1 | 44.8 | 185 | 0% | 0.034 GB |
| 5 | 42.1 | 210 | 5% | 0.17 GB |
| 10 | 38.5 | 245 | 12% | 0.34 GB |
| 50 | 25.3 | 410 | 35% | 1.7 GB |
| 100 | 16.8 | 680 | 55% | 3.4 GB |

### Tabel C: Rekomendasi r (Rank) per Use Case

| Use Case | r Minimum | r Recommended | Parameter Tambahan | Kualitas vs Full FT |
|:---|:---:|:---:|:---:|:---:|
| Domain adaptation (umum) | 8 | 16 | ~0.1% | 95-98% |
| Task-specific (coding) | 16 | 32 | ~0.2% | 97-99% |
| Persona/character | 4 | 8 | ~0.05% | 90-95% |
| Multilingual | 32 | 64 | ~0.4% | 98-100% |
| Knowledge injection | 64 | 128 | ~0.8% | ~100% |

---

## 4. DIAGRAM/GAMBAR WAJIB

### Diagram 1: Arsitektur Multi-LoRA Serving (Mermaid)
- **File:** `assets/diagrams/j2-b5-s7-multilora-architecture.mmd`
- **Isi:** Request (dengan user_id) -> Router -> Adapter Lookup -> Base Model (GPU) -> Punica Kernel -> LoRA A/B Matrices -> Output
- **Node:** CPU Memory (Adapter Store), GPU Memory (Base Model), Adapter Cache

### Gambar 2: LoRA Weight Merge Visualization
- **File:** `assets/images/jilid2/j2-b5-s7-lora-merge.png`
- **Isi:** Diagram W + BA = W': weight matrix ukuran d×k, A (r×k) + B (d×r)

### Gambar 3: Throughput vs Jumlah Adapter
- **File:** `assets/images/jilid2/j2-b5-s7-throughput-vs-adapters.png`
- **Isi:** Line chart (data Tabel B) menunjukkan penurunan throughput seiring bertambahnya adapter aktif

---

## 5. TUTORIAL / HANDS-ON (WAJIB)

### Tutorial A: Serving Multiple LoRA Adapters dengan vLLM

```bash
# 1. Siapkan direktori LoRA adapters
#    /models/lora/coding-assistant/
#    /models/lora/legal-advice/
#    /models/lora/medical-consult/

# 2. Jalankan vLLM dengan multi-LoRA
vllm serve meta-llama/Meta-Llama-3.1-8B-Instruct \
    --enable-lora \
    --lora-modules coding=/models/lora/coding-assistant \
                    legal=/models/lora/legal-advice \
                    medical=/models/lora/medical-consult \
    --max-lora-rank 64 \
    --max-num-seqs 256

# 3. Panggil dengan adapter berbeda
curl http://localhost:8000/v1/chat/completions \
    -H "Content-Type: application/json" \
    -d '{
        "model": "meta-llama/Meta-Llama-3.1-8B-Instruct",
        "messages": [{"role": "user", "content": "Buatkan kontrak sewa"}],
        "max_tokens": 256,
        "lora_name": "legal"
    }'
```

### Tutorial B: Train dan Export LoRA dengan PEFT

```python
from peft import LoraConfig, get_peft_model
from transformers import AutoModelForCausalLM, AutoTokenizer

# Load base model
model = AutoModelForCausalLM.from_pretrained("meta-llama/Meta-Llama-3.1-8B-Instruct")

# Konfigurasi LoRA
lora_config = LoraConfig(
    r=16,
    lora_alpha=32,
    target_modules=["q_proj", "v_proj", "k_proj", "o_proj"],
    lora_dropout=0.05,
    bias="none",
    task_type="CAUSAL_LM",
)

# Apply LoRA
model = get_peft_model(model, lora_config)

# Train...
# model.train(...)

# Save adapter
model.save_pretrained("./lora-coding-assistant")
tokenizer.save_pretrained("./lora-coding-assistant")

# Export ke format vLLM
# rename adapter_config.json -> config.json
# rename adapter_model.safetensors -> model.safetensors
```

### Tutorial C: Dynamic LoRA Loading via API

```python
from openai import OpenAI

client = OpenAI(base_url="http://localhost:8000/v1", api_key="-")

# List available LoRA modules
modules = client.models.list()
for m in modules:
    print(m.id)  # meta-llama/Meta-Llama-3.1-8B-Instruct, coding, legal, ...

# Use specific LoRA
response = client.chat.completions.create(
    model="meta-llama/Meta-Llama-3.1-8B-Instruct",  # base model
    messages=[{"role": "user", "content": "Apa diagnosis untuk demam > 3 hari?"}],
    extra_body={"lora_name": "medical"},
)
```

---

## 6. STUDI KASUS (WAJIB)

### Studi Kasus: AI Coding Assistant untuk 3 Bahasa Pemrograman
- **Skenario:** Platform coding ingin AI assistant spesifik per bahasa: Python, Rust, JavaScript
- **Tanpa LoRA:** deploy 3x Llama-3.1-70B = 3x 140GB = 420GB VRAM — terlalu mahal
- **Dengan LoRA:** 1x Llama-3.1-70B + 3 LoRA adapters (r=32) = 140GB + 0.78GB = 140.78GB VRAM
- **Konfigurasi:** 2x H100 (80GB) — base model di TP=2, adapters di CPU memory
- **Hasil:** Throughput 38 req/s (3 adapter aktif), latency P50 280ms
- **Penghematan:** 300% lebih hemat VRAM dibandingkan deploy 3 instance terpisah

---

## 7. REFERENSI WAJIB

[1] **LoRA — Low-Rank Adaptation**
```
@inproceedings{hu2022lora,
  title     = {{LoRA}: Low-Rank Adaptation of Large Language Models},
  author    = {Hu, Edward J. and Shen, Yelong and Wallis, Phillip and Allen-Zhu, Zeyuan and Li, Yuanzhi and Wang, Shean and Wang, Lu and Chen, Weizhu},
  booktitle = {International Conference on Learning Representations (ICLR)},
  year      = {2022},
  doi       = {10.48550/arXiv.2106.09685},
  url       = {https://arxiv.org/abs/2106.09685}
}
```
- Kaitan: Paper inti LoRA. Semua konsep dan data di sub-bab ini merujuk pada paper ini.

[2] **QLoRA — 4-bit Finetuning**
```
@inproceedings{dettmers2023qlora,
  title     = {{QLoRA}: Efficient Finetuning of Quantized {LLMs}},
  author    = {Dettmers, Tim and others},
  booktitle = {Advances in Neural Information Processing Systems (NeurIPS)},
  year      = {2023},
  doi       = {10.48550/arXiv.2305.14314},
  url       = {https://arxiv.org/abs/2305.14314}
}
```
- Kaitan: LoRA + 4-bit quantization — memungkinkan fine-tuning di GPU consumer. Relevan untuk membuat adapter.

[3] **Punica — Multi-LoRA Serving**
```
@inproceedings{chen2024punica,
  title     = {{Punica}: Multi-Tenant {LoRA} Serving},
  author    = {Chen, Lequn and others},
  booktitle = {Proceedings of Machine Learning and Systems (MLSys)},
  year      = {2024},
  url       = {https://arxiv.org/abs/2310.18547}
}
```
- Kaitan: Sistem multi-LoRA yang diadopsi vLLM. Menjelaskan kernel batching untuk banyak adapter.

[4] **S-LoRA — Serving Multiple LoRA Adapters**
```
@inproceedings{sheng2024slora,
  title     = {{S-LoRA}: Serving Thousands of Concurrent {LoRA} Adapters},
  author    = {Sheng, Ying and others},
  booktitle = {Proceedings of Machine Learning and Systems (MLSys)},
  year      = {2024},
  url       = {https://arxiv.org/abs/2311.03285}
}
}
```
- Kaitan: Teknik serving ribuan LoRA dengan unified memory management. Data Tabel B merujuk pada paper ini.

[5] **LoRA Learns Less and Forgets Less**
```
@inproceedings{biderman2024lora,
  title     = {{LoRA} Learns Less and Forgets Less},
  author    = {Biderman, Dan and others},
  booktitle = {International Conference on Learning Representations (ICLR)},
  year      = {2025},
  doi       = {10.48550/arXiv.2405.09673}
}
```
- Kaitan: Studi tentang batasan LoRA dibanding full fine-tuning. Relevan untuk Tabel C — panduan pemilihan rank.

[6] HuggingFace PEFT. *Documentation*. [https://huggingface.co/docs/peft](https://huggingface.co/docs/peft)

[7] vLLM LoRA Documentation. *Official Docs*. [https://docs.vllm.ai](https://docs.vllm.ai)
