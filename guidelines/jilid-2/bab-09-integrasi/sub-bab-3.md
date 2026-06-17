# [Jilid 2] Bab 9.3: Flowise — Eksperimen RAG Drag-and-Drop Manajemen Data Perusahaan
> **Tipe Konten:** Praktikal — Tutorial + Eksperimen RAG Pipeline
> **Target Pembaca:** Developer / Data Engineer yang ingin prototyping RAG dengan cepat

---

## 1. TUJUAN SUB-BAB
Pembaca mampu:
- Memahami Flowise sebagai visual RAG builder berbasis LangChain
- Membangun pipeline RAG end-to-end: ingestion -> chunking -> embedding -> retrieval -> generation
- Mengeksperimen berbagai strategi chunking, embedding, dan retrieval dalam antarmuka drag-and-drop

---

## 2. KERANGKA KONTEN (WAJIB DITULIS)

### A. Flowise dalam Ekosistem LLM Visual (1-2 paragraf)
- Flowise: open-source drag-and-drop UI untuk LangChain (53K+ GitHub stars)
- Perbedaan dengan Dify: Flowise lebih low-level (ekspos LangChain components langsung), Dify lebih product-oriented
- Ideal untuk: developer yang ingin rapid prototyping RAG pipeline sebelum production
- Base: TypeScript, React frontend + Node.js backend, modular plugin architecture

### B. Arsitektur Komponen Flowise (1-2 paragraf)
- **Nodes:** Setiap LangChain component direpresentasikan sebagai node visual
- **Kategori Node:** LLM Models, Document Loaders, Embeddings, Vector Stores, Retrievers, Chains, Agents, Tools, Memory
- **Canvas:** DAG editor dengan zoom, auto-layout, dan debug mode
- **Chat Widget:** Built-in embeddable widget untuk testing langsung

### C. Pipeline RAG di Flowise (masing-masing 1 paragraf)
- **Document Loader:** 50+ loader (PDF, CSV, JSON, Notion, Confluence, S3, Web Scraper)
- **Text Splitter:** Chunking strategi (RecursiveCharacter, Token, Markdown, HTML, Code)
- **Embedding Model:** OpenAI, Ollama, HuggingFace, SentenceTransformers
- **Vector Store:** ChromaDB, Qdrant, Milvus, Pinecone, Weaviate, Supabase, PGVector
- **Retriever:** Similarity search, MMR, Self-query, Multi-query, Contextual compression
- **Chain:** RetrievalQA, ConversationalRetrievalChain, Stuff/MapReduce/Refine

### D. Agentic RAG & Multi-Agent (1-2 paragraf)
- Agentic RAG: agent yang bisa memutuskan kapan perlu retrieve vs generate langsung
- Self-correcting RAG: relevance checker -> loop-back jika hasil tidak relevan
- Multi-agent orchestration: Supervisor + Specialist agents untuk dokumen heterogen
- Tool calling: agent bisa akses SQL, API, calculator, search engine

### E. Eksperimen & Evaluasi (1 paragraf)
- Visual debugging: lihat input/output setiap node secara real-time
- Prompt templating: variasi prompt di LLM node yang berbeda
- A/B testing manual: duplikasi flow, ganti parameter, bandingkan output
- Export/import flow sebagai JSON untuk version control

### F. Production Deployment (1 paragraf)
- Flowise Cloud: managed service
- Self-hosted: Docker (sederhana), Kubernetes (skala)
- Embedded Chat: embed di website via iframe / React component
- API Endpoint: setiap flow bisa diekspos sebagai REST API

---

## 3. TABEL WAJIB

### Tabel A: Perbandingan Strategi Chunking untuk Dokumen Perusahaan

| Strategi | Karakter per Chunk | Overlap | Recall (test set) | Precision | Best Untuk |
|:---|:---:|:---:|:---:|:---:|:---|
| **RecursiveCharacter** | 500 | 50 | 0.81 | 0.76 | Dokumen naratif (laporan, memo) |
| **RecursiveCharacter** | 1000 | 200 | 0.85 | 0.72 | Dokumen teknis (manual, SOP) |
| **Token-based** | 512 tokens | 128 | 0.83 | 0.74 | Kode, data terstruktur |
| **Markdown splitter** | Per header | 0 | 0.88 | 0.85 | Dokumen dengan struktur jelas |
| **Semantic chunking** | Variabel | 10% | 0.91 | 0.87 | Konten padat informasi |

