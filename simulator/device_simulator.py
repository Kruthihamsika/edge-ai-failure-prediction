import time
import random
import uuid
import requests
from datetime import datetime

# Backend API URL
API_URL = "http://127.0.0.1:8000/telemetry"

# Number of virtual edge devices
NUM_DEVICES = 5

# Create device IDs
DEVICES = [str(uuid.uuid4())[:8] for _ in range(NUM_DEVICES)]

def generate_metrics(device_id):
    normal = random.random() > 0.15  # 85% normal, 15% abnormal

    if normal:
        cpu = random.uniform(10, 60)
        memory = random.uniform(20, 70)
        latency = random.uniform(20, 100)
        errors = random.randint(0, 1)
    else:
        cpu = random.uniform(85, 100)
        memory = random.uniform(80, 95)
        latency = random.uniform(200, 500)
        errors = random.randint(5, 20)

    return {
        "device_id": device_id,
        "timestamp": datetime.utcnow().isoformat(),
        "cpu": round(cpu, 2),
        "memory": round(memory, 2),
        "latency": round(latency, 2),
        "errors": errors
    }

print("Starting Edge Device Telemetry Streaming...\n")

while True:
    for device in DEVICES:
        data = generate_metrics(device)

        try:
            response = requests.post(API_URL, json=data, timeout=2)
            print("Sent:", data, "| Status:", response.status_code)
        except Exception as e:
            print("Failed to send data:", e)

    print("-" * 60)
    time.sleep(2)
