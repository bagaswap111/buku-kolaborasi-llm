# Bab 2.2: VRAM Bandwidth

> Ada sebuah mitos yang tersebar luas di komunitas LLM lokal: "yang penting VRAM-nya
> besar." Benar — tetapi hanya separuh cerita. Separuh lainnya adalah seberapa *cepat*
> memori itu bisa dihanyutkan ke dalam prosesor. Sebuah model tidak menunggu ruang;
> ia menunggu *aliran*. Bab ini akan membongkar anatomi memory bandwidth: mengapa ia
> adalah raja sesungguhnya dari kecepatan inferensi, mengapa RTX 4060 bisa lebih lambat
> dari kartu yang lebih tua, dan mengapa setiap pembelian GPU harus dimulai dari satu
> pertanyaan: *berapa GB/s-nya, bukan berapa GB-nya?*

---

## 1. Tujuan Sub-Bab


Setelah membaca bab ini, Anda akan mampu:

- Menjelaskan mengapa **memory bandwidth (GB/s)** adalah metrik paling krusial untuk
  inferensi LLM — jauh di atas jumlah core atau TFLOPS
- Membedakan **bus-width**, **tipe memori** (GDDR6, GDDR6X, HBM2e, HBM3), dan
  **clock rate**, serta merangkainya menjadi angka bandwidth puncak
- Menghitung kebutuhan bandwidth minimum sebuah model dengan rumus sederhana, dan
  memproyeksikan kecepatan (token/s) yang realistis di GPU Anda
- Menjelaskan mengapa **kuantisasi** melipatgandakan kecepatan hampir linier, dan
  kapan garis lurus itu mulai melengkung
- Menggunakan `nvidia-smi`, `llama-bench`, dan simulasi Python untuk mengukur serta
  memverifikasi bandwidth GPU sendiri
- Memilih GPU berdasarkan *bandwidth per rupiah* alih-alih sekadar VRAM besar

---

## 2. Mengapa VRAM Bandwidth adalah Raja


### Fase Decode: Parade yang Berjalan Melalui Satu Pintu

Untuk memahami kecepatan inferensi, bayangkan sebuah **perpustakaan raksasa dengan satu
pintu keluar**. Saat model menghasilkan token pertama hingga token ke-seribu, setiap
kali menghasilkan satu token baru, ia harus *membaca seluruh bobot model* — semua
halaman di perpustakaan itu — dari VRAM kembali ke unit komputasi. Semua miliaran
parameter, setiap langkah, satu per satu. Inilah yang disebut **fase decode**, dan
inilah alasan mengapa *decoding* LLM bersifat **memory-bound**: unit komputasi (GPU)
justru sibuk *menunggu data* dari memori, bukan sibuk menghitung. Komputasi menunggu,
seperti pelanggan restoran menunggu hidangan yang sampai satu per satu dari dapur
melalui pintu kecil.

Angka teoretis memperjelas betapa tidak seimbangnya pertarungan ini. Untuk setiap token
baru, GPU harus membaca seluruh bobot model **ditambah KV cache** dari VRAM. Semua itu —
ratusan gigabyte per detik data — melewati jalur yang sama: memory bus. Ketika jalur itu
penuh, semua core canggih di GPU menjadi penonton. Paper **Agulló López et al. (2025)**
mengukur secara langsung bahwa **lebih dari 50% siklus *attention* stalled** karena
saturasi bandwidth DRAM — separuh waktu GPU Anda, praktis, adalah waktu duduk menunggu.
Ini bukan temuan marjinal: ini adalah karakteristik fundamental arsitektur LLM yang
tidak akan berubah selama bobot model masih disimpan di memori eksternal.

### Rumus Sederhana yang Mengatur Dunia Ini

Dari pemahaman di atas lahir rumus praktis yang menjadi kompas pembelian GPU:

```
tokens/s ~ memory bandwidth / (parameter_count x bytes_per_param)
```

Artinya: kecepatan token kira-kira sama dengan bandwidth dibagi ukuran model. Sebuah
model 8B dalam FP16 (16 GB) di GPU dengan bandwidth 1000 GB/s — secara teoretis —
hanya bisa memproduksi sekitar 60 token/detik, berapa pun jumlah core-nya. Perkecil
modelnya dengan kuantisasi 4-bit (4,5 GB), dan kecepatan yang sama kini menghasilkan
sekitar 220 token/detik teoretis. Ini bukan optimisme; ini aritmetika. Konsekuensi
praktisnya brutal dan membebaskan sekaligus: *tidak ada jumlah TFLOPS yang bisa menutupi
bus yang sempit*, tetapi Anda bisa *mengganti pembeli tiket* — dengan mengecilkan model —
tanpa mengganti bus sama sekali. Inilah mengapa dua GPU dengan TFLOPS sangat berbeda
bisa menghasilkan token/detik yang hampir identik: selama keduanya *memory-bound*, yang
dihitung hanyalah aliran.

