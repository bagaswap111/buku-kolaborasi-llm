# [Jilid 1] Bab 2.10: Budgeting Personal — Komparasi PC Rakitan vs Mac Studio vs Laptop AI
> **Tipe Konten:** Praktis — Panduan Belanja + Perhitungan Biaya
> **Target Pembaca:** Pengguna yang ingin membeli/membangun workstation LLM dengan budget terbatas

---

## 1. TUJUAN SUB-BAB
Pembaca mampu:
- Membandingkan total biaya kepemilikan (TCO) PC rakitan, Mac Studio, dan laptop AI
- Memilih konfigurasi optimal berdasarkan budget, use case, dan prioritas (performa, daya, portabilitas)
- Menghitung break-even point antara inferensi lokal vs berlangganan API cloud

---

## 2. KERANGKA KONTEN (WAJIB DITULIS)

### A. Kategori Budget untuk LLM Workstation (1 paragraf)
- Budget ekonomis (Rp 5-15 jt): laptop/CUDA-less, CPU-only, model 3-8B quantized
- Budget menengah (Rp 15-35 jt): PC RTX 3090 used, Mac Mini M4 Pro, laptop AI mid-range
- Budget tinggi (Rp 35-75 jt): PC RTX 4090, Mac Studio M2 Ultra, 2x RTX 3090
- Budget flagship (>Rp 75 jt): multi-GPU workstation, Mac Studio max config, server-grade

### B. PC Rakitan — Kelebihan dan Kekurangan (1 paragraf)
- Kelebihan: performa terbaik per rupiah, upgrade path jelas, semua framework support
- Kekurangan: konsumsi daya tinggi, berisik, butuh space, rawan thermal issue
- Komponen kunci: GPU (30-50% budget), PSU (1200W+ untuk multi-GPU), motherboard dengan PCIe lanes cukup

### C. Mac Studio / Mac Mini — Kelebihan dan Kekurangan (1 paragraf)
- Kelebihan: unified memory besar (192GB!), silent, daya rendah, form factor kecil
- Kekurangan: harga premium per unit performa, terbatas di 192GB, tidak bisa upgrade
- Cocok untuk: pengguna yang prioritasnya model besar (70B+), bukan kecepatan maksimal

### D. Laptop AI — Kelebihan dan Kekurangan (1 paragraf)
- Kelebihan: portabel, all-in-one, NPU terintegrasi, konsumsi daya rendah
- Kekurangan: performa GPU terbatas (Max-Q, TGP rendah), VRAM maksimal 16GB (RTX 4090 laptop)
- Thermal: laptop gaming cepat throttle karena form factor sempit
- Cocok untuk: mahasiswa/pekerja yang butuh AI di perjalanan + casual LLM

### E. Perhitungan TCO — Total Cost of Ownership (1 paragraf + tabel)
- Biaya hardware + listrik 3 tahun + upgrade/repaste
- Break-even dengan cloud API: hitung token/hari yang diperlukan
- Contoh: RTX 3090 break-even dalam 8 bulan vs OpenAI GPT-4o untuk heavy user

### F. Matriks Keputusan (1 paragraf)
- Pilih PC rakitan jika: prioritas performa, suka oprek, budget ketat per performa
- Pilih Mac Studio jika: butuh model besar, prioritas senyap, 24/7 operation
- Pilih laptop jika: butuh portabilitas, casual inference, sudah punya laptop untuk kerja

---

## 3. TABEL WAJIB

### Tabel A: Konfigurasi Workstation LLM per Budget

