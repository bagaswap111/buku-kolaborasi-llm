# [Jilid 1] Bab 4.6: File System Mastery — Sortir, Rename, Analisa Ribuan File
> **Tipe Konten:** Praktikal — Automation + Scripting + Agent Workflow
> **Target Pembaca:** Pengguna dengan ribuan file yang perlu diorganisir secara otomatis

---

## 1. TUJUAN SUB-BAB
Pembaca mampu:
- Membangun agent yang bisa sortir, rename, dan analisa file secara otonom
- Menggunakan function calling untuk operasi file system batch
- Membuat workflow backup dan organisasi file berbasis AI

---

## 2. KERANGKA KONTEN

### A. Masalah File System Modern (1 paragraf)
- Rata-rata user Mac: 50.000-100.000 file di hard drive
- File tidak terstruktur: "Documents", "Downloads" jadi tempat sampah digital
- Manual sorting tidak scalable — butuh agent otonom

### B. Tool Set untuk File Agent (1-2 paragraf)
- Python: `os`, `shutil`, `pathlib`, `watchdog`
- CLI: `find`, `grep`, `rsync`, `exiftool`
- LLM: klasifikasi konten, ekstraksi metadata, penamaan cerdas

### C. Strategi Sorting Berbasis AI (1 paragraf)
- By file type (extension) → dasar
- By content (LLM baca konten → kategorikan) → cerdas
- By date/usage pattern → kontekstual
- Hybrid: kombinasi metadata + content analysis

### D. Rename Cerdas (1 paragraf)
- Pattern: `[YYYY-MM-DD]_[Kategori]_[Deskripsi_Pendek].[ext]`
- LLM generate nama file berdasarkan konten
- Batch rename dengan safety: dry-run first, confirm before write

### E. Analisa File Otomatis (1 paragraf)
- Scan folder → ekstrak metadata → generate laporan
- Deteksi duplikat (by hash + konten)
- Identifikasi file tidak terpakai (last accessed > 1 tahun)

### F. Safety & Backup (1 paragraf)
- Prinsip: "read before write, backup before modify"
- Agent harus punya permission level: read-only, dry-run, full-access
- Snapshots sebelum operasi massal

---

## 3. TABEL WAJIB

### Tabel A: Strategi Organisasi File

| Strategi | Metode | Akurasi | Kecepatan | Cocok untuk |
|:---|:---|:---:|:---:|:---|
| **By Extension** | Rule-based | 100% | 10.000 file/detik | Semua file |
| **By Metadata** | EXIF/ID3 | 85-95% | 1.000 file/detik | Foto, musik, dokumen |
| **By Content (LLM)** | AI classification | 90-95% | 10 file/detik | Dokumen, kode |
| **By Usage Pattern** | atime/mtime log | 70-80% | 100.000 file/detik | Arsip, backup |
| **Hybrid** | Multi-pass | 95%+ | Bervariasi | Best practice |

### Tabel B: Tools Comparison

| Tool | Fungsi | Platform | Batch | LLM Integration | Safety |
|:---|:---|:---|:---:|:---:|:---:|
| **Python pathlib** | File ops | Cross | Ya | Manual | Manual |
| **rsync** | Backup/sync | Unix | Ya | Tidak | --dry-run |
| **exiftool** | Metadata | Cross | Ya | Tidak | Read-only |
| **fdupes** | Duplicate find | Unix | Ya | Tidak | --delete |
| **rclone** | Cloud sync | Cross | Ya | Tidak | --dry-run |
| **OpenClaw file tools** | Agent-based | Cross | Ya | Built-in | Permission gates |

### Tabel C: Contoh Klasifikasi Konten (LLM-based)

| Jenis File | Ekstensi | Kategori Default | Informasi Ekstrak |
|:---|:---|:---|:---|
| **Dokumen** | .pdf, .docx, .txt | Laporan, Surat, Notulensi | Judul, tanggal, penulis |
| **Kode** | .py, .js, .tsx | Project web, script, config | Bahasa, framework, fungsi |
| **Gambar** | .jpg, .png, .raw | Foto, screenshot, desain | Tanggal, lokasi, objek |
| **Audio** | .mp3, .wav, .m4a | Musik, podcast, rekaman | Artist, durasi, genre |
| **Video** | .mp4, .mov, .mkv | Video pendek, film, tutorial | Resolusi, durasi, codec |

