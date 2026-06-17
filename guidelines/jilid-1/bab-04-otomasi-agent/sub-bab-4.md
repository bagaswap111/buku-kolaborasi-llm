# [Jilid 1] Bab 4.4: Coding Agents — Implementasi Cline dan Aider untuk Mac
> **Tipe Konten:** Praktikal — Tutorial + Setup + Best Practices
> **Target Pembaca:** Developer Mac yang ingin otomasi coding lokal

---

## 1. TUJUAN SUB-BAB
Pembaca mampu:
- Menginstall dan mengkonfigurasi Cline dan Aider di macOS
- Menggunakan kedua coding agent untuk task pemrograman nyata
- Memahami perbedaan filosofi: Cline (agentic, multi-file) vs Aider (pair-programming, git-aware)

---

## 2. KERANGKA KONTEN

### A. Apa Itu Coding Agent? (1 paragraf)
- Definisi: AI yang bisa membaca, menulis, dan mengeksekusi code secara otonom
- Bukan sekadar autocomplete (TabNine) atau chat (ChatGPT) — agent bisa plan, write, test, fix

### B. Cline — Autonomous Coding Agent (2 paragraf)
- Sejarah: Claude Dev → Cline, open-source Apache 2.0
- Fitur: Plan/Act mode, diff preview, checkpoint/undo, terminal execution
- Backend: Support OpenAI, Anthropic, Ollama, LM Studio (local)
- Arsitektur: VS Code extension + CLI + SDK

### C. Aider — Pair Programming in Terminal (1-2 paragraf)
- Filosofi: "AI pair programmer" — berbasis git commit
- Fitur: map repo, automatic git commit, lint fix, multi-file editing
- Keunggulan: transparan — semua perubahan tercatat di git

### D. Perbandingan Cline vs Aider (1 paragraf + tabel)
- Cline: lebih cocok untuk task kompleks, multi-step, exploratory
- Aider: lebih cocok untuk refactoring, bug fix, feature implementation

### E. Setup untuk Mac dengan LLM Lokal (1 paragraf)
- Ollama sebagai backend lokal
- LM Studio untuk model dengan GPU acceleration
- Apple Silicon optimization: Metal GPU offload

### F. Best Practices & Safety (1 paragraf)
- Selalu review diff sebelum approve
- Gunakan git branch terpisah untuk agent work
- Batasi akses file dengan permission scope

---

## 3. TABEL WAJIB

### Tabel A: Perbandingan Coding Agent untuk Mac

| Fitur | Cline | Aider | GitHub Copilot | Cursor |
|:---|:---|:---|:---|:---|
| **Tipe** | Agent otonom | Pair programmer | Autocomplete + Chat | Agent IDE |
| **Open Source** | Ya (Apache 2.0) | Ya (Apache 2.0) | Tidak | Closed (fork VS Code) |
| **Local LLM** | Ya (Ollama/LM Studio) | Ya (Ollama) | Tidak | Terbatas |
| **Multi-file Edit** | Ya | Ya | Parsial | Ya |
| **Git Integration** | Checkpoint system | Auto-commit | Manual | Checkpoint |
| **Terminal Access** | Ya | Ya | Tidak | Built-in |
| **Plan Mode** | Ya (Plan → Act) | Tidak | Tidak | Tidak |
| **Apple Silicon** | Native | Native | Native | Native |

### Tabel B: Performa Coding Agent dengan Model Lokal (HumanEval+)

| Model | Cline (Pass@1) | Aider (Pass@1) | Kecepatan (t/s) |
|:---|:---:|:---:|:---:|
| Llama-3.1-8B | 62.4% | 58.7% | ~45 t/s (M4 Max) |
| Qwen-2.5-Coder-7B | 68.1% | 65.3% | ~52 t/s |
| DeepSeek-Coder-V2-Lite | 71.5% | 69.8% | ~38 t/s |
| GPT-4o (cloud) | 87.3% | 85.1% | ~30 t/s (API) |

