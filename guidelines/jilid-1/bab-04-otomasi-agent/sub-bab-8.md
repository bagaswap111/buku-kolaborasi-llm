# [Jilid 1] Bab 4.8: Keamanan & Sandbox — Docker-in-Docker Cegah AI Hapus Data
> **Tipe Konten:** Keamanan — Arsitektur + Best Practices + Implementasi
> **Target Pembaca:** Pengguna yang peduli safety saat memberikan akses shell ke AI

---

## 1. TUJUAN SUB-BAB
Pembaca mampu:
- Memahami threat model agentic AI: apa yang bisa salah jika agent punya akses shell
- Mengimplementasikan Docker sandbox untuk isolasi agent
- Menerapkan strategi defense-in-depth: permission, network isolation, rollback

---

## 2. KERANGKA KONTEN

### A. Threat Model Agentic AI (1-2 paragraf)
- Agent punya akses: file system, shell, network, API
- Risiko: `rm -rf /`, malware download, data exfiltration, privilege escalation
- Bukan soal "AI jahat" — tapi LLM bisa salah interpretasi instruksi

### B. Docker Sandbox — Lapisan Dasar (1 paragraf)
- Container: isolation via Linux namespaces + cgroups
- Keterbatasan: shared kernel — container escape masih mungkin
- Volume mount: baca-saja untuk kode sumber, /tmp untuk output

### C. Docker-in-Docker (DinD) (1-2 paragraf)
- Konsep: agent menjalankan Docker di dalam container Docker
- Isolasi penuh: agent bisa `docker run` tanpa akses ke host Docker socket
- MicroVM: tambahan lapisan hypervisor (Firecracker, gVisor)

### D. Network Isolation (1 paragraf)
- Blokir akses internet dari sandbox (kecuali API tertentu)
- DNS whitelist: hanya domain yang diizinkan
- Tidak boleh akses LAN/host internal

### E. Permission & Approval Gates (1 paragraf)
- Permission levels: read-only → dry-run → with-approval → full-auto
- Setiap operasi destruktif: `rm`, `mv`, `chmod`, `format` — butuh konfirmasi
- Audit log: semua command dicatat

### F. Rollback & Snapshot (1 paragraf)
- Sebelum agent mulai: snapshot filesystem (ZFS/btrfs/timeshift)
- Jika error: rollback ke snapshot
- Transactional approach: atomic changes

---

## 3. TABEL WAJIB

### Tabel A: Sandbox Isolation Levels

| Level | Teknologi | Isolasi Kernel | Boot Time | Overhead | Container Escape Risk |
|:---|:---|:---:|:---:|:---:|:---:|
| **1 — Container** | Docker | Shared | ~200ms | Rendah | Ada |
| **2 — DinD** | Docker-in-Docker | Shared (nested) | ~500ms | Rendah | Minimal |
| **3 — gVisor** | gVisor | Sandboxed kernel | ~300ms | Sedang | Sangat rendah |
| **4 — MicroVM** | Firecracker | Dedicated kernel | ~150ms | Sedang | Hampir tidak ada |
| **5 — Full VM** | QEMU/KVM | Dedicated | ~5-30s | Tinggi | Tidak ada |

### Tabel B: Risk Matrix — File Operations

| Operasi | Risiko | Minimal Permission | Approval Needed | Mitigasi |
|:---|:---:|:---|:---:|:---|
| **Read file** | Rendah | read | Tidak | - |
| **Write file** | Sedang | write | Opsional | Backup dulu |
| **Delete file** | Tinggi | write + delete | Ya | Trash instead |
| **Execute command** | Tinggi | execute | Ya | Timeout + log |
| **Network access** | Sedang | network | Ya | Whitelist |
| **Install package** | Sedang | write + execute | Ya | Allow list |
| **Format disk** | Kritis | root | Ya (manual) | Block by default |

### Tabel C: Perbandingan Sandbox Tools untuk AI Agent

| Tool | Isolasi | Network | Filesystem | Rollback | Setup | Cocok untuk |
|:---|:---|:---|:---|:---:|:---|:---|
| **Docker Sandbox (Docker)** | Container | Proxy | Volume mount | Manual | Mudah | Developer lokal |
| **Docker Sandbox (MicroVM)** | MicroVM | Isolated | Clone mode | Snapshot | Sedang | Production |
| **llm-sandbox (vndee)** | Container | None mode | RO mount | Ephemeral | Mudah | Code execution |
| **CubeSandbox** | MicroVM | eBPF | Full isolation | Snapshot | Sulit | Enterprise |
| **Fault-Tolerant Sandbox** | Container + FS | VXLAN | Transactional | Auto-rollback | Sulit | Research |

