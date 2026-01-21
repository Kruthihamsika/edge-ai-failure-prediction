import sqlite3
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
import joblib

DB_PATH = "../backend/telemetry.db"

print("Loading telemetry data...")

conn = sqlite3.connect(DB_PATH)
df = pd.read_sql_query("SELECT * FROM telemetry", conn)
conn.close()

print("Rows loaded:", len(df))

# Convert timestamp
df["timestamp"] = pd.to_datetime(df["timestamp"])

# Sort by device and time
df = df.sort_values(["device_id", "timestamp"])

# Feature Engineering
print("Engineering features...")

# Rolling windows per device
df["cpu_avg"] = df.groupby("device_id")["cpu"].transform(lambda x: x.rolling(5, min_periods=1).mean())
df["mem_avg"] = df.groupby("device_id")["memory"].transform(lambda x: x.rolling(5, min_periods=1).mean())
df["lat_avg"] = df.groupby("device_id")["latency"].transform(lambda x: x.rolling(5, min_periods=1).mean())
df["error_rate"] = df.groupby("device_id")["errors"].transform(lambda x: x.rolling(5, min_periods=1).mean())

# Failure label (define your own logic here)
# Failure if system is under stress
df["failure"] = (
    (df["cpu_avg"] > 80) |
    (df["mem_avg"] > 80) |
    (df["lat_avg"] > 300) |
    (df["error_rate"] > 5)
).astype(int)

features = ["cpu_avg", "mem_avg", "lat_avg", "error_rate"]
X = df[features]
y = df["failure"]

# Train/Test split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=42)

print("Training model...")
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

print("\nEvaluation:")
y_pred = model.predict(X_test)
print(classification_report(y_test, y_pred))

# Save model
joblib.dump(model, "failure_model.pkl")
print("\nModel saved as failure_model.pkl")
