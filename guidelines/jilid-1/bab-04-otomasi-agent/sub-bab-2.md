# [Jilid 1] Bab 4.2: Tool Use (Function Calling) — JSON-Schema Instruksi ke OS
> **Tipe Konten:** Teknis — Implementasi + Format + Integrasi
> **Target Pembaca:** Developer yang ingin agent bisa memanggil API/tools

---

## 1. TUJUAN SUB-BAB
Pembaca mampu:
- Menjelaskan mekanisme function calling: definisi tool → LLM decides → execute → return
- Menulis JSON-schema tool definition untuk berbagai API sistem
- Mengimplementasikan function calling dengan OpenClaw, Ollama, dan OpenAI-compatible API

---

## 2. KERANGKA KONTEN

### A. Konsep Function Calling (1 paragraf)
- Definisi: LLM menghasilkan JSON terstruktur berisi nama fungsi + parameter, bukan teks biasa
- Analogi: "LLM sebagai resepsionis yang menulis surat tugas — bukan yang mengerjakan"
- Alur: Tool definitions → LLM pilih tool + argumen → Developer eksekusi → Return ke LLM

### B. JSON Schema untuk Tool Definition (2-3 paragraf)
- Struktur dasar: `name`, `description`, `parameters` (JSON Schema)
- Tipe parameter: string, number, array, object — dengan description
- Required fields vs optional
- Contoh: `{"name": "search_web", "parameters": {"type": "object", "properties": {"query": {"type": "string"}}, "required": ["query"]}}`

### C. OpenAI Function Calling API (1 paragraf)
- Parameter `tools` di chat completion
- Strict schema validation (`strict: true`)
- Parallel function calling — multi-tool dalam satu respons

### D. Open Source Function Calling (1-2 paragraf)
- Ollama: dukungan tool via `tools` parameter di `/api/chat`
- Llama 3.1+ / Mistral: fine-tuned untuk function calling
- Berkeley Function Calling Leaderboard (BFCL)

### E. Function Calling untuk Sistem Operasi (1 paragraf)
- Tool: `execute_command`, `read_file`, `write_file`, `list_directory`
- Security: validasi argumen sebelum eksekusi — jangan trust LLM mentah-mentah
- Pattern: "LLM proposes, human disposes"

### F. Error Handling & Retry (1 paragraf)
- Tool bisa gagal (network error, invalid args)
- Pattern: return error ke LLM → LLM decide alternative action
- Validasi schema sebelum eksekusi tool

---

## 3. TABEL WAJIB

### Tabel A: Perbandingan Provider Function Calling

| Provider | Format Tool | Strict Schema | Parallel Calls | Open Source | Local |
|:---|:---|:---|:---|:---|:---|
| **OpenAI** | JSON Schema | Ya (strict:true) | Ya (max 10) | Tidak | Tidak |
| **Anthropic** | `input_schema` | Ya | Ya | Tidak | Tidak |
| **Ollama** | JSON Schema | Tidak | Terbatas | Ya | Ya |
| **Llama 3.1** | Built-in function calling | Parsial | Terbatas | Ya | Ya |
| **Mistral** | JSON Schema | Tidak | Ya | Ya | Ya |
| **Google Gemini** | FunctionDeclaration | Ya | Ya | Tidak | Tidak |

### Tabel B: Tool Categories untuk System Agent

| Kategori | Contoh Tool | Risiko Keamanan |
|:---|:---|:---:|
| **File System** | `read_file`, `write_file`, `list_dir`, `search_files` | Sedang (baca/tulis) |
| **Shell** | `execute_command`, `run_script` | Tinggi (eksekusi) |
| **Network** | `http_get`, `search_web`, `fetch_url` | Rendah (read-only) |
| **Database** | `query_sql`, `read_db` | Tinggi (data bocor) |
| **Code** | `run_python`, `compile` | Tinggi (sandbox wajib) |
| **Browser** | `navigate`, `click`, `type`, `screenshot` | Rendah (headless) |

### Tabel C: Benchmark Function Calling Accuracy (BFCL)