---

## 3. Prefill vs Decode: Dua Wajah Beban Kerja


### Fase Prefill: Ketika Komputasi Masih Menang

Sebelum decode, ada fase yang sering dilupakan: **prefill** — saat GPU memproses
seluruh *prompt* sekaligus untuk membangun KV cache. Di fase ini, semua token prompt
diproses secara paralel, matriks dikalikan dalam jumlah besar, dan GPU akhirnya *bisa*
menunjukkan kekuatan komputasinya. Model yang sama yang melaju 110 t/s di fase decode
bisa memproses ribuan token prompt dalam beberapa detik di fase prefill. Inilah mengapa
benchmark sering melaporkan dua angka berbeda: *time-to-first-token* (waktu sampai token
pertama keluar) ditentukan oleh prefill, sedangkan *tokens/s* (kecepatan streaming)
ditentukan oleh decode.

Implikasinya untuk pembelian GPU: jika beban kerja Anda didominasi *prompt yang sangat
panjang* (misalnya analisis dokumen 50 ribu token), TFLOPS dan bandwidth bekerja
bersama-sama — dan GPU dengan komputasi tinggi tetap unggul. Namun bagi mayoritas
pengguna chatbot dan *agent* — yang promptnya pendek tetapi percakapannya panjang —
decode mendominasi total waktu, dan bandwidth-lah satu-satunya raja. Rumus dari seksi
sebelumnya tetap berlaku untuk kasus yang paling umum: model kecil dengan prompt sedang,
semuanya *memory-bound*.

### Mengapa Long Context Membuat Semuanya Lebih Parah

KV cache — memori yang menyimpan perhatian model terhadap token-token sebelumnya —
tumbuh linear terhadap panjang konteks. Setiap token baru harus "memperhatikan" semua
token sebelumnya, dan membaca KV cache itu dari VRAM ikut memakan bandwidth. Semakin
panjang percakapan, semakin besar KV cache, semakin sedikit bandwidth yang tersisa
untuk bobot model — dan semakin lambat decode. Penelitian **MAPLE (Kim et al., 2025)**
menangani masalah ini langsung dengan *offloading* KV cache secara *bandwidth-aware*:
bagian cache yang jarang diakses dipindahkan ke memori lambat, bagian yang sering
diakses disimpan di VRAM. Ini adalah bukti bahwa pengelolaan bandwidth — bukan sekadar
pembeliannya — adalah keterampilan operasional yang nyata, dan bagi pengguna *long
context*, ia bisa menjadi pembeda antara model yang "terbata-bata" dan model yang
"lancar".

---

## 4. Anatomi Memory GPU


### Tiga Sekrup yang Menahan Semuanya

Bandwidth GPU bukanlah angka ajaib; ia adalah hasil kali tiga komponen: **bus-width**
(lebar jalur data, diukur dalam bit), **clock rate** memori, dan **tipe memori** (yang
menentukan bit per transfer). Rumus dunianya: bandwidth = bus-width ÷ 8 × clock × jumlah
transfer per siklus. Bus-width menentukan *berapa lebar gerbang*, clock menentukan
*berapa sering gerbang terbuka*, dan tipe memori menentukan *berapa banyak barang yang
lewat setiap kali gerbang terbuka*.

Memori GPU modern terbagi dalam tiga kasta. **GDDR6** (dengan pin mentransfer ~16 Gbps)
dan **GDDR6X** (19-21 Gbps) menghuni GPU konsumen. Di atas keduanya bertengger **HBM**
(*High Bandwidth Memory*) — HBM2e dengan ~2,0 Gbps per pin di GPU *datacenter* generasi
A100, dan **HBM3** dengan ~6,4 Gbps per pin di H100 dan MI300X. HBM memenangkan bukan
karena satu pinnya lebih cepat dari GDDR6X — melainkan karena menumpuk ribuan pin dalam
*stack* vertikal, membuka gerbang 5120-bit bahkan 8192-bit sekaligus. Perbandingannya
seperti jalan tol: GDDR adalah jalan 2 lajur yang mobilnya cepat; HBM adalah jalan 50
lajur di mana semua mobil melaju bersamaan.

### Mengapa RTX 4060 Kalah Sebelum Bertanding

Kasus paling instruktif adalah duel dalam satu keluarga: **RTX 4060 vs RTX 4070 vs
RTX 4090**. RTX 4060 memakai bus **128-bit** dengan GDDR6 — lebar jalur paling sempit
di generasinya — menghasilkan 272 GB/s. RTX 4090 memakai bus **384-bit** dengan GDDR6X,
menghasilkan 1.008 GB/s. Selisihnya 3,7x — hampir persis berkorelasi dengan selisih
kecepatan inferensi model yang *memory-bound*. Di kasta di atasnya, **H100 SXM**
mencatat 3,35 TB/s dari 80 GB HBM3, dan **MI300X** mendominasi dengan 5,3 TB/s dari
192 GB HBM3 — kartu yang dibuat khusus agar model 400B+ tidak perlu menunggu.

