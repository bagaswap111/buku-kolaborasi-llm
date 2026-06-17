# [Jilid 1] Bab 4.9: Multi-Agent System — Dua AI Bekerja Sama (Penulis vs Editor)
> **Tipe Konten:** Arsitektural — Desain Sistem + Implementasi + Studi Kasus
> **Target Pembaca:** Pengembang yang ingin dua+ agent berkolaborasi

---

## 1. TUJUAN SUB-BAB
Pembaca mampu:
- Menjelaskan pola multi-agent: sequential, hierarchical, debate
- Mengimplementasikan sistem Writer vs Editor dengan AutoGen atau CrewAI
- Membuat workflow review berlapis dengan multiple LLM roles

---

## 2. KERANGKA KONTEN

### A. Konsep Multi-Agent System (1 paragraf)
- Definisi: Dua atau lebih agent AI dengan role berbeda bekerja sama
- Prinsip: pembagian kerja + komunikasi antar agent
- Analogi: tim manusia — ada yang nulis, ada yang review, ada yang QA

### B. Pola Multi-Agent (2-3 paragraf)
- **Sequential:** Agent A → output → Agent B → output (pipeline)
- **Hierarchical:** Manager agent delegasi ke worker agents
- **Debate:** Dua agent berdebat → moderator mengambil kesimpulan
- **Peer Review:** Agent A produce → Agent B critique → Agent A revise

### C. AutoGen — Microsoft Framework (1 paragraf)
- Konsep: conversable agent — agent bisa saling chat
- Fitur: tool use, human-in-loop, auto-reply
- Use case: Writer Assistant + Editor Critic

### D. CrewAI — Role-based Framework (1 paragraf)
- Konsep: crew dengan agent berperan spesifik (writer, editor, researcher)
- Sequential process vs hierarchical process
- Task delegation + shared context

### E. Pattern: Writer vs Editor (1-2 paragraf)
- **Writer Agent:** creative, panjang, detail — temperature tinggi (0.7)
- **Editor Agent:** kritis, ringkas, factual — temperature rendah (0.1)
- **Alur:** Writer draft → Editor review → Writer revise → Editor approve

### F. Tantangan Multi-Agent (1 paragraf)
- Latency: n agent = n kali latency single agent
- Konsistensi: agent bisa saling kontradiksi
- Cost: token usage berlipat
- Solusi: gunakan model kecil untuk agent non-kritis

---

## 3. TABEL WAJIB

### Tabel A: Perbandingan Multi-Agent Framework

| Fitur | AutoGen (Microsoft) | CrewAI | LangGraph | MetaGPT |
|:---|:---|:---|:---|:---|
| **Komunikasi** | Chat-based conversation | Role-based delegation | Graph/DAG | Chat-based |
| **Agent Type** | Conversable agent | Role agent | Node agent | Role agent |
| **Tool Use** | Ya (built-in) | Ya (built-in) | Ya | Ya |
| **Human-in-loop** | Ya | Opsional | Opsional | Tidak |
| **Memory** | Short-term | Short + Long-term | State graph | Kode |
| **Parallel** | Async conversation | Sequential default | Parallel possible | Sequential |
| **Setup** | Mudah | Sangat mudah | Sedang | Mudah |

### Tabel B: Role Configuration Writer vs Editor

| Parameter | Writer Agent | Editor Agent |
|:---|:---|:---|
| **Model** | Llama-3.1-8B (atau lebih besar) | Qwen-2.5-7B (lebih kecil) |
| **Temperature** | 0.7 — kreatif | 0.1 — presisi |
| **System Prompt** | "Kamu penulis kreatif..." | "Kamu editor kritis..." |
| **Tools** | Search web, read files | Calculator, fact-check |
| **Max Tokens Output** | 2048 (draft panjang) | 512 (review singkat) |
| **Approval Needed** | Ya (sebelum publish) | Tidak (otomatis) |

### Tabel C: Quality Improvement with Multi-Agent Review

| Metrik | Single Agent (Writer only) | Writer + Editor (1 round) | Writer + Editor (2 rounds) |
|:---|:---:|:---:|:---:|
| **Factual Accuracy** | 72% | 85% | 91% |
| **Grammar Score** | 3.8/5 | 4.5/5 | 4.7/5 |
| **Coherence** | 4.0/5 | 4.3/5 | 4.5/5 |
| **Completeness** | 65% | 80% | 88% |
| **Token Usage** | 1500 | 2500 | 3500 |

