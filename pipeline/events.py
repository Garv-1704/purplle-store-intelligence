from ultralytics import YOLO
import json
import sys
from datetime import datetime

# Usage:
# python pipeline/events.py "CAM 1"

CAMERA = sys.argv[1]

CAMERA_CONFIG = {
    "CAM 1": 1200,
    "CAM 2": 1070,
    "CAM 3": 1620,
    "CAM 4": 1000,
    "CAM 5": 1100
}

ENTRY_LINE_X = CAMERA_CONFIG[CAMERA]

model = YOLO("yolov8n.pt")

results = model.track(
    source=f"data/{CAMERA}.mp4",
    tracker="bytetrack.yaml",
    persist=True,
    stream=True
)

BUFFER = 5

LEFT_ZONE = ENTRY_LINE_X - BUFFER
RIGHT_ZONE = ENTRY_LINE_X + BUFFER

last_position = {}
last_event = {}
last_event_time = {}

COOLDOWN_SECONDS = 10

for result in results:

    if result.boxes.id is None:
        continue

    boxes = result.boxes.xyxy.cpu().numpy()
    ids = result.boxes.id.cpu().numpy()

    for box, track_id in zip(boxes, ids):

        x1, y1, x2, y2 = box

        center_x = (x1 + x2) / 2
        center_y = (y1 + y2) / 2

        print(
            f"Track {int(track_id)} "
            f"x={center_x:.1f} "
            f"y={center_y:.1f}"
        )

        previous_x = last_position.get(track_id)

        if previous_x is not None:
            if abs(center_x - previous_x) > 20:
                print(
                    f"CROSSING CANDIDATE -> Track {int(track_id)} "
                    f"prev={previous_x:.1f} current={center_x:.1f}"
                )

        print(
            f"Track {int(track_id)} "
            f"prev={previous_x} current={center_x}"
        )

        if previous_x is not None:

            now = datetime.now()

            last_time = last_event_time.get(track_id)

            cooldown_ok = (
                last_time is None or
                (now - last_time).total_seconds() > COOLDOWN_SECONDS
            )

            # ENTRY
            if (
                previous_x > RIGHT_ZONE and
                center_x < LEFT_ZONE and
                last_event.get(track_id) != "ENTRY" and
                cooldown_ok
            ):

                event = {
                    "visitor_id": f"VIS_{int(track_id)}",
                    "event_type": "ENTRY",
                    "camera": CAMERA.replace(" ", "_"),
                    "timestamp": now.isoformat()
                }

                print(event)

                with open("events.jsonl", "a") as f:
                    f.write(json.dumps(event) + "\n")

                last_event[track_id] = "ENTRY"
                last_event_time[track_id] = now

            # EXIT
            elif (
                previous_x < LEFT_ZONE and
                center_x > RIGHT_ZONE and
                last_event.get(track_id) != "EXIT" and
                cooldown_ok
            ):

                event = {
                    "visitor_id": f"VIS_{int(track_id)}",
                    "event_type": "EXIT",
                    "camera": CAMERA.replace(" ", "_"),
                    "timestamp": now.isoformat()
                }

                print(event)

                with open("events.jsonl", "a") as f:
                    f.write(json.dumps(event) + "\n")

                last_event[track_id] = "EXIT"
                last_event_time[track_id] = now

        last_position[track_id] = center_x