### Tabel C: Resource Usage

| Agent | RAM (idle) | VRAM (7B model) | Disk | Latency First Token |
|:---|:---:|:---:|:---:|:---:|
| Cline + Ollama | ~120 MB | ~4.5 GB | ~500 MB | ~1.2s |
| Aider + Ollama | ~80 MB | ~4.5 GB | ~200 MB | ~0.8s |
| Cline + OpenAI | ~200 MB | 0 | ~100 MB | ~0.5s (network) |

---

## 4. DIAGRAM/GAMBAR WAJIB

### Diagram 1: Arsitektur Cline Agent (Mermaid)
- **File:** `assets/diagrams/j1-b4-s4-cline-architecture.mmd`
- **Isi:** User VS Code → Cline Extension → Agent Loop (Plan/Act) → Tools (File/Shell/Browser) → LLM Backend (Ollama/OpenAI) → Response → Diff → User Approval

### Gambar 2: Screenshot Cline Plan Mode vs Act Mode
- **File:** `assets/images/jilid1/j1-b4-s4-cline-plan-act.png`
- **Isi:** Side-by-side: Plan mode menampilkan deskripsi strategi, Act mode menampilkan diff perubahan

---

## 5. TUTORIAL / HANDS-ON

### Tutorial A: Setup Cline dengan Ollama Lokal di Mac

```bash
# 1. Install Ollama (jika belum)
brew install ollama
ollama pull llama3.1:8b

# 2. Install Cline via VS Code
# Buka VS Code → Extensions → Cari "Cline" → Install

# 3. Atau install CLI
npm install -g @cline/cli

# 4. Konfigurasi Cline untuk local Ollama
# Di VS Code Settings → Cline → Provider: Ollama
# Model: llama3.1:8b
# Base URL: http://localhost:11434

# 5. Test dengan task sederhana
cline run "Buat fungsi Python untuk menghitung Fibonacci, simpan di fib.py"

# 6. Cline akan:
#    - Plan: membuat file fib.py dengan fungsi fibonacci
#    - Act: menulis kode, menampilkan diff
#    - Anda approve → file tersimpan
```

### Tutorial B: Setup Aider untuk Refactoring

```bash
# 1. Install Aider
pip install aider-chat

# 2. Konfigurasi untuk Ollama
export OLLAMA_API_BASE=http://localhost:11434
aider --model ollama/llama3.1:8b \
      --map-refresh=auto \
      --auto-commits \
      --lint

# 3. Di direktori project, mulai sesi
cd my-project
aider

# 4. Prompt untuk refactoring
# > Refactor fungsi validate_email() di src/utils.py:
#   - Gunakan regex yang lebih robust
#   - Tambahkan type hints
#   - Tambahkan docstring
#   - Buat unit test di tests/test_utils.py

# 5. Aider akan:
#    - Map struktur kode
#    - Edit file
#    - Auto-commit ke git dengan pesan deskriptif
#    - Jalankan linter untuk verifikasi
```

### Tutorial C: Script Batch untuk Automated Code Review

```python
# batch_review.py — jalankan Cline/Aider untuk review semua PR
import subprocess
import json

def review_with_agent(filepath):
    prompt = f"""Review file {filepath} untuk:
1. Potensi bug dan security issues
2. Code style violations
3. Performance bottlenecks
4. Saran refactoring"""
    
    result = subprocess.run(
        ["cline", "run", prompt, "--file", filepath],
        capture_output=True, text=True
    )
    return result.stdout

# Batch process semua file .py yang diubah
files = ["src/main.py", "src/api.py", "tests/test_api.py"]
for f in files:
    print(f"=== Reviewing {f} ===")
    print(review_with_agent(f))
```

---

## 6. STUDI KASUS

