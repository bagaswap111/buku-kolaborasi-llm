# Bab 1.1: Evolusi Transformer ke Lokal

> Perjalanan dari arsitektur Transformer (2017) hingga model open-source yang bisa dijalankan di laptop (2026-2027) — sebuah narasi teknologi yang mengubah wajah AI selamanya.

---

## 1. Tujuan Sub-Bab

Setelah membaca bab ini, Anda akan mampu:

- Menjelaskan evolusi arsitektur Transformer dari tahun 2017 hingga 2026 dengan memahami konteks setiap tonggak sejarah
- Memahami mengapa model open-source kini bisa menyaingi GPT-4/4.5 di perangkat lokal dengan biaya nol per query
- Mengidentifikasi tonggak sejarah utama: Transformer, GPT-2, GPT-3, LLaMA, Mistral, DeepSeek-R1, Llama 4, Qwen3.5, Mistral Large 3, GPT-5.5, DeepSeek V4, dan Claude Fable 5
- Memproyeksikan arah pengembangan model lokal hingga 2027 berdasarkan tren terkini

---

## 2. Pendahuluan

Pada awal 2017, dunia kecerdasan buatan masih didominasi oleh arsitektur RNN (Recurrent Neural Network) dan LSTM (Long Short-Term Memory) untuk pemrosesan bahasa alami. Model-model ini lambat, sulit dilatih, dan tidak bisa menangani konteks panjang. Kemudian datanglah sebuah makalah yang tidak hanya mengubah NLP — tetapi seluruh lanskap AI. Makalah "Attention Is All You Need" dari Vaswani et al. memperkenalkan arsitektur Transformer, sebuah pendekatan revolusioner yang murni berbasis mekanisme *self-attention*, tanpa RNN sama sekali.

Dalam waktu kurang dari satu dekade, arsitektur ini berevolusi dari model 0.1 miliar parameter (GPT-1) menjadi model 1,6 triliun parameter (DeepSeek V4 Pro) yang bisa diunduh dan dijalankan di workstation kelas menengah. Perjalanan ini bukan sekadar cerita tentang parameter yang semakin besar — ini adalah cerita tentang demokratisasi AI, tentang bagaimana teknologi yang awalnya hanya dikuasai oleh raksasa teknologi akhirnya bisa dimiliki oleh siapa pun dengan sebuah laptop.

---

## 3. Era Yayasan: Lahirnya Arsitektur Transformer (2017-2018)

### Transformer: Attention Is All You Need

 Pada bulan Juni 2017, tim peneliti Google — Ashish Vaswani, Noam Shazeer, Niki Parmar, dan rekan-rekan — mempublikasikan makalah yang menjadi fondasi semua LLM modern. Transformer memperkenalkan arsitektur *encoder-decoder* yang sepenuhnya mengandalkan mekanisme *self-attention*, di mana setiap token dalam sebuah urutan dapat "memperhatikan" token lainnya tanpa batasan jarak. Ini adalah terobosan fundamental: RNN dan LSTM memproses token secara sekuensial (token ke-5 harus menunggu token ke-1 sampai 4), sementara Transformer memproses semua token secara paralel.

Keunggulan Transformer tidak hanya pada kecepatan training. Mekanisme *self-attention* memungkinkan model menangkap ketergantungan jarak jauh yang sebelumnya mustahil bagi RNN. Dalam praktiknya, ini berarti Transformer bisa memahami konteks kalimat dengan lebih baik — misalnya, menghubungkan kata ganti "dia" dengan subjek yang disebutkan lima kalimat sebelumnya.

### BERT dan GPT-1: Dua Cabang Evolusi

 Makalah Transformer membuka jalan bagi dua garis keturunan arsitektur yang berbeda. Pertama, **BERT** (Bidirectional Encoder Representations from Transformers) yang dirilis oleh Google pada 2018. BERT adalah *encoder-only* — ia membaca teks secara dua arah (kiri-ke-kanan dan kanan-ke-kiri) dan unggul dalam tugas pemahaman seperti klasifikasi teks, menjawab pertanyaan, dan analisis sentimen. Dengan 340 juta parameter, BERT menjadi standar baru untuk NLP pada masanya.

Kedua, **GPT-1** (Generative Pre-trained Transformer) yang dirilis oleh OpenAI pada Juni 2018. GPT-1 adalah *decoder-only* — ia membaca teks secara searah (kiri-ke-kanan) dan unggul dalam tugas generasi seperti menulis teks, percakapan, dan kode. Dengan hanya 117 juta parameter, GPT-1 adalah model kecil, tetapi ia memperkenalkan konsep penting: *pre-training* pada data besar tanpa label, diikuti *fine-tuning* untuk tugas spesifik.

Kedua arsitektur ini — encoder-only (BERT) dan decoder-only (GPT) — menjadi fondasi semua LLM modern. Pada tahun-tahun berikutnya, arsitektur decoder-only terbukti lebih skalaibel dan menjadi pilihan dominan untuk model generatif.

---

## 4. GPT-2 dan GPT-3: Era Model Tertutup (2019-2022)

### GPT-2: Kontroversi yang Mengguncang Dunia

 Pada 2019, OpenAI merilis GPT-2 dengan 1,5 miliar parameter — hampir 13 kali lebih besar dari GPT-1. Kualitas teks yang dihasilkan sangat meyakinkan sehingga OpenAI memutuskan untuk tidak merilis model penuh, dengan alasan "terlalu berbahaya" karena potensi penyalahgunaan untuk menghasilkan berita palsu, spam, dan konten manipulatif. Keputusan ini memicu perdebatan sengit di komunitas AI: apakah menahan model adalah tindakan bertanggung jawab atau justru kontraproduktif?

