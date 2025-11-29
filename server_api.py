from fastapi import FastAPI
from pydantic import BaseModel
import joblib
import uvicorn
import numpy as np
import os

app = FastAPI()

# --- KONFIGURASI MODEL ---
MODEL_FILENAME = 'ocsvm_maggot.pkl'  

# Cekfile sebelum load
if not os.path.exists(MODEL_FILENAME):
    raise FileNotFoundError(f"File '{MODEL_FILENAME}' tidak ditemukan! Masukkan ke folder yang sama.")

# Load Model 
print(f"Sedang meload model: {MODEL_FILENAME}...")
try:
    model = joblib.load(MODEL_FILENAME)
    print("✅ Model BERHASIL diload!")
except Exception as e:
    print(f"❌ Gagal load model: {e}")
    
    # from tensorflow.keras.models import load_model
    # model = load_model(MODEL_FILENAME)

# Variabel Memori Sementara
latest_result = {
    "suhu": 0,
    "kelembaban": 0,
    "status": "MENUNGGU...",
    "pesan": "Server siap menerima data"
}

class SensorData(BaseModel):
    suhu: float
    kelembaban: float

@app.post("/push-sensor")
def receive_data(data: SensorData):
    global latest_result
    
    # 1. Prediksi AI
    input_features = [[data.suhu, data.kelembaban]]
    try:
        pred = model.predict(input_features)[0] # Output: 1 (Normal) atau -1 (Anomali)
    except:
        pred = 1 # Default aman jika error

    # 2. Tentukan 3 Kategori (Logic Hybrid)
    status = "AMAN"
    pesan = "Kondisi Ideal."

    if pred == 1:
        # AI bilang Normal
        status = "AMAN"
        pesan = "✅ Maggot Sehat."
    else:
        # AI bilang Anomali (-1), sekarang kita cek seberapa parah?
        # Range Waspada: Suhu 36-38 ATAU Lembab < 50
        if (36.0 <= data.suhu <= 38.0) or (40.0 <= data.kelembaban <= 55.0):
            status = "WASPADA"
            pesan = "⚠️ Perlu Pengecekan Ringan."
        # Range Bahaya: Suhu > 38 ATAU Lembab < 40 (Ekstrim)
        else:
            status = "BAHAYA"
            pesan = "🚨 SUHU KRITIS! Kipas Nyala Max."

    # Update Data Terakhir
    latest_result = {
        "suhu": data.suhu,
        "kelembaban": data.kelembaban,
        "status": status,
        "pesan": pesan
    }
    
    print(f"Masuk: {data.suhu}°C | {data.kelembaban}% -> {status}")
    return {"msg": "Sukses"}

@app.get("/get-latest")
def get_latest_data():
    return latest_result

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)