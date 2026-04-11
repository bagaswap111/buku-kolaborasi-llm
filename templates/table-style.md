
### **2. Isi File: `templates/table-style.md`**
Gunakan format tabel ini untuk menjaga standar objektivitas di setiap bab.

#### **A. Tabel Komparasi Software/Tools**
Gunakan ini untuk membandingkan antar library atau GUI.

| Kriteria | Opsi A (Nama Tool) | Opsi B (Nama Tool) | Catatan |
| :--- | :--- | :--- | :--- |
| **Kemudahan** | ⭐⭐⭐⭐⭐ (Easy) | ⭐⭐⭐ (Advanced) | |
| **VRAM Usage** | Rendah | Menengah/Tinggi | |
| **API Support** | Native OpenAI | Plugin / Eksternal | |
| **Lisensi** | MIT (Open Source) | Proprietary | |
| **Best For** | Pemula / Personal | Pengembang / Dev | |

#### **B. Tabel Komparasi Hardware**
Gunakan ini di Bab Hardware atau Jilid 2 (Enterprise).

| Komponen | Spesifikasi Utama | Est. Harga (IDR) | Performa (Tokens/s) |
| :--- | :--- | :--- | :--- |
| **Apple M3 Max** | 128GB Unified RAM | ~ Rp 60jt++ | 15-20 t/s (70B Model) |
| **RTX 4090** | 24GB VRAM GDDR6X | ~ Rp 30jt - 35jt | 40-50 t/s (7B Model) |
| **RTX 3090 (Used)** | 24GB VRAM GDDR6X | ~ Rp 12jt - 15jt | Budget-to-Performance King |

#### **C. Tabel Skalabilitas (Khusus Jilid 2)**
Gunakan ini untuk membedakan Home vs Office.

| Fitur | Home Assistant | Small Office | General Office |
| :--- | :--- | :--- | :--- |
| **Target User** | 4-8 Orang | 9-20 Orang | 21-50 Orang |
| **Concurrence** | Rendah (Sequential) | Menengah | Tinggi (Batching) |
| **Security** | WPA3 / Local VPN | SSO / OAuth2 | AD / LDAP / Audit Logs |

---

### **3. Tips Styling untuk Penulis**
* **Bold Penting:** Gunakan **tebal** untuk istilah kunci atau tombol UI.
* **Warning Box:** Gunakan blok kutipan untuk peringatan:
    > ⚠️ **PENTING:** Jangan pernah mengekspos API Key atau port lokal ke internet publik tanpa SSH Tunnel atau VPN.
* **Diagram Mermaid:** Gunakan blok kode `mermaid` untuk alur:
    ```mermaid
    graph TD;
        A[User Prompt] --> B{Agent Logic};
        B --> C[Execute Shell];
        C --> D[Return Result];
    ```

Dengan template ini, siapa pun dari 10 penulis kamu yang mulai menulis akan langsung tahu standar apa yang harus mereka penuhi. Kamu bisa langsung menaruh kedua file ini di folder `/templates/` repositori kamu.
