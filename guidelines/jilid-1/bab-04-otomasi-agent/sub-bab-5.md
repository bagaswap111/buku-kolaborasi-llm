# [Jilid 1] Bab 4.5: Browser Agents — Skyvern atau MultiOn Navigasi Web Lokal
> **Tipe Konten:** Teknis — Implementasi + Komparasi + Automation
> **Target Pembaca:** Pengguna yang ingin otomasi web scraping dan form filling lokal

---

## 1. TUJUAN SUB-BAB
Pembaca mampu:
- Menjelaskan cara kerja browser agent: observasi → action loop
- Mengimplementasikan Skyvern atau Playwright-based agent lokal
- Membuat workflow otomasi web (isi form, scraping, booking) dengan agent

---

## 2. KERANGKA KONTEN

### A. Konsep Browser Agent (1 paragraf)
- Definisi: AI yang mengontrol browser seperti manusia — klik, ketik, scroll, baca
- Input: screenshot + HTML DOM → Output: action (click, type, navigate)
- Loop: Observasi → Decision → Action → New State → Repeat

### B. Skyvern — Open Source Browser Agent (1-2 paragraf)
- Fitur: computer vision + LLM untuk navigasi web
- Keunggulan: tidak tergantung HTML structure (bisa handle JS-heavy sites)
- Arsitektur: Playwright + GPT-4V / local VLM

### C. MultiOn (1 paragraf)
- API-first browser agent, closed-source
- Alternatif: Playwright + Ollama untuk lokal

### D. WebVoyager & AutoWebGLM (1 paragraf)
- WebVoyager: multimodal web agent (screenshot + text)
- AutoWebGLM: open-source, bilingual (EN+ZH), outperform GPT-4 di benchmark web

### E. Setup untuk Mac Lokal (1 paragraf)
- Playwright + Ollama + Qwen-VL (multimodal lokal) atau GPT-4V (cloud)
- Headless mode vs headed mode untuk debugging

### F. Use Cases (1 paragraf)
- Otomasi isi form, booking tiket, scraping data, monitoring harga
- Eksekusi workflow multi-step: login → search → extract → save

---

## 3. TABEL WAJIB

### Tabel A: Perbandingan Browser Agent

| Agent | Open Source | Local VLM | Navigasi | Form Filling | Screenshot | Biaya |
|:---|:---:|:---:|:---:|:---:|:---:|:---|
| **Skyvern** | Ya (AGPL) | Opsional | Ya | Ya | Ya | Gratis (self-host) |
| **MultiOn** | Tidak | Tidak | Ya | Ya | Ya | API per call |
| **AutoWebGLM** | Ya (MIT) | Ya (6B) | Ya | Terbatas | Tidak | Gratis |
| **WebVoyager** | Ya | Ya (LMM) | Ya | Ya | Ya | Gratis |
| **Playwright + LLM** | Kustom | Ya | Ya | Ya | Ya | Gratis |

### Tabel B: Performa Web Agent (Task Success Rate)

| Agent | WebArena | Mind2Web | MiniWoB++ | Real-world Tasks |
|:---|:---:|:---:|:---:|:---:|
| **Claude Fable 5** + Vision | 22.5% | 55.8% | 94.2% | **72.3%** |
| GPT-5.5 + Vision | 20.1% | 52.4% | 92.8% | 68.9% |
| GPT-4V + ReAct | 14.4% | 42.3% | 88.7% | 55.7% (WebVoyager) |
| AutoWebGLM-6B | 17.2%* | 38.5% | 82.1% | - |
| DeepSeek V4 Pro + Vision | 18.5% | 48.2% | 90.5% | 60.3% |
| Skyvern (GPT-4V) | - | - | - | ~65% |
| Playwright + Qwen-VL | ~10% | ~30% | ~75% | ~40% |

### Tabel C: Resource Usage Browser Agent Lokal

| Komponen | RAM | VRAM | Storage | Latency per Action |
|:---|:---:|:---:|:---:|:---:|
| Playwright (headless) | ~200 MB | 0 | ~300 MB | 0.1s (browser) |
| Qwen-VL 7B (VLM) | ~200 MB | ~6 GB | ~15 GB | ~2s (inference) |
| Skyvern (full stack) | ~2 GB | ~6-24 GB | ~20 GB | 3-8s |

---

## 4. DIAGRAM/GAMBAR WAJIB

### Diagram 1: Browser Agent Loop (Mermaid)
- **File:** `assets/diagrams/j1-b4-s5-browser-agent-loop.mmd`
- **Isi:** Task → Screenshot + DOM → VLM/LLM → Action Decision → Playwright Execute → New Page State → Loop → Task Complete

### Gambar 2: Screenshot Skyvern Dashboard
- **File:** `assets/images/jilid1/j1-b4-s5-skyvern-dashboard.png`
- **Isi:** Tampilan Skyvern UI menampilkan log langkah, screenshot per step, dan status task

---

## 5. TUTORIAL / HANDS-ON

### Tutorial A: Browser Agent Sederhana dengan Playwright + Ollama

