File `CONTRIBUTING.md` sangat krusial agar 10 penulis kamu tidak bekerja secara serabutan dan hasil tulisannya memiliki standar kualitas yang sama. 

Berikut adalah isi lengkap untuk file `CONTRIBUTING.md` yang bisa langsung kamu salin:

---

# ✍️ Panduan Kontribusi: The Local LLM Bible

Selamat datang di tim! File ini berisi standar teknis dan prosedur operasional untuk memastikan proses penulisan buku kita berjalan mulus, terstruktur, dan memiliki kualitas profesional.

---

## 🚀 1. Alur Kerja Git (Git Workflow)

Untuk menghindari konflik file, kita akan menggunakan **Feature Branch Workflow**:

1.  **Sync Local:** Pastikan branch `main` kamu selalu *up-to-date*.
    ```bash
    git checkout main
    git pull origin main
    ```
2.  **Buat Branch Baru:** Gunakan format `nama-penulis/nama-bab`.
    ```bash
    git checkout -b budi/bab-02-gpu-benchmarks
    ```
3.  **Commit Secara Berkala:** Gunakan pesan commit yang jelas.
    ```bash
    git commit -m "Add: Komparasi benchmark RTX 4090 vs Mac Studio M3"
    ```
4.  **Push & Pull Request (PR):** Push branch kamu ke GitHub dan buka Pull Request untuk di-review oleh Project Leader.

---

## 📝 2. Standar Penulisan & Format

Semua dokumen ditulis menggunakan **Markdown (.md)**. Ikuti aturan berikut:

### **A. Struktur File (SOP)**
Setiap sub-bab wajib memiliki komponen berikut:
* **Header H1:** Judul Sub-bab.
* **Context:** Mengapa topik ini penting (1-2 paragraf).
* **Comparative Table:** Perbandingan antar opsi (Tools/Hardware/Model).
* **Hands-on:** Perintah terminal, konfigurasi `.yaml`, atau snippet kode.
* **Insight:** Analisis penulis (Pros & Cons).
* **References:** Link sumber primer.

### **B. Gaya Bahasa**
* Gunakan bahasa Indonesia yang teknis namun komunikatif.
* Gunakan istilah asing dalam *italic* jika belum ada padanan yang pas (contoh: *inference*, *latency*, *throughput*).

### **C. Blok Kode**
Sertakan bahasa pemrograman agar syntax highlighting berfungsi:
```bash
# Contoh perintah terminal
ollama run llama3
```

---

## 🖼️ 3. Manajemen Gambar & Diagram

* **Format:** Gunakan `.png` atau `.jpg` berkualitas tinggi.
* **Lokasi:** Simpan semua gambar di folder `/assets/images/jilidX/`.
* **Penamaan:** `jX-bX-sX-deskripsi.png` (Contoh: `j1-b2-s3-benchmark-vram.png`).
* **Diagram:** Sangat disarankan menggunakan **Mermaid.js** untuk diagram alur agar bisa diedit oleh penulis lain.

---

## 📊 4. Aturan Komparasi & Data

Buku ini berfokus pada **Objectivity**. Jangan membuat klaim tanpa data:
1.  **Benchmark:** Jika menyebutkan "X lebih cepat", sertakan angka *Token per Second* (TPS).
2.  **Hardware:** Berikan perbandingan harga ($ vs Rp) dan ketersediaan di pasar.
3.  **Model:** Gunakan data dari *Open LLM Leaderboard* atau *LMSYS Arena*.

---

## ⚖️ 5. Sitasi & Plagiarisme

1.  **Dilarang Plagiat:** Dilarang melakukan *copy-paste* langsung dari dokumentasi atau blog orang lain. Sadur informasi dan tulis ulang dengan gaya bahasa tim.
2.  **Sitasi:** Gunakan format Markdown link di akhir dokumen.
    * *Contoh:* `[1] Vaswani et al. (2017). "Attention is All You Need". [Link](https://arxiv.org/abs/1706.03762)`

---

## ✅ 6. Checklist Sebelum Submit Pull Request

Sebelum klik "Create Pull Request", pastikan:
- [ ] File berada di folder yang benar.
- [ ] Tidak ada *broken link* atau gambar yang tidak muncul.
- [ ] Perintah kode sudah dites dan berjalan (terutama di Mac/Linux).
- [ ] Tabel komparasi sudah disertakan.
- [ ] Daftar pustaka sudah diperbarui.

---

**Kontak Project Leader:** Jika ada kendala teknis atau kebingungan mengenai scope tulisan, silakan hubungi **Bagaskoro Saputro** di Discord/Grup Koordinasi.

---
