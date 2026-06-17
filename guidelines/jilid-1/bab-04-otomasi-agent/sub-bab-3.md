# [Jilid 1] Bab 4.3: Planning & Reasoning — Chain-of-Thought (CoT) Lokal
> **Tipe Konten:** Teknis — Algoritma + Prompting + Implementasi
> **Target Pembaca:** Pengguna menengah yang ingin agent bisa berpikir step-by-step

---

## 1. TUJUAN SUB-BAB
Pembaca mampu:
- Menjelaskan mekanisme Chain-of-Thought prompting dan variasinya
- Menerapkan CoT, ReAct, Tree-of-Thought pada LLM lokal
- Memilih strategi reasoning yang tepat berdasarkan kompleksitas tugas

---

## 2. KERANGKA KONTEN

### A. Konsep Chain-of-Thought (1-2 paragraf)
- Definisi: Meminta LLM menghasilkan langkah-langkah reasoning antara sebelum jawaban akhir
- Paper asli (Wei et al. 2022): emergent ability pada model >100B parameter
- Contoh: "Hitung 25 * 4 + 10 = ?" → "25 * 4 = 100, 100 + 10 = 110"

### B. Jenis-Jenis CoT Prompting (2-3 paragraf)
- **Few-shot CoT:** Beri 2-3 contoh reasoning di prompt
- **Zero-shot CoT:** "Let's think step by step" (Kojima et al. 2022)
- **Self-Consistency:** Generate multiple CoT → majority voting
- **Tree-of-Thoughts (ToT):** Eksplorasi multiple reasoning paths secara simultan

### C. ReAct — Reasoning + Acting (1 paragraf)
- Yao et al. 2023: Gabungkan reasoning trace dengan action
- Format: Thought → Action → Observation → Thought → Action → ...
- Keunggulan: mengurangi halusinasi dengan grounding ke observasi eksternal

### D. CoT untuk LLM Lokal (1 paragraf)
- Model kecil (7B-14B) bisa CoT tapi akurasi lebih rendah
- Teknik: prompt engineering + format terstruktur
- Model terbaik: Llama-3.1-8B, Qwen-2.5-7B, DeepSeek-R1-Distill, DeepSeek V4 Pro (hybrid CSA/HCA attention untuk reasoning mendalam)
- **GPT-5.5** (Apr 2026) memperkenalkan parameter `reasoning_effort` (low/medium/high/xhigh) yang mengontrol depth reasoning secara eksplisit — relevan untuk agent yang butuh menyesuaikan effort berdasarkan kompleksitas task

### E. Planning vs Reasoning (1 paragraf)
- Reasoning: memecahkan masalah dengan langkah logis
- Planning: menyusun urutan aksi untuk mencapai goal
- Agent butuh keduanya: plan dulu, lalu reason saat eksekusi

### F. Evaluasi Kualitas Reasoning (1 paragraf)
- GSM8K (math word problems), MATH, HotpotQA (multi-hop QA)
- Local eval: verifikasi step-by-step, cek kontradiksi

---

## 3. TABEL WAJIB

### Tabel A: Perbandingan Metode Reasoning

| Metode | Tahun | Kebutuhan Token | Akurasi (GSM8K) | Cocok untuk | Implementasi Lokal |
|:---|:---:|:---:|:---:|:---|:---:|
| **Standard Prompting** | 2022 | Rendah | ~20% | Tugas sederhana | Mudah |
| **Few-shot CoT** | 2022 | Sedang | ~58% | Soal cerita | Mudah |
| **Zero-shot CoT** | 2022 | Rendah | ~43% | General reasoning | Sangat mudah |
| **Self-Consistency** | 2022 | Tinggi (5x) | ~72% | High-stakes decision | Berat (5x inference) |
| **Tree-of-Thoughts** | 2023 | Tinggi | ~74% | Planning kompleks | Kompleks |
| **ReAct** | 2023 | Sedang | ~60%* | Agent tasks | Mudah |

> *ReAct diukur pada HotpotQA (EM), bukan GSM8K

### Tabel B: Performa CoT pada Model Lokal (GSM8K)

| Model | Standard | Few-shot CoT | Zero-shot CoT | Self-Consistency (5) |
|:---|:---:|:---:|:---:|:---:|
| **DeepSeek V4 Pro** | 42.1% | 78.3% | 62.5% | 85.2% |
| Llama-3.1-8B | 18.2% | 52.3% | 38.7% | 64.1% |
| Qwen-2.5-7B | 22.5% | 56.8% | 42.1% | 68.3% |
| DeepSeek-R1-Distill-Qwen-7B | 25.1% | 61.2% | 45.6% | 72.4% |
| Mistral Large 3 | 35.8% | 72.5% | 55.3% | 80.1% |
| Mistral-7B | 16.8% | 48.5% | 35.2% | 60.8% |

