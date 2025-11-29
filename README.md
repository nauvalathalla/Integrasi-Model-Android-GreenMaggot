# 🐛 Green Maggot - Smart Biopond Ecosystem

> **Solusi IoT & AI untuk Budidaya Maggot BSF Terintegrasi.** > *Project MVP untuk Hackathon Innovillage / EISD 2025.*

![Status](https://img.shields.io/badge/Status-MVP_Ready-green)
![Tech](https://img.shields.io/badge/Stack-Python_Kotlin_IoT-blue)

## 📖 Deskripsi
**Green Maggot** adalah sistem monitoring cerdas untuk kandang Maggot (Biopond). Sistem ini menggunakan **AI (Isolation Forest)** untuk mendeteksi anomali suhu/kelembaban secara *real-time* dan memberikan peringatan dini (Early Warning System) ke aplikasi Android.

Proyek ini terdiri dari 3 komponen utama:
1.  **Server AI (Python/FastAPI):** Otak yang memproses data dan memprediksi status.
2.  **Dummy IoT (Python Script):** Simulasi perangkat ESP32 yang mengirim data sensor.
3.  **Mobile App (Android/Kotlin):** Dashboard monitoring untuk pengguna.

---

## 🏗️ Arsitektur Sistem

```mermaid
graph LR
    A[IoT Sensor / Dummy Script] -- POST JSON --> B(Server API & AI Model)
    B -- Response Status --> A
    C[Android App] -- GET Polling --> B
    B -- JSON Data {Suhu, Status} --> C
