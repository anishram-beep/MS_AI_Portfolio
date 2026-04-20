import cv2
import numpy as np
import os
from ultralytics import YOLO

# =========================
# PATHS
# =========================
MODEL_PATH = r"C:\Users\anish\PycharmProjects\DeerDetectionProject\runs\detect\runs_deer\baseline_raw3\weights\best.pt"
IMAGE_PATH = r"C:\Users\anish\PycharmProjects\DeerDetectionProject\loc_0004_im_002082.jpg"   # <-- change if needed
OUTPUT_DIR = r"C:\Users\anish\PycharmProjects\DeerDetectionProject\single_image_results_test4"


os.makedirs(OUTPUT_DIR, exist_ok=False)

# =========================
# SETTINGS
# =========================
CONF_THRESHOLD = 0.25

CLAHE_CLIP_LIMIT = 0.8
CLAHE_TILE_GRID = (8, 8)

GAMMA_VALUE = 1.15

GAUSSIAN_KERNEL = (3, 3)
GAUSSIAN_SIGMA = 0

# Retinex tuning
RETINEX_SIGMA = 20
RETINEX_GAIN = 128.0
RETINEX_OFFSET = 128.0

# Resize large image for faster inference if needed
RESIZE_FOR_TEST = False
RESIZE_WIDTH = 1280
RESIZE_HEIGHT = 720


# =========================
# PREPROCESSING FUNCTIONS
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


def apply_gamma(image, gamma=1.15):
    inv_gamma = 1.0 / gamma
    table = np.array([
        ((i / 255.0) ** inv_gamma) * 255 for i in np.arange(256)
    ]).astype("uint8")
    return cv2.LUT(image, table)


def apply_retinex_ssr(image, sigma=20, gain=128.0, offset=128.0):
    """
    Single Scale Retinex on the LAB lightness channel.
    This is more stable than the previous washed-out grayscale version.
    """
    lab = cv2.cvtColor(image, cv2.COLOR_BGR2LAB)
    l, a, b = cv2.split(lab)

    l_float = l.astype(np.float32) + 1.0
    blur = cv2.GaussianBlur(l_float, (0, 0), sigma)

    retinex = np.log(l_float) - np.log(blur + 1.0)

    # Controlled scaling instead of full normalize
    retinex = gain * retinex + offset
    retinex = np.clip(retinex, 0, 255).astype(np.uint8)

    merged = cv2.merge((retinex, a, b))
    return cv2.cvtColor(merged, cv2.COLOR_LAB2BGR)


def save_image(path, image):
    ok = cv2.imwrite(path, image)
    print(f"Saved {path}: {ok}", flush=True)


# =========================
# INFERENCE
# =========================
def run_inference(model, image_path, tag):
    print(f"\n--- Running inference on: {tag} ---", flush=True)

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
        print(f"{tag}: No detections", flush=True)
    else:
        print(f"{tag}: {len(boxes)} detection(s)", flush=True)
        for i, box in enumerate(boxes):
            conf = float(box.conf[0])
            cls = int(box.cls[0])
            xyxy = box.xyxy[0].tolist()
            print(
                f"  Detection {i+1}: class={cls}, conf={conf:.4f}, box={xyxy}",
                flush=True
            )


# =========================
# MAIN
# =========================
def main():
    print("Starting test4.py", flush=True)

    if not os.path.exists(MODEL_PATH):
        raise FileNotFoundError(f"Model not found: {MODEL_PATH}")

    if not os.path.exists(IMAGE_PATH):
        raise FileNotFoundError(f"Image not found: {IMAGE_PATH}")

    print("Loading model...", flush=True)
    model = YOLO(MODEL_PATH)
    print("Model loaded.", flush=True)

    print("Reading image...", flush=True)
    image = cv2.imread(IMAGE_PATH)
    if image is None:
        raise FileNotFoundError(f"Could not read image: {IMAGE_PATH}")

    print(f"Original shape: {image.shape}", flush=True)

    if RESIZE_FOR_TEST:
        image = cv2.resize(image, (RESIZE_WIDTH, RESIZE_HEIGHT))
        print(f"Resized shape: {image.shape}", flush=True)

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

    # 4. Gamma + Gaussian + CLAHE
    gamma_gauss_img = apply_gamma(image, GAMMA_VALUE)
    gamma_gauss_img = apply_gaussian_blur(gamma_gauss_img)
    gamma_gauss_clahe_img = apply_clahe(gamma_gauss_img)
    gamma_gauss_clahe_path = os.path.join(OUTPUT_DIR, "gamma_gaussian_clahe_input.jpg")
    save_image(gamma_gauss_clahe_path, gamma_gauss_clahe_img)

    # 5. Retinex
    retinex_img = apply_retinex_ssr(
        image,
        sigma=RETINEX_SIGMA,
        gain=RETINEX_GAIN,
        offset=RETINEX_OFFSET
    )
    retinex_path = os.path.join(OUTPUT_DIR, "retinex_input.jpg")
    save_image(retinex_path, retinex_img)

    # 6. Retinex + CLAHE
    retinex_clahe_img = apply_clahe(retinex_img)
    retinex_clahe_path = os.path.join(OUTPUT_DIR, "retinex_clahe_input.jpg")
    save_image(retinex_clahe_path, retinex_clahe_img)

    # 7. Gamma + Retinex
    gamma_retinex_img = apply_gamma(image, GAMMA_VALUE)
    gamma_retinex_img = apply_retinex_ssr(
        gamma_retinex_img,
        sigma=RETINEX_SIGMA,
        gain=RETINEX_GAIN,
        offset=RETINEX_OFFSET
    )
    gamma_retinex_path = os.path.join(OUTPUT_DIR, "gamma_retinex_input.jpg")
    save_image(gamma_retinex_path, gamma_retinex_img)

    # Optional: Gaussian + Retinex
    gauss_retinex_img = apply_gaussian_blur(image)
    gauss_retinex_img = apply_retinex_ssr(
        gauss_retinex_img,
        sigma=RETINEX_SIGMA,
        gain=RETINEX_GAIN,
        offset=RETINEX_OFFSET
    )
    gauss_retinex_path = os.path.join(OUTPUT_DIR, "gaussian_retinex_input.jpg")
    save_image(gauss_retinex_path, gauss_retinex_img)

    # Run inference on all versions
    run_inference(model, raw_path, "raw")
    run_inference(model, clahe_path, "clahe")
    run_inference(model, gamma_path, "gamma")
    run_inference(model, gamma_gauss_clahe_path, "gamma_gaussian_clahe")
    run_inference(model, retinex_path, "retinex")
    run_inference(model, retinex_clahe_path, "retinex_clahe")
    run_inference(model, gamma_retinex_path, "gamma_retinex")
    run_inference(model, gauss_retinex_path, "gaussian_retinex")

    print("\nDone. Check outputs here:", flush=True)
    print(OUTPUT_DIR, flush=True)


if __name__ == "__main__":
    main()