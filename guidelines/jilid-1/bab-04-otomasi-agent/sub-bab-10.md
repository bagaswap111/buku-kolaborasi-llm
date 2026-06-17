# [Jilid 1] Bab 4.10: Daily Workflow Automation — Rangkuman Meeting dari Audio Lokal
> **Tipe Konten:** Praktikal — Tutorial Real-world + Pipeline Lengkap
> **Target Pembaca:** Pengguna yang ingin otomasi workflow harian dengan agent lokal

---

## 1. TUJUAN SUB-BAB
Pembaca mampu:
- Membangun pipeline otomasi: audio meeting → transkrip → rangkuman → task tracker
- Mengintegrasikan STT, LLM, dan tools dalam satu workflow agent
- Menjadwalkan workflow harian dengan cron/launchd

---

## 2. KERANGKA KONTEN

### A. Problem: Meeting Overload (1 paragraf)
- Rata-rata pekerja: 10-15 jam meeting per minggu
- 30% waktu terbuang untuk catatan manual
- Solusi: pipeline otomatis dari audio ke actionable summary

### B. Pipeline End-to-End (1-2 paragraf)
- Flow: Audio → STT (Whisper) → Rangkuman (LLM) → Ekstrak Action Items → Simpan ke Markdown → Integrasi Task Tracker
- Semua lokal, tanpa cloud, privasi terjaga

### C. Komponen Pipeline (masing-masing 1 paragraf)
1. **Audio Capture:** Otter.ai, QuickTime recording, atau Zoom lokal
2. **STT:** Whisper medium/large untuk akurasi Bahasa Indonesia
3. **Speaker Diarization:** Identifikasi siapa bicara kapan (pyannote-audio)
4. **Summarization:** LLM generate structured summary + action items
5. **Output:** File .md + Integrasi Taskwarrior/Todoist

### D. Format Output (1 paragraf)
- Meeting Title + Date + Duration
- Attendees list + Speakers
- Key Discussion Points (bullet)
- Action Items (owner + deadline)
- Full transcript (link/reference)

### E. Scheduling (1 paragraf)
- Cron job atau macOS launchd untuk auto-process folder tertentu
- Watchdog: `watchdog` Python library untuk monitor folder baru
- Notifikasi: `terminal-notifier` setelah selesai

### F. Extending Workflow (1 paragraf)
- Integrasi ke Notion/Obsidian via API
- Auto-create calendar events untuk deadline
- Email draft ke peserta meeting

---

## 3. TABEL WAJIB

### Tabel A: Pipeline Components & Resource

| Komponen | Tool | RAM | VRAM | Waktu Proses (1 jam audio) | Akurasi |
|:---|:---|:---:|:---:|:---:|:---:|
| **STT (Indonesia)** | Whisper medium | ~5 GB | ~5 GB | ~8 menit | ~9% WER |
| **STT (Indonesia)** | Whisper large-v3 | ~10 GB | ~10 GB | ~15 menit | ~7% WER |
| **Speaker Diarization** | pyannote-audio | ~2 GB | ~2 GB | ~12 menit | ~85% |
| **Summarization** | Llama-3.1-8B | ~4 GB | ~4 GB | ~2 menit | - |
| **Action Items Extraction** | Qwen-2.5-7B | ~4 GB | ~4 GB | ~1 menit | - |
| **Total Pipeline** | - | ~16 GB | ~16 GB | ~25-35 menit | - |

### Tabel B: Format Structured Output

```markdown
---
title: "Sprint Planning Week 24"
date: 2025-06-16
duration: 45 menit
attendees: ["Alice", "Bob", "Charlie"]
---

## Key Points
- Feature X 80% selesai, target deploy Jumat
- Bug Y critical — perlu hotfix hari ini
- Q3 roadmap perlu direvisi

## Action Items
- [ ] Alice: Deploy Feature X → deadline: Jumat
- [ ] Bob: Hotfix Bug Y → deadline: Hari ini
- [ ] Charlie: Revisi Q3 roadmap → deadline: Rabu

## Full Transcript
[link ke file transcript.md]
```

### Tabel C: Task Tracker Integration

| Platform | API Method | Auth | Free Tier | Notes |
|:---|:---|:---|:---:|:---|
| **Taskwarrior** | CLI lokal | None | Ya | Setup paling mudah |
| **Todoist** | REST API | OAuth | Ya (5 project) | Sync multi-device |
| **Notion** | REST API | Internal Integration | Ya (personal) | Plus database |
| **Obsidian** | Local files | None | Ya | Markdown native |
| **ClickUp** | REST API | API Key | Ya (100MB) | Enterprise ready |

---

## 4. DIAGRAM/GAMBAR WAJIB

### Diagram 1: End-to-End Meeting Pipeline (Mermaid)
- **File:** `assets/diagrams/j1-b4-s10-meeting-pipeline.mmd`
- **Isi:** Folder Audio → Whisper STT → Speaker Diarization → LLM Summarization → Action Items → Markdown Output → Task Tracker → Notifikasi

