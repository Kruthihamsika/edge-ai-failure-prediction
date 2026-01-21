from fastapi import FastAPI
from pydantic import BaseModel
import sqlite3
import joblib
import pandas as pd

# =========================
# App Initialization
# =========================

app = FastAPI(title="Edge AI Telemetry + Failure Prediction Backend")

# =========================
# Load ML Model
# =========================

MODEL_PATH = "failure_model.pkl"
model = joblib.load(MODEL_PATH)

# =========================
# Database Setup
# =========================

DB_PATH = "telemetry.db"

conn = sqlite3.connect(DB_PATH, check_same_thread=False)
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS telemetry (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    device_id TEXT,
    timestamp TEXT,
    cpu REAL,
    memory REAL,
    latency REAL,
    errors INTEGER
)
""")
conn.commit()

# =========================
# Data Model
# =========================

class Telemetry(BaseModel):
    device_id: str
    timestamp: str
    cpu: float
    memory: float
    latency: float
    errors: int

# =========================
# API Endpoints
# =========================

@app.post("/telemetry")
def receive_telemetry(data: Telemetry):
    cursor.execute("""
    INSERT INTO telemetry (device_id, timestamp, cpu, memory, latency, errors)
    VALUES (?, ?, ?, ?, ?, ?)
    """, (
        data.device_id,
        data.timestamp,
        data.cpu,
        data.memory,
        data.latency,
        data.errors
    ))
    conn.commit()

    return {"status": "stored", "device": data.device_id}


@app.get("/telemetry")
def get_telemetry(limit: int = 50):
    cursor.execute("""
    SELECT device_id, timestamp, cpu, memory, latency, errors
    FROM telemetry
    ORDER BY id DESC
    LIMIT ?
    """, (limit,))
    
    rows = cursor.fetchall()

    return [
        {
            "device_id": r[0],
            "timestamp": r[1],
            "cpu": r[2],
            "memory": r[3],
            "latency": r[4],
            "errors": r[5]
        }
        for r in rows
    ]


@app.get("/predict/{device_id}")
def predict_device_failure(device_id: str):
    cursor.execute("""
    SELECT cpu, memory, latency, errors
    FROM telemetry
    WHERE device_id = ?
    ORDER BY id DESC
    LIMIT 5
    """, (device_id,))

    rows = cursor.fetchall()

    if len(rows) < 5:
        return {"device": device_id, "status": "Not enough data yet"}

    df = pd.DataFrame(rows, columns=["cpu", "memory", "latency", "errors"])

    # Feature Engineering (must match training)
    features = pd.DataFrame([{
        "cpu_avg": df["cpu"].mean(),
        "mem_avg": df["memory"].mean(),
        "lat_avg": df["latency"].mean(),
        "error_rate": df["errors"].mean()
    }])

    # Predict failure probability
    failure_prob = model.predict_proba(features)[0][1]

    # Risk Classification
    if failure_prob > 0.7:
        risk = "RED"
    elif failure_prob > 0.4:
        risk = "YELLOW"
    else:
        risk = "GREEN"

    return {
        "device": device_id,
        "failure_probability": round(float(failure_prob), 3),
        "risk_level": risk
    }