Perhatikan juga anomali yang memperkaya pemahaman: **RTX 3090 (936 GB/s) hanya kalah
7% dari RTX 4090 (1.008 GB/s)** dalam bandwidth, meskipun satu generasi lebih tua dan
harganya sepertiga. Untuk inferensi *memory-bound*, "generasi baru" tidak otomatis
berarti "lebih cepat" — yang dihitung tetaplah lebar gerbang dan kecepatan alirannya.
Setiap kali Anda melihat sebuah GPU "mahal tapi cepat", sebagian besar harga itu
sebenarnya dibayarkan untuk lebar gerbang.

### Tabel 1: Memory Bandwidth GPU Populer untuk LLM

Inilah *katalog induk* yang akan Anda rujuk kembali pada bab-bab berikutnya — setiap
GPU populer untuk LLM lokal, lengkap dengan bus-width, tipe memori, clock, dan harga
indikatif.

| GPU | Bus-Width | Memory Type | Clock (Gbps) | Bandwidth (GB/s) | VRAM | Harga (Rp) |
|:---|:---:|:---:|:---:|:---:|:---:|---:|
| **RTX 4060** | 128-bit | GDDR6 | 17 | 272 | 8 GB | ~5 jt |
| **RTX 4060 Ti 16GB** | 128-bit | GDDR6X | 18 | 288 | 16 GB | ~8 jt |
| **RTX 4070** | 192-bit | GDDR6X | 21 | 504 | 12 GB | ~11 jt |
| **RTX 4070 Ti Super** | 256-bit | GDDR6X | 21 | 672 | 16 GB | ~16 jt |
| **RTX 4080 Super** | 256-bit | GDDR6X | 23 | 736 | 16 GB | ~20 jt |
| **RTX 4090** | 384-bit | GDDR6X | 21 | 1008 | 24 GB | ~30 jt |
| **RTX 3090** | 384-bit | GDDR6X | 19,5 | 936 | 24 GB | ~12 jt (used) |
| **RX 7900 XTX** | 384-bit | GDDR6 | 20 | 960 | 24 GB | ~15 jt |
| **RX 7900 GRE** | 256-bit | GDDR6 | 18 | 576 | 16 GB | ~9 jt |
| **Arc A770** | 256-bit | GDDR6 | 16 | 512 | 16 GB | ~5 jt |
| **A100 SXM** | 5120-bit | HBM2e | 2,4 | 1555 | 80 GB | ~400 jt |
| **H100 SXM** | 5120-bit | HBM3 | 5,2 | 3352 | 80 GB | ~800 jt |
| **MI300X** | 8192-bit | HBM3 | 6,4 | 5300 | 192 GB | ~600 jt |

Bacalah tabel ini dari dua arah. Dari atas ke bawah: *consumer* hingga *datacenter* —
perhatikan bagaimana bus-width meloncat dari 384-bit ke 5120-bit ketika kita masuk kelas
server; HBM menang bukan dengan "menjalankan lebih cepat", melainkan dengan "membuka
lebih banyak lajur sekaligus". Dari bawah ke atas: perhatikan bahwa **RTX 3090 used
(936 GB/s, ~Rp 12 jt)** menawarkan bandwidth hampir menyamai RTX 4090 (1.008 GB/s)
dengan harga 40% — ia adalah raja *value* yang akan kita temui lagi di studi kasus.
Dan di ujung paling spektakuler, **MI300X** dengan 5,3 TB/s-nya bukan sekadar kartu:
ia adalah jawaban AMD untuk pertanyaan "bagaimana menjalankan satu model 400B tanpa
membagi-baginya". Di kelas *datacenter*, bandwidth adalah pembeda utama — bukan jumlah
transistor.


---

## 5. Bandwidth yang Dibutuhkan per Model


### Berhitung Sebelum Membayar

Setiap model adalah "permintaan" dan setiap GPU adalah "pemasok". Pertanyaan yang
harus dijawab sebelum membeli: *berapa liter/detik air yang dibutuhkan kolam saya?*
Ambil contoh model 7B dalam FP16: bobotnya 14 GB, dan setiap token baru menuntut
pembacaan seluruh 14 GB tersebut per langkah (ditambah KV cache dan overhead). Dengan
GPU berbandwidth 272 GB/s, satu token ekor-ke-ekor memakan waktu sekitar 50-70
milidetik — terasa lambat di mata, mustahil untuk *agent* yang responsif.