---

## 4. DIAGRAM/GAMBAR WAJIB

### Diagram 1: Arsitektur Sandbox Defense-in-Depth (Mermaid)
- **File:** `assets/diagrams/j1-b4-s8-sandbox-architecture.mmd`
- **Isi:** Host → Docker Engine → Container Agent → MicroVM → Network Proxy → Filesystem Filter → Audit Log. Setiap lapisan punya checkpoint keamanan.

### Gambar 2: Screenshot Audit Log Agent
- **File:** `assets/images/jilid1/j1-b4-s8-audit-log.png`
- **Isi:** Terminal menampilkan log setiap command yang dieksekusi agent, timestamp, status approve/reject

---

## 5. TUTORIAL / HANDS-ON

### Tutorial A: Docker Sandbox untuk AI Agent

```bash
# setup_sandbox.sh — Docker sandbox untuk agent
#!/bin/bash

# 1. Buat Dockerfile untuk sandbox
cat > Dockerfile.sandbox << 'EOF'
FROM ubuntu:22.04
RUN apt-get update && apt-get install -y \
    python3 python3-pip curl git jq \
    && rm -rf /var/lib/apt/lists/*
RUN pip3 install --no-cache-dir requests
WORKDIR /workspace
EOF

# 2. Build image
docker build -t agent-sandbox -f Dockerfile.sandbox .

# 3. Jalankan container dengan limited permissions
docker run --rm -it \
    --name agent-sandbox \
    --read-only \                    # Filesystem read-only
    --tmpfs /tmp:rw,noexec,nosuid,size=100m \  # Hanya /tmp bisa write
    --network none \                 # No network access
    --security-opt no-new-privileges \
    --cap-drop ALL \                 # Drop all capabilities
    --memory 2g \
    --cpus 2 \
    -v "$(pwd)/workspace:/workspace:ro" \  # Mount read-only
    agent-sandbox \
    python3 -c "
import os
# Agent akan jalan di sini
# Tidak bisa: rm -rf /, akses network, atau baca file di luar /workspace
print('Sandbox aktif!')
"
```

### Tutorial B: Approval Gate System

```python
# safety_gate.py — approval system untuk agent commands
import os
import json

DANGEROUS_COMMANDS = ["rm", "mv", "dd", "format", "mkfs",
                       "chmod 777", ">:*", "wget", "curl"]

class SafetyGate:
    def __init__(self, mode="interactive"):
        self.mode = mode  # interactive | auto_approve | deny_all

    def check_command(self, cmd):
        """Cek apakah command berbahaya"""
        for dangerous in DANGEROUS_COMMANDS:
            if dangerous in cmd:
                return False, f"Command terlarang: {dangerous}"
        return True, "OK"

    def execute(self, cmd, timeout=30):
        """Eksekusi dengan safety check"""
        safe, reason = self.check_command(cmd)
        if not safe:
            log_action(cmd, "REJECTED", reason)
            return {"status": "rejected", "reason": reason}

        if self.mode == "interactive":
            print(f"\n[APPROVAL] Command: {cmd}")
            choice = input("Approve? (y/N/skip): ").lower()
            if choice != 'y':
                log_action(cmd, "REJECTED", "User declined")
                return {"status": "rejected"}

        log_action(cmd, "APPROVED", "")
        result = os.popen(f"timeout {timeout} {cmd}").read()
        return {"status": "executed", "output": result}

    def log_action(self, cmd, status, reason):
        with open("audit.log", "a") as f:
            entry = {"cmd": cmd, "status": status,
                     "reason": reason, "timestamp": time.time()}
            f.write(json.dumps(entry) + "\n")

# Penggunaan
gate = SafetyGate(mode="interactive")
gate.execute("rm -rf /important")  # Akan ditolak
gate.execute("ls -la")            # Akan minta approval
```

### Tutorial C: Docker-in-Docker untuk Agent