Meskipun kontroversial, GPT-2 membuktikan bahwa *scaling* — memperbesar model dan data — menghasilkan peningkatan kualitas yang dramatis. Model ini juga menunjukkan bahwa *few-shot learning* mulai muncul: GPT-2 bisa melakukan tugas yang tidak pernah dilatih secara spesifik, hanya dengan diberikan beberapa contoh dalam *prompt*.

### GPT-3: Loncatan Kuantum

 Puncak era model tertutup datang pada 2020 dengan GPT-3: 175 miliar parameter, dilatih pada 570 GB teks, dan mampu melakukan *few-shot learning* yang mengejutkan dunia. Tanpa *fine-tuning* khusus, GPT-3 bisa menulis esai, membuat kode Python, menjawab pertanyaan rumit, dan bahkan melakukan terjemahan bahasa — hanya dengan beberapa contoh dalam *prompt*.

Bersamaan dengan GPT-3, makalah "Scaling Laws for Neural Language Models" (Kaplan et al., 2020) merumuskan hukum empiris: semakin besar parameter dan semakin banyak data training, semakin baik performa model. Hukum ini menjadi kredo industri selama bertahun-tahun dan mendorong perlombaan model raksasa.

Komersialisasi dimulai: GPT-3 tersedia hanya melalui API berbayar, ChatGPT diluncurkan pada November 2022 dan mencapai 100 juta pengguna dalam dua bulan — adopsi tercepat dalam sejarah teknologi. Namun, keterbatasan model tertutup mulai terasa: tidak bisa diunduh, setiap query harus bayar, data pengguna dikirim ke cloud, dan tidak ada kontrol atas model.

---

## 5. LLaMA-1 dan Ledakan Open-Source (Februari 2023)

Titik balik sejarah terjadi pada Februari 2023. Meta merilis LLaMA-1 (Large Language Model Meta AI) dalam empat ukuran: 7B, 13B, 33B, dan 65B parameter. Yang membedakan LLaMA dari model sebelumnya adalah efisiensi training: LLaMA-1 7B hanya dilatih dengan 1 triliun token, sementara GPT-3 175B dilatih dengan 300 miliar token. Ini berarti model yang lebih kecil bisa mencapai kualitas kompetitif dengan biaya training yang jauh lebih rendah.

Beberapa minggu setelah rilis, model LLaMA-1 "bocor" ke publik melalui forum 4chan — siapa pun bisa mengunduhnya. Bocornya LLaMA-1 memicu ledakan ekosistem lokal. Georgi Gerganov mengembangkan llama.cpp, implementasi C++ murni yang bisa menjalankan LLaMA di CPU tanpa GPU mahal. Lahirlah format GGUF (GGML Universal Format) untuk kuantisasi model, dan tools seperti Ollama serta LM Studio yang membuat instalasi model lokal semudah *drag-and-drop*.

Dampaknya revolusioner: untuk pertama kalinya, individu dengan laptop gaming bisa menjalankan LLM berkualitas tanpa koneksi internet. Komunitas open-source mulai melakukan *fine-tuning* untuk bahasa daerah, domain medis, hukum, dan coding — sesuatu yang mustahil dilakukan dengan API tertutup.

---

## 6. Mistral 7B: Era Model Kecil Bertenaga (September 2023)

Pada September 2023, Mistral AI — sebuah startup asal Prancis — merilis Mistral 7B dengan klaim berani: model 7B ini mengalahkan LLaMA-2 13B di hampir semua benchmark. Ini adalah momen penting yang membuktikan bahwa jumlah parameter bukanlah segalanya.

Inovasi arsitektur Mistral 7B meliputi **Sliding Window Attention** (SWA) yang memungkinkan konteks hingga 8.192 token dengan biaya komputasi linier — bukan kuadratik — serta **Grouped Query Attention** (GQA) yang mengoptimalkan penggunaan memori KV-cache. GQA kemudian diadopsi oleh Llama-3 dan menjadi standar industri.

Mistral 7B membuka pintu bagi filosofi baru: model yang lebih kecil dan lebih efisien bisa sama kompetennya dengan model besar jika arsitektur dirancang dengan baik. Ini adalah awal dari era model "kecil bertenaga" (*small language models* atau SLM) yang menjadi tren utama pada tahun-tahun berikutnya.

---

## 7. Llama-3 dan Standar Baru Model Lokal (April 2024)

Meta kembali mengguncang industri pada April 2024 dengan Llama-3 — sebuah *herd of models* (kawanan model) dalam tiga ukuran: 8B, 70B, dan 405B parameter, semuanya dilatih pada lebih dari 15 triliun token. Ini adalah peningkatan 15 kali lipat dalam jumlah data training dibandingkan LLaMA-1.

Fitur unggulan Llama-3 meliputi:
- **Context window 128K** — 128 kali lebih besar dari GPT-3
- **Grouped Query Attention** — mengadopsi inovasi Mistral
- **Flash Attention 2** — attention yang dioptimalkan untuk GPU modern
- **Tool use dan function calling native** (Llama-3.1, Juli 2024)

Dampaknya terhadap ekosistem lokal sangat signifikan. Dengan ukuran hanya 5,2 GB dalam format Q4_K_M, Llama-3 8B bisa dijalankan di laptop dengan GPU kelas RTX 2060. Kualitasnya setara atau melebihi GPT-3.5 untuk sebagian besar tugas — dan GPT-3.5 adalah model yang setahun sebelumnya masih memerlukan API berbayar.

