import requests
import time
import random

# Ganti localhost dengan IP Laptop jika pakai emulator Android nanti
API_URL = "http://localhost:8000/push-sensor"

print("--- MEMULAI SIMULASI SENSOR ESP32 ---")

while True:
    # Randomizer untuk Demo (0-100)
    chance = random.randint(0, 100)

    if chance < 50: 
        # 50% Kemungkinan AMAN (Suhu 30-35)
        temp = round(random.uniform(30.0, 35.0), 1)
        hum = round(random.uniform(60.0, 80.0), 1)
        
    elif chance < 80:
        # 30% Kemungkinan WASPADA (Suhu 36-37.9)
        temp = round(random.uniform(36.0, 37.9), 1)
        hum = round(random.uniform(50.0, 60.0), 1)
        
    else:
        # 20% Kemungkinan BAHAYA (Suhu 38+)
        temp = round(random.uniform(38.0, 45.0), 1)
        hum = round(random.uniform(30.0, 49.0), 1)
    
    payload = {"suhu": temp, "kelembaban": hum}
    
    try:
        requests.post(API_URL, json=payload)
        print(f"Kirim: {temp}°C | {hum}%")
    except Exception as e:
        print(f"Server Error: {e}")
        
    time.sleep(2)