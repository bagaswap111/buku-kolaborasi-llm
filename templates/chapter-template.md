Berikut adalah rancangan template profesional yang dirancang untuk menjaga konsistensi visual dan teknis di seluruh buku. File ini menggunakan elemen Markdown yang dioptimalkan agar mudah dibaca di GitHub maupun saat dikonversi ke PDF/LaTeX.

---

### **1. Isi File: `templates/chapter-template.md`**
Template ini adalah struktur wajib untuk setiap sub-bab.

```markdown
# [Jilid X] Bab X.X: [Judul Sub-Bab]

> **Status:** 🟡 Draft / 🟢 Review / 🔵 Final  
> **Penulis:** @[UsernamePenulis]  
> **Terakhir Diperbarui:** YYYY-MM-DD
```
---

## 📌 1. Konteks & Objektif
[Berikan penjelasan singkat 1-2 paragraf mengenai apa yang dibahas, mengapa teknologi ini relevan, dan masalah apa yang diselesaikannya dalam konteks LLM lokal.]

## 📊 2. Analisis Komparatif
[Masukkan tabel komparasi di sini menggunakan referensi dari table-style.md. Berikan narasi singkat yang merangkum data di tabel.]

## 🛠 3. Implementasi & Konfigurasi (Hands-on)
[Instruksi langkah demi langkah. Gunakan blok kode dengan indikator bahasa yang jelas.]

### A. Persiapan Environment
```bash
# Contoh perintah setup
pip install -r requirements.txt
```

### B. Konfigurasi
```yaml
# Contoh file config (jika ada)
model: "llama3-8b"
temperature: 0.7
max_tokens: 4096
```

## 💡 4. Insight Penulis (Pros & Cons)
[Analisis kritis penulis berdasarkan hasil pengujian/riset.]

* **Kelebihan:**
    * ...
* **Kekurangan:**
    * ...

## ⚠️ 5. Troubleshooting & Tips
[Sebutkan masalah umum yang sering muncul dan solusinya.]
* **Masalah:** Out of Memory (OOM).
* **Solusi:** Turunkan tingkat kuantisasi ke 4-bit atau gunakan GGUF split.

---

## 📚 Referensi & Sitasi
* [1] Nama Penulis. (Tahun). *Judul Paper/Dokumentasi*. [Link URL]
* [2] GitHub Repository: `username/repo-name`