Pada September 2024, Qwen2.5 dari Alibaba meramaikan persaingan. Model dense (non-MoE) dalam rentang 0,5B hingga 72B ini dilatih pada 18 triliun token dan mendukung 29 bahasa. Qwen2.5-7B mencapai MMLU 70,5%, hampir menyamai GPT-3 175B yang hanya 70,7% — menunjukkan bahwa model kecil kini bisa menyaingi model raksasa dari empat tahun sebelumnya.

---

## 8. DeepSeek-V3/R1: Era Reasoning (Desember 2024 - Januari 2025)

Akhir 2024 menjadi saksi gebrakan dari DeepSeek, laboratorium AI asal Tiongkok. DeepSeek-V3, dirilis pada Desember 2024, adalah model Mixture-of-Experts (MoE) dengan 671 miliar parameter total, tetapi hanya 37 miliar aktif per token. Dengan arsitektur Multi-head Latent Attention (MLA) dan DeepSeekMoE, model ini dilatih hanya dengan biaya sekitar $5,5 juta — jauh di bawah perkiraan industri yang menaksir biaya training model setara >$100 juta.

Angka $5,5 juta mengguncang asumsi industri. Jika model sekelas GPT-4 bisa dilatih dengan biaya kurang dari harga satu rumah mewah, maka hambatan masuk ke dunia LLM turun drastis. DeepSeek membuktikan bahwa inovasi arsitektur (MLA, MoE) dan optimasi training (FP8 mixed precision) bisa memangkas biaya tanpa mengorbankan kualitas.

Pada Januari 2025, DeepSeek-R1 menyusul dengan terobosan lain: *reasoning via pure reinforcement learning* menggunakan algoritma GRPO (Group Relative Policy Optimization). Tanpa data reasoning buatan manusia, model belajar berpikir langkah demi langkah (*chain-of-thought*) dan mencapai performa setara OpenAI o1 pada benchmark matematika dan coding. Yang lebih menarik, R1 bisa didistilasi ke model kecil — Qwen dan Llama versi kecil kini memiliki kemampuan reasoning yang sebelumnya hanya dimiliki model raksasa.

---

## 9. Llama 4 dan Era MoE Lokal (April 2025)

April 2025 menjadi bulan penting dengan dirilisnya Llama 4 — model MoE pertama dalam keluarga Llama. Dua varian utama dirilis:

- **Scout (17B x 16 experts):** Total 109B, aktif 17B per token, dengan context window 10 juta token — cukup untuk memproses seluruh buku Harry Potter berkali-kali lipat. Dalam format INT4, model ini muat di satu GPU kelas RTX 4070.
- **Maverick (17B x 128 experts):** Total 400B, aktif 17B per token, performa setara GPT-4.5 di beberapa benchmark.

Bersamaan dengan Llama 4, Qwen3 dari Alibaba menawarkan inovasi *unified thinking mode*: dalam satu model, pengguna bisa memilih mode *thinking* (berpikir langkah demi langkah) atau *non-thinking* (jawaban langsung). Qwen3 mendukung 119 bahasa dan tersedia dalam varian dense (0,6B-235B) maupun MoE (30B-A3B yang hanya 3B aktif).

Phi-4 dari Microsoft, dengan hanya 14B parameter tetapi mencapai MMLU 82,1%, membuktikan bahwa *synthetic data* — data buatan yang dihasilkan oleh model lain — bisa lebih efektif daripada data alami. Ini membuka paradigma baru: model kecil yang dilatih dengan data sintetis berkualitas tinggi bisa mengalahkan model besar yang dilatih dengan data mentah.

---

## 10. Mistral Large 3: Open-Source Eropa (Desember 2025)

Pada Desember 2025, Mistral AI kembali dengan gebrakan besar: Mistral Large 3, model granular MoE dengan 675 miliar parameter total dan 41 miliar aktif — semuanya dirilis di bawah lisensi Apache 2.0 yang sangat permisif. Model ini dilatih pada 3.000 GPU H200 NVIDIA dan menjadi model open-source non-Tiongkok terkuat yang pernah ada.

Arsitektur Mistral Large 3 menggunakan 128 *experts* per lapisan dengan *Multi-Latent Attention*, mendukung konteks 256K token, dan memiliki encoder vision 2,5B untuk pemahaman gambar. Dalam berbagai benchmark, model ini mencapai parity dengan model open-source terbaik dari Tiongkok dan mendekati performa model proprietary kelas atas.

Dampak strategis Mistral Large 3 sangat signifikan: ia membuktikan bahwa Eropa mampu menghasilkan model *frontier* open-weight yang setara dengan AS dan Tiongkok. Lisensi Apache 2.0 memungkinkan penggunaan komersial tanpa batas — perusahaan bisa memodifikasi, mendistribusikan, dan menjual turunan model tanpa membayar lisensi.

Bersamaan dengan Large 3, Mistral merilis **Ministral 3** — keluarga model kecil (3B, 8B, 14B) yang dihasilkan melalui *Cascade Distillation*, teknik yang menggabungkan *pruning* (pemangkasan) dan distilasi untuk menciptakan model efisien dari model yang lebih besar. Ministral 3 3B bisa berjalan di smartphone, sementara varian 14B memberikan kualitas setara model 30B dari generasi sebelumnya.

---

## 11. Qwen3.5/3.6 dan Puncak SLM (Februari - April 2026)

