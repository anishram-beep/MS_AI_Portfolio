import cv2
import shutil
import numpy as np
from pathlib import Path
from ultralytics import YOLO

MODEL_PATH = r"C:\Users\anish\PycharmProjects\DeerDetectionProject\runs\detect\runs_deer\baseline_raw3\weights\best.pt"

SOURCE_DATASET = Path(r"C:\Users\anish\PycharmProjects\DeerDetectionProject\DeerImages")
SOURCE_SPLIT = "valid"

FAILED_RAW_DATASET = Path(r"C:\Users\anish\PycharmProjects\DeerDetectionProject\DeerImages_FailedRawOnly")
FAILED_ADAPTIVE_DATASET = Path(r"C:\Users\anish\PycharmProjects\DeerDetectionProject\DeerImages_FailedAdaptiveOnly")

IMPROVED_RAW_DIR = Path(r"C:\Users\anish\PycharmProjects\DeerDetectionProject\improved_cases\raw")
IMPROVED_ADAPTIVE_DIR = Path(r"C:\Users\anish\PycharmProjects\DeerDetectionProject\improved_cases\adaptive")

DARK_THRESHOLD = 90.0
UNEVEN_ILLUM_THRESHOLD = 40.0
IOU_FAILURE_THRESHOLD = 0.50

CLAHE_CLIP_LIMIT = 0.3
CLAHE_TILE_GRID = (8, 8)
GAMMA_VALUE = 1

GAUSSIAN_KERNEL = (3, 3)
GAUSSIAN_SIGMA = 0

IMAGE_EXTS = {".jpg", ".jpeg", ".png", ".bmp"}