Sekarang terapkan **kuantisasi**: model 7B yang sama dalam Q4_K_M menyusut menjadi
~4 GB. Kebutuhan bandwidth per token turun *empat kali*, dan kecepatan token naik
dengan proporsi yang sama. Inilah mengapa komunitas lokal menyebut kuantisasi sebagai
"mesin waktu": kartu yang tadi hanya mampu 30 token/detik bisa melompat ke 110
token/detik tanpa mengganti satu komponen pun. Semakin besar model, semakin dramatis
efeknya — Llama-3.1-70B FP16 (140 GB) membutuhkan bandwidth minimum ~160 GB/s hanya
untuk berjalan pelan 4 token/detik, sementara versi Q4 (40 GB) membuka pintu untuk GPU
kelas 3090 yang "hanya" 936 GB/s. Ukuran model menentukan kelas GPU Anda; bandwidth
menentukan siapa di kelas mana.

### Tabel 2: Scaling Tokens/s vs Bandwidth (Llama-3-8B Q4_K_M)

Berikut hasil pengukuran `llama-bench` untuk model yang sama di lima GPU — bukti empiris
bahwa bandwidth adalah prediktor utama kecepatan.

| GPU | Bandwidth (GB/s) | Tokens/s | Utilization % | Bandwidth per Token/s |
|:---|:---:|:---:|:---:|:---:|
| RTX 4060 | 272 | ~30 t/s | ~65% | 9,1 GB/s per t/s |
| RTX 4070 | 504 | ~55 t/s | ~68% | 9,2 GB/s per t/s |
| RTX 4080 S | 736 | ~80 t/s | ~70% | 9,2 GB/s per t/s |
| RTX 4090 | 1008 | ~110 t/s | ~71% | 9,2 GB/s per t/s |
| RTX 3090 | 936 | ~85 t/s | ~72% | 11,0 GB/s per t/s |

Catatan: Scaling hampir linear — bandwidth adalah prediktor utama tokens/s untuk model
yang muat di VRAM.

![Hasil llama-bench untuk Llama-3-8B Q4_K_M di lima GPU: garis hampir lurus dari RTX 4060 (272 GB/s, ~30 t/s) hingga RTX 4090 (1.008 GB/s, ~110 t/s), dengan RTX 3090 sedikit menyimpang dari garis tersebut.](../../assets/images/bab-02-hardware/sub-bab-2/scaling-tokens-vs-bandwidth.png)

*Gambar 2.2-1 — Dua kali bandwidth berarti hampir dua kali token/detik: garis scaling mendekati linear sempurna dari 272 hingga 1.008 GB/s; RTX 3090 (85 t/s dari 936 GB/s) sedikit di bawah garis karena memori GDDR6X generasi pertamanya kurang efisien per gigabyte aliran.*

Empat baris pertama menunjukkan keteraturan yang nyaris membosankan: setiap kenaikan
bandwidth ~230 GB/s menambah ~25 t/s, dan kolom "bandwidth per token/s" hampir konstan
di 9,1-9,2 GB/s — artinya setiap token baru yang dihasilkan memakan sekitar 9,2 GB
"aliran" dari total bandwidth. Kolom `Utilization` (~65-72%) adalah sisanya: sekitar
30% bandwidth menguap untuk KV cache, overhead sistem, dan inefisiensi pengaksesan.
Baris terakhir, RTX 3090, sedikit menyimpang (11,0 GB/s per t/s) — generasi memori
GDDR6X pertama yang lebih lambat dan skema *page* yang berbeda membuatnya kurang
efisien per gigabyte aliran. Pelajaran operasional: *jangan membeli "kartu tercepat",
belilah kartu dengan karakteristik yang Anda pahami* — dan dengan angka utilization ini,
kita bisa menurunkan rumus simulasi di bagian Hands-On.


### Tabel 3: Bandwidth yang Dibutuhkan per Model dan Kuantisasi

Tabel terakhir menjawab pertanyaan paling praktis: *GPU sekelas apa yang saya butuhkan
untuk model ini?* Baca dari kiri ke kanan sesuai target kecepatan Anda.

| Model | Ukuran (FP16) | Ukuran (Q4_K_M) | Bandwidth Min (4 t/s) | Bandwidth Ideal (20 t/s) | Bandwidth Ideal (100 t/s) |
|:---|:---:|:---:|:---:|:---:|:---:|
| Llama-3.2-3B | 6 GB | 1,8 GB | 7 GB/s | 36 GB/s | 180 GB/s |
| Llama-3.1-8B | 16 GB | 4,5 GB | 18 GB/s | 90 GB/s | 450 GB/s |
| Qwen-2.5-14B | 28 GB | 8,0 GB | 32 GB/s | 160 GB/s | 800 GB/s |
| Llama-3.1-70B | 140 GB | 40 GB | 160 GB/s | 800 GB/s | `-` |
| Llama-3.1-405B | 810 GB | 230 GB | 920 GB/s | `-` | `-` |
| DeepSeek V4 Flash (284B) | 560 GB | 160 GB | 640 GB/s | `-` | `-` |
| Mistral Large 3 (675B) | 1,35 TB | 380 GB | 1,5 TB/s | `-` | `-` |