Awal 2026 menyaksikan kematangan model kecil (*Small Language Models* / SLM) yang mencengangkan. Qwen3.5, dirilis pada Februari 2026, adalah model multimodal dengan arsitektur Hybrid-Attention MoE (397B total, 17B aktif) yang mendukung 113 bahasa dan konteks 256K token. Kemampuan *native agent* — model bisa menggunakan tools, merencanakan tugas, dan menjalankan workflow secara mandiri — menjadi fitur standar.

Dua bulan kemudian, Qwen3.6 hadir dengan spesialisasi *coding*. Varian 27B dense-nya mampu menyaingi GPT-4o untuk tugas pemrograman Python dan Rust, dengan ukuran hanya 16 GB dalam format Q4_K_M — cukup untuk dijalankan di laptop dengan RTX 3090. Varian MoE 35B-A3B (hanya 3B aktif) bahkan bisa berjalan di GPU kelas menengah.

Fenomena yang lebih menarik adalah model 1-3B yang kini mampu menjalankan agen dan workflow kompleks — tugas yang dua tahun lalu hanya bisa dilakukan model 70B+. Ini adalah hasil dari kombinasi arsitektur efisien (MoE, GQA, sliding window), kuantisasi (INT4, FP4), dan distilasi dari model besar.

---

## 12. Era Frontier Baru: GPT-5.5, DeepSeek V4, Qwen3.7, Claude Fable 5 (April - Juni 2026)

### GPT-5.5: Kecerdasan untuk Kerja Nyata

 Pada 23 April 2026, OpenAI merilis GPT-5.5 — model proprietary yang dirancang untuk *agentic coding*, *computer use*, dan pekerjaan profesional yang kompleks. Dengan konteks 1 juta token dan dukungan *reasoning effort* (low, medium, high, xhigh), GPT-5.5 bisa merencanakan, menggunakan tools, memverifikasi hasil, dan terus bekerja hingga tugas selesai.

GPT-5.5 dibanderol dengan harga $5 per juta token input dan $30 per juta token output — mahal, tetapi sebanding dengan kualitas yang ditawarkan. Varian Pro, yang menggunakan *parallel test-time compute* untuk akurasi lebih tinggi, dibanderol $30/$180 per juta token.

### DeepSeek V4: Open-Source Terbesar

 Sehari setelah GPT-5.5, pada 24 April 2026, DeepSeek merilis DeepSeek V4 — model open-source di bawah lisensi MIT yang langsung menjadi model terbuka terbesar di dunia. Dua varian dirilis:

- **DeepSeek V4 Pro:** 1,6 triliun parameter total, 49 miliar aktif, dilatih pada 33 triliun token, konteks 1 juta token. Arsitektur hybrid CSA/HCA (Compressed Sparse Attention + Heavily Compressed Attention) memangkas FLOPs hingga 27% dan KV cache hingga 10% dibandingkan V3.2 pada konteks 1 juta token. MMLU-Pro mencapai 87,5%, LiveCodeBench 93,5%.
- **DeepSeek V4 Flash:** 284 miliar parameter total, 13 miliar aktif, konteks 1 juta token. Cukup efisien untuk dijalankan di workstation 2xRTX 6000 melalui INT4.

Yang membuat DeepSeek V4 istimewa adalah lisensi MIT — pengguna bisa menggunakan, memodifikasi, dan mendistribusikan tanpa batasan. Ini kontras dengan GPT-5.5 yang sepenuhnya proprietary. DeepSeek V4 membuktikan bahwa open-source bisa menyaingi frontier proprietary.

### Qwen3.7-Max: Agen Tanpa Batas

 Pada 20 Mei 2026, Alibaba meluncurkan Qwen3.7-Max, model proprietary yang diposisikan sebagai "*The Agent Frontier*". Dengan konteks 1 juta token dan arsitektur MoE yang parameter pastinya tidak diungkapkan (diperkirakan ~1 triliun+), model ini dirancang untuk eksekusi tugas otonom jangka panjang — hingga ribuan panggilan tools dalam satu sesi. Sayangnya, Alibaba memilih untuk tidak membuka *weights* model ini, melanjutkan tren pergeseran dari open-source ke proprietary.

### Claude Fable 5: Kekuatan dengan Pengaman

 Puncak dari periode ini adalah rilis Claude Fable 5 oleh Anthropic pada 9 Juni 2026. Fable 5 adalah model *Mythos*-class — tingkat keamanan tertinggi Anthropic — yang dibuat tersedia untuk publik dengan *safety classifiers* yang bisa menolak permintaan berbahaya di bidang keamanan siber, biologi, dan kimia.

Fable 5 mencapai SWE-bench Verified 95,0% — tertinggi untuk model publik pada saat rilis. Dengan konteks 1 juta token dan harga $10/$50 per juta token, model ini menjadi pilihan utama untuk tugas *reasoning* dan coding paling berat. Namun, *safety classifiers*-nya menuai kontroversi: sekitar 5% sesi pengalaman *false positive* di mana permintaan yang tidak berbahaya ditolak, memicu perdebatan tentang keseimbangan antara keamanan dan kegunaan.

### Pergeseran Tren

Periode April-Juni 2026 menunjukkan polarisasi yang menarik. Di satu sisi, model proprietary (GPT-5.5, Qwen3.7, Claude Fable 5) menawarkan kualitas terbaik tetapi dengan harga tinggi, kontrol terpusat, dan *lock-in* vendor. Di sisi lain, model open-weight (DeepSeek V4, Mistral Large 3) menawarkan kebebasan total dengan kualitas yang mendekati — dan dalam beberapa benchmark, menyamai — model proprietary.