> Data dari eksperimen Flowise dengan dataset 500 dokumen PDF perusahaan. Penulis WAJIB verifikasi.

### Tabel B: Perbandingan Mode Retrieval di Flowise

| Mode Retrieval | Deskripsi | Latency | Recall@5 | Best For |
|:---|:---|:---:|:---:|:---|
| **Similarity Search** | Cosine similarity standar | <50ms | 0.78 | QA sederhana |
| **MMR (Max Marginal Relevance)** | Diversity + relevance | <100ms | 0.82 | Butuh variasi hasil |
| **Multi-Query** | Generate 3 variants query | <300ms | 0.88 | Query ambigu |
| **Self-Query** | Filter by metadata | <150ms | 0.85 | Dokumen terstruktur |
| **Contextual Compression** | Rangkai + filter chunks | <500ms | 0.90 | Konteks panjang |

### Tabel C: Perbandingan Node LLM Model di Flowise

| Provider | Model Default | Kecepatan | Kualitas | Biaya | Cocok untuk |
|:---|:---|:---:|:---:|:---:|:---|
| **Ollama** | llama3.1:8b | Cepat | Baik | Gratis | Prototyping, data sensitif |
| **OpenAI** | GPT-4o | Sangat cepat | Terbaik | $0.01/query | Production dengan budget |
| **HuggingFace** | Mixtral-8x7B | Sedang | Baik | Gratis | Eksperimen model |
| **vLLM** | Qwen-2.5-14B | Cepat | Baik | Gratis | Self-hosted production |

---

## 4. DIAGRAM/GAMBAR WAJIB

### Diagram 1: Arsitektur Flowise RAG Pipeline (Mermaid)
- **File:** `assets/diagrams/j2-b9-s3-flowise-rag-pipeline.mmd`
- **Isi:**

```mermaid
graph LR
    subgraph "Ingestion"
        PDF[PDF Loader]
        WEB[Web Scraper]
        DB[SQL Connector]
    end
    subgraph "Processing"
        SPLIT[Text Splitter]
        EMBED[Embedding Model]
        STORE[(Vector Store)]
    end
    subgraph "Retrieval"
        Q[User Query]
        RET[Retriever Node]
    end
    subgraph "Generation"
        CONTEXT[Context]
        LLM[LLM Node]
        ANS[Answer]
    end
    PDF --> SPLIT
    WEB --> SPLIT
    DB --> SPLIT
    SPLIT --> EMBED --> STORE
    Q --> RET --> STORE
    STORE --> CONTEXT
    CONTEXT --> LLM --> ANS
```

### Diagram 2: Screenshot Flowise Canvas
- **File:** `assets/images/jilid2/j2-b9-s3-flowise-canvas.png`
- **Isi:** Canvas Flowise dengan node: PDF Loader -> RecursiveCharacterTextSplitter -> OpenAI Embeddings -> Pinecone Vector Store -> RetrievalQA Chain -> ChatOpenAI

---

## 5. TUTORIAL / HANDS-ON (WAJIB)

### Tutorial A: Setup Flowise Self-hosted

```bash
# Opsi 1: Docker (langsung)
docker run -d --name flowise \
  -p 3001:3001 \
  -v ~/.flowise:/root/.flowise \
  flowiseai/flowise:latest

# Opsi 2: Docker Compose
cat > docker-compose.yml << 'EOF'
version: "3.8"
services:
  flowise:
    image: flowiseai/flowise:latest
    ports:
      - "3001:3001"
    volumes:
      - ~/.flowise:/root/.flowise
    environment:
      - PORT=3001
      - DATABASE_PATH=/root/.flowise
      - APIKEY_PATH=/root/.flowise
    restart: always
EOF
docker compose up -d

# Opsi 3: Local install (npm)
npm install -g flowise
npx flowise start --port 3001

# Akses di http://localhost:3001
```

