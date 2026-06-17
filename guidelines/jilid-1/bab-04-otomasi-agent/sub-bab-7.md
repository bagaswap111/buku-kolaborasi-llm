# [Jilid 1] Bab 4.7: Integrasi Suara (STT/TTS) — Whisper & Piper Tanpa Cloud
> **Tipe Konten:** Teknis — Implementasi + Integrasi Voice Pipeline
> **Target Pembaca:** Pengguna yang ingin kontrol suara lokal tanpa cloud

---

## 1. TUJUAN SUB-BAB
Pembaca mampu:
- Menginstall dan menjalankan Whisper untuk speech-to-text lokal
- Menginstall dan menjalankan Piper TTS untuk text-to-speech lokal
- Membangun voice pipeline: Mic → STT → LLM → TTS → Speaker

---

## 2. KERANGKA KONTEN

### A. Konsep STT/TTS Lokal (1 paragraf)
- STT (Speech-to-Text): ubah suara ke teks — Whisper (OpenAI), open-source, multi-bahasa
- TTS (Text-to-Speech): ubah teks ke suara — Piper (Rhasspy), lokal, enteng
- Keuntungan lokal: privasi (tidak ada audio ke cloud), latency (no network), gratis

### B. Whisper — Model dan Varian (1-2 paragraf)
- Arsitektur: Encoder-decoder Transformer, trained on 680rb jam audio
- Varian: tiny (39M), base (74M), small (244M), medium (769M), large (1.55B), turbo (809M)
- Kualitas: large-v3 ≈ human-level WER
- faster-whisper: CTranslate2 backend — 4x lebih cepat

### C. Piper TTS — Arsitektur (1 paragraf)
- Berbasis VITS + ONNX Runtime
- Output: 16kHz-22kHz audio
- 30+ bahasa, 4 level kualitas (x_low, low, medium, high)

### D. Pipeline Voice Agent (1 paragraf)
- Flow: Microphone → VAD (Voice Activity Detection) → Whisper STT → LLM → Piper TTS → Speaker
- Latency target: < 3 detik end-to-end untuk real-time
- Tools: `speech_recognition` (Python), `pyaudio`, `sounddevice`

### E. Optimasi untuk Mac (1 paragraf)
- Apple Silicon: CoreML Whisper (via `mlx-whisper`) — 2x lebih cepat
- Piper: ONNX Runtime dengan CPU saja sudah memadai
- VAD: Silero VAD untuk deteksi kapan mulai/selesai bicara

### F. Use Cases (1 paragraf)
- Voice assistant lokal (Siri lokal tanpa cloud)
- Transkripsi meeting otomatis
- Audio journaling dengan LLM

---

## 3. TABEL WAJIB

### Tabel A: Perbandingan Varian Whisper

| Model | Parameter | RAM | Relative Speed | WER (English) | WER (Indonesia) |
|:---|:---:|:---:|:---:|:---:|:---:|
| **tiny** | 39M | ~1 GB | ~10x | 9.8% | 18.5% |
| **base** | 74M | ~1 GB | ~7x | 7.9% | 15.2% |
| **small** | 244M | ~2 GB | ~4x | 6.1% | 11.8% |
| **medium** | 769M | ~5 GB | ~2x | 5.0% | 9.3% |
| **large-v3** | 1550M | ~10 GB | 1x | 4.2% | 7.1% |
| **turbo** | 809M | ~6 GB | ~2.5x | 4.5% | 7.8% |

### Tabel B: Perbandingan TTS Lokal

| Engine | Kualitas Suara | Kecepatan (RTF) | Bahasa | Parameter | Platform |
|:---|:---:|:---:|:---:|:---:|:---:|
| **Piper** | Medium-Tinggi | 0.3-0.8 RTF | 30+ | ~50M | CPU/GPU |
| **Coqui TTS** | Tinggi | 0.5-1.5 RTF | 20+ | ~100M | GPU |
| **eSpeak-NG** | Rendah (robotik) | 0.01 RTF | 100+ | 0 (rule-based) | CPU |
| **MeloTTS** | Tinggi | 0.2-0.5 RTF | 5 | ~80M | CPU/GPU |

### Tabel C: Pipeline Latency Budget (target <3 detik)

