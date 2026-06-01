from ultralytics import YOLO

model = YOLO("yolov8n.pt")

cameras = [
    "CAM 1",
    "CAM 2",
    "CAM 3",
    "CAM 4",
    "CAM 5"
]

for camera in cameras:

    print(f"\nProcessing {camera}...")

    model.track(
        source=f"data/{camera}.mp4",
        tracker="bytetrack.yaml",
        save=True,
        persist=True
    )

print("\nAll cameras processed successfully!")