### Tabel C: Resource Usage per Metode (7B Model)

| Metode | VRAM | Latency per Task | Cost (Token) |
|:---|:---:|:---:|:---:|
| Standard | ~4 GB | ~0.5s | ~100 tokens |
| Zero-shot CoT | ~4 GB | ~1.2s | ~250 tokens |
| Few-shot CoT (3-shot) | ~4 GB | ~1.5s | ~400 tokens |
| Self-Consistency (5) | ~4 GB | ~6.0s | ~1250 tokens |
| Tree-of-Thoughts (3 branches) | ~6 GB | ~10s | ~2000 tokens |

---

## 4. DIAGRAM/GAMBAR WAJIB

### Diagram 1: CoT vs ReAct Flow (Mermaid)
- **File:** `assets/diagrams/j1-b4-s3-cot-vs-react.mmd`
- **Isi:** Side-by-side: CoT = Question → Reasoning Steps → Answer (linear). ReAct = Question → Thought → Action → Observation → Thought → Action → Final Answer (loop)

### Gambar 2: Contoh CoT Output Terminal
- **File:** `assets/images/jilid1/j1-b4-s3-cot-terminal.png`
- **Isi:** Screenshot output Llama 3.1 menjawab soal matematika dengan langkah-langkah reasoning

---

## 5. TUTORIAL / HANDS-ON

### Tutorial A: Zero-shot CoT dengan Ollama

```python
# zero_shot_cot.py
import requests

def zero_shot_cot(model, question):
    """Zero-shot Chain-of-Thought prompting"""
    prompt = f"""{question}

Mari kita berpikir langkah demi langkah:
"""
    response = requests.post("http://localhost:11434/api/generate", json={
        "model": model,
        "prompt": prompt,
        "stream": False,
        "options": {"temperature": 0.0}
    })
    return response.json()["response"]

# Contoh
question = "Sebuah toko menjual 12 apel. Setiap apel berharga Rp 5.000. Jika ada diskon 20%, berapa total harga?"
result = zero_shot_cot("llama3.1:8b", question)
print(result)
# Output yang diharapkan: "1. Harga total tanpa diskon = 12 x 5000 = 60.000
#  2. Diskon 20% = 20/100 x 60.000 = 12.000
#  3. Total harga = 60.000 - 12.000 = 48.000
#  Jadi total harga adalah Rp 48.000"
```

### Tutorial B: ReAct Agent Sederhana

```python
# react_agent.py — implementasi ReAct untuk search knowledge base
import requests

class ReActAgent:
    def __init__(self, model="llama3.1:8b"):
        self.model = model
        self.tools = {"search_knowledge": self.search_knowledge}

    def search_knowledge(self, query):
        knowledge = {
            "ibukota Indonesia": "Jakarta",
            "luas Indonesia": "1.905 juta km²",
            "pulau terbesar": "Kalimantan"
        }
        return knowledge.get(query.lower(), "Tidak ditemukan")

    def think_act(self, task, max_steps=5):
        prompt = f"""Task: {task}
Gunakan format berikut:
Thought: [analisis langkah]
Action: [nama_tool]
Action Input: [input_tool]
Observation: [hasil_tool]

... (ulangi sampai selesai)

Thought: Saya tahu jawabannya
Final Answer: [jawaban]

Task: {task}
Thought: """
        step = 0
        while step < max_steps:
            resp = requests.post("http://localhost:11434/api/generate", json={
                "model": self.model, "prompt": prompt, "stream": False
            }).json()["response"]
            print(f"\n[Step {step}] {resp}")

            if "Final Answer:" in resp:
                return resp.split("Final Answer:")[-1].strip()

            # Parse action
            if "Action:" in resp and "Action Input:" in resp:
                tool = resp.split("Action:")[1].split("\n")[0].strip()
                inp = resp.split("Action Input:")[1].split("\n")[0].strip()
                obs = self.tools[tool](inp)
                prompt += f"\nObservation: {obs}\nThought: "
            step += 1

agent = ReActAgent()
result = agent.think_act("Apa ibukota Indonesia dan berapa luasnya?")
print(f"\n=== FINAL: {result} ===")
```

---

## 6. STUDI KASUS