Bagi ekosistem lokal, implikasinya jelas: DeepSeek V4 Flash (284B) bisa dijalankan di workstation 2xRTX 6000 melalui INT4 dengan biaya inference nol, sementara model 1-3B seperti Ministral 3 dan Qwen3.6-27B makin mumpuni untuk agen kompleks di laptop. Era model lokal yang *really useful* telah tiba.

---

## 13. Proyeksi 2027: Masa Depan Model Lokal

Berdasarkan tren yang terlihat pada 2025-2026, beberapa proyeksi dapat dibuat untuk 2027 — meskipun perlu ditekankan bahwa ini adalah proyeksi berdasarkan tren saat ini, bukan prediksi pasti.

**Model 1-3B di perangkat wearable.** Smartphone, smartwatch, dan perangkat IoT akan memiliki LLM lokal yang berfungsi sebagai asisten pribadi tanpa perlu koneksi cloud. Ministral 3 3B adalah cikal bakal tren ini.

**Reasoning native.** Semua model, bahkan yang terkecil sekalipun, akan memiliki kemampuan *reasoning* setara o1-mini secara *default*. Distilasi dari model reasoning besar ke model kecil akan menjadi praktik standar.

**Multimodal lokal.** LLM lokal akan secara *native* memproses gambar, suara, dan video tanpa API eksternal. Model seperti Qwen3.5 (multimodal native) adalah langkah awal menuju tren ini.

**Spesialisasi ekstrem.** Akan muncul model khusus industri — untuk hukum, medis, teknik — yang bisa dijalankan di laptop. Fine-tuning dan distilasi akan menjadi lebih mudah dan murah.

**Green AI.** Model akan semakin efisien. Proyeksi optimis: model 70B berjalan di 16 GB RAM dengan kuantisasi 2-bit, sementara efisiensi arsitektur seperti CSA/HCA (DeepSeek V4) akan menjadi standar.

**Potensi open vs closed.** DeepSeek V4 dan Mistral Large 3 membuktikan bahwa open-weight bisa menyaingi proprietary. Namun, Qwen3.7 dan GPT-5.5 menunjukkan tren sebaliknya — model proprietary tetap unggul di *benchmark* tertentu. Pertanyaan besarnya: apakah 2027 akan menjadi tahun open-source mendominasi, atau justru terjadi fragmentasi?

**Potensi perubahan paradigma.** Apakah *scaling law* (lebih besar = lebih baik) masih berlaku? Atau *synthetic data* dan teknik distilasi (seperti yang digunakan Phi-4 dan Ministral 3) akan menjadi kunci utama? Indikasi awal menunjukkan bahwa kualitas data dan arsitektur efisien mungkin lebih penting daripada jumlah parameter mentah.

---

## 14. Tabel Wajib

### Tabel 1: Timeline Evolusi Model (2017-2026)

| Tahun | Tonggak | Parameter | Arsitektur | Konteks | Keunikan / Dampak |
|:---|:---|:---:|:---|:---:|:---|
| 2017 | Transformer (Vaswani et al.) | - | Encoder-Decoder | - | Fondasi semua LLM modern |
| 2018 | GPT-1 / BERT | 0,1B / 0,3B | Decoder / Encoder | 512 | Awal era pre-training + fine-tuning |
| 2019 | GPT-2 | 1,5B | Decoder-only | 1.024 | Kontroversi rilis "too dangerous" |
| 2020 | GPT-3 | 175B | Decoder-only | 2.048 | Few-shot learning, Scaling Laws |
| 2022 | ChatGPT | - | RLHF enhanced | 4.096 | Ledakan adopsi publik |
| 2023 | LLaMA-1 | 7B-65B | Decoder-only | 2.048 | Titik balik open-source LLM |
| 2023 | Mistral 7B | 7B | Sliding Window Attn | 8.192 | GQA, outperforms LLaMA-2 13B |
| 2024 | Llama-3 / 3.1 | 8B-405B | Decoder + GQA | 128K | Tool use, multilingual, 15T+ token |
| 2024 | Qwen2.5 | 0,5B-72B | Dense decoder | 32K | Multilingual 29 bahasa, 18T token |
| 2024 | DeepSeek-V3 | 671B (37B aktif) | MoE + MLA | 128K | Training $5,5M, efisiensi ekstrem |
| 2025 | DeepSeek-R1 | 671B (37B aktif) | MoE + GRPO RL | 128K | Reasoning via pure RL, setara o1 |
| 2025 | Llama 4 Scout | 109B (17B aktif) | MoE 16 experts | 10M | Multimodal, 1 GPU via INT4 |
| 2025 | Llama 4 Maverick | 400B (17B aktif) | MoE 128 experts | 1M | Setara GPT-4.5 (benchmark tertentu) |
| 2025 | Qwen3 | 0,6B-235B | Dense + MoE | 128K | Thinking mode, 119 bahasa |
| 2025 | Phi-4 / Phi-4-reasoning | 14B | Dense decoder | 16K | Synthetic data > distilasi |
| 2025 | Mistral Large 3 | 675B (41B aktif) | Granular MoE + Vision | 256K | Apache 2.0, open-source Eropa |
| 2026 | Qwen3.5 | 35B-397B MoE | Hybrid-Attn MoE | 256K | Multimodal native, 113 bahasa |
| 2026 | Qwen3.6 | 27B-35B MoE | Coding specialist | 128K | Model lokal 27B setara GPT-4o |
| 2026 | GPT-5.5 / 5.5 Pro | - | Proprietary decoder | 1M | Reasoning effort, $5/$30 per M token |
| 2026 | DeepSeek-V4 Pro | 1,6T (49B aktif) | MoE + CSA/HCA | 1M | MIT, open-source terbesar |
| 2026 | DeepSeek-V4 Flash | 284B (13B aktif) | MoE + CSA/HCA | 1M | MIT, companion efisien |
| 2026 | Qwen3.7-Max | ~1T+ (est.) | Proprietary MoE | 1M | Agent-centric, closed-weight |
| 2026 | Claude Fable 5 | - | Proprietary decoder | 1M | Mythos-class, safety classifiers |

