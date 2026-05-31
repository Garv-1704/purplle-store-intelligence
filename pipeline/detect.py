from ultralytics import YOLO

model = YOLO("yolov8n.pt")

results = model(
    source="data/CAM 1.mp4",
    save=True,
    conf=0.3
)

print("Detection Complete")