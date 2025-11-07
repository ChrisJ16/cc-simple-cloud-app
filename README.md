# Simple Sensor Messaging App

This small project demonstrates a backend that generates a short sequence of deterministic sensor messages and a Streamlit frontend that polls and displays them.

Description
- Backend (FastAPI): on startup it emits an initial status message "Backend initialized, waiting for sensor data" and then generates up to 10 deterministic sensor messages at 60-second intervals. Messages include date, time, sensor_id (S1..S6), sensor_type (temperature, humidity, light) and sensor_value (1-100).
- Frontend (Streamlit): polls the backend `/api/messages` endpoint, displays the initial status in a textbox labeled "Backend status:", and appends sensor data rows to a table. Polling stops after 10 data messages.

Quick local build & run

Prerequisites: Python 3.8+ (3.11 recommended), pip

1) Create and activate a virtual environment (PowerShell):

```wsl
python -m venv .venv; .venv\Scripts\Activate.ps1
```

2) Install backend dependencies and run the API (from repo root):

```wsl
pip install fastapi uvicorn pandas
uvicorn backend.main:app --reload --port 8000
```

3) Run the Streamlit frontend (in another shell):

```wsl
pip install streamlit requests pandas
streamlit run frontend/app.py
```

Behavior notes
- When the backend starts it immediately appends the initial status message. The frontend will display this status right away and then begin showing sensor data every 60 seconds.
- For faster local testing: edit `backend/main.py` and change `await asyncio.sleep(60)` to a lower value (e.g., 2 or 5 seconds). Remember to change back to 60s for the final demo.
- The backend uses in-memory storage; restarting the backend clears messages. For persistence, add a database or cache.

Endpoints
- `GET /api/data` — returns the most recent message
- `GET /api/messages` — returns an array of messages (first is status, then data)

Example data message:

```json
{
  "type": "data",
  "timestamp": "2025-11-06T12:00:00+00:00",
  "date": "2025-11-06",
  "time": "12:00:00",
  "sensor_id": "S1",
  "sensor_type": "temperature",
  "sensor_value": 25
}
```

# System diagram

![alt text](/diagrams/assigment1_diagram.png "System diagram")