### Tabel 2: Perbandingan Ukuran Model dan Kebutuhan Hardware (Lokal)

| Model | Ukuran Q4_K_M | RAM Min. | GPU Minimum | Bisa di Laptop? |
|:---|:---:|:---:|:---|:---:|
| GPT-2 (1,5B) | 1,2 GB | 4 GB | CPU saja | Ya |
| LLaMA-7B | 4,5 GB | 8 GB | GTX 1060 6GB | Ya (GPU low-end) |
| Mistral 7B | 4,5 GB | 8 GB | GTX 1060 6GB | Ya |
| Llama-3 8B | 5,2 GB | 8 GB | RTX 2060 8GB | Ya |
| Phi-4 (14B) | 8,5 GB | 12 GB | RTX 3060 12GB | Ya (laptop gaming) |
| Qwen2.5-32B | 18 GB | 24 GB | RTX 3090 24GB | Ya (high-end) |
| Qwen3-30B-A3B | 2,5 GB | 6 GB | CPU/GPU ringan | Ya (efisien MoE) |
| Llama 4 Scout | ~12 GB (INT4) | 16 GB | RTX 4070 12GB+ | Ya (high-end) |
| DeepSeek-R1 (671B) | ~280 GB | 320 GB | Cluster GPU | Tidak |
| Llama-3 70B | 42 GB | 48 GB | 2x RTX 4090 | Tidak (server) |
| Qwen3.6-27B | 16 GB | 24 GB | RTX 3090 24GB | Ya (high-end) |
| Mistral Large 3 (675B) | ~280 GB (FP8) | 320 GB | 8xH200 / GB200 NVL72 | Tidak (server) |
| DeepSeek V4 Flash (284B) | ~150 GB (INT4) | 192 GB | 2xRTX 6000 Ada | Server/workstation |
| DeepSeek V4 Pro (1,6T) | ~865 GB | 1 TB+ | Cluster GPU HGX B200 | Tidak (datacenter) |
| Ministral 3 14B | 8,5 GB | 12 GB | RTX 3060 12GB | Ya (laptop gaming) |
| Ministral 3 3B | 2 GB | 4 GB | CPU/GPU ringan | Ya (semua perangkat) |

### Tabel 3: Benchmark Lintas Generasi

| Model | MMLU | GSM8K | HumanEval | Tahun | Kategori |
|:---|:---:|:---:|:---:|:---:|:---|
| GPT-2 1,5B | 32,4% | - | - | 2019 | Dense kecil |
| GPT-3 175B | 70,7% | 45,0% | 48,1% | 2020 | Dense besar |
| LLaMA-1 7B | 46,9% | 16,8% | 14,0% | 2023 | Dense kecil |
| Mistral 7B | 62,5% | 45,2% | 30,5% | 2023 | Dense kecil |
| Llama-3 8B | 66,7% | 79,6% | 62,2% | 2024 | Dense kecil |
| Qwen2.5-7B | 70,5% | 80,1% | 75,1% | 2024 | Dense kecil |
| Phi-4 14B | 82,1% | 91,8% | 82,6% | 2024 | Dense kecil |
| DeepSeek-V3 (671B) | 88,5% | 92,3% | 89,5% | 2024 | MoE besar |
| DeepSeek-R1 (671B) | 90,8% | 96,3% | 92,4% | 2025 | MoE + RL reasoning |
| Llama 4 Scout (109B) | 84,2% | 89,5% | 80,1% | 2025 | MoE multimodal |
| Qwen3-30B-A3B | 85,1% | 92,0% | 85,5% | 2025 | MoE efisien |
| Qwen3.6-27B | 85,9% | 93,1% | 90,2% | 2026 | Dense coding specialist |
| Mistral Large 3 (675B) | ~87% | ~93% | ~85% | 2025 | MoE granular open-source |
| DeepSeek V4 Pro (1,6T) | 87,5% (MMLU-Pro) | 95,2% (HMMT) | 93,5% (LiveCode) | 2026 | MoE CSA/HCA + MIT |
| GPT-5.5 | ~91%\* | ~96%\* | ~93%\* | 2026 | Proprietary frontier |
| Qwen3.7-Max | ~89%\* | ~95%\* | ~91%\* | 2026 | Proprietary MoE agent |
| Claude Fable 5 | ~90%\* (GPQA) | ~95%\* | 95,0% (SWE-bench) | 2026 | Mythos-class proprietary |

*\* Perkiraan berdasarkan data benchmark tidak langsung. Model proprietary jarang mempublikasikan MMLU/GSM8K standar.*

---

## 15. Tutorial / Hands-On

### Tutorial 1: Merasakan Perbedaan Generasi Model

Cara terbaik memahami evolusi model adalah menjalankannya langsung. Ikuti langkah-langkah berikut untuk merasakan perbedaan kualitas dari setiap era.