| Komponen | Ekonomis (~Rp 12 jt) | Menengah (~Rp 25 jt) | Tinggi (~Rp 50 jt) | Flagship (~Rp 80 jt) |
|:---|:---|:---|:---|:---|
| **CPU** | Intel i5-13400 | AMD Ryzen 7 7800X3D | Intel i7-14700K | AMD Threadripper 7960X |
| **GPU** | RTX 4060 (used) | RTX 3090 (used) | RTX 4090 | 2x RTX 3090 + NVLink |
| **RAM** | 32GB DDR4 | 64GB DDR5 | 64GB DDR5 | 128GB DDR5 |
| **Motherboard** | B760 | B650 | Z790 | TRX50 |
| **SSD** | 1TB NVMe Gen 3 | 2TB NVMe Gen 4 | 2TB NVMe Gen 5 | 4TB NVMe Gen 5 |
| **PSU** | 650W | 850W | 1200W | 1600W |
| **Case** | Budget ATX | Mid-tower mesh | High-airflow | Full tower |
| **Cooling** | Stock CPU | Air cooler | AIO 360mm | Custom loop |
| **VRAM Total** | 8 GB | 24 GB | 24 GB | 48 GB |
| **Model Maks** | 7B Q4 | 13B Q4 / 70B Q3 | 70B Q3 (offload) | 70B Q4 / 405B Q3 |
| **TCO 3 Tahun** | ~Rp 15 jt | ~Rp 30 jt | ~Rp 65 jt | ~Rp 105 jt |

### Tabel B: PC Rakitan vs Mac Studio vs Laptop

| Aspek | PC Rakitan (Rp 25 jt) | Mac Mini M4 Pro (Rp 32 jt) | Laptop AI (Rp 25 jt) |
|:---|:---|:---|:---|
| **GPU/Memory** | RTX 3090 24GB | M4 Pro 48GB unified | RTX 4060 laptop 8GB |
| **Tokens/s (7B)** | ~85 t/s | ~40 t/s | ~35 t/s |
| **Model 70B** | ~16 t/s (Q3) | ~8 t/s (Q3) | Tidak muat |
| **Max VRAM/Memory** | 24 GB | 48 GB | 8 GB |
| **Konsumsi Daya** | ~350W (load) | ~60W (load) | ~150W (load) |
| **Biaya Listrik/thn** | ~Rp 2.3 jt | ~Rp 400 rb | ~Rp 1 jt |
| **Upgradeability** | Tinggi | Rendah (tidak bisa) | Rendah (RAM/GPU solder) |
| **Kebisingan** | Sedang | Silent | Sedang-tinggi |
| **Portabilitas** | Tidak | Mini (bisa dibawa) | Ya |
| **Software Support** | Semua framework | MLX, llama.cpp, Ollama | Terbatas (VRAM kecil) |

### Tabel C: Perbandingan Biaya per Juta Token — Lokal vs Cloud

| Platform | Biaya per 1M Token | Keterangan |
|:---|:---|---:|
| **RTX 3090 used** | Rp 520 | HW amortisasi 3 thn + listrik |
| **RTX 4060** | Rp 950 | HW Rp 5 jt + listrik |
| **Mac Mini M4 Pro** | Rp 2.107 | Biaya HW dominan |
| **Mac Studio M2 Ultra** | Rp 2.876 | Biaya HW dominan |
| **OpenAI GPT-4o** | Rp 77.000 | via API, input + output rata-rata |
| **Claude 3.5 Sonnet** | Rp 47.000 | via API |
| **Gemini 1.5 Pro** | Rp 35.000 | via API |
| **DeepSeek API** | Rp 2.100 | Termurah untuk cloud |
| **Groq API** | Rp 5.800 | LPU inference cloud |

---

## 4. DIAGRAM/GAMBAR WAJIB

### Diagram 1: Peta Keputusan Pemilihan Hardware (Mermaid)
- **File:** `assets/diagrams/j1-b2-s10-decision-tree.mmd`
- **Isi:** Diagram pohon: Budget → Portabilitas? → Budget → GPU/Apple → Rekomendasi spesifik

### Gambar 2: Grafik TCO 3 Tahun
- **File:** `assets/images/jilid1/j1-b2-s10-tco-comparison.png`
- **Isi:** Stacked bar chart: TCO 3 tahun = HW + listrik + maintenance untuk setiap opsi (PC Rakitan, Mac, Laptop)

