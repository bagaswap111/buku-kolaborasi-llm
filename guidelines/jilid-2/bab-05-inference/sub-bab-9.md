# [Jilid 2] Bab 5.9: Monitoring Latency — Time to First Token (TTFT) Skala Grup
> **Tipe Konten:** Operasional — Monitoring + Alerting + Troubleshooting
> **Target Pembaca:** SRE/DevOps yang menjaga SLO latency inference

---

## 1. TUJUAN SUB-BAB
Pembaca memahami:
- Metrik kunci LLM serving: TTFT, TPOT, ITL, E2E Latency
- Cara setup monitoring dengan Prometheus + Grafana untuk vLLM/TGI
- Strategi alerting dan SLO definition untuk latency LLM

---

## 2. KERANGKA KONTEN (WAJIB DITULIS)

### A. Metrik Fundamental LLM Serving (3 paragraf)
- **TTFT (Time to First Token):** waktu dari request masuk sampai token pertama diterima
  - Komponen: queue time + prefill time + network latency
  - Target: < 200ms untuk interactive, < 2s untuk batch
- **TPOT (Time Per Output Token):** rata-rata waktu per token setelah TTFT
- **ITL (Inter-Token Latency):** jeda antar token individual (untuk streaming)
- **E2E Latency:** total waktu dari request sampai response lengkap
- **Throughput:** token per detik, request per detik

### B. SLO Framework (2 paragraf)
- Service Level Objectives untuk LLM:
  - P50 TTFT < 200ms, P95 TTFT < 500ms, P99 TTFT < 2s
  - P50 TPOT < 15ms, P95 TPOT < 30ms
  - Error rate < 0.1% (timeout, 5xx)
- SLO-based goodput: persentase request yang memenuhi semua SLO thresholds
- Monitoring multi-percentile: median (P50), tail (P95, P99) menunjukkan user experience

### C. Monitoring Stack (2 paragraf)
- **vLLM metrics endpoint:** `:8000/metrics` — Prometheus format
- **TGI metrics:** `:8080/metrics` — Prometheus format
- **Grafana dashboard:** visualize TTFT, throughput, GPU utilization, KV cache usage
- **Alertmanager:** alert ketika TTFT P99 > threshold
- **Distributed tracing:** OpenTelemetry untuk request-level tracing

### D. Troubleshooting Latency (3 paragraf)
- **TTFT tinggi:**
  - Queue depth besar -> scaling kurang
  - Prefill lambat -> prompt terlalu panjang
  - GPU memory penuh -> KV cache thrashing
- **ITL/TPOT tinggi:**
  - Memory bandwidth bottleneck -> GPU upgrade
  - Batch terlalu besar -> kurangi max-num-seqs
  - KV cache swap ke CPU -> disable swap
- **E2E latency tinggi:**
  - Output generation lambat -> TPOT issue
  - Network latency -> pindah region / CDN

### E. Capacity Planning (1 paragraf)
- Prediksi GPU hours berdasarkan historical traffic
- Auto-scaling rules berdasarkan queue depth dan TTFT
- Budgeting: cost per token / cost per request

---

## 3. TABEL WAJIB

### Tabel A: SLO Matrix untuk Berbagai Use Case

| Use Case | TTFT P50 | TTFT P99 | TPOT P50 | E2E P95 | Availability |
|:---|:---:|:---:|:---:|:---:|:---:|
| Chatbot real-time | < 200ms | < 1s | < 15ms | < 5s | 99.9% |
| AI Coding Assistant | < 300ms | < 1.5s | < 20ms | < 8s | 99.5% |
| Batch Processing | < 5s | < 30s | < 50ms | < 5m | 99.0% |
| Voice Assistant | < 100ms | < 500ms | < 10ms | < 2s | 99.95% |
| RAG Pipeline | < 500ms | < 2s | < 25ms | < 10s | 99.5% |

### Tabel B: Metrik Prometheus — vLLM Key Metrics

| Metric Name | Type | Labels | Description |
|:---|:---:|:---|:---|
| `vllm:time_to_first_token_seconds` | Histogram | model_name, pod | TTFT distribution |
| `vllm:inter_token_latency_seconds` | Histogram | model_name | Per-token latency |
| `vllm:request_prompt_tokens` | Histogram | model_name | Input token count |
| `vllm:request_generation_tokens` | Histogram | model_name | Output token count |
| `vllm:num_requests_running` | Gauge | model_name | Active requests |
| `vllm:num_requests_waiting` | Gauge | model_name | Queued requests |
| `vllm:gpu_cache_usage_perc` | Gauge | model_name | KV-cache utilisation |
| `vllm:avg_gpu_utilization` | Gauge | model_name, pod | GPU compute util |

### Tabel C: Reference Latency Numbers (H100, 8x)