```bash
# 1. Install Ollama
curl -fsSL https://ollama.com/install.sh | sh

# 2. Jalankan model dari era berbeda
# Era 2023 — Mistral 7B (revolusi model kecil)
ollama run mistral "Jelaskan AI dalam bahasa Indonesia"

# Era 2024 — Llama-3.1 8B (standar baru model lokal)
ollama run llama3.1:8b "Jelaskan AI dalam bahasa Indonesia"

# Era 2025 — Qwen3 8B (thinking mode)
ollama run qwen3:8b "Jelaskan AI dalam bahasa Indonesia"

# Era 2026 — DeepSeek V4 Flash (284B, MIT — via Ollama)
# Tersedia di Ollama mulai pertengahan 2026
ollama pull deepseek-v4-flash
ollama run deepseek-v4-flash "Jelaskan AI dalam bahasa Indonesia"
```

### Tutorial 2: Benchmark Model Lama vs Baru

Untuk mengukur secara kuantitatif seberapa jauh perkembangan model:

```bash
# Install lm-evaluation-harness
pip install lm-eval

# Benchmark GPT-2 (2019)
lm_eval --model hf --model_args pretrained=gpt2 \
    --tasks mmlu --num_fewshot 5 --batch_size 1

# Benchmark Phi-4 (2024) — butuh GPU
lm_eval --model hf --model_args pretrained=microsoft/phi-4 \
    --tasks mmlu --num_fewshot 5 --batch_size auto

# Bandingkan hasilnya — perhatikan lonjakan dari 32% (GPT-2) ke 82% (Phi-4)
```

### Tutorial 3: Visualisasi Evolusi Model (Python)

```python
import matplotlib.pyplot as plt

models = [
    'GPT-2\n2019', 'GPT-3\n2020', 'LLaMA-1 7B\n2023',
    'Mistral 7B\n2023', 'Llama-3 8B\n2024', 'Phi-4 14B\n2024',
    'DeepSeek-V3\n2024', 'Qwen3 30B\n2025', 'Mistral L3\n2025',
    'Qwen3.6 27B\n2026', 'DS V4 Pro\n2026'
]
params = [1.5, 175, 7, 7, 8, 14, 671, 30, 675, 27, 1600]
params_active = [1.5, 175, 7, 7, 8, 14, 37, 3, 41, 27, 49]
mmlu = [32.4, 70.7, 46.9, 62.5, 66.7, 82.1, 88.5, 85.1, 87.0, 85.9, 87.5]

fig, ax1 = plt.subplots(figsize=(14, 6))
bars = ax1.bar(models, params, alpha=0.5, label='Total Parameter (Miliar)')
bars_active = ax1.bar(models, params_active, alpha=0.8, label='Aktif per Token (Miliar)')
ax1.set_ylabel('Parameter (Miliar)')
ax1.set_yscale('log')

ax2 = ax1.twinx()
ax2.plot(models, mmlu, 'ro-', linewidth=2, label='MMLU (%)')
ax2.set_ylabel('MMLU (%)')
ax2.set_ylim(0, 100)

plt.title('Evolusi Model: Parameter vs Performa (2019-2026)')
plt.legend(loc='upper left')
plt.savefig('evolusi-model-2019-2026.png', dpi=150, bbox_inches='tight')
```

Grafik ini akan menunjukkan dua hal penting: (1) parameter total terus membesar secara eksponensial, tetapi (2) parameter aktif (untuk model MoE) jauh lebih kecil, dan (3) skor MMLU meningkat dari 32% (GPT-2) menjadi 87,5% (DeepSeek V4 Pro) — peningkatan hampir 3x dalam 7 tahun.

---

## 16. Studi Kasus: Perjalanan Seorang Developer dari GPT-2 ke DeepSeek V4 (2019-2026)

**Profil:** Seorang AI engineer di Indonesia yang menggunakan model bahasa untuk produktivitas coding dan menulis konten teknis.

**2019-2022:** Memulai dengan GPT-2 (1,5B) untuk eksperimen NLP sederhana. Sering frustrasi karena output tidak koheren untuk Bahasa Indonesia — model ini dominan terlatih pada data Inggris. Konteks hanya 1.024 token, sehingga dokumen panjang harus dipecah manual per paragraf. Biaya: nol (berjalan di laptop), tetapi hasilnya lebih mirip *mad-libs* daripada teks bermakna.

**2023:** Bocornya LLaMA-1 7B mengubah segalanya. Untuk pertama kalinya, model mulai memahami instruksi Bahasa Indonesia — meskipun masih sering salah memahami konteks budaya lokal (misalnya, mengartikan "bawang merah" sebagai *red onion* dalam konteks investasi pasar tradisional). Menggunakan llama.cpp di laptop dengan GTX 1060 6GB, kecepatan ~5 token/detik.

**2024:** Upgrade ke Llama-3.1-8B. 128K context window memungkinkan memproses seluruh dokumen tanpa *chunking*. *Tool use* dan *function calling* native memungkinkan model berinteraksi dengan API dan database. Kualitas output setara GPT-3.5 — yang sebelumnya membutuhkan API berbayar. Ukuran hanya 5,2 GB (Q4_K_M) — muat di laptop dengan RTX 2060. Biaya: nol.

**2025:** Tahun eksperimen intensif. Menggunakan DeepSeek-R1 via API untuk *reasoning* kompleks (analisis kode, matematika), Phi-4 14B lokal untuk *daily coding*, dan Mistral Large 3 via API untuk tugas multibahasa. Phi-4 14B mencapai MMLU 82% — lebih tinggi dari LLaMA-1 65B yang 63%. Mistral Large 3 (675B, Apache 2.0) membuktikan bahwa open-source non-Tiongkok bisa setara *frontier*. Biaya: masih nol untuk model lokal, ~$20/bulan untuk API.