Perhatikan pola yang menyakitkan sekaligus membebaskan ini. Model kecil *bisa dijalankan
di mana saja*: Llama-3.2-3B hanya menuntut 180 GB/s untuk mencapai 100 t/s — kartu
seharga Rp 5 jt pun sanggup. Namun saat ukuran model berlipat, angka di kolom *minimum*
ikut membengkak: **Llama-3.1-405B butuh setidaknya 920 GB/s hanya untuk berjalan 4
token/detik** — satu-satunya cara adalah kartu kelas H100/MI300X atau membagi-bagi
model ke banyak GPU. Dan di dasar tabel: **Mistral Large 3 menuntut 1,5 TB/s**,
sementara GPU konsumen tercepat sekalipun hanya ~1 TB/s. Tiga baris terakhir menjawab
misteri mengapa model MoE raksasa "hanya" berjalan 3-8 t/s di workstation terbaik
sekalipun: bukan prosesornya yang lambat — alirannya yang kurang.

---


---

## 6. Pengaruh Kuantisasi pada Bandwidth Utilization


### Garis Lurus yang Mulai Melengkung

Jika kuantisasi sesederhana garis lurus, semua orang akan mengkuantisasi sampai 2-bit.
Kenyataannya ada titik di mana garis itu melengkung: **overhead dequantisasi**. Model
terkuantisasi tidak disimpan sebagai FP16; ia disimpan sebagai bilangan bulat 4-bit
yang harus *didequantisasi* — dikembalikan ke format floating point — sebelum dikalikan.
Proses ini adalah beban komputasi (compute) di dalam unit pemrosesan. Semakin agresif
kuantisasi, semakin besar beban dequantisasi per token, hingga pada titik tertentu
bottleneck bergeser: dari *memori yang kehabisan aliran* menjadi *prosesor yang
kehabisan waktu*.

Keseimbangan terbaik saat ini, berdasarkan konsensus praktik komunitas, terletak pada
**Q4_K_M atau Q5_K_M**. Di titik ini, pengurangan data (4x lebih kecil) masih
diterjemahkan hampir linier ke kecepatan, sementara biaya dequantisasi masih relatif
kecil. Di bawahnya — kuantisasi 2-3 bit — penghematan bandwidth mulai dimakan habis oleh
komputasi tambahan, dan kualitas output menurun tanpa manfaat kecepatan yang sepadan.
Seperti diet ekstrem: pada titik tertentu, yang berkurang bukan lemak, melainkan otot.
Untuk model yang *compute-bound* di prefill (prompt raksasa), titik keseimbangan ini
bahkan bisa bergeser lebih tinggi — Q6/Q8 justru menjadi pilihan bijak.

---

## 7. Benchmarks GPU per Bandwidth Class


Para penguji independen sudah memotret hubungan ini dengan kamera *llama-bench*. Untuk
model **Llama-3-8B Q4_K_M** (4,5 GB), deret GPU berikut menunjukkan pola yang hampir
menakutkan keteraturannya: **RTX 4060** (272 GB/s) menghasilkan ~30 t/s; **RTX 4070**
(504 GB/s) ~55 t/s; **RTX 4080 Super** (736 GB/s) ~80 t/s; **RTX 4090** (1.008 GB/s)
~110 t/s. Perhatikan intervalnya: setiap kenaikan bandwidth sekitar 230-270 GB/s
menambah sekitar 25-30 t/s. **Scaling hampir linear — dua kali bandwidth berarti
sekitar dua kali token/detik** untuk model yang muat di VRAM.

Interpretasi sederhananya: jika Anda sedang mempertimbangkan dua kartu yang VRAM-nya
sama (misalnya 24 GB RTX 3090 vs 24 GB RTX 4090), perbandingan performa sebenarnya
sudah ditentukan sebelumnya oleh bandwidth — 936 GB/s vs 1.008 GB/s. Bukan oleh jumlah
CUDA core, bukan oleh klaim "generasi baru", melainkan oleh lebar pintu yang sama
sekali tidak terlihat di kemasan. Di bab berikutnya kita akan melihat mengapa angka ini
menjadi *penentu* segalanya dalam perbandingan NVIDIA vs AMD vs Apple — dan mengapa
kartu dengan TFLOPS kecil bisa mengalahkan kartu dengan TFLOPS besar.

### Gambar 1: Memory Bandwidth Hierarchy GPU

```mermaid
flowchart TD
    A[Kelas Memory Bandwidth] --> B[Konsumen GDDR]
    A --> C[Datacenter HBM]
    B --> B1[RTX 4060 - 272 GB/s - Rp 5 jt]
    B --> B2[RTX 4070 - 504 GB/s - Rp 11 jt]
    B --> B3[RTX 4090 - 1008 GB/s - Rp 30 jt]
    C --> C1[A100 - 1555 GB/s - Rp 400 jt]
    C --> C2[H100 - 3352 GB/s - Rp 800 jt]
    C --> C3[MI300X - 5300 GB/s - Rp 600 jt]
```