```bash
# dind_agent.sh — Docker-in-Docker untuk agent
# Agent bisa 'docker run' tapi tidak punya akses ke host docker

# 1. Jalankan DinD container
docker run --privileged --name dind -d docker:27-dind

# 2. Jalankan agent dengan koneksi ke DinD
docker run --rm -it \
    --link dind:docker \
    -e DOCKER_HOST=tcp://docker:2376 \
    alpine sh -c "
# Agent ada di sini — bisa docker run image apa pun
# Tapi tidak bisa akses Docker host asli
docker run --rm alpine echo 'Hello from inside sandbox!'
"
```

---

## 6. STUDI KASUS

### Studi Kasus: Insiden Nyata — Agent Hampir Hapus Production Database
- **Skenario:** Agent diminta "bersihkan file log lama" di server
- **Masalah:** Agent salah interpretasi — menjalankan `rm -rf /var/log/*` tanpa filter tanggal
- **Dampak:** Hampir menghapus semua log, termasuk yang masih dibutuhkan audit
- **Mengapa tidak terjadi:** Safety gate memblock `rm -rf` karena termasuk dangerous command
- **Pelajaran:** Tanpa sandbox + approval gate, satu prompt salah bisa = bencana

---

## 7. REFERENSI WAJIB

[1] **Quantifying Frontier LLM Capabilities for Container Sandbox Escape**
```
@article{marchand2026sandboxescape,
  title     = {Quantifying Frontier {LLM} Capabilities for Container Sandbox Escape},
  author    = {Marchand, Rahul and O'Cathain, Art and Wynne, Jerome and others},
  journal   = {arXiv preprint arXiv:2603.02277},
  year      = {2026},
  doi       = {10.48550/arXiv.2603.02277}
}
```
- Kaitan: SandboxEscapeBench — benchmark kemampuan LLM breakout dari container. Dasar mitigasi Tabel A.

[2] **LLM-in-Sandbox Elicits General Agentic Intelligence**
```
@article{cheng2026llminsandbox,
  title     = {{LLM}-in-{Sandbox} Elicits General Agentic Intelligence},
  author    = {Cheng, Daixuan and Huang, Shaohan and Gu, Yuxian and Song, Huatong and Chen, Guoxin and Dong, Li and Zhao, Wayne Xin and Wen, Ji-Rong and Wei, Furu},
  journal   = {arXiv preprint arXiv:2601.16206},
  year      = {2026},
  doi       = {10.48550/arXiv.2601.16206}
}
```
- Kaitan: Docker sandbox + file system sebagai long-term memory — arsitektur isolasi untuk agent.

[3] **Fault-Tolerant Sandboxing for AI Coding Agents: A Transactional Approach**
```
@article{yan2025sandbox,
  title     = {Fault-Tolerant Sandboxing for {AI} Coding Agents: {A} Transactional Approach to Safe Autonomous Execution},
  author    = {Yan, Boyang and others},
  journal   = {arXiv preprint arXiv:2512.12806},
  year      = {2025},
  doi       = {10.48550/arXiv.2512.12806}
}
```
- Kaitan: Transactional sandboxing — atomic changes + auto-rollback pada failure.

[4] **Agentic AI Frameworks: Architectures, Protocols, and Design Challenges**
```
@article{masterman2024agenticai,
  title     = {Agentic {AI} Frameworks: Architectures, Protocols, and Design Challenges},
  author    = {Masterman, Tula and Besen, Sandi},
  journal   = {arXiv preprint arXiv:2404.11584},
  year      = {2024},
  doi       = {10.48550/arXiv.2404.11584}
}
```
- Kaitan: Arsitektur keamanan agent — safety guardrails, permission models, audit trails.

[5] **A Survey on Large Language Model based Autonomous Agents**
```
@article{wang2024agentsurvey,
  title     = {A Survey on Large Language Model based Autonomous Agents},
  author    = {Wang, Lei and Ma, Chen and Feng, Xueyang and others},
  journal   = {Frontiers of Computer Science},
  volume    = {18},
  number    = {6},
  pages     = {186345},
  year      = {2024},
  doi       = {10.1007/s11704-024-40231-1}
}
```
- Kaitan: Kategorisasi risiko agent — termasuk safety dan security sebagai dimensi evaluasi.

### Referensi Pendukung
[6] Docker Security Documentation. [https://docs.docker.com/engine/security/](https://docs.docker.com/engine/security/)
[7] gVisor — Sandboxed Container Runtime. [https://gvisor.dev](https://gvisor.dev)
[8] Firecracker MicroVM (AWS). [https://firecracker-microvm.github.io](https://firecracker-microvm.github.io)