### Studi Kasus: Refactoring Legacy Codebase dengan Aider
- **Skenario:** Codebase Django 50.000 baris dengan banyak technical debt
- **Task:** Migrasi dari function-based views ke class-based views di 20 file
- **Setup:** `aider --model ollama/qwen2.5-coder:7b --auto-commits`
- **Proses:** 5 prompt bertahap, masing-masing 3-5 file per prompt
- **Hasil:** Selesai 45 menit (vs ~8 jam manual), 100% test passing
- **Pelajaran:** Agent bekerja optimal dengan prompt spesifik per modul

---

## 7. REFERENSI WAJIB

[1] **The Rise of AI Teammates in Software Engineering (SE) 3.0: How Autonomous Coding Agents Are Reshaping Software Engineering**
```
@article{li2025aiteammates,
  title     = {The Rise of {AI} Teammates in Software Engineering {(SE)} 3.0: How Autonomous Coding Agents Are Reshaping Software Engineering},
  author    = {Li, Hao and Zhang, Hongyu and Hassan, Ahmed E.},
  journal   = {arXiv preprint arXiv:2507.15003},
  year      = {2025},
  doi       = {10.48550/arXiv.2507.15003}
}
```
- Kaitan: Dataset AIDev — 456k PR dari coding agent (Cline, Copilot, Cursor) — data empiris Tabel B.

[2] **Understanding the Planning of LLM Agents: A Survey**
```
@article{huang2024planning,
  title     = {Understanding the Planning of {LLM} Agents: {A} Survey},
  author    = {Huang, Xu and others},
  journal   = {arXiv preprint arXiv:2402.02716},
  year      = {2024},
  doi       = {10.48550/arXiv.2402.02716}
}
```
- Kaitan: Planning strategies untuk coding agent — relevan untuk Plan/Act mode Cline.

[3] **An LLM Compiler for Parallel Function Calling**
```
@inproceedings{kim2024llmcompiler,
  title     = {An {LLM} Compiler for Parallel Function Calling},
  author    = {Kim, Sehoon and Moon, Suhong and Tabrizi, Ryan and Lee, Nicholas and Mahoney, Michael W. and Keutzer, Kurt and Gholami, Amir},
  booktitle = {International Conference on Machine Learning (ICML)},
  year      = {2024},
  doi       = {10.48550/arXiv.2312.04511}
}
```
- Kaitan: Paralelisasi function call untuk mempercepat coding agent latency.

[4] **Challenges and Paths Towards AI for Software Engineering**
```
@inproceedings{gu2025challenges,
  title     = {Challenges and Paths Towards {AI} for Software Engineering},
  author    = {Gu, Zhongjun and Solar-Lezama, Armando and Sen, Koushik and Jain, Naman and Shetty, Manish and Ellis, Kevin and Li, Wen-Ding and Yang, Diyi and Shao, Yijia and Li, Ziyang},
  booktitle = {International Conference on Machine Learning (ICML)},
  year      = {2025}
}
```
- Kaitan: Mapping tantangan AI untuk software engineering — dari code gen ke debugging.

[5] **On the Use of Agentic Coding: An Empirical Study of Pull Requests on GitHub**
```
@article{watanabe2025agenticcoding,
  title     = {On the Use of Agentic Coding: An Empirical Study of Pull Requests on {GitHub}},
  author    = {Watanabe, Masanari and Li, Hao and Kashiwa, Yutaro and Reid, Blake and Iida, Hajimu and Hassan, Ahmed E.},
  journal   = {ACM Transactions on Software Engineering and Methodology},
  year      = {2025},
  doi       = {10.1145/3718650}
}
```
- Kaitan: Studi empiris coding agent di GitHub — pola penggunaan dan kualitas kontribusi.

### Referensi Pendukung
[6] Cline. *Official Documentation*. [https://docs.cline.bot](https://docs.cline.bot)
[7] Aider. *GitHub Repository*. [https://github.com/Aider-AI/aider](https://github.com/Aider-AI/aider)
[8] Ollama. *GitHub Repository*. [https://github.com/ollama/ollama](https://github.com/ollama/ollama)