### Tutorial B: RAG Pipeline — Chat dengan Dokumen Keuangan

1. **Add Document Loader Node:** Pilih `PDF File` -> Upload file laporan keuangan.
2. **Add Text Splitter Node:** `RecursiveCharacterTextSplitter` -> chunk 1000, overlap 200.
3. **Add Embeddings Node:** Pilih `OpenAI Embeddings` (atau `Ollama Embeddings` untuk lokal).
4. **Add Vector Store Node:** Pilih `ChromaDB` -> Create New Collection.
5. **Upsert Document:** Koneksikan Loader -> Splitter -> Embeddings -> ChromaDB.
6. **Add LLM Node:** Pilih `ChatOllama` -> model `llama3.1:8b`.
7. **Add RetrievalQA Chain Node:**
   - Koneksikan: LLM -> RetrievalQA
   - Koneksikan: ChromaDB -> RetrievalQA (sebagai retriever)
   - Parameter: `chainType = stuff`, `returnSourceDocuments = true`
8. **Add Chat Widget Node:** Koneksikan ke RetrievalQA -> Save.
9. **Test:** Ketik "Berapa total pendapatan tahun 2024?" di chat widget.

### Tutorial C: Agentic RAG dengan Self-Correction

1. **Buat Agent Node:** Pilih `OpenAI Function Agent` (karena perlu tool calling).
2. **Buat Tool:**
   - `Vector Store Tool` -> koneksikan ke ChromaDB retriever
   - `Calculator Tool` -> untuk perhitungan
3. **System Prompt:**
   ```
   You are a financial analyst assistant. Use the vector store to
   answer questions about company documents. Use calculator for
   financial calculations. If documents don't contain the answer,
   say so clearly — do not hallucinate.
   ```
4. **Add Relevancy Checker (LLM node + Condition):**
   - Prompt: "Are these documents relevant to: {{query}}? YES/NO"
   - Condition: if YES -> generate answer; if NO -> regenerate query.
5. **Loop Node:** Koneksikan output "NO" kembali ke retriever dengan query baru.
6. **Max 5 Loops:** Set loop counter untuk menghindari infinite loop.

---

## 6. STUDI KASUS (WAJIB)

### Studi Kasus: RAG untuk Manajemen Kontrak Perusahaan (10,000+ dokumen)
- **Latar Belakang:** Departemen legal perlu mencari klausul dalam 10,000+ kontrak vendor. Pencarian manual butuh 30-60 menit.
- **Solusi:** Flowise + ChromaDB + Ollama (Llama-3.1-8B) + vLLM (Qwen-2.5-14B untuk dokumen kompleks)
- **Pipeline:**
  - Ingestion: PDF Loader -> Markdown splitter (per section kontrak) -> Ollama Embeddings -> ChromaDB
  - Retrieval: Multi-Query retriever (3 variant queries) -> Contextual compression
  - Generation: LLM with citation extraction -> output berupa klausul + nomor halaman
- **Hasil:**
  - Waktu pencarian turun dari ~45 menit -> ~15 detik
  - Akurasi retrieval 93% (test set 200 query)
  - 100% data lokal (no cloud) — kepatuhan GDPR terpenuhi
- **Skalabilitas:** ChromaDB handle 10k dokumen (500k+ chunks) tanpa degradasi signifikan

---

## 7. REFERENSI WAJIB (SOP: minimal 5 paper 5 tahun terakhir + DOI)

### Paper Jurnal/Konferensi

[1] **Review of Tools for Zero-Code LLM Based Application Development**
```
@article{mehrgardt2025zerocode,
  title     = {Review of Tools for Zero-Code {LLM} Based Application Development},
  author    = {Mehrgardt, Philipp and others},
  journal   = {arXiv preprint arXiv:2510.19747},
  year      = {2025},
  doi       = {10.48550/arXiv.2510.19747},
  url       = {https://arxiv.org/abs/2510.19747}
}
```
- Kaitan: Review 14 zero-code platform termasuk Flowise. Analisis perbandingan visual builder (flow/graph vs form-based). Relevan untuk Tabel A sub-bab 3.