---

## 4. DIAGRAM/GAMBAR WAJIB

### Diagram 1: File Agent Workflow (Mermaid)
- **File:** `assets/diagrams/j1-b4-s6-file-agent-workflow.mmd`
- **Isi:** Input Folder → Scan → Read Metadata + Content → LLM Classification → Generate New Path → Dry Run → User Confirm → Execute Move/Rename → Log Report

### Gambar 2: Contoh Before-After Folder Sorting
- **File:** `assets/images/jilid1/j1-b4-s6-folder-sorting.png`
- **Isi:** Screenshot folder "Downloads" sebelum (berantakan) dan sesudah (terstruktur oleh agent)

---

## 5. TUTORIAL / HANDS-ON

### Tutorial A: File Sorting Agent dengan Python + Ollama

```python
# file_sorter_agent.py
import os
import shutil
import json
import requests
from pathlib import Path

class FileSorterAgent:
    def __init__(self, model="deepseek-v4-flash"):
        self.model = model
        self.categories = [
            "dokumen", "kode", "gambar", "audio",
            "video", "arsip", "data", "lainnya"
        ]

    def classify_file(self, filepath):
        """Gunakan LLM (DeepSeek V4 Flash atau llama3.1) untuk klasifikasi file by content"""
        ext = Path(filepath).suffix.lower()
        name = Path(filepath).name

        # Rule-based untuk yang jelas
        if ext in ['.jpg', '.png', '.gif', '.webp']:
            return "gambar"
        if ext in ['.mp3', '.wav', '.m4a', '.flac']:
            return "audio"
        if ext in ['.mp4', '.mov', '.mkv']:
            return "video"
        if ext in ['.zip', '.tar', '.gz']:
            return "arsip"
        if ext in ['.py', '.js', '.ts', '.go', '.rs']:
            return "kode"

        # Untuk dokumen, coba baca konten via LLM
        if ext in ['.txt', '.md', '.pdf']:
            try:
                with open(filepath, 'r', errors='ignore') as f:
                    content = f.read()[:500]
                prompt = f"""Klasifikasikan file ini ke kategori: {self.categories}
Nama: {name}
Konten: {content}
Jawab hanya dengan satu kata kategori."""
                resp = requests.post("http://localhost:11434/api/generate", json={
                    "model": self.model, "prompt": prompt, "stream": False
                })
                category = resp.json()["response"].strip().lower()
                return category if category in self.categories else "dokumen"
            except:
                return "dokumen"
        return "lainnya"

    def organize(self, source_dir, target_dir, dry_run=True):
        source = Path(source_dir)
        target = Path(target_dir)
        results = []

        for filepath in source.iterdir():
            if filepath.is_file():
                category = self.classify_file(filepath)
                dest_dir = target / category
                dest_path = dest_dir / filepath.name

                if dry_run:
                    results.append(f"[DRY-RUN] {filepath.name} → {category}/")
                else:
                    dest_dir.mkdir(parents=True, exist_ok=True)
                    shutil.move(str(filepath), str(dest_path))
                    results.append(f"[MOVED] {filepath.name} → {category}/")

        return results

# Penggunaan
agent = FileSorterAgent()
report = agent.organize("~/Downloads", "~/Organized", dry_run=True)
for line in report[:20]:
    print(line)
print(f"... dan {len(report)-20} file lainnya")
```

### Tutorial B: Smart Rename dengan AI

```python
# smart_rename.py
import os
import re
from datetime import datetime
import requests

def smart_rename(filepath, model="llama3.1:8b"):
    """Generate nama file deskriptif berdasarkan konten"""
    ext = os.path.splitext(filepath)[1]
    mod_time = os.path.getmtime(filepath)
    date_str = datetime.fromtimestamp(mod_time).strftime("%Y-%m-%d")

    try:
        with open(filepath, 'r', errors='ignore') as f:
            content = f.read()[:300]
    except:
        content = ""

    prompt = f"""Beri nama pendek deskriptif (max 5 kata, tanpa ekstensi) untuk file ini:
Konten: {content[:300]}
Nama asli: {os.path.basename(filepath)}
Format: kata1-kata2 (lowercase, pakai dash)"""

    resp = requests.post("http://localhost:11434/api/generate", json={
        "model": model, "prompt": prompt, "stream": False
    })
    desc = resp.json()["response"].strip()

    new_name = f"{date_str}_{desc}{ext}"
    new_path = os.path.join(os.path.dirname(filepath), new_name)

    print(f"{os.path.basename(filepath)} → {new_name}")
    return new_path

# Batch rename dengan dry-run
folder = "/path/to/files"
for f in os.listdir(folder)[:5]:  # test 5 dulu
    smart_rename(os.path.join(folder, f))
```