**H1 2026:** Beralih ke Qwen3.6-27B sebagai *coding assistant* lokal — model 27B ini menyamai GPT-4o untuk generate Python dan Rust. Mulai bereksperimen dengan DeepSeek V4 Flash (284B, MIT) di workstation 2xRTX 6000 via INT4. Menguji GPT-5.5 dan Claude Fable 5 via API untuk tugas yang memerlukan *reasoning* terdalam — hasilnya mengesankan, tetapi biaya API membuatnya tidak praktis untuk penggunaan harian.

**Pelajaran:** Dari GPT-2 (MMLU 32%) ke DeepSeek V4 Flash (LiveCodeBench 91,6%) dalam 7 tahun — peningkatan kualitas hampir 3x. Biaya per query: dari ~$0,01 (GPT-3 API 2020) menjadi $0 (lokal, open-weight 2026). Konteks: dari 1.024 token menjadi 1 juta token. Ekosistem: dari 1 model proprietary menjadi ribuan model open-source. Transformasi ini bukan hanya tentang teknologi — ini tentang siapa yang memiliki akses ke AI.

---

## 17. Referensi

### Paper Jurnal/Konferensi

[1] Vaswani, A., et al. (2017). *Attention Is All You Need*. NeurIPS. DOI: [10.48550/arXiv.1706.03762](https://arxiv.org/abs/1706.03762)

[2] Radford, A., et al. (2019). *Language Models are Unsupervised Multitask Learners*. OpenAI Blog.

[3] Brown, T.B., et al. (2020). *Language Models are Few-Shot Learners*. NeurIPS. DOI: [10.48550/arXiv.2005.14165](https://arxiv.org/abs/2005.14165)

[4] Kaplan, J., et al. (2020). *Scaling Laws for Neural Language Models*. NeurIPS. DOI: [10.48550/arXiv.2001.08361](https://arxiv.org/abs/2001.08361)

[5] Touvron, H., et al. (2023). *LLaMA: Open and Efficient Foundation Language Models*. arXiv: [2302.13971](https://arxiv.org/abs/2302.13971)

[6] Jiang, A.Q., et al. (2023). *Mistral 7B*. arXiv: [2310.06825](https://arxiv.org/abs/2310.06825)

[7] Grattafiori, A., et al. (2024). *The Llama 3 Herd of Models*. arXiv: [2407.21783](https://arxiv.org/abs/2407.21783)

[8] DeepSeek-AI. (2024). *DeepSeek-V3 Technical Report*. arXiv: [2412.19437](https://arxiv.org/abs/2412.19437)

[9] DeepSeek-AI. (2025). *DeepSeek-R1: Incentivizing Reasoning Capability in LLMs via RL*. arXiv: [2501.12948](https://arxiv.org/abs/2501.12948)

[10] Abdin, M., et al. (2024). *Phi-4 Technical Report*. arXiv: [2412.08905](https://arxiv.org/abs/2412.08905)

[11] Yang, A., et al. (2024). *Qwen2.5 Technical Report*. arXiv: [2412.15115](https://arxiv.org/abs/2412.15115)

[12] Yang, A., et al. (2025). *Qwen3 Technical Report*. arXiv: [2505.09388](https://arxiv.org/abs/2505.09388)

[13] Qwen Team. (2026). *Qwen3.5-Omni Technical Report*. arXiv: [2604.15804](https://arxiv.org/abs/2604.15804)

[14] DeepSeek-AI. (2026). *DeepSeek-V4: Towards Highly Efficient Million-Token Context Intelligence*. [PDF](https://huggingface.co/deepseek-ai/DeepSeek-V4-Pro/blob/main/DeepSeek_V4.pdf)

[15] Mistral AI. (2025). *Introducing Mistral 3*. [Blog](https://mistral.ai/news/mistral-3/)

[16] OpenAI. (2026). *GPT-5.5 System Card*. [System Card](https://openai.com/index/gpt-5-5-system-card/)

[17] Anthropic. (2026). *Claude Fable 5 and Claude Mythos 5*. [Blog](https://www.anthropic.com/news/claude-fable-5-mythos-5)

[18] Mistral AI. (2026). *Ministral 3*. arXiv: [2601.08584](https://arxiv.org/abs/2601.08584)

[19] Lin, T., et al. (2021). *A Survey of Transformers*. arXiv: [2106.04554](https://arxiv.org/abs/2106.04554)

### Referensi Pendukung

[20] Meta AI. *Llama 4 Model Card*. [GitHub](https://github.com/meta-llama/llama-models/blob/main/models/llama4/MODEL_CARD.md)

[21] Qwen Team. *Qwen3.6 Release Blog*. [qwen.ai](https://qwen.ai/blog?id=qwen3.6-27b)

[22] Ollama. *GitHub Repository*. [github.com/ollama/ollama](https://github.com/ollama/ollama)

[23] ggerganov. *llama.cpp*. [github.com/ggerganov/llama.cpp](https://github.com/ggerganov/llama.cpp)

[24] LMSYS Chatbot Arena. *Leaderboard*. [lmarena.ai](https://lmarena.ai)

[25] Hugging Face. *Open LLM Leaderboard*. [huggingface.co](https://huggingface.co/spaces/open-llm-leaderboard/open_llm_leaderboard)

[26] Qwen Team. *Qwen3.7: The Agent Frontier*. [qwen.ai](https://qwen.ai/blog?id=qwen3.7)

[27] DeepSeek. *DeepSeek V4 Preview Release*. [api-docs.deepseek.com](https://api-docs.deepseek.com/news/news260424)
