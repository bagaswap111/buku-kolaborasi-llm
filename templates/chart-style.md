# PANDUAN GAYA GRAFIK STATIS (WAJIB DIIKUTI SAAT GENERATE GAMBAR)

> Panduan ini dipakai untuk semua gambar statis PNG yang di-generate dari data tabel konten.
> Setiap agen yang membuat gambar WAJIB mengikuti gaya di bawah ini agar seluruh buku tampil konsisten.

---

## 1. Aturan Umum

- **Sumber data:** HANYA angka yang sudah tertulis di file konten (tabel/paragraf). Dilarang mengarang data baru untuk keperluan grafik.
- **Format output:** PNG, dpi 150, `bbox_inches="tight"`.
- **Bahasa label:** Bahasa Indonesia (kecuali nama produk/istilah teknis seperti VRAM, token/s, Q4_K_M).
- **Jumlah gambar:** minimal 1 per file konten, maksimal 2 agar tidak berlebihan. Letakkan tepat SETELAH tabel yang datanya dipakai, dengan narasi pengantar 1 kalimat.
- **Nama file:** singkat, huruf kecil, tanpa spasi (contoh: `perbandingan-vram.png`, `skor-mmlu.png`).
- **Lokasi:** `konten/assets/images/<folder-bab>/sub-bab-N/<nama>.png` — buat direktori jika belum ada.
- **Keterangan gambar:** format
  ```markdown
  *Gambar X.N-i — keterangan singkat + insight utama (1-2 kalimat).*
  ```
  Penomoran `i` berurutan per file (1, 2, dst).

---

## 2. Gaya Visual (gaya resmi buku)

```python
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

WARNA = ["#3949ab", "#00897b", "#f9a825", "#e53935", "#6a1b9a", "#546e7a", "#7cb342", "#fb8c00"]

def gaya_dasar():
    plt.rcParams.update({
        "font.size": 11,
        "axes.titlesize": 13,
        "axes.titleweight": "bold",
        "axes.labelweight": "bold",
        "axes.grid": True,
        "grid.alpha": 0.25,
        "grid.color": "#546e7a",
        "figure.facecolor": "white",
        "axes.facecolor": "white",
        "axes.edgecolor": "#b0bec5",
        "legend.framealpha": 0.9,
    })
```

- **Bar chart:** `figsize=(11, 5)`, bar `edgecolor="white"`, `linewidth=0.8`. Label sumbu X diputar 30° jika panjang (`rotation=30, ha="right"`).
- **Line chart / multi-seri:** `figsize=(11, 5)`, garis `linewidth=2.2`, `marker="o"/"s"/"D"` bergantian di antara WARNA.
- **Pie/donut:** `figsize=(8, 6)`, `autopct="%1.1f%%"`, `startangle=90`, warna dari WARNA.
- **Horizontal bar (label panjang):** `figsize=(11, 7)`, `barh`, urutkan descending.
- **Sumbu Y logaritmik** jika rentang data sangat lebar (mis. parameter model 1,5B vs 1.600B).

## 3. Contoh Elemen Judul

```python
plt.title("Perbandingan Kebutuhan VRAM Antar Model", pad=14)
```

Judul harus deskriptif dan langsung menjawab "apa yang dibandingkan".

## 4. Verifikasi Wajib Sebelum Selesai

1. Script matplotlib dijalankan sampai sukses (tidak ada error).
2. File PNG tersimpan dan `ukuran > 0` (cek dengan `ls -la <path>`).
3. Path relatif embed benar: dari `konten/jilid-1/bab-XX-folder/sub-bab-N.md` ke `konten/assets/images/...` selalu berupa `../../assets/images/...`.
4. Angka pada grafik sesuai persis dengan angka di tabel sumber (periksa ulang 3 sampel nilai).