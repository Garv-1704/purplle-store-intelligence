from ultralytics import YOLO

model = YOLO("yolov8n.pt")

results = model.track(
    source="data/CAM 1.mp4",
    tracker="bytetrack.yaml",
    save=True,
    persist=True
)

print("Tracking Complete")