### Studi Kasus: Agent Research dengan ReAct + CoT
- **Skenario:** Agent diminta riset "Bandingkan performa Llama 3.1 8B vs Qwen 2.5 7B untuk coding"
- **Alur ReAct:**
  1. Thought: "Saya perlu cari benchmark coding untuk kedua model"
  2. Action: `search_web(query="Llama 3.1 8B vs Qwen 2.5 7B HumanEval benchmark")`
  3. Observation: "Llama 3.1-8B: 72.6%, Qwen 2.5-7B: 75.2% pada HumanEval"
  4. Thought: "Qwen 2.5 unggul tipis. Saya juga perlu cek kecepatan."
  5. Action: `search_web(query="Llama 3.1 8B vs Qwen 2.5 7B inference speed")`
- **Hasil:** Laporan komparatif lengkap dengan data dan rekomendasi

---

## 7. REFERENSI WAJIB

[1] **Chain-of-Thought Prompting Elicits Reasoning in Large Language Models**
```
@inproceedings{wei2022chainofthought,
  title     = {Chain-of-Thought Prompting Elicits Reasoning in Large Language Models},
  author    = {Wei, Jason and Wang, Xuezhi and Schuurmans, Dale and Bosma, Maarten and Ichter, Brian and Xia, Fei and Chi, Ed H. and Le, Quoc V. and Zhou, Denny},
  booktitle = {Advances in Neural Information Processing Systems (NeurIPS)},
  year      = {2022},
  doi       = {10.48550/arXiv.2201.11903}
}
```
- Kaitan: Paper perintis CoT — emergent ability pada model >100B parameter.

[2] **ReAct: Synergizing Reasoning and Acting in Language Models**
```
@inproceedings{yao2023react,
  title     = {{ReAct}: Synergizing Reasoning and Acting in Language Models},
  author    = {Yao, Shunyu and Zhao, Jeffrey and Yu, Dian and Du, Nan and Shafran, Izhak and Narasimhan, Karthik and Cao, Yuan},
  booktitle = {International Conference on Learning Representations (ICLR)},
  year      = {2023},
  doi       = {10.48550/arXiv.2210.03629}
}
```
- Kaitan: Interleaving reasoning + acting — dasar untuk agent planning loop.

[3] **Self-Consistency Improves Chain of Thought Reasoning in Language Models**
```
@inproceedings{wang2023selfconsistency,
  title     = {Self-Consistency Improves Chain of Thought Reasoning in Language Models},
  author    = {Wang, Xuezhi and Wei, Jason and Schuurmans, Dale and Le, Quoc V. and Chi, Ed H. and Zhou, Denny},
  booktitle = {International Conference on Learning Representations (ICLR)},
  year      = {2023},
  doi       = {10.48550/arXiv.2203.11171}
}
```
- Kaitan: Majority voting atas multiple CoT — referensi untuk Tabel A.

[4] **Large Language Model-based Human-Agent Collaboration for Complex Task Solving**
```
@article{feng2024humanagent,
  title     = {Large Language Model-based Human-Agent Collaboration for Complex Task Solving},
  author    = {Feng, Xueyang and others},
  journal   = {arXiv preprint arXiv:2402.12914},
  year      = {2024},
  doi       = {10.48550/arXiv.2402.12914}
}
```
- Kaitan: Planning + execution dengan human-in-loop — relevan untuk agent planning.

[5] **Tree of Thoughts: Deliberate Problem Solving with Large Language Models**
```
@inproceedings{yao2023treeofthoughts,
  title     = {Tree of Thoughts: Deliberate Problem Solving with Large Language Models},
  author    = {Yao, Shunyu and Yu, Dian and Zhao, Jeffrey and Shafran, Izhak and Griffiths, Thomas L. and Cao, Yuan and Narasimhan, Karthik},
  booktitle = {Advances in Neural Information Processing Systems (NeurIPS)},
  year      = {2023},
  doi       = {10.48550/arXiv.2305.10601}
}
```
- Kaitan: Eksplorasi multi-path reasoning untuk tugas yang memerlukan pencarian.

### Referensi Pendukung
[6] Kojima et al. *Large Language Models are Zero-Shot Reasoners*. NeurIPS 2022. arXiv:2205.11916.
[7] GSM8K Benchmark. [https://github.com/openai/grade-school-math](https://github.com/openai/grade-school-math)
[8] LangChain ReAct Agent Documentation. [https://python.langchain.com/docs/modules/agents/agent_types/react](https://python.langchain.com/docs/modules/agents/agent_types/react)