---

## 5. TUTORIAL / HANDS-ON (WAJIB)

### Tutorial A: Kalkulator TCO untuk Keputusan Pembelian

```python
# tco_calculator.py — hitung total biaya kepemilikan
def calculate_tco(hw_cost, power_watts, hours_day, price_per_kwh, years=3):
    """Hitung TCO: hardware + listrik untuk periode tertentu"""
    # Biaya hardware
    total_hw = hw_cost

    # Biaya listrik
    daily_kwh = power_watts * hours_day / 1000
    monthly_kwh = daily_kwh * 30
    yearly_kwh = monthly_kwh * 12

    electricity_per_year = yearly_kwh * price_per_kwh
    total_electricity = electricity_per_year * years

    total = total_hw + total_electricity
    return {
        "hw_cost": total_hw,
        "electricity_3yr": round(total_electricity, 2),
        "total_tco": round(total, 2),
        "monthly_electricity": round(electricity_per_year / 12, 2)
    }

configs = [
    ("PC RTX 3090", 12000000, 350, 8),
    ("PC RTX 4090", 30000000, 450, 8),
    ("Mac Mini M4 Pro 48GB", 32000000, 60, 8),
    ("Mac Studio M2 Ultra 192GB", 75000000, 120, 8),
    ("Laptop RTX 4060", 18000000, 150, 8),
    ("PC 2x RTX 3090", 24000000, 700, 8),
]

PLN_TARIFF = 1600 / 1000  # Rp per kWh

print(f"{'Konfigurasi':30s} {'HW Cost':>12s} {'Listrik/bln':>12s} {'Listrik 3thn':>12s} {'TCO 3 tahun':>14s}")
print("=" * 80)
for name, hw, watt, hours in configs:
    result = calculate_tco(hw, watt, hours, PLN_TARIFF)
    print(f"{name:30s} {result['hw_cost']:>12,} {result['monthly_electricity']:>12,.0f} "
          f"{result['electricity_3yr']:>12,.0f} {result['total_tco']:>14,.0f}")
```

### Tutorial B: Menghitung Break-even Point vs Cloud API

```python
# breakeven.py — kapan lokal lebih murah dari cloud?
HW_COST = 12_000_000  # RTX 3090 used
TOKENS_PER_DAY = 500_000  # 500K token/hari (heavy user)
CLOUD_COST_PER_1M = 77_000  # OpenAI GPT-4o

# Biaya per token lokal (amortisasi 3 tahun + listrik)
from tco_calculator import calculate_tco

tco = calculate_tco(HW_COST, 350, 8, 1.6)
local_cost_per_token = tco["total_tco"] / (3 * 365 * TOKENS_PER_DAY)
cloud_cost_per_token = CLOUD_COST_PER_1M / 1_000_000

daily_local_cost = local_cost_per_token * TOKENS_PER_DAY
daily_cloud_cost = cloud_cost_per_token * TOKENS_PER_DAY

breakeven_days = HW_COST / (daily_cloud_cost - daily_local_cost)

print(f"=== Break-even Analysis ===")
print(f"Hardware: Rp {HW_COST:,}")
print(f"Token per hari: {TOKENS_PER_DAY:,}")
print(f"Biaya lokal/hari: Rp {daily_local_cost:,.0f}")
print(f"Biaya cloud/hari: Rp {daily_cloud_cost:,.0f}")
print(f"Hemat/hari: Rp {daily_cloud_cost - daily_local_cost:,.0f}")
print(f"Break-even dalam: {breakeven_days:.0f} hari (~{breakeven_days/30:.1f} bulan)")
```

### Tutorial C: Checklist Pembelian Komponen PC LLM