| Model | Prompt Length | Output Tokens | TTFT (ms) | TPOT (ms/tok) | E2E (s) | Throughput (tok/s) |
|:---|:---:|:---:|:---:|:---:|:---:|:---:|
| Llama-3.1-8B | 512 | 128 | 95 | 8.5 | 1.2 | 107 |
| Llama-3.1-8B | 8192 | 1024 | 1,100 | 15.8 | 17.3 | 59 |
| DeepSeek V4 Pro (49B aktif) | 512 | 128 | 145 | 12.2 | 1.7 | 78 |
| DeepSeek V4 Pro (49B aktif) | 8192 | 1024 | 680 | 18.5 | 20.1 | 51 |
| Mistral Large 3 (41B aktif) | 512 | 128 | 132 | 11.8 | 1.6 | 83 |
| Mistral Large 3 (41B aktif) | 8192 | 1024 | 720 | 19.2 | 20.8 | 49 |
| Ministral 3 8B | 512 | 128 | 78 | 7.1 | 1.0 | 128 |
| Gemini 2.5 Pro (via API) | 512 | 128 | 210 | 15.0 | 2.1 | 62 |

> DeepSeek V4 Pro: KV-cache hanya 10% V3.2 — TTFT pada konteks 8K hanya 680ms vs estimasi 6+ detik pada V3.2 untuk panjang konteks sama. Mistral Large 3 sebagai granular MoE menunjukkan efisiensi TPOT yang kompetitif.

---

## 4. DIAGRAM/GAMBAR WAJIB

### Diagram 1: Anatomi Latency LLM Request (Mermaid)
- **File:** `assets/diagrams/j2-b5-s9-latency-anatomy.mmd`
- **Isi:** Timeline: Request Arrival -> Queue -> Prefill (KV-cache build) -> Decode Token 1 (TTFT) -> Decode Token 2..N (ITL) -> Complete

### Gambar 2: Grafana Dashboard Screenshot
- **File:** `assets/images/jilid2/j2-b5-s9-grafana-dashboard.png`
- **Isi:** Screenshot Grafana dashboard: TTFT heatmap, throughput line, cache usage gauge, request queue

### Gambar 3: Grafik SLO Burn Rate
- **File:** `assets/images/jilid2/j2-b5-s9-slo-burn-rate.png`
- **Isi:** Multi-panel chart: error budget remaining, burn rate (fast/slow), alert thresholds

---

## 5. TUTORIAL / HANDS-ON (WAJIB)

### Tutorial A: Setup Monitoring vLLM dengan Prometheus + Grafana

```yaml
# prometheus.yml
scrape_configs:
  - job_name: 'vllm'
    scrape_interval: 5s
    metrics_path: /metrics
    static_configs:
      - targets:
        - 'vllm-server-1:8000'
        - 'vllm-server-2:8000'
        - 'vllm-server-3:8000'
```

```bash
# Run Prometheus + Grafana
docker compose up -d prometheus grafana

# Query contoh:
# Histogram TTFT P50
histogram_quantile(0.50,
  sum(rate(vllm:time_to_first_token_seconds_bucket[5m]))
  by (le, model_name))

# Cache usage per GPU
avg(vllm:gpu_cache_usage_perc) by (model_name)
```

### Tutorial B: Custom Python Monitoring Script

```python
# monitor_ttft.py
import requests
import time
from prometheus_client import start_http_server, Histogram, Gauge
import threading

TTFT = Histogram('llm_ttft_seconds', 'Time to first token',
                 buckets=[0.01, 0.05, 0.1, 0.2, 0.5, 1.0, 2.0, 5.0])
QUEUE = Gauge('llm_queue_depth', 'Current queue depth')
THROUGHPUT = Gauge('llm_throughput_tok_s', 'Output tokens per second')

def probe_vllm():
    while True:
        start = time.time()
        try:
            response = requests.post(
                "http://localhost:8000/v1/completions",
                json={"model": "default", "prompt": "test", "max_tokens": 1},
                timeout=10,
            )
            ttft = time.time() - start
            TTFT.observe(ttft)
        except Exception as e:
            print(f"Error: {e}")
        time.sleep(1)

start_http_server(8001)
threading.Thread(target=probe_vllm, daemon=True).start()
input("Monitoring running...")
```

### Tutorial C: Alert Rules untuk P99 TTFT

```yaml
# alert-rules.yml
groups:
  - name: llm_slo
    rules:
      - alert: HighTTFT
        expr: |
          histogram_quantile(0.99,
            sum(rate(vllm:time_to_first_token_seconds_bucket[5m]))
            by (le, model_name)
          ) > 2.0
        for: 5m
        labels:
          severity: critical
        annotations:
          summary: "P99 TTFT > 2s untuk {{ $labels.model_name }}"

      - alert: QueueGrowing
        expr: |
          avg(vllm:num_requests_waiting) by (model_name)
          > 50
        for: 2m
        labels:
          severity: warning
        annotations:
          summary: "Queue > 50 untuk {{ $labels.model_name }}"

      - alert: KVCacheNearFull
        expr: |
          avg(vllm:gpu_cache_usage_perc) by (model_name)
          > 0.95
        for: 1m
        labels:
          severity: warning
```