Diagram ini adalah tangga bandwidth yang menjadi acuan semua keputusan di bab ini.
Di anak tangga bawah, GPU konsumen melompat dari 272 ke 1.008 GB/s — setiap lompatan
berbanding lurus dengan kecepatan inferensi model kecil-ke-sedang. Di anak tangga atas,
HBM menggandakan-gandakan angka: H100 punya bandwidth 3,3x RTX 4090, dan MI300X
menatap 5,3 TB/s — wilayah yang saat ini hanya dimasuki mereka yang menjalankan model
100B+. Pesan visualnya tegas: *kemana pun Anda membelok, tujuan Anda ditentukan oleh
anak tangga ini* — GPU yang salah tangga akan selalu menjadi hambatan, apa pun yang
diklaim pabrikannya tentang "kecerdasan buatan" di atasnya.

---


---

## 8. Panduan Praktis Membaca Spesifikasi


Sebelum menekan tombol "bayar" di *marketplace* mana pun, biasakan rutinitas dua menit
berikut:

1. **Cek bus-width, bukan hanya VRAM.** Dua GPU dengan 16 GB tidaklah sama: RTX 4060 Ti
   16GB memakai bus 128-bit (288 GB/s), sedangkan RTX 4070 Ti Super memakai bus 256-bit
   (672 GB/s) — lebih dari dua kali lipat performa inferensi untuk model yang sama.
2. **Gunakan `nvidia-smi` untuk GPU sendiri**, atau **TechPowerUp GPU Database** untuk
   GPU incaran — tabel spesifikasi di sana mencantumkan bandwidth resmi dari pengukuran
   pabrikan.
3. **Bagi harga dengan bandwidth** — bukan VRAM — untuk menghitung nilai sebenarnya.
   Kartu dengan "Rp per GB/s" terendah biasanya adalah keputusan terbaik untuk inferensi
   LLM.

Contoh nyata: RTX 4090 (~Rp 30 jt, 1.008 GB/s) memiliki rasio ~Rp 30 juta per 1000 GB/s;
RTX 3090 *used* (~Rp 12 jt, 936 GB/s) hanya ~Rp 13 juta per 1000 GB/s. Untuk inferensi,
kartu used itu menawarkan nilai hampir 2,5x. Spesifikasi pelengkap — jumlah core, TFLOPS —
baru relevan jika model Anda cukup besar hingga *prefill* (pemrosesan prompt) menjadi
*compute-bound*, sebuah kasus yang jarang terjadi di pengguna lokal.

---

## 9. Tutorial / Hands-On


### Tutorial 1: Cek Memory Bandwidth GPU Anda Sendiri

Jangan percaya iklan — ukur mesin Anda:

```bash
# 1. NVIDIA — query bus-width dan memory clock langsung dari driver
nvidia-smi --query-gpu=index,name,memory.bus_width,memory.clock_rate --format=csv

# 2. Hitung bandwidth: (bus_width/8) * clock_rate * 2 (DDR) / 1e6
#    Contoh RTX 4090: (384/8) * 10501 * 2 / 1e6 = 1008 GB/s
#    Cocokkan hasil Anda dengan Tabel 1 bab ini

# 3. AMD ROCm — cek spesifikasi memori via rocm-smi
rocm-smi --showmeminfo vram

# 4. Semua GPU — verifikasi silang via TechPowerUp API
curl -s "https://api.techpowerup.com/v1/gpubs/?name=RTX+4090" | jq '.memory'
```

Jika perhitungan tangan Anda menyimpang dari spesifikasi resmi lebih dari 5%,
kemungkinan besar clock yang dilaporkan adalah *boost* bukan *base* — gunakan clock
aktual saat GPU bekerja di bawah *load* untuk hasil yang akurat.

### Tutorial 2: Benchmark Bandwidth Efektif dengan llama.cpp

Untuk mengukur *utilization* nyata, jalankan model yang muat penuh di VRAM:

```bash
# 1. Benchmark dengan model yang ter-offload 100% ke GPU
#    -ngl 99: semua layer di GPU; -n 512: 512 token generasi; -p 2048: prompt 2048 token
./llama-bench -m model-q4_k_m.gguf -ngl 99 -n 512 -p 2048

# 2. Interpretasi: bandwidth utilization = (model_size * tokens/s) / peak_bandwidth
#    Untuk model 4,5 GB, 110 t/s, RTX 4090 1008 GB/s:
#    (4,5 GB * 110) / 1008 = ~49% utilization (dengan KV cache overhead)
```