```python
# simple_browser_agent.py
import asyncio
from playwright.async_api import async_playwright
import requests
import json

class SimpleBrowserAgent:
    def __init__(self, llm_model="llama3.1:8b"):
        self.model = llm_model

    async def run(self, task, url):
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=False)
            page = await browser.new_page()
            await page.goto(url)

            for step in range(10):
                # 1. Observasi — ambil screenshot dan URL
                screenshot = await page.screenshot()
                title = await page.title()
                content = await page.content()

                # 2. Decision — LLM pilih action
                prompt = f"""Task: {task}
Halaman: {title}
URL: {page.url}
Actions available: CLICK_BUTTON, TYPE_TEXT, SCROLL, EXTRACT, NAVIGATE
Pilih action dan argumen dalam JSON."""
                
                resp = requests.post("http://localhost:11434/api/generate", json={
                    "model": self.model, "prompt": prompt, "stream": False
                })
                decision = json.loads(resp.json()["response"])

                # 3. Action
                if decision["action"] == "EXTRACT":
                    text = await page.text_content(decision["selector"])
                    print(f"[Extract] {text[:200]}...")
                elif decision["action"] == "CLICK_BUTTON":
                    await page.click(decision["selector"])
                elif decision["action"] == "TYPE_TEXT":
                    await page.fill(decision["selector"], decision["value"])
                elif decision["action"] == "SCROLL":
                    await page.evaluate(f"window.scrollBy(0, {decision['amount']})")

                # 4. Cek selesai
                if task.lower() in (await page.content()).lower():
                    print("Task selesai!")
                    break

            await browser.close()

# Run
agent = SimpleBrowserAgent()
asyncio.run(agent.run(
    "Cari informasi tentang AI Agent di Wikipedia",
    "https://www.wikipedia.org"
))
```

### Tutorial B: Setup Skyvern Lokal

```bash
# 1. Clone Skyvern
git clone https://github.com/Skyvern-AI/skyvern.git
cd skyvern

# 2. Setup environment
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

# 3. Setup Playwright
playwright install chromium

# 4. Konfigurasi environment variables
export LLM_PROVIDER=ollama
export OLLAMA_BASE_URL=http://localhost:11434
export MODEL_NAME=qwen2.5:7b

# 5. Jalankan Skyvern server
uvicorn skyvern.server:app --reload --port 8000

# 6. Test via API
curl -X POST http://localhost:8000/task \
  -H "Content-Type: application/json" \
  -d '{
    "url": "https://www.google.com",
    "task": "Search for AI agents and save the first result title"
  }'
```

---

## 6. STUDI KASUS

### Studi Kasus: Otomasi Booking Tiket Kereta
- **Skenario:** Setiap pagi cek harga tiket kereta Jakarta-Bandung untuk akhir pekan
- **Agent:** Skyvern + multi-step workflow
- **Workflow:**
  1. Buka KAI Access / Traveloka
  2. Isi stasiun asal-tujuan
  3. Pilih tanggal
  4. Search → extract harga
  5. Bandingkan dengan kemarin → kirim notifikasi jika turun
- **Hasil:** Running daily via cron, save ~30% dengan beli saat harga turun

---

## 7. REFERENSI WAJIB

[1] **AutoWebGLM: A Large Language Model-based Web Navigating Agent**
```
@inproceedings{lai2024autowebglm,
  title     = {{AutoWebGLM}: A Large Language Model-based Web Navigating Agent},
  author    = {Lai, Hanyu and others},
  booktitle = {Proceedings of the 30th ACM SIGKDD Conference (KDD '24)},
  year      = {2024},
  doi       = {10.1145/3637528.3671620}
}
```
- Kaitan: HTML simplification + curriculum training untuk web agent — baseline performa Tabel B.

[2] **WebVoyager: Building an End-to-End Web Agent with Large Multimodal Models**
```
@article{he2024webvoyager,
  title     = {{WebVoyager}: Building an End-to-End Web Agent with Large Multimodal Models},
  author    = {He, Hongliang and Yao, Wenlin and Ma, Kaixin and Yu, Wenhao and Dai, Yong and Zhang, Hongming and Lan, Zhenzhong and Yu, Dong},
  journal   = {arXiv preprint arXiv:2401.13919},
  year      = {2024},
  doi       = {10.48550/arXiv.2401.13919}
}
```
- Kaitan: Multimodal web agent dengan evaluation protocol — referensi arsitektur.

[3] **WebAgent: Self-experienced Agent for Web Automation**
```
@inproceedings{gur2024webagent,
  title     = {{WebAgent}: A Self-experienced Agent for Web Automation},
  author    = {Gur, Izhar and others},
  booktitle = {International Conference on Learning Representations (ICLR)},
  year      = {2024}
}
```
- Kaitan: HTML-T5 untuk summarization + plan decomposition untuk web navigation.

[4] **NNetNav: Unsupervised Learning of Browser Agents Through Environment Interaction**
```
@article{pan2024nnetnav,
  title     = {{NNetNav}: Unsupervised Learning of Browser Agents Through Environment Interaction in the Wild},
  author    = {Pan, Jiayi and others},
  journal   = {arXiv preprint arXiv:2410.02907},
  year      = {2024},
  doi       = {10.48550/arXiv.2410.02907}
}
```
- Kaitan: Self-supervised training untuk browser agent — relevan untuk praktik lokal.

[5] **OpenWebVoyager: Building Multimodal Web Agents via Iterative Real-World Exploration**
```
@article{he2024openwebvoyager,
  title     = {{OpenWebVoyager}: Building Multimodal Web Agents via Iterative Real-World Exploration, Feedback and Optimization},
  author    = {He, Hongliang and others},
  journal   = {arXiv preprint arXiv:2410.19609},
  year      = {2024},
  doi       = {10.48550/arXiv.2410.19609}
}
```
- Kaitan: Iterative self-improvement untuk web agent — siklus exploration-feedback-optimization.

### Referensi Pendukung
[6] Skyvern. *GitHub Repository*. [https://github.com/Skyvern-AI/skyvern](https://github.com/Skyvern-AI/skyvern)
[7] Playwright. *Documentation*. [https://playwright.dev](https://playwright.dev)
[8] WebArena Benchmark. [https://webarena.dev](https://webarena.dev)