def brightness_score(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    return float(gray.mean())


def uneven_illumination_score(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    small = cv2.resize(gray, (256, 256), interpolation=cv2.INTER_AREA).astype(np.float32)
    illumination = cv2.GaussianBlur(small, (51, 51), 0)
    return float(np.std(illumination))


def classify_image_condition(image):
    b = brightness_score(image)
    u = uneven_illumination_score(image)

    if b < DARK_THRESHOLD:
        return "dark", b, u
    if u > UNEVEN_ILLUM_THRESHOLD:
        return "uneven", b, u
    return "normal", b, u


def apply_gaussian_blur(image):
    return cv2.GaussianBlur(image, GAUSSIAN_KERNEL, GAUSSIAN_SIGMA)


def apply_clahe(image):
    lab = cv2.cvtColor(image, cv2.COLOR_BGR2LAB)
    l, a, b = cv2.split(lab)

    clahe = cv2.createCLAHE(
        clipLimit=CLAHE_CLIP_LIMIT,
        tileGridSize=CLAHE_TILE_GRID
    )

    l_clahe = clahe.apply(l)
    merged = cv2.merge((l_clahe, a, b))
    return cv2.cvtColor(merged, cv2.COLOR_LAB2BGR)


def apply_gamma(image, gamma=1.15):
    inv_gamma = 1.0 / gamma
    table = np.array([
        ((i / 255.0) ** inv_gamma) * 255 for i in np.arange(256)
    ]).astype("uint8")
    return cv2.LUT(image, table)


def adaptive_preprocess(image):
    condition, b, u = classify_image_condition(image)

    processed = apply_gamma(image, GAMMA_VALUE)
    processed = apply_gaussian_blur(processed)
    processed = apply_clahe(processed)

    if condition == "dark":
        method = "gamma_gaussian_clahe_dark"
    elif condition == "uneven":
        method = "gamma_gaussian_clahe_uneven"
    else:
        method = "gamma_gaussian_clahe"

    return processed, condition, method, b, u


def reset_dir(path):
    if path.exists():
        shutil.rmtree(path)
    path.mkdir(parents=True, exist_ok=True)


def make_yolo_dirs(base):
    (base / "images").mkdir(parents=True, exist_ok=True)
    (base / "labels").mkdir(parents=True, exist_ok=True)


def write_data_yaml(dataset_dir):
    yaml_text = f"""path: {dataset_dir.as_posix()}
train: images
val: images
test: images

nc: 1
names: ['Deer']
"""
    with open(dataset_dir / "data.yaml", "w", encoding="utf-8") as f:
        f.write(yaml_text)


def yolo_label_to_xyxy(label_path, image_shape):
    h, w = image_shape[:2]
    gt_boxes = []

    with open(label_path, "r") as f:
        for line in f:
            parts = line.strip().split()
            if len(parts) < 5:
                continue

            _, x_center, y_center, bw, bh = map(float, parts[:5])

            x_center *= w
            y_center *= h
            bw *= w
            bh *= h

            x1 = x_center - bw / 2
            y1 = y_center - bh / 2
            x2 = x_center + bw / 2
            y2 = y_center + bh / 2

            gt_boxes.append([x1, y1, x2, y2])

    return gt_boxes


def compute_iou(box_a, box_b):
    ax1, ay1, ax2, ay2 = box_a
    bx1, by1, bx2, by2 = box_b

    inter_x1 = max(ax1, bx1)
    inter_y1 = max(ay1, by1)
    inter_x2 = min(ax2, bx2)
    inter_y2 = min(ay2, by2)

    inter_w = max(0, inter_x2 - inter_x1)
    inter_h = max(0, inter_y2 - inter_y1)
    inter_area = inter_w * inter_h

    area_a = max(0, ax2 - ax1) * max(0, ay2 - ay1)
    area_b = max(0, bx2 - bx1) * max(0, by2 - by1)

    union = area_a + area_b - inter_area

    if union <= 0:
        return 0.0

    return inter_area / union


def detection_status_iou(model, img_path, label_path, image):
    gt_boxes = yolo_label_to_xyxy(label_path, image.shape)

    results = model.predict(
        source=str(img_path),
        conf=0.25,
        verbose=False
    )

    pred_boxes = results[0].boxes

    if pred_boxes is None or len(pred_boxes) == 0:
        return "no_detection", 0.0, 0.0

    best_iou = 0.0
    best_conf = 0.0

    for pred in pred_boxes:
        pred_xyxy = pred.xyxy[0].cpu().numpy().tolist()
        pred_conf = float(pred.conf[0])

        for gt in gt_boxes:
            iou = compute_iou(pred_xyxy, gt)
            if iou > best_iou:
                best_iou = iou
                best_conf = pred_conf

    if best_iou < IOU_FAILURE_THRESHOLD:
        return "bad_iou", best_conf, best_iou

    return "good_detection", best_conf, best_iou


def build_failed_only_datasets():
    model = YOLO(MODEL_PATH)

    src_images = SOURCE_DATASET / SOURCE_SPLIT / "images"
    src_labels = SOURCE_DATASET / SOURCE_SPLIT / "labels"

    reset_dir(FAILED_RAW_DATASET)
    reset_dir(FAILED_ADAPTIVE_DATASET)
    reset_dir(IMPROVED_RAW_DIR)
    reset_dir(IMPROVED_ADAPTIVE_DIR)

    make_yolo_dirs(FAILED_RAW_DATASET)
    make_yolo_dirs(FAILED_ADAPTIVE_DATASET)

    log_rows = []
    kept = 0
    improved = 0

    for idx, img_path in enumerate(src_images.iterdir()):
        if idx % 25 == 0:
            print(f"Scanning image {idx}: {img_path.name}", flush=True)

        if img_path.suffix.lower() not in IMAGE_EXTS:
            continue

        label_path = src_labels / f"{img_path.stem}.txt"
        if not label_path.exists():
            continue

        image = cv2.imread(str(img_path))
        if image is None:
            continue

        condition, b, u = classify_image_condition(image)

        if condition not in {"dark", "uneven"}:
            continue

        raw_status, raw_conf, raw_iou = detection_status_iou(
            model,
            img_path,
            label_path,
            image
        )

        if raw_status not in {"no_detection", "bad_iou"}:
            continue

        shutil.copy2(img_path, FAILED_RAW_DATASET / "images" / img_path.name)
        shutil.copy2(label_path, FAILED_RAW_DATASET / "labels" / label_path.name)

        processed, condition, method, b, u = adaptive_preprocess(image)
        adaptive_img_path = FAILED_ADAPTIVE_DATASET / "images" / img_path.name
        cv2.imwrite(str(adaptive_img_path), processed)
        shutil.copy2(label_path, FAILED_ADAPTIVE_DATASET / "labels" / label_path.name)

        adaptive_status, adaptive_conf, adaptive_iou = detection_status_iou(
            model,
            adaptive_img_path,
            label_path,
            processed
        )

        if adaptive_iou > raw_iou or (
            raw_status == "no_detection" and adaptive_status != "no_detection"
        ):
            shutil.copy2(img_path, IMPROVED_RAW_DIR / img_path.name)
            cv2.imwrite(str(IMPROVED_ADAPTIVE_DIR / img_path.name), processed)
            improved += 1

        log_rows.append(
            f"{img_path.name},{condition},{method},"
            f"{raw_status},{raw_conf:.4f},{raw_iou:.4f},"
            f"{adaptive_status},{adaptive_conf:.4f},{adaptive_iou:.4f},"
            f"{b:.2f},{u:.2f}"
        )
        kept += 1

    write_data_yaml(FAILED_RAW_DATASET)
    write_data_yaml(FAILED_ADAPTIVE_DATASET)

    with open(FAILED_ADAPTIVE_DATASET / "failed_only_log.csv", "w", encoding="utf-8") as f:
        f.write(
            "filename,condition,method,"
            "raw_status,raw_conf,raw_iou,"
            "adaptive_status,adaptive_conf,adaptive_iou,"
            "brightness,uneven_score\n"
        )
        f.write("\n".join(log_rows))

    print(f"\nCreated true failed-only dataset with {kept} images.")
    print(f"Improved/flipped cases saved: {improved}")
    print(f"Raw failed dataset: {FAILED_RAW_DATASET}")
    print(f"Adaptive failed dataset: {FAILED_ADAPTIVE_DATASET}")
    print(f"Improved raw cases: {IMPROVED_RAW_DIR}")
    print(f"Improved adaptive cases: {IMPROVED_ADAPTIVE_DIR}")


def extract_metrics(m):
    return {
        "mAP50": float(m.box.map50),
        "mAP50-95": float(m.box.map),
        "precision": float(m.box.mp),
        "recall": float(m.box.mr)
    }


def save_metrics(raw_metrics, adaptive_metrics, txt_path, csv_path):
    raw = extract_metrics(raw_metrics)
    adaptive = extract_metrics(adaptive_metrics)

    with open(txt_path, "w") as f:
        f.write("===== TRUE FAILED-ONLY RAW VS ADAPTIVE RESULTS =====\n\n")

        f.write("FAILED RAW DATASET:\n")
        for k, v in raw.items():
            f.write(f"{k}: {v:.4f}\n")

        f.write("\nFAILED ADAPTIVE DATASET:\n")
        for k, v in adaptive.items():
            f.write(f"{k}: {v:.4f}\n")

        f.write("\nDIFFERENCE (Adaptive - Raw):\n")
        for k in raw:
            diff = adaptive[k] - raw[k]
            f.write(f"{k}: {diff:+.4f}\n")

    with open(csv_path, "w") as f:
        f.write("metric,raw_failed,adaptive_failed,difference\n")
        for k in raw:
            diff = adaptive[k] - raw[k]
            f.write(f"{k},{raw[k]},{adaptive[k]},{diff}\n")

    print(f"\nSaved metrics to {txt_path} and {csv_path}")


def evaluate_failed_only():
    model = YOLO(MODEL_PATH)

    print("\nEvaluating TRUE FAILED RAW dataset...")
    raw_metrics = model.val(
        data=str(FAILED_RAW_DATASET / "data.yaml"),
        split="test",
        project="runs_deer_eval",
        name="true_failed_raw_eval",
        exist_ok=True
    )

    print("\nEvaluating TRUE FAILED ADAPTIVE dataset...")
    adaptive_metrics = model.val(
        data=str(FAILED_ADAPTIVE_DATASET / "data.yaml"),
        split="test",
        project="runs_deer_eval",
        name="true_failed_adaptive_eval",
        exist_ok=True
    )

    print("\nCreating TRUE FAILED RAW visual detections...")
    model.predict(
        source=str(FAILED_RAW_DATASET / "images"),
        conf=0.25,
        save=True,
        save_txt=True,
        save_conf=True,
        project="runs_deer_visuals",
        name="true_failed_raw_predictions",
        exist_ok=True
    )

    print("\nCreating TRUE FAILED ADAPTIVE visual detections...")
    model.predict(
        source=str(FAILED_ADAPTIVE_DATASET / "images"),
        conf=0.25,
        save=True,
        save_txt=True,
        save_conf=True,
        project="runs_deer_visuals",
        name="true_failed_adaptive_predictions",
        exist_ok=True
    )

    save_metrics(
        raw_metrics,
        adaptive_metrics,
        "true_failed_only_results.txt",
        "true_failed_only_results.csv"
    )


def main():
    build_failed_only_datasets()
    evaluate_failed_only()
    print("\nAll done.")


if __name__ == "__main__":
    main()