| Komponen | Waktu (ms) | Keterangan |
|:---|:---:|:---|
| VAD (Silero) | 20-50 | Deteksi mulai bicara |
| Whisper STT (small) | 300-800 | Transkripsi |
| LLM Inference (7B, 128 token) | 500-1500 | Generate respons |
| Piper TTS (medium) | 200-500 | Sintesis suara |
| **Total** | **~1000-2850** | **Target tercapai** |

---

## 4. DIAGRAM/GAMBAR WAJIB

### Diagram 1: Voice Agent Pipeline (Mermaid)
- **File:** `assets/diagrams/j1-b4-s7-voice-pipeline.mmd`
- **Isi:** Mic → VAD → Whisper STT → Teks → LLM → Teks Respons → Piper TTS → Audio → Speaker
- **Anotasi:** Waktu tempuh setiap stage

### Gambar 2: Screenshot Whisper Transkripsi Terminal
- **File:** `assets/images/jilid1/j1-b4-s7-whisper-terminal.png`
- **Isi:** Output terminal Whisper mentranskrip audio Bahasa Indonesia

---

## 5. TUTORIAL / HANDS-ON

### Tutorial A: STT Lokal dengan Whisper

```python
# whisper_stt.py
import whisper
import time

# 1. Load model (download otomatis pertama kali)
model = whisper.load_model("small")  # atau "base", "medium", "large"

# 2. Transkrip file audio
result = model.transcribe(
    "recording.wav",
    language="id",
    task="transcribe",
    verbose=True
)
print(f"Teks: {result['text']}")
print(f"Bahasa: {result['language']}")
print(f"Durasi: {result['segments'][-1]['end']:.2f}s")

# 3. Real-time dari mic (versi sederhana)
import sounddevice as sd
import numpy as np

def record_audio(duration=5, samplerate=16000):
    print("Rekam...")
    audio = sd.rec(int(duration * samplerate),
                   samplerate=samplerate,
                   channels=1, dtype='float32')
    sd.wait()
    return audio.flatten()

audio = record_audio(5)
result = model.transcribe(audio, language="id")
print(f"Anda: {result['text']}")
```

### Tutorial B: TTS Lokal dengan Piper

```python
# piper_tts.py
import subprocess
import tempfile

def text_to_speech(text, voice="id_ID-female-medium", output="output.wav"):
    """Konversi teks ke speech dengan Piper"""
    cmd = [
        "piper",
        "--model", voice,
        "--output_file", output
    ]
    proc = subprocess.Popen(
        cmd, stdin=subprocess.PIPE, stdout=subprocess.PIPE
    )
    proc.stdin.write(text.encode())
    proc.stdin.close()
    proc.wait()
    print(f"Audio saved: {output}")

# Atau via Python API (piper-tts library)
from piper import PiperVoice
import wave

voice = PiperVoice.load("id_ID-female-medium.onnx")
with wave.open("output.wav", "w") as wav:
    voice.synthesize("Selamat datang di buku Local LLM Encyclopedia", wav)

# Play audio (Mac)
import subprocess
subprocess.run(["afplay", "output.wav"])
```

### Tutorial C: Voice Agent End-to-End

```python
# voice_agent.py — mic → STT → LLM → TTS → speaker
import whisper
import subprocess
import sounddevice as sd
import numpy as np
import requests
import tempfile
import wave

class VoiceAgent:
    def __init__(self):
        self.stt = whisper.load_model("small")
        self.llm_url = "http://localhost:11434/api/generate"

    def listen(self, duration=5):
        audio = sd.rec(int(duration * 16000),
                       samplerate=16000, channels=1, dtype='float32')
        sd.wait()
        return audio.flatten()

    def transcribe(self, audio):
        result = self.stt.transcribe(audio, language="id")
        return result["text"]

    def think(self, text):
        resp = requests.post(self.llm_url, json={
            "model": "deepseek-v4-flash",
            "prompt": f"Jawab singkat: {text}",
            "stream": False
        })
        return resp.json()["response"]

    def speak(self, text):
        subprocess.run(["piper", "--model", "id_ID-female-medium",
                        "--output_file", "/tmp/response.wav"],
                       input=text.encode())
        subprocess.run(["afplay", "/tmp/response.wav"])

    def run(self):
        print("Agent siap. Tekan Enter untuk mulai bicara...")
        input()
        audio = self.listen()
        teks = self.transcribe(audio)
        print(f"Anda: {teks}")
        jawaban = self.think(teks)
        print(f"Agent: {jawaban}")
        self.speak(jawaban)

agent = VoiceAgent()
agent.run()
```