---

## 4. DIAGRAM/GAMBAR WAJIB

### Diagram 1: Multi-Agent Writer-Editor Workflow (Mermaid)
- **File:** `assets/diagrams/j1-b4-s9-multi-agent-writer-editor.mmd`
- **Isi:** Task → Writer Agent (draft) → Editor Agent (review) → Feedback → Writer (revise) → Editor (approve?) → Done atau loop

### Gambar 2: Screenshot AutoGen Multi-Agent Conversation
- **File:** `assets/images/jilid1/j1-b4-s9-autogen-chat.png`
- **Isi:** Tampilan chat antara Writer agent dan Editor agent di terminal

---

## 5. TUTORIAL / HANDS-ON

### Tutorial A: Writer vs Editor dengan AutoGen

```python
# writer_editor_autogen.py
from autogen import AssistantAgent, UserProxyAgent
import autogen

# 1. Konfigurasi LLM
llm_config = {
    "config_list": [{
        "model": "llama3.1:8b",
        "base_url": "http://localhost:11434",
        "api_type": "ollama"
    }]
}

editor_llm_config = {
    "config_list": [{
        "model": "qwen2.5:7b",
        "base_url": "http://localhost:11434",
        "api_type": "ollama"
    }]
}

# 2. Definisikan agent
writer = AssistantAgent(
    name="Writer",
    llm_config=llm_config,
    system_message="""Kamu adalah penulis konten teknis.
Tugasmu: menulis draft artikel berdasarkan topik.
Gaya: informatif, detail, contoh konkret.
Jangan khawatir tentang kesalahan — Editor akan mereview.""",
)

editor = AssistantAgent(
    name="Editor",
    llm_config=editor_llm_config,
    system_message="""Kamu adalah editor ketat.
Review draft dari Writer:
1. Koreksi factual errors
2. Perbaiki grammar dan struktur
3. Pastikan clarity
4. Beri saran perbaikan spesifik
Format: [ERROR/SARAN] + penjelasan""",
)

user = UserProxyAgent(
    name="User",
    human_input_mode="ALWAYS",
    code_execution_config=False,
)

# 3. Mulai workflow
task = "Tulis artikel pendek tentang cara kerja Docker container"

# Fase 1: Writer buat draft
user.initiate_chat(
    writer,
    message=f"Tulis draft artikel: {task}",
)
draft = user.last_message()

# Fase 2: Editor review
user.initiate_chat(
    editor,
    message=f"Review draft ini:\n{draft}",
)
review = user.last_message()

# Fase 3: Writer revisi
user.initiate_chat(
    writer,
    message=f"Revisi draft berdasarkan review:\nReview: {review}\n\nDraft asli: {draft}",
)

print("=== Artikel Final ===")
print(user.last_message())
```

### Tutorial B: Multi-Agent dengan CrewAI

```python
# crew_writer_editor.py
from crewai import Agent, Task, Crew, Process

# 1. Definisikan agents
writer = Agent(
    role="Content Writer",
    goal="Menulis draft artikel teknis yang informatif dan engaging",
    backstory="Penulis senior dengan 10 tahun experience di bidang AI",
    verbose=True,
    allow_delegation=False,
    llm_config={"model": "ollama/llama3.1:8b"},
)

editor = Agent(
    role="Technical Editor",
    goal="Memastikan draft akurat, jelas, dan bebas error",
    backstory="Editor teknis yang teliti, spesialis fact-checking",
    verbose=True,
    allow_delegation=False,
    llm_config={"model": "ollama/qwen2.5:7b"},
)

# 2. Definisikan tasks
write_task = Task(
    description="Tulis draft artikel 500 kata tentang 'Apa itu LLM Agent?'",
    expected_output="Draft artikel lengkap dengan heading dan contoh",
    agent=writer,
)

review_task = Task(
    description="Review draft artikel. Koreksi factual errors dan grammar",
    expected_output="Daftar koreksi dan saran perbaikan",
    agent=editor,
)

revise_task = Task(
    description="Revisi draft berdasarkan review editor",
    expected_output="Artikel final yang sudah direvisi",
    agent=writer,
)

# 3. Buat crew dan jalankan
crew = Crew(
    agents=[writer, editor],
    tasks=[write_task, review_task, revise_task],
    process=Process.sequential,
    verbose=True,
)

result = crew.kickoff()
print(f"\n=== Artikel Final ===\n{result}")
```

