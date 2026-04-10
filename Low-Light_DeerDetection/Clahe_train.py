from ultralytics import YOLO


def main():
    model = YOLO("yolov8n.pt")

    model.train(
        data=r"C:\Users\anish\PycharmProjects\DeerDetectionProject\DeerImages_DarkCLAHE\data.yaml",
        epochs=10,
        imgsz=640,
        batch=8,
        project="runs_deer",
        name="dark_clahe",
        pretrained=True,
        patience=10,
        save=True,
        plots=True
    )

    print("Dark CLAHE training complete.")


if __name__ == "__main__":
    main()