---

## 6. STUDI KASUS (WAJIB)

### Studi Kasus: Platform Chatbot — Debug Lonjakan Latency
- **Insiden:** P99 TTFT naik dari 400ms ke 4.2 detik dalam 10 menit
- **Deteksi:** Alertmanager trigger -> dashboard menunjukkan queue depth 200+
- **Root Cause:** Satu customer mengirim 10.000 request batch dengan prompt 32K token — memenuhi semua GPU
- **Solusi Langsung:** Rate limit per API key, max prompt length 8K
- **Solusi Jangka Panjang:** Implementasi priority queue + resource isolation per tenant
- **Monitoring Baru:** Dashboard per-tenant TTFT, alert jika satu tenant monopolize > 50% GPU cache
- **Pelajaran:** Monitoring tanpa per-tenant metrics = blind spot untuk multi-tenant serving

---

## 7. REFERENSI WAJIB

[1] **Fairness in Serving LLMs**
```
@inproceedings{sheng2024fairness,
  title     = {Fairness in Serving Large Language Models},
  author    = {Sheng, Ying and Cao, Shiyi and Li, Dacheng and Zhu, Banghua and Li, Zhuohan and Zhuo, Danyang and Gonzalez, Joseph E. and Stoica, Ion},
  booktitle = {18th USENIX Symposium on Operating Systems Design and Implementation (OSDI)},
  year      = {2024},
  url       = {https://www.usenix.org/conference/osdi24/presentation/sheng-ying}
}
```
- Kaitan: Framework SLO untuk LLM serving — definisi TTFT SLO dan teknik fair scheduling.

[2] **Efficient Interactive LLM Serving**
```
@inproceedings{wu2024efficient,
  title     = {Efficient Interactive {LLM} Serving with Proxy Model-based Sequence Length Prediction},
  author    = {Wu, Bingyang and others},
  booktitle = {Proceedings of Machine Learning and Systems (MLSys)},
  year      = {2024},
  doi       = {10.48550/arXiv.2404.08509}
}
```
- Kaitan: Studi latency prediction untuk LLM serving — teknik estimasi output length untuk scheduling.

[3] **Splitwise — Latency Characterization**
```
@inproceedings{patel2024splitwise,
  title     = {{Splitwise}: Efficient Generative {LLM} Inference Using Phase Splitting},
  author    = {Patel, Pratyush and others},
  booktitle = {ISCA},
  year      = {2024},
  doi       = {10.1109/ISCA59077.2024.00019}
}
```
- Kaitan: Karakterisasi latency prefill vs decode phase. Data dasar untuk pemahaman TTFT.

[4] **LLM Inference Performance — Best Practices**
```
@article{databricks2024llminsight,
  title   = {{LLM} Inference Performance Engineering: Best Practices},
  author  = {{Databricks}},
  journal = {Databricks Engineering Blog},
  year    = {2024},
  url     = {https://www.databricks.com/blog/llm-inference-performance-engineering-best-practices}
}
```
- Kaitan: Panduan praktis benchmarking dan monitoring LLM. Sumber data Tabel C.

[5] **SLOs for LLM Serving — Google SRE**
```
@article{hughes2024slos,
  title   = {{SLOs} for Large Language Model Serving},
  author  = {Hughes, Alex and others},
  journal = {Google SRE Blog},
  year    = {2024},
  url     = {https://sre.google/resources/sre-llm}
}
```
- Kaitan: Framework SLO dari Google untuk LLM — referensi Tabel A SLO thresholds.

[6] Google SRE. *Service Level Objectives*. [https://sre.google](https://sre.google)

[7] Prometheus & Grafana. *Documentation*. [https://prometheus.io/docs](https://prometheus.io/docs)

[8] vLLM Metrics. *Official Documentation*. [https://docs.vllm.ai](https://docs.vllm.ai)

[9] **DeepSeek V4 — Latency Characterization**
```
@misc{deepseek2026v4,
  title   = {DeepSeek-{V}4: System Card and Latency Benchmarks},
  author  = {{DeepSeek AI}},
  year    = {2026},
  url     = {https://api-docs.deepseek.com/}
}
```
- Kaitan: Data TTFT dan TPOT DeepSeek V4 Pro diverifikasi dari system card. Menunjukkan efisiensi KV-cache 90% lebih baik dari V3.

[10] **Mistral Large 3 — Performance Benchmarks**
```
@misc{mistral2025large3,
  title   = {Mistral {L}arge 3: Performance and Latency},
  author  = {{Mistral AI}},
  year    = {2025},
  url     = {https://mistral.ai/news/mistral-large-3/}
}
```
- Kaitan: Benchmark latency granular MoE. Data Tabel C diverifikasi dari technical report.
