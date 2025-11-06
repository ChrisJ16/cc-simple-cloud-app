from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import asyncio
from typing import List, Dict
from datetime import datetime, timezone

app = FastAPI()

# Allow all origins for CORS (development). For production set FRONTEND_URL and restrict origins.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


# In-memory message store. Each message is a dict. Background task will populate messages.
app.state.messages: List[Dict] = []


def _current_date_time():
    now = datetime.now(timezone.utc)
    return now.date().isoformat(), now.time().replace(microsecond=0).isoformat()


async def _generate_sensor_messages():
    """Background task that populates app.state.messages.

    Behavior:
    - Immediately append an initial status message: "Backend initialized, waiting for sensor data"
    - Then every 60 seconds append up to 10 sensor data messages
    """
    # Initial status message
    init_msg = {
        "type": "status",
        "message": "Backend initialized, waiting for sensor data",
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }
    app.state.messages.append(init_msg)

    # Deterministic sensor generation (no randomness)
    sensor_types = ["temperature", "humidity", "light"]
    sensor_ids = [f"S{i}" for i in range(1, 7)]

    # Generate 10 messages, 60 seconds apart
    for i in range(10):
        await asyncio.sleep(60)
        date_str, time_str = _current_date_time()
        sensor_type = sensor_types[i % len(sensor_types)]
        sensor_id = sensor_ids[i % len(sensor_ids)]
        # deterministic value in 1..100
        sensor_value = ((i * 17) % 100) + 1

        data_msg = {
            "type": "data",
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "date": date_str,
            "time": time_str,
            "sensor_id": sensor_id,
            "sensor_type": sensor_type,
            "sensor_value": sensor_value,
        }
        app.state.messages.append(data_msg)


@app.on_event("startup")
async def startup_event():
    # Start background task but don't await it so startup completes
    asyncio.create_task(_generate_sensor_messages())


@app.get("/api/data")
def get_data():
    """Return the most recent message (for compatibility with simple frontends).

    If no messages are present yet, return a friendly placeholder.
    """
    if not app.state.messages:
        return JSONResponse({"message": "No messages yet"})
    return app.state.messages[-1]


@app.get("/api/messages")
def get_messages():
    """Return the full list of produced messages (initial status + data messages)."""
    return app.state.messages