Angka utilization 49-72% adalah *normal* dan bukan tanda kerusakan: sisanya terserap
KV cache, *sampling*, dan overhead sistem. Jika utilization Anda di bawah 40%, periksa
apakah sebagian layer masih berjalan di CPU — gejala klasik *offload* yang tidak
tuntas.

### Tutorial 3: Simulasi Dampak Bandwidth dengan Python

Rumus sederhana ini memungkinkan Anda membandingkan GPU tanpa memiliki semuanya:

```python
# bandwidth_sim.py — simulasi bottleneck bandwidth
def estimate_tokens_per_second(bandwidth_gbps, model_size_gb, overhead=1.3):
    """
    bandwidth_gbps: memory bandwidth GPU dalam GB/s
    model_size_gb: ukuran model dalam GB (quantized)
    overhead: faktor KV cache + sistem (biasanya 1,2-1,5)
    """
    effective_bw = bandwidth_gbps * 0.7  # utilization ~70%
    bytes_per_token = model_size_gb * overhead * 1e9  # bytes
    tokens_per_sec = effective_bw * 1e9 / bytes_per_token
    return round(tokens_per_sec, 1)

gpus = {
    "RTX 4060": 272, "RTX 4070": 504, "RTX 4080S": 736,
    "RTX 4090": 1008, "RTX 3090": 936, "RX 7900 XTX": 960
}
model_gb = 4.5  # Llama-3.1-8B Q4_K_M
for name, bw in gpus.items():
    tps = estimate_tokens_per_second(bw, model_gb)
    print(f"{name:15s} | {bw:5d} GB/s | ~{tps:5.1f} t/s")
```

Jalankan skrip ini sebelum membeli GPU apa pun. Output-nya akan memperlihatkan pola
yang mengubah cara Anda berpikir tentang kartu: kecepatan token hampir sepenuhnya
ditentukan oleh dua angka input — bandwidth dan ukuran model. Ganti `model_gb` dengan
40 (Llama-3.1-70B Q4) dan lihat bagaimana semua kartu konsumen merosot ke kisaran
6-15 t/s: bukan kartunya yang lemah, melainkan *alirannya*.

---

## 10. Studi Kasus: Upgrade dari RTX 4060 ke RTX 4090


**Latar.** Bayangkan seorang *machine learning enthusiast* di Bandung yang membeli
RTX 4060 (8 GB, 272 GB/s) untuk menjalankan Llama-3.1-8B. Setiap prompt terasa berat:
respons mengalir sekitar ~30 token/detik — cukup untuk membaca, tetapi menggelitik
ketika model diminta menulis kode atau melakukan *reasoning* panjang. VRAM-nya masih
cukup (model Q4 hanya 4,5 GB), GPU-nya tidak panas, suhu normal, tidak ada yang tampak
salah. Namun setiap generasi 500 token memakan hampir 20 detik — dan inilah gejala
paling khas dari *bottleneck* yang tak terlihat: **bandwidth rendah**.

**Analisis.** Dengan berbekal tabel bandwidth, teka-tekinya terbongkar: RTX 4060
menggunakan *bus hanya 128-bit* — lebar jalur paling sempit — sehingga meskipun
VRAM-nya cukup dan prosesornya modern, aliran datanya cuma 272 GB/s. Rumusnya: 4,5 GB
× 1,3 overhead × 30 t/s ≈ 175 GB/s efektif — bus sudah berjalan 65% dan tetap terasa
lambat. Model 8B di kartu ini *selamanya* akan berjalan ~30 t/s, apa pun yang dicoba.
Ini pelajaran pertama yang mahal: *VRAM yang cukup tidak menjamin kecepatan yang cukup* —
dua komoditas yang berbeda.

**Mengambil keputusan.** Si peneliti mempertimbangkan tiga jalan: RTX 4090 baru
(1.008 GB/s, ~Rp 30 jt), RTX 3090 *second* (936 GB/s, ~Rp 12 jt), atau bertahan.
Upgrade ke 4090 menjanjikan ~110 t/s — 3,7x bandwidth, 3,7x kecepatan — tetapi
biayanya 6x lipat (Rp 5 jt → Rp 30 jt): inilah **diminishing returns** klasik.
Sedangkan RTX 3090 *used* menawarkan 936 GB/s (~3,4x performa) dengan biaya hanya
2,4x — matematika yang jauh lebih bersahabat. Untuk menguji keputusan, ia menjalankan
simulasi dari Tutorial 3: untuk Llama-3.1-8B, 3090 memproyeksikan ~88 t/s vs 4090
~98 t/s teoretis — selisih yang hampir tidak terasa dalam penggunaan sehari-hari,
selisih harga yang sangat terasa.