| Model | Simple Function | Multiple Function | Parallel Function | Overall |
|:---|:---:|:---:|:---:|:---:|
| GPT-4o | 94.2% | 89.1% | 86.5% | 90.3% |
| Llama-3.1-70B | 88.5% | 81.3% | 75.2% | 82.7% |
| Mistral-Large | 90.1% | 84.7% | 79.8% | 85.2% |
| Qwen-2.5-72B | 91.0% | 85.5% | 80.1% | 86.2% |
| DeepSeek-V2 | 87.3% | 79.8% | 72.4% | 80.5% |

---

## 4. DIAGRAM/GAMBAR WAJIB

### Diagram 1: Alur Function Calling (Mermaid)
- **File:** `assets/diagrams/j1-b4-s2-function-calling-flow.mmd`
- **Isi:** User → LLM (dengan tool definitions) → LLM output JSON → Validator → Eksekutor → Result → LLM generate final response → User

### Gambar 2: Contoh JSON Schema Tool Definition
- **File:** `assets/images/jilid1/j1-b4-s2-json-schema-tool.png`
- **Isi:** Screenshot kode JSON schema untuk tool `search_files` dengan parameter pattern, path, recursive

---

## 5. TUTORIAL / HANDS-ON

### Tutorial A: Function Calling dengan Ollama + Python

```python
# function_calling_demo.py
import json
import requests

# 1. Definisikan tool dalam format JSON Schema
tools = [
    {
        "type": "function",
        "function": {
            "name": "get_current_time",
            "description": "Dapatkan waktu saat ini di zona waktu tertentu",
            "parameters": {
                "type": "object",
                "properties": {
                    "timezone": {
                        "type": "string",
                        "description": "Zona waktu (contoh: Asia/Jakarta, US/Eastern)",
                    }
                },
                "required": ["timezone"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "calculate",
            "description": "Lakukan operasi matematika",
            "parameters": {
                "type": "object",
                "properties": {
                    "expression": {
                        "type": "string",
                        "description": "Ekspresi matematika (contoh: 2 + 2 * 3)",
                    }
                },
                "required": ["expression"]
            }
        }
    }
]

# 2. Implementasi tool handler
def handle_tool_call(tool_call):
    name = tool_call["function"]["name"]
    args = json.loads(tool_call["function"]["arguments"])

    if name == "get_current_time":
        from datetime import datetime
        import pytz
        tz = pytz.timezone(args["timezone"])
        return datetime.now(tz).strftime("%H:%M:%S")

    elif name == "calculate":
        return str(eval(args["expression"]))

    return "Tool tidak dikenal"

# 3. Kirim ke Ollama dengan tool definitions
response = requests.post("http://localhost:11434/api/chat", json={
    "model": "llama3.1:8b",
    "messages": [{"role": "user", "content": "Jam berapa sekarang di Jakarta? Hitung juga 25 * 4 + 10"}],
    "tools": tools,
    "stream": False
})

data = response.json()
for msg in data["message"]["content"]:
    if "tool_calls" in msg:
        for tc in msg["tool_calls"]:
            result = handle_tool_call(tc)
            print(f"Tool: {tc['function']['name']} → {result}")
```

### Tutorial B: Membuat Custom Tool untuk File System

```python
# file_tools.py — tool definition untuk operasi file
FILE_TOOLS = [
    {
        "name": "read_file",
        "description": "Baca konten file teks",
        "parameters": {
            "type": "object",
            "properties": {
                "path": {"type": "string", "description": "Path absolut file"},
                "encoding": {"type": "string", "enum": ["utf-8", "latin-1"]}
            },
            "required": ["path"]
        }
    },
    {
        "name": "write_file",
        "description": "Tulis konten ke file (HATI-HATI: akan overwrite)",
        "parameters": {
            "type": "object",
            "properties": {
                "path": {"type": "string"},
                "content": {"type": "string", "description": "Konten yang akan ditulis"}
            },
            "required": ["path", "content"]
        }
    },
    {
        "name": "list_directory",
        "description": "List file dalam direktori",
        "parameters": {
            "type": "object",
            "properties": {
                "path": {"type": "string", "default": "."},
                "pattern": {"type": "string", "description": "Filter glob pattern"}
            }
        }
    }
]

# Pattern: jangan pernah execute tool call tanpa validasi
def validate_tool_call(tool_call, allowed_tools):
    name = tool_call["function"]["name"]
    if name not in [t["name"] for t in allowed_tools]:
        raise PermissionError(f"Tool {name} tidak diizinkan")
    return True
```

