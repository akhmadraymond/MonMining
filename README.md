# MonMining Reporter 📡

Script Python untuk memantau mining VerusCoin dari STB Android/Linux dan mengirim laporan rutin ke Discord via Webhook. Cocok buat kamu yang pakai miner `ccminer` dan butuh monitoring suhu, hashrate, uptime, pool, hingga ping!

---

## 🔧 Fitur

- 💡 Deteksi dan kirim:
  - CPU Load
  - CPU Temperature
  - Hashrate
  - Uptime
  - Wallet & Worker
  - Mining Pool
  - Local IP
  - Ping ke internet (default: 8.8.8.8)
- 📡 Kirim ke Discord Webhook setiap 10 menit
- 💬 Format laporan sudah rapi dan stylish dengan icon

---

## 📂 File

- `reporter.py` → script utama monitoring dan pengiriman webhook

---

## 🚀 Cara Pakai

1. Clone atau unduh repo ini:
   ```bash
   git clone https://github.com/namakamu/monmonitor.git
