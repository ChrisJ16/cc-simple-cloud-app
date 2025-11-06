import streamlit as st
import requests
import time
import pandas as pd

st.title("Frontend Streamlit - Sensor Data Viewer")

# This should point to your backend API (the /api/data path or base that includes /api)
backend_url = "https://backendcloudcomputing-a4f4c6cvdcdsghaf.norwayeast-01.azurewebsites.net/api/data"


def _messages_url_from_backend(backend_api_url: str) -> str:
    # If the provided URL ends with /api/data, replace with /api/messages
    if backend_api_url.endswith("/api/data"):
        return backend_api_url[:-len("/api/data")] + "/api/messages"
    # otherwise append /messages
    return backend_api_url.rstrip("/") + "/messages"


messages_url = _messages_url_from_backend(backend_url)

st.write(f"Polling backend messages at: {messages_url}")

# Placeholders for UI
status_placeholder = st.empty()
table_placeholder = st.empty()
info_placeholder = st.empty()

# Polling loop: check for messages repeatedly until 10 data messages have been received
prev_count = 0
max_wait_seconds = 11 * 60  # small safety cap (initial + 10 messages at 60s -> ~11 minutes)
start_time = time.time()

while True:
    try:
        resp = requests.get(messages_url, timeout=10)
        resp.raise_for_status()
        msgs = resp.json()
    except Exception as e:
        status_placeholder.error(f"The backend couldn't be reached: {e}")
        # retry after short sleep
        time.sleep(2)
        if time.time() - start_time > 30:
            info_placeholder.info("Still attempting to reach the backend; waiting...")
        continue

    if not isinstance(msgs, list) or len(msgs) == 0:
        status_placeholder.info("No messages available yet from backend.")
        time.sleep(2)
        continue

    # initial status is expected to be the first message of type 'status'
    init_msg = next((m for m in msgs if m.get("type") == "status"), None)
    if init_msg:
        status_placeholder.text_area("Backend status:", value=init_msg.get("message", ""), height=50)
    else:
        status_placeholder.text_area("Backend status:", value="(no status message yet)", height=50)

    # build table of data messages
    data_msgs = [m for m in msgs if m.get("type") == "data"]
    if data_msgs:
        df = pd.DataFrame(data_msgs)
        # show only the columns we expect, in order
        cols = ["date", "time", "sensor_id", "sensor_type", "sensor_value"]
        for c in cols:
            if c not in df.columns:
                df[c] = ""
        table_placeholder.table(df[cols])
    else:
        table_placeholder.info("Waiting for sensor data messages...")

    # If we have new messages, update info
    if len(msgs) != prev_count:
        info_placeholder.info(f"Received {len(data_msgs)} data messages (total messages: {len(msgs)})")
        prev_count = len(msgs)

    # stop when we have 10 data messages
    if len(data_msgs) >= 10:
        info_placeholder.success("Received maximum 10 sensor messages — stopping polling.")
        break

    # safety stop
    if time.time() - start_time > max_wait_seconds:
        info_placeholder.warning("Reached max wait time; stopping polling.")
        break

    # poll every 10 seconds (frontend polls faster than backend's 60s interval)
    time.sleep(10)