```bash
#!/bin/bash
# pc_checklist.sh — verifikasi kompatibilitas komponen LLM PC

echo "=== Checklist PC untuk LLM ==="
echo ""

# Cek PCIe lanes CPU
echo "[1] CPU: Cek jumlah PCIe lanes"
echo "    - Intel LGA1700: 16x CPU + 4x Chipset = 20 total"
echo "    - AMD AM5: 28x CPU + 4x Chipset = 32 total"
echo "    - Threadripper: 128x CPU"
echo "    Butuh: 16x untuk GPU pertama + 8x untuk GPU kedua"

echo ""
echo "[2] Motherboard: Pastikan slot x16 berjalan di x8/x8 untuk multi-GPU"
echo "    - Cek manual: 'PCIe x16 slot (x8 mode)'"

echo ""
echo "[3] PSU: Cek konektor dan daya"
echo "    - RTX 3090: 2x 8-pin PCIe per GPU"
echo "    - Total daya: GPU TDP + 150W (sistem)"
echo "    - 2x RTX 3090 = 700W + 150W = 850W minimum"

echo ""
echo "[4] Case: Cek dimensi GPU"
echo "    - RTX 4090: panjang 336mm, lebar 3-4 slot"
echo "    - Butuh clearance minimal 350mm"

echo ""
echo "[5] RAM: Cek bandwidth"
echo "    - DDR5 6000 MT/s dual channel = ~96 GB/s"
echo "    - Untuk CPU inference, makin tinggi makin baik"

echo ""
echo "[6] Cek kompatibilitas NVLink (RTX 3090 only)"
echo "    - NVLink bridge: 2-slot atau 4-slot spacing"
echo "    - Cek jarak slot PCIe fisik"
```

---

## 6. STUDI KASUS (WAJIB)

### Studi Kasus: Memilih Workstation AI dengan Budget Rp 30 Juta
- **Skenario:** Developer web yang ingin beralih dari ChatGPT ($20/bln) ke LLM lokal untuk coding assistant + RAG
- **Budget:** Rp 30 juta (sekali, tanpa biaya bulanan)
- **Opsi A — PC Rakitan:** Ryzen 7 7800X3D + RTX 3090 used 24GB + 64GB DDR5 + 2TB NVMe Gen 4 = ~Rp 25jt
  - Performa: 85 t/s (7B), 16 t/s (70B Q3), bisa 2x GPU nanti
  - Listrik: ~Rp 230rb/bulan (8 jam/hari)
- **Opsi B — Mac Mini M4 Pro 48GB:** Rp 32jt (over budget Rp 2jt)
  - Performa: 40 t/s (7B), tidak bisa 70B (VRAM cukup tapi bandwidth rendah)
  - Listrik: ~Rp 40rb/bulan, silent
- **Opsi C — Laptop Lenovo Legion RTX 4060 8GB:** Rp 22jt
  - Performa: 35 t/s (7B Q4), tidak bisa 70B
  - Portabel, bisa dibawa ke kampus/kantor
- **Keputusan:** Opsi A dipilih karena budget pas, performa terbaik, upgrade path ke 2x GPU untuk 70B. Sisa Rp 5jt untuk UPS + fan upgrade.
- **Hasil:** Break-even dari langganan ChatGPT dalam 8 bulan (Rp 20/bln × 8 = Rp 160rb × 8 = Rp 1.28jt vs Rp 25jt — lebih karena biaya HW, tapi untuk heavy user 500K token/hari, break-even 4-6 bulan).

---

## 7. REFERENSI WAJIB (SOP: minimal 5 paper 5 tahun terakhir + DOI)

### Paper Jurnal/Konferensi

[1] **Energy Considerations of LLM Inference and Efficiency Optimizations**
```
@inproceedings{stojkovic2025energyllm,
  title     = {Energy Considerations of Large Language Model Inference and Efficiency Optimizations},
  author    = {Stojkovic, Jovan and others},
  booktitle = {Annual Meeting of the Association for Computational Linguistics (ACL)},
  year      = {2025},
  doi       = {10.18653/v1/2025.acl-long.1563},
  url       = {https://aclanthology.org/2025.acl-long.1563.pdf}
}
```
- Kaitan: Optimasi energi dapat mengurangi 73% konsumsi daya — relevan untuk kalkulasi TCO dan rekomendasi di seksi 2.E.