### Gambar 2: Screenshot Hasil Rangkuman Meeting
- **File:** `assets/images/jilid1/j1-b4-s10-meeting-summary.png`
- **Isi:** File markdown hasil pipeline — ada title, key points, action items, dan durasi

---

## 5. TUTORIAL / HANDS-ON

### Tutorial A: Full Pipeline Meeting Summarizer

```python
# meeting_pipeline.py
import os
import json
import subprocess
from datetime import datetime
import whisper
import requests

class MeetingPipeline:
    def __init__(self):
        self.stt_model = whisper.load_model("medium")
        self.llm_url = "http://localhost:11434/api/generate"

    def transcribe(self, audio_path):
        """Step 1: Speech-to-text"""
        print(f"[1/4] Transkripsi {audio_path}...")
        result = self.stt_model.transcribe(
            audio_path, language="id",
            task="transcribe", verbose=False
        )
        transcript = result["text"]
        segments = result["segments"]

        # Simpan transcript
        transcript_path = audio_path.replace(".wav", "_transcript.txt")
        with open(transcript_path, "w") as f:
            for seg in segments:
                start = seg["start"]
                text = seg["text"]
                f.write(f"[{start:.0f}s] {text}\n")

        return transcript, transcript_path

    def summarize(self, transcript, meeting_title):
        """Step 2: LLM summarization"""
        print("[2/4] Membuat rangkuman...")
        prompt = f"""Buat rangkuman meeting dari transkrip berikut.

Judul: {meeting_title}
Transkrip:
{transcript[:8000]}

Format output:
## Key Points
- [poin utama 1]
- [poin utama 2]

## Action Items
- [ ] [tugas] → deadline: [tanggal]
- [ ] [tugas] → deadline: [tanggal]

## Kesimpulan
"""
        resp = requests.post(self.llm_url, json={
            "model": "llama3.1:8b",
            "prompt": prompt,
            "stream": False,
            "options": {"temperature": 0.2}
        })
        return resp.json()["response"]

    def extract_actions(self, summary):
        """Step 3: Ekstrak action items terstruktur"""
        print("[3/4] Ekstrak action items...")
        prompt = f"""Dari rangkuman meeting berikut, ekstrak semua action items dalam format JSON array.
Setiap item: {{"task": "...", "owner": "...", "deadline": "..."}}

Rangkuman:
{summary}

JSON:"""
        resp = requests.post(self.llm_url, json={
            "model": "qwen2.5:7b",
            "prompt": prompt,
            "stream": False,
            "format": "json"
        })
        try:
            return json.loads(resp.json()["response"])
        except:
            return []

    def save_output(self, summary, actions, metadata):
        """Step 3: Simpan ke file markdown"""
        print("[4/4] Menyimpan output...")
        date = datetime.now().strftime("%Y-%m-%d")
        filename = f"meeting_{date}_{metadata['title'].replace(' ', '_')}.md"

        with open(filename, "w") as f:
            f.write(f"---\ntitle: \"{metadata['title']}\"\n")
            f.write(f"date: {date}\nduration: {metadata['duration']} menit\n---\n\n")
            f.write(summary)
            f.write("\n## Action Items (Structured)\n")
            for item in actions:
                owner = item.get("owner", "TBD")
                deadline = item.get("deadline", "TBD")
                f.write(f"- [ ] {item['task']} (Owner: {owner}, Deadline: {deadline})\n")

        print(f"Output: {filename}")
        return filename

    def run(self, audio_path, title="Untitled Meeting", duration=60):
        metadata = {"title": title, "duration": duration}
        transcript, _ = self.transcribe(audio_path)
        summary = self.summarize(transcript, title)
        actions = self.extract_actions(summary)
        output = self.save_output(summary, actions, metadata)
        print(f"\n✅ Pipeline selesai! File: {output}")

# Penggunaan
pipeline = MeetingPipeline()
pipeline.run("meeting_2025-06-16.wav",
             title="Sprint Planning Week 24",
             duration=45)
```

### Tutorial B: Folder Watcher Otomatis (macOS + launchd)

```bash
# 1. Buat script watcher
cat > ~/bin/meeting_watcher.sh << 'SCRIPT'
#!/bin/bash
WATCH_DIR=~/Documents/Meetings/Audio
PROCESSED_DIR=~/Documents/Meetings/Processed

inotifywait -m "$WATCH_DIR" -e create -e moved_to |
    while read path action file; do
        if [[ "$file" == *.wav ]] || [[ "$file" == *.m4a ]]; then
            echo "[$(date)] New audio: $file"
            cd ~/Documents/Meetings
            python3 meeting_pipeline.py "$WATCH_DIR/$file"
            mv "$WATCH_DIR/$file" "$PROCESSED_DIR/"
            terminal-notifier -title "Meeting Pipeline" \
                -message "Rangkuman selesai: $file" \
                -sound default
        fi
    done
SCRIPT

# 2. Atau pakai cron untuk batch harian
echo "0 18 * * 1-5 cd ~/Documents/Meetings && python3 batch_process.py" | crontab -
```

### Tutorial C: Batch Process Harian

