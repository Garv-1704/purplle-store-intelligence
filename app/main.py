from fastapi import FastAPI
import json

app = FastAPI()

@app.get("/")
def home():
    return {"status": "running"}

@app.get("/metrics")
def metrics():

    entries = 0
    exits = 0

    try:
        with open("events.jsonl", "r") as f:
            for line in f:

                event = json.loads(line)

                if event["event_type"] == "ENTRY":
                    entries += 1

                if event["event_type"] == "EXIT":
                    exits += 1

    except FileNotFoundError:
        pass

    return {
        "total_entries": entries,
        "total_exits": exits,
        "active_visitors": entries - exits
    }