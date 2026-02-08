# 🚀 Edge AI-Based Device Failure Prediction & Telemetry Monitoring System

## 📌 Overview

This project implements an end-to-end intelligent monitoring and failure prediction system for distributed edge and IoT devices. It continuously collects telemetry data, processes it in real time, and applies machine learning models to predict early signs of device failure before critical breakdowns occur.

The system focuses on reliability engineering rather than post-failure alerts, enabling proactive maintenance and system health assurance.

---

## 🎯 Objectives

- Collect real-time telemetry from simulated edge devices  
- Store and manage device health data in a structured database  
- Engineer meaningful features from raw system metrics  
- Train and deploy a machine learning model for failure risk prediction  
- Expose system functionality through REST APIs  
- Visualize device health and prediction results via a live dashboard  

---

## 🧠 System Architecture
Edge Devices (Simulator)
↓
FastAPI Backend (REST APIs)
↓
Telemetry Database (SQLite)
↓
ML Prediction Engine (Scikit-learn)
↓
Dashboard (Visualization Layer)




---

## 🔄 Workflow

1. Telemetry Generation  
   Simulated devices generate system metrics including CPU usage, memory usage, network latency, and error counts.

2. Data Ingestion  
   Telemetry is transmitted to the backend using HTTP POST requests.

3. Storage  
   Incoming data is stored in a structured SQLite database for persistence and analysis.

4. Feature Engineering  
   Raw metrics are transformed into predictive signals such as load stress indicators and error density.

5. Model Training & Inference  
   A classification model is trained to predict failure risk and deployed to serve predictions through an API.

6. Visualization  
   A dashboard displays real-time telemetry and device risk levels.

---

## 🤖 Machine Learning Approach

- Problem Type: Binary Classification  
  - 0 → Normal Operation  
  - 1 → High Failure Risk  

- Features:
  - CPU utilization (%)
  - Memory utilization (%)
  - Network latency (ms)
  - Error frequency
  - Engineered stress indicators

- Model Pipeline:
  - Data preprocessing
  - Feature engineering
  - Model training using Scikit-learn
  - Evaluation using precision, recall, and F1-score
  - Model persistence using Joblib

---

## 🌐 API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | /telemetry | Ingest telemetry data |
| GET | /telemetry | Retrieve recent telemetry records |
| GET | /predict/{device_id} | Predict failure risk for a device |
| GET | /docs | Interactive API documentation |

---

## 📊 Sample Prediction Output

```json
{
  "device": "device_id",
  "failure_probability": 0.87,
  "risk_level": "RED"
}