---

## 6. STUDI KASUS

### Studi Kasus: Agent Backup Otomatis dengan Function Calling
- **Skenario:** Agent diminta "Backup folder Documents ke external drive, kecuali file .tmp"
- **Tools yang digunakan:** `list_directory` (scan source), `read_file_metadata` (filter by extension), `copy_file` (backup), `create_archive` (kompresi)
- **Alur:** LLM panggil list_directory → filter .tmp → panggil create_archive → copy ke external drive
- **Keamanan:** Tool `delete_file` tidak disediakan — agent tidak bisa hapus data
- **Hasil:** Backup 5GB selesai dalam 2 menit dengan satu prompt

---

## 7. REFERENSI WAJIB

[1] **Toolformer: Language Models Can Teach Themselves to Use Tools**
```
@inproceedings{schick2024toolformer,
  title     = {{Toolformer}: Language Models Can Teach Themselves to Use Tools},
  author    = {Schick, Timo and Dwivedi-Yu, Jane and Dess{\`\i}, Roberto and Raileanu, Roberta and Lomeli, Maria and Zettlemoyer, Luke and Cancedda, Nicola and Scialom, Thomas},
  booktitle = {Advances in Neural Information Processing Systems (NeurIPS)},
  year      = {2024},
  doi       = {10.48550/arXiv.2302.04761}
}
```
- Kaitan: Paper perintis yang mengajarkan LLM menggunakan tools via API — dasar konsep tool use.

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
- Kaitan: Reasoning + acting secara interleaved — fondasi untuk function calling agent loop.

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
- Kaitan: Optimasi latency function calling melalui paralelisasi — relevan untuk Tabel B.

[4] **Granite-Function Calling Model: Introducing Function Calling Abilities via Multi-task Learning**
```
@inproceedings{abdelaziz2024granite,
  title     = {Granite-Function Calling Model: Introducing Function Calling Abilities via Multi-task Learning of Granular Tasks},
  author    = {Abdelaziz, Ibrahim and Basu, Kinjal and Agarwal, Mayank and others},
  booktitle = {Proceedings of EMNLP 2024 Industry Track},
  year      = {2024},
  doi       = {10.48550/arXiv.2407.00121}
}
```
- Kaitan: Multi-task training untuk function calling — benchmark BFCL di Tabel C.

[5] **Gorilla: Large Language Model Connected with Massive APIs**
```
@inproceedings{patil2023gorilla,
  title     = {{Gorilla}: Large Language Model Connected with Massive {APIs}},
  author    = {Patil, Shishir G. and Zhang, Tianjun and Wang, Xin and Gonzalez, Joseph E.},
  booktitle = {Advances in Neural Information Processing Systems (NeurIPS)},
  year      = {2023},
  doi       = {10.48550/arXiv.2305.15334}
}
```
- Kaitan: API call generation via retrieval — dasar untuk tool selection dari ribuan API.

### Referensi Pendukung
[6] Berkeley Function Calling Leaderboard (BFCL). [https://gorilla.cs.berkeley.edu/leaderboard.html](https://gorilla.cs.berkeley.edu/leaderboard.html)
[7] Ollama Tools Documentation. [https://github.com/ollama/ollama/blob/main/docs/api.md](https://github.com/ollama/ollama/blob/main/docs/api.md)
[8] OpenAI Function Calling Guide. [https://platform.openai.com/docs/guides/function-calling](https://platform.openai.com/docs/guides/function-calling)
