import cv2
import numpy as np
import os
from ultralytics import YOLO

# =========================
# PATHS
# =========================
MODEL_PATH = r"C:\Users\anish\PycharmProjects\DeerDetectionProject\runs\detect\runs_deer\baseline_raw3\weights\best.pt"
IMAGE_PATH = r"C:\Users\anish\PycharmProjects\DeerDetectionProject\loc_0081_im_000387.jpg"
OUTPUT_DIR = r"C:\Users\anish\PycharmProjects\DeerDetectionProject\single_image_results"

os.makedirs(OUTPUT_DIR, exist_ok=True)

# =========================
# SETTINGS
# =========================
CLAHE_CLIP_LIMIT = 0.5
CLAHE_TILE_GRID = (8, 8)

GAMMA_VALUE = 1.1
CONF_THRESHOLD = 0.25

# Gaussian settings (light smoothing!)
GAUSSIAN_KERNEL = (3, 3)
GAUSSIAN_SIGMA = 0


# =========================
# FUNCTIONS
# =========================
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


def apply_gamma(image, gamma=1.6):
    inv_gamma = 1.0 / gamma
    table = np.array([
        ((i / 255.0) ** inv_gamma) * 255 for i in np.arange(256)
    ]).astype("uint8")
    return cv2.LUT(image, table)


def save_image(path, image):
    cv2.imwrite(path, image)


def run_inference(model, image_path, tag):
    print(f"\n--- Running inference on: {tag} ---")
    results = model.predict(
        source=image_path,
        conf=CONF_THRESHOLD,
        save=True,
        save_txt=True,
        save_conf=True,
        project=OUTPUT_DIR,
        name=tag,
        exist_ok=True,
        verbose=False
    )

    boxes = results[0].boxes
    if boxes is None or len(boxes) == 0:
        print(f"{tag}: No detections")
    else:
        print(f"{tag}: {len(boxes)} detection(s)")
        for i, box in enumerate(boxes):
            conf = float(box.conf[0])
            cls = int(box.cls[0])
            xyxy = box.xyxy[0].tolist()
            print(f"  Detection {i+1}: class={cls}, conf={conf:.4f}, box={xyxy}")


# =========================
# MAIN
# =========================
def main():
    model = YOLO(MODEL_PATH)

    image = cv2.imread(IMAGE_PATH)
    if image is None:
        raise FileNotFoundError(f"Could not read image: {IMAGE_PATH}")

    # 1. Raw
    raw_path = os.path.join(OUTPUT_DIR, "raw_input.jpg")
    save_image(raw_path, image)

    # 2. CLAHE
    clahe_img = apply_clahe(image)
    clahe_path = os.path.join(OUTPUT_DIR, "clahe_input.jpg")
    save_image(clahe_path, clahe_img)

    # 3. Gamma
    gamma_img = apply_gamma(image, GAMMA_VALUE)
    gamma_path = os.path.join(OUTPUT_DIR, "gamma_input.jpg")
    save_image(gamma_path, gamma_img)

    # 4. Gamma + CLAHE
    gamma_clahe_img = apply_clahe(gamma_img)
    gamma_clahe_path = os.path.join(OUTPUT_DIR, "gamma_clahe_input.jpg")
    save_image(gamma_clahe_path, gamma_clahe_img)

    # 🔥 5. Gaussian + CLAHE (NEW)
    gauss_img = apply_gaussian_blur(image)
    gauss_clahe_img = apply_clahe(gauss_img)
    gauss_clahe_path = os.path.join(OUTPUT_DIR, "gaussian_clahe_input.jpg")
    save_image(gauss_clahe_path, gauss_clahe_img)

    # 🔥 6. Gamma + Gaussian + CLAHE (NEW)
    gamma_gauss = apply_gamma(image, GAMMA_VALUE)
    gamma_gauss = apply_gaussian_blur(gamma_gauss)
    gamma_gauss_clahe = apply_clahe(gamma_gauss)
    gamma_gauss_clahe_path = os.path.join(OUTPUT_DIR, "gamma_gaussian_clahe_input.jpg")
    save_image(gamma_gauss_clahe_path, gamma_gauss_clahe)

    # Run inference
    run_inference(model, raw_path, "raw")
    run_inference(model, clahe_path, "clahe")
    run_inference(model, gamma_path, "gamma")
    run_inference(model, gamma_clahe_path, "gamma_clahe")
    run_inference(model, gauss_clahe_path, "gaussian_clahe")              # NEW
    run_inference(model, gamma_gauss_clahe_path, "gamma_gaussian_clahe")  # NEW

    print("\nDone. Check output folders in:")
    print(OUTPUT_DIR)


if __name__ == "__main__":
    main()