---

## 6. STUDI KASUS

### Studi Kasus: Organisasi Foto Keluarga 10 Tahun
- **Skenario:** 50.000 foto dari 2015-2025 tersebar di 3 hard drive dan 2 cloud
- **Agent Workflow:**
  1. Scan semua drive → kumpulkan semua .jpg/.raw/.heic
  2. Ekstrak EXIF: tanggal, lokasi, kamera
  3. LLM klasifikasi: "liburan", "ulang tahun", "daily", "makanan"
  4. Sortir ke folder: `~/Photos/[YYYY]/[YYYY-MM-DD]_[Event]/`
  5. Deteksi duplikat: hash comparison → simpan yang resolusi tertinggi
- **Hasil:** 50.000 foto terorganisir dalam 3 jam, menghemat 200GB duplikat
- **Safety:** Semua operasi dry-run dulu, backup ke external drive sebelum move

---

## 7. REFERENSI WAJIB

[1] **Voyager: An Open-Ended Embodied Agent with Large Language Models**
```
@article{wang2023voyager,
  title     = {Voyager: An Open-Ended Embodied Agent with Large Language Models},
  author    = {Wang, Guanzhi and Xie, Yuqi and Jiang, Yunfan and Mandlekar, Ajay and Xiao, Chaowei and Zhu, Yuke and Fan, Linxi and Anandkumar, Anima},
  journal   = {arXiv preprint arXiv:2305.16291},
  year      = {2023},
  doi       = {10.48550/arXiv.2305.16291}
}
```
- Kaitan: Skill library untuk code execution — konsep yang bisa diadaptasi untuk file manipulation skills.

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
- Kaitan: Agent loop untuk file operations: observe filesystem → decide action → execute → verify.

[3] **LLM-in-Sandbox Elicits General Agentic Intelligence**
```
@article{cheng2026llminsandbox,
  title     = {{LLM}-in-{Sandbox} Elicits General Agentic Intelligence},
  author    = {Cheng, Daixuan and Huang, Shaohan and Gu, Yuxian and Song, Huatong and Chen, Guoxin and Dong, Li and Zhao, Wayne Xin and Wen, Ji-Rong and Wei, Furu},
  journal   = {arXiv preprint arXiv:2601.16206},
  year      = {2026},
  doi       = {10.48550/arXiv.2601.16206}
}
}
```
- Kaitan: File system sebagai long-term memory — agent memanfaatkan file system untuk persistent context.

[4] **A Survey on Large Language Model based Autonomous Agents**
```
@article{wang2024agentsurvey,
  title     = {A Survey on Large Language Model based Autonomous Agents},
  author    = {Wang, Lei and Ma, Chen and Feng, Xueyang and others},
  journal   = {Frontiers of Computer Science},
  volume    = {18},
  number    = {6},
  pages     = {186345},
  year      = {2024},
  doi       = {10.1007/s11704-024-40231-1}
}
```
- Kaitan: Framework tool use untuk agent — termasuk file system tools sebagai kategori penting.

[5] **Agentic AI Frameworks: Architectures, Protocols, and Design Challenges**
```
@article{masterman2024agenticai,
  title     = {Agentic {AI} Frameworks: Architectures, Protocols, and Design Challenges},
  author    = {Masterman, Tula and Besen, Sandi},
  journal   = {arXiv preprint arXiv:2404.11584},
  year      = {2024},
  doi       = {10.48550/arXiv.2404.11584}
}
```
- Kaitan: Arsitektur agent untuk task execution — termasuk file system sebagai environment.

### Referensi Pendukung
[6] Python `pathlib` Documentation. [https://docs.python.org/3/library/pathlib.html](https://docs.python.org/3/library/pathlib.html)
[7] `exiftool` by Phil Harvey. [https://exiftool.org](https://exiftool.org)
[8] `rsync` man page. [https://linux.die.net/man/1/rsync](https://linux.die.net/man/1/rsync)