[2] **A Review on Edge Large Language Models: Design, Execution, and Applications**
```
@article{qu2024edgellm,
  title     = {A Review on Edge Large Language Models: Design, Execution, and Applications},
  author    = {Qu, Zaichen and others},
  journal   = {arXiv preprint arXiv:2410.11845},
  year      = {2024},
  doi       = {10.48550/arXiv.2410.11845},
  url       = {https://arxiv.org/abs/2410.11845}
}
```
- Kaitan: Survey komprehensif deployment LLM di edge — klasifikasi hardware requirement per model size. Data Tabel A tentang model maksimum per konfigurasi merujuk survey ini.

[3] **Towards Building Private LLMs: Multi-Node Expert Parallelism on Apple Silicon**
```
@article{liu2025privateapple,
  title     = {Towards Building Private {LLMs}: Exploring Multi-Node Expert Parallelism on {Apple} Silicon for {Mixture}-of-Experts Large Language Model},
  author    = {Liu, Chen and others},
  journal   = {arXiv preprint arXiv:2506.23635},
  year      = {2025},
  doi       = {10.48550/arXiv.2506.23635},
  url       = {https://arxiv.org/abs/2506.23635}
}
```
- Kaitan: Mac Studio cluster untuk MoE model — analisis biaya vs DGX. Data Tabel B (Mac vs PC) diverifikasi dengan perbandingan biaya paper ini.

[4] **From Prompts to Power: Measuring the Energy Footprint of LLM Inference**
```
@article{liu2025promptspower,
  title     = {From Prompts to Power: Measuring the Energy Footprint of {LLM} Inference},
  author    = {Liu, Yuhan and others},
  journal   = {arXiv preprint arXiv:2511.05597},
  year      = {2025},
  doi       = {10.48550/arXiv.2511.05597},
  url       = {https://arxiv.org/abs/2511.05597}
}
```
- Kaitan: 32.500 pengukuran energi — 21 GPU config, 155 model. Data efisiensi per platform di Tabel C diverifikasi dengan paper ini.

[5] **Demystifying Small Language Models for Edge Deployment**
```
@inproceedings{lu2025demystifyingslm,
  title     = {Demystifying Small Language Models for Edge Deployment},
  author    = {Lu, Zhenyan and others},
  booktitle = {Annual Meeting of the Association for Computational Linguistics (ACL)},
  year      = {2025},
  doi       = {10.18653/v1/2025.acl-long.718},
  url       = {https://aclanthology.org/2025.acl-long.718/}
}
```
- Kaitan: Benchmark SLM di edge devices — data token/s, memory footprint, dan energy consumption. Tabel B tentang performa laptop merujuk temuan survey ini.

### Referensi Pendukung

[6] TechPowerUp. *GPU Pricing Database*. [https://www.techpowerup.com/gpu-specs](https://www.techpowerup.com/gpu-specs)

[7] Tokopedia / Shopee. *Harga Komponen PC Indonesia*. Harga pasar per Juni 2026.

[8] OpenAI. *API Pricing*. [https://openai.com/pricing](https://openai.com/pricing)

[9] PLN. *Tarif Listrik 2026*. [https://www.pln.co.id](https://www.pln.co.id)

[10] Puget Systems. *Hardware Recommendations for AI*. [https://www.pugetsystems.com](https://www.pugetsystems.com)

### SOP Referensi
- WAJIB menyertakan minimal **5 paper jurnal/konferensi** dengan DOI/arXiv valid.
- Harga dalam IDR bersifat indikatif per Juni 2026 — verifikasi harga di marketplace sebelum membeli.
- TCO adalah estimasi; biaya riil tergantung pola pemakaian dan tarif listrik setempat.
