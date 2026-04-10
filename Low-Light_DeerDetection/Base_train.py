from ultralytics import YOLO


def main():
    model = YOLO("yolov8n.pt")

    model.train(
        data=r"C:\Users\anish\PycharmProjects\DeerDetectionProject\DeerImages_DarkRaw\data.yaml",
        epochs=10,
        imgsz=640,
        batch=8,
        project="runs_deer",
        name="dark_raw",
        pretrained=True,
        patience=10,
        save=True,
        plots=True
    )

    print("Dark RAW training complete.")


if __name__ == "__main__":
    main()