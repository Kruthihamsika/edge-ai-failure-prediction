import streamlit as st
import requests
import pandas as pd
import time

API_URL = "http://127.0.0.1:8000/telemetry"

st.set_page_config(page_title="Edge Device Health Monitor", layout="wide")

st.title("🧠 Edge Device Health Monitoring Dashboard")

placeholder = st.empty()

while True:
    try:
        response = requests.get(API_URL)
        data = response.json()

        if len(data) == 0:
            st.warning("No telemetry data available yet.")
        else:
            df = pd.DataFrame(data)

            df["timestamp"] = pd.to_datetime(df["timestamp"])

            with placeholder.container():
                st.subheader("📋 Latest Device Telemetry")
                st.dataframe(df, use_container_width=True)

                st.subheader("📊 Device Performance Trends")

                for device in df["device_id"].unique():
                    st.markdown(f"### Device {device}")
                    device_df = df[df["device_id"] == device]

                    st.line_chart(
                        device_df.set_index("timestamp")[["cpu", "memory", "latency"]]
                    )

                st.subheader("🚨 Error Counts")
                st.bar_chart(df.groupby("device_id")["errors"].sum())

    except Exception as e:
        st.error(f"Error fetching telemetry: {e}")

    time.sleep(5)