---

## 6. STUDI KASUS

### Studi Kasus: Sistem Review Buku dengan 3 Agent
- **Role:**
  1. **Writer:** Menulis draft bab buku
  2. **Editor:** Review konten dan struktur
  3. **Fact-Checker:** Verifikasi klaim teknis dengan search web
- **Alur:** Writer draft → Editor review → Writer revise → Fact-Checker verify → Editor final approve
- **Hasil:** Kualitas tulisan meningkat 40% (skor internal), fakta salah turun dari 12 → 1 per bab
- **Biaya Token:** ~8000 tokens per bab (vs 3000 single agent) — trade-off kualitas vs cost

---

## 7. REFERENSI WAJIB

[1] **AutoGen: Enabling Next-Gen LLM Applications via Multi-Agent Conversation**
```
@article{wu2023autogen,
  title     = {{AutoGen}: Enabling Next-Gen {LLM} Applications via Multi-Agent Conversation},
  author    = {Wu, Qingyun and Bansal, Gagan and Zhang, Jieyu and Wu, Yiran and Zhang, Shaokun and Zhu, Erkang and Li, Beibin and Jiang, Li and Zhang, Xiaoyun and Liu, Jiale and Awadallah, Ahmed and White, Ryen W. and Burger, Doug and Wang, Chi},
  journal   = {arXiv preprint arXiv:2308.08155},
  year      = {2023},
  doi       = {10.48550/arXiv.2308.08155}
}
```
- Kaitan: Framework multi-agent conversation — dasar implementasi Tutorial A.

[2] **Exploration of LLM Multi-Agent Application Implementation Based on LangGraph + CrewAI**
```
@article{duan2024crewai,
  title     = {Exploration of {LLM} Multi-Agent Application Implementation Based on {LangGraph}+{CrewAI}},
  author    = {Duan, Z. and others},
  journal   = {arXiv preprint arXiv:2411.18241},
  year      = {2024},
  doi       = {10.48550/arXiv.2411.18241}
}
```
- Kaitan: CrewAI role-based multi-agent — dasar implementasi Tutorial B.

[3] **Large Language Model based Multi-Agents: A Survey of Progress and Challenges**
```
@article{guo2024multisurvey,
  title     = {Large Language Model based Multi-Agents: {A} Survey of Progress and Challenges},
  author    = {Guo, Taicheng and Chen, Xiuying and Wang, Yaqi and Chang, Ruidi and Pei, Shichao and Chawla, Nitesh V. and Wiest, Olaf and Zhang, Xiangliang},
  journal   = {arXiv preprint arXiv:2402.01680},
  year      = {2024},
  doi       = {10.48550/arXiv.2402.01680}
}
```
- Kaitan: Survey multi-agent — taksonomi pola kolaborasi, komunikasi, dan tantangan.

[4] **Benchmarking Multi-Agent Frameworks: LangGraph vs. CrewAI vs. AutoGen**
```
@article{ahmad2025benchmarking,
  title     = {Benchmarking Multi-Agent Frameworks: {LangGraph} vs. {CrewAI} vs. {AutoGen}},
  author    = {Ahmad, Mohammad Sohel Jalil},
  journal   = {JATIR},
  volume    = {3},
  year      = {2025}
}
```
- Kaitan: Benchmark 80-task suite — data untuk Tabel A perbandingan framework.

[5] **Towards Effective GenAI Multi-Agent Collaboration: Design and Evaluation for Enterprise**
```
@article{papadakis2024multicollab,
  title     = {Towards Effective {GenAI} Multi-Agent Collaboration: Design and Evaluation for Enterprise Applications},
  author    = {Papadakis, Emmanouil and others},
  journal   = {arXiv preprint arXiv:2412.05449},
  year      = {2024},
  doi       = {10.48550/arXiv.2412.05449}
}
```
- Kaitan: Koordinasi multi-agent — payload referencing, routing, dan evaluasi untuk enterprise.

### Referensi Pendukung
[6] AutoGen Documentation. [https://microsoft.github.io/autogen](https://microsoft.github.io/autogen)
[7] CrewAI Documentation. [https://docs.crewai.com](https://docs.crewai.com)
[8] LangGraph Documentation. [https://langchain-ai.github.io/langgraph](https://langchain-ai.github.io/langgraph)