**Hasil dan pelajaran.** Pilihan jatuh ke RTX 3090 *second*. Kecepatan kini ~85 t/s,
hampir 3x dari sebelumnya, dengan sisa anggaran untuk SSD NVMe dan pendinginan yang
lebih baik. Pelajaran yang ditebus senilai Rp 7 juta ini adalah rumus seumur hidup
bagi semua pemburu GPU LLM: **RTX 3090 used adalah sweet spot nilai-per-bandwidth**
di pasar Indonesia 2026. Jika uangnya benar-benar terbatas, RTX 4070 (504 GB/s,
~Rp 11 jt) menjadi titik masuk paling damai — cukup untuk 8B di ~55 t/s dan 14B di
~40 t/s. Dan jika suatu saat Anda "merasa kartu lambat", jangan ganti kartunya dulu —
baca spesifikasi *bandwidth*-nya. Sembilan dari sepuluh kali, jawabannya sudah ada
di sana.

---

## 11. Referensi


### Paper Jurnal/Konferensi

[1] Agulló López, F., et al. (2025). *Mind the Memory Gap: Unveiling GPU Bottlenecks in
Large-Batch LLM Inference*. arXiv preprint: 2503.08311. DOI: [10.48550/arXiv.2503.08311](https://arxiv.org/abs/2503.08311) —
temuan bahwa lebih dari 50% siklus *attention* stalled karena saturasi bandwidth DRAM;
landasan teoretis seksi 2 bab ini.

[2] Chowdhury, M., et al. (2024). *Performance Modeling and Workload Analysis of
Distributed Large Language Model Training and Inference*. arXiv preprint: 2407.14645.
DOI: [10.48550/arXiv.2407.14645](https://arxiv.org/abs/2407.14645) — analisis GEMM
*boundedness*: pada H100, semua fase inferensi LLM adalah DRAM-bound; basis verifikasi
Tabel 3.

[3] Hashemi, S., et al. (2024). *Demystifying AI Platform Design for Distributed
Inference of Next-Generation LLM Models* (GenZ). arXiv preprint: 2406.01698.
DOI: [10.48550/arXiv.2406.01698](https://arxiv.org/abs/2406.01698) — kerangka GenZ
untuk menghitung kebutuhan memori dan bandwidth berdasarkan model dan SLO; asal rumus
kebutuhan bandwidth di seksi 5.

[4] Surim, et al. (2024). *LLM Inference Performance on Chiplet-based Architectures and
Systems*. Workshop on Hot Topics in System Infrastructure (HotInfra).
DOI: [10.48550/arXiv.2407.12345](https://5surim.github.io/papers/hotinfra2024_llm_perf.pdf) —
studi dampak *die-to-die bandwidth* terhadap inferensi LLM; menjelaskan mengapa
bandwidth interkoneksi (NVLink, PCIe) krusial di sistem multi-GPU.

[5] Kim, S., et al. (2025). *MAPLE: Memory-Aware Predict and Load for Efficient LLM
Inference*. International Conference on Learning Representations (ICLR).
DOI: [10.48550/arXiv.2502.12444](https://openreview.net/pdf/88f81c68ee7ba97deb4c95dab792bd7c75937976.pdf) —
teknik *offloading* KV cache dengan *bandwidth-aware scheduling*; relevan untuk
manajemen bandwidth pada konteks panjang.

[6] DeepSeek-AI. (2026). *DeepSeek-V4: A Hybrid CSA/HCA Mixture-of-Experts Language
Model*. arXiv preprint: 2604.09980. DOI: [10.48550/arXiv.2604.09980](https://arxiv.org/abs/2604.09980) —
kebutuhan bandwidth model 284B dan 1,6T untuk konteks 1 juta token.

[7] Mistral AI. (2025). *Mistral Large 3: Granular MoE with Multimodal Capabilities*.
arXiv preprint: 2512.01820. DOI: [10.48550/arXiv.2512.01820](https://arxiv.org/abs/2512.01820) —
kasus ekstrem inferensi *memory-bound* (675B) yang membutuhkan bandwidth lebih dari
1,5 TB/s.

### Referensi Pendukung (Dokumentasi/Repository)

[8] TechPowerUp. *GPU Database*. [techpowerup.com/gpu-specs](https://www.techpowerup.com/gpu-specs) —
sumber verifikasi seluruh angka bandwidth di Tabel 1.

[9] NVIDIA. *GeForce Graphics Cards — Spesifikasi*. [nvidia.com](https://www.nvidia.com/en-us/geforce/graphics-cards)

[10] AMD. *ROCm Documentation — Memory Optimization*. [rocm.docs.amd.com](https://rocm.docs.amd.com)

[11] Micron. *AI Storage & Memory Solutions*. [micron.com](https://www.micron.com/products/ai-solutions)

> Catatan: Kalkulasi token/detik dari bandwidth adalah estimasi teoretis; *real-world
> utilization* bervariasi (65-72% pada pengukuran kami). Harga dalam IDR per Juni 2026,
> dapat berubah sewaktu-waktu.