[2] **Retrieval-Augmented Generation for Natural Language Processing: A Survey**
```
@article{huang2024ragsurvey,
  title     = {Retrieval-Augmented Generation for Natural Language Processing: {A} Survey},
  author    = {Huang, Y. and others},
  journal   = {arXiv preprint arXiv:2407.13193},
  year      = {2024},
  doi       = {10.48550/arXiv.2407.13193},
  url       = {https://arxiv.org/abs/2407.13193}
}
```
- Kaitan: Taksonomi retrieval fusion (query-based, logits-based, latent, parametric). Menjadi acuan teknis untuk sub-bab 2.C (Pipeline RAG) dan Tabel B.

[3] **Reasoning RAG via System 1 or System 2: A Survey on Reasoning Agentic RAG**
```
@inproceedings{li2025reasoningrag,
  title     = {Reasoning {RAG} via System 1 or System 2: {A} Survey on Reasoning Agentic Retrieval-Augmented Generation for Industry Challenges},
  author    = {Li, Y. and others},
  booktitle = {Findings of the International Joint Conference on Natural Language Processing (IJCNLP)},
  year      = {2025},
  url       = {https://aclanthology.org/2025.findings-ijcnlp.122.pdf}
}
```
- Kaitan: Klasifikasi Reasoning Agentic RAG — predefined vs agentic reasoning. Relevan untuk Tutorial C (Agentic RAG dengan self-correction).

[4] **RAG and LLMs for Enterprise Knowledge Management and Document Automation: A Systematic Literature Review**
```
@article{sari2025ragenterprise,
  title     = {Retrieval-Augmented Generation ({RAG}) and Large Language Models ({LLMs}) for Enterprise Knowledge Management and Document Automation: {A} Systematic Literature Review},
  author    = {Sari, W. and others},
  journal   = {Applied Sciences},
  volume    = {16},
  number    = {1},
  pages     = {368},
  year      = {2025},
  doi       = {10.3390/app16010368},
  url       = {https://www.mdpi.com/2076-3417/16/1/368}
}
```
- Kaitan: SLR mencakup publikasi 2015-2025 tentang RAG untuk enterprise document management. Kasus penggunaan kontrak di Studi Kasus harus merujuk temuan paper ini.

[5] **A Systematic Literature Review of RAG: Techniques, Metrics, and Challenges**
```
@article{fernando2025ragslr,
  title     = {A Systematic Literature Review of Retrieval-Augmented Generation: Techniques, Metrics, and Challenges},
  author    = {Fernando, K. and others},
  journal   = {Big Data and Cognitive Computing},
  volume    = {9},
  number    = {12},
  pages     = {320},
  year      = {2025},
  doi       = {10.3390/bdcc9120320},
  url       = {https://www.mdpi.com/2504-2289/9/12/320}
}
```
- Kaitan: Analisis 128 studi RAG — pergeseran ke modular/policy-driven RAG. Data evaluasi di Tabel A dan B harus diverifikasi dengan temuan paper ini.

### Referensi Pendukung (Non-Paper/Dokumentasi)

[6] FlowiseAI. *Official Documentation*. [https://docs.flowiseai.com](https://docs.flowiseai.com)

[7] FlowiseAI. *GitHub Repository*. [https://github.com/FlowiseAI/Flowise](https://github.com/FlowiseAI/Flowise)

[8] Flowise. *RAG Tutorial Documentation*. [https://docs.flowiseai.com/tutorials/rag](https://docs.flowiseai.com/tutorials/rag)

[9] Flowise. *Agentic RAG Tutorial*. [https://github.com/FlowiseAI/FlowiseDocs/blob/main/en/tutorials/agentic-rag.md](https://github.com/FlowiseAI/FlowiseDocs/blob/main/en/tutorials/agentic-rag.md)

[10] LangChain. *Official Documentation*. [https://python.langchain.com](https://python.langchain.com)

### SOP Referensi
- WAJIB menyertakan minimal **5 paper jurnal/konferensi** dari 5 tahun terakhir (2021-2026) dengan DOI/arXiv yang valid.
- Data perbandingan chunking dan retrieval di Tabel A/B WAJIB diverifikasi dengan eksperimen aktual menggunakan Flowise.

(End of file - total 252 lines)