---

## 6. STUDI KASUS

### Studi Kasus: Voice Journal Harian
- **Skenario:** Setiap malam, user ngobrol 5 menit ke voice agent tentang aktivitas hari ini
- **Pipeline:** Mic → Whisper STT → DeepSeek V4 Flash / Llama 3.1 → Ringkasan harian → Simpan ke file .md
- **Hasil:** 1 bulan → 30 file jurnal terstruktur, bisa di-search dan dianalisa; DeepSeek V4 Flash memberikan ringkasan lebih detail berkat context window 1M
- **Privasi:** Tidak ada audio/data yang meninggalkan Mac — aman untuk jurnal pribadi

---

## 7. REFERENSI WAJIB

[1] **Robust Speech Recognition via Large-Scale Weak Supervision**
```
@inproceedings{radford2023whisper,
  title     = {Robust Speech Recognition via Large-Scale Weak Supervision},
  author    = {Radford, Alec and Kim, Jong Wook and Xu, Tao and Brockman, Greg and McLeavey, Christine and Sutskever, Ilya},
  booktitle = {Proceedings of the 40th International Conference on Machine Learning (ICML)},
  pages     = {28492--28518},
  year      = {2023},
  doi       = {10.48550/arXiv.2212.04356}
}
```
- Kaitan: Paper utama Whisper — trained on 680rb jam audio, 97 bahasa. Dasar seluruh implementasi STT lokal.

[2] **Distil-Whisper: Robust Knowledge Distillation via Large-Scale Pseudo Labelling**
```
@article{gandhi2023distilwhisper,
  title     = {{Distil-Whisper}: Robust Knowledge Distillation via Large-Scale Pseudo Labelling},
  author    = {Gandhi, Sanchit and others},
  journal   = {arXiv preprint arXiv:2311.00430},
  year      = {2023},
  doi       = {10.48550/arXiv.2311.00430}
}
```
- Kaitan: Distilasi Whisper untuk resource-constrained — model lebih kecil dengan WER mendekati large.

[3] **Turning Whisper into Real-Time Transcription System**
```
@article{machacek2023whisperstreaming,
  title     = {Turning {Whisper} into Real-Time Transcription System},
  author    = {Mach{\'a}{\v{c}}ek, Dominik and others},
  journal   = {arXiv preprint arXiv:2307.14743},
  year      = {2023},
  doi       = {10.48550/arXiv.2307.14743}
}
}
```
- Kaitan: Whisper-Streaming — local agreement policy untuk transkripsi real-time dengan latency 3.3s.

[4] **Piper: A Fast, Local Neural Text to Speech System**
```
@misc{rhasspy2023piper,
  title     = {Piper: A Fast, Local Neural Text to Speech System},
  author    = {Rhasspy contributors},
  year      = {2023},
  note      = {GitHub repository: https://github.com/rhasspy/piper}
}
```
- Kaitan: Piper TTS engine — VITS-based, ONNX runtime, 30+ bahasa, pemilihan di Tabel B.

[5] **On-Device LLMs for Home Assistant: Dual Role in Intent Detection and Response Generation**
```
@article{lang2025ondevice,
  title     = {On-Device {LLMs} for Home Assistant: Dual Role in Intent Detection and Response Generation},
  author    = {Lang, Martin and others},
  journal   = {arXiv preprint arXiv:2502.12923},
  year      = {2025},
  doi       = {10.48550/arXiv.2502.12923}
}
```
- Kaitan: Integrasi STT/TTS dengan LLM lokal untuk voice assistant — arsitektur voice pipeline.

### Referensi Pendukung
[6] OpenAI Whisper. *GitHub Repository*. [https://github.com/openai/whisper](https://github.com/openai/whisper)
[7] Piper TTS. *Voices & Samples*. [https://rhasspy.github.io/piper-samples](https://rhasspy.github.io/piper-samples)
[8] Silero VAD. *GitHub Repository*. [https://github.com/snakers4/silero-vad](https://github.com/snakers4/silero-vad)