```python
# batch_process.py — proses semua audio hari ini
from meeting_pipeline import MeetingPipeline
from pathlib import Path
import sys

pipeline = MeetingPipeline()
audio_dir = Path("~/Documents/Meetings/Audio").expanduser()
processed_dir = Path("~/Documents/Meetings/Processed").expanduser()
processed_dir.mkdir(exist_ok=True)

audio_files = list(audio_dir.glob("*.[wW][aA][vV]")) + \
              list(audio_dir.glob("*.[mM]4[aA]"))

for i, audio in enumerate(audio_files):
    print(f"\n=== Processing {i+1}/{len(audio_files)}: {audio.name} ===")
    pipeline.run(str(audio), title=audio.stem)
    audio.rename(processed_dir / audio.name)

print(f"\n✅ Selesai! {len(audio_files)} meeting diproses.")
```

---

## 6. STUDI KASUS

### Studi Kasus: Otomasi Meeting Management — Startup 10 Orang
- **Setup:** Mac Mini M4 Pro 48GB, Ollama + Whisper + pipeline Python
- **Workflow:**
  1. Semua meeting direkam via Zoom → otomatis tersimpan di folder
  2. Pukul 18:00 setiap hari, cron trigger batch_process.py
  3. Pipeline: STT → Rangkuman → Action Items → Simpan ke Obsidian
  4. Action items auto-sync ke Taskwarrior via script
- **Hasil:** 15 jam meeting/minggu → 30 menit review rangkuman
- **Efisiensi:** 96% waktu hemat untuk notulensi

---

## 7. REFERENSI WAJIB

[1] **Summaries, Highlights, and Action Items: Design, Implementation and Evaluation of an LLM-powered Meeting Recap System**
```
@article{yang2025meetingrecap,
  title     = {Summaries, Highlights, and Action Items: Design, Implementation and Evaluation of an {LLM}-powered Meeting Recap System},
  author    = {Yang, Yifei and others},
  journal   = {Proceedings of the ACM on Human-Computer Interaction (CSCW)},
  volume    = {9},
  number    = {2},
  pages     = {CSCW176},
  year      = {2025},
  doi       = {10.1145/3711074}
}
```
- Kaitan: Desain sistem recap meeting — highlights vs structured minutes, evaluasi dengan 7 user.

[2] **Re-FRAME the Meeting Summarization SCOPE: Fact-Based Summarization and Personalization via Questions**
```
@article{kirstein2025frame,
  title     = {Re-{FRAME} the Meeting Summarization {SCOPE}: Fact-Based Summarization and Personalization via Questions},
  author    = {Kirstein, Fabian and others},
  journal   = {arXiv preprint arXiv:2503.19843},
  year      = {2025}
}
```
- Kaitan: FRAME pipeline untuk meeting summarization — richness extraction + fact verification.

[3] **Robust Speech Recognition via Large-Scale Weak Supervision**
```
@inproceedings{radford2023whisper,
  title     = {Robust Speech Recognition via Large-Scale Weak Supervision},
  author    = {Radford, Alec and Kim, Jong Wook and Xu, Tao and Brockman, Greg and McLeavey, Christine and Sutskever, Ilya},
  booktitle = {Proceedings of the 40th International Conference on Machine Learning (ICML)},
  pages     = {28492--28518},
  year      = {2023},
  doi       = {10.48550/arXiv.2212.04356}
}
}
```
- Kaitan: Whisper sebagai STT backbone pipeline — akurasi dan resource di Tabel A.

[4] **AutoFlow: Automated Workflow Generation for Large Language Model Agents**
```
@article{zhang2024autoflow,
  title     = {{AutoFlow}: Automated Workflow Generation for Large Language Model Agents},
  author    = {Zhang, Yifan and others},
  journal   = {arXiv preprint arXiv:2407.12821},
  year      = {2024},
  doi       = {10.48550/arXiv.2407.12821}
}
```
- Kaitan: Automated workflow generation — natural language to agentic workflow pipeline.

[5] **AI-Powered Meeting Assistant: An LLM-Centric, Agentic AI Approach for Automating Post-Meeting Workflows**
```
@article{patel2025meetingassistant,
  title     = {{AI}-Powered Meeting Assistant: An {LLM}-Centric, Agentic {AI} Approach for Automating Post-Meeting Workflows},
  author    = {Patel, Nikit and Patel, Kaushal},
  journal   = {Scientific Research Journal of Science, Engineering and Technology},
  volume    = {3},
  number    = {1},
  pages     = {55--60},
  year      = {2025}
}
```
- Kaitan: Arsitektur end-to-end meeting assistant — audio ingestion to task tracker integration.

### Referensi Pendukung
[6] Whisper (OpenAI). *GitHub Repository*. [https://github.com/openai/whisper](https://github.com/openai/whisper)
[7] pyannote-audio. *Speaker Diarization*. [https://github.com/pyannote/pyannote-audio](https://github.com/pyannote/pyannote-audio)
[8] Taskwarrior. *Task Management CLI*. [https://taskwarrior.org](https://taskwarrior.org)
