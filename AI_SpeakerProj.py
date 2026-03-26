import pandas as pd
import numpy as np
from sklearn.gaussian_process import GaussianProcessRegressor
from sklearn.gaussian_process.kernels import RBF, WhiteKernel, ConstantKernel
import glob
import os

# ===========================================================
# 1. FUNCTION — LOAD SINGLE SPECTRUM TXT FILE
# ===========================================================
def load_spectrum_txt(file_path):
    """
    Loads a spectrum TXT exported from Audacity Plot Spectrum.
    Format:
    Frequency(Hz) <tab> Level(dB)
    """
    df = pd.read_csv(file_path, sep="\t", skiprows=1, names=["Frequency", "Level"])
    df = df.dropna()
    return df

import numpy as np

def compute_harman_score(df):
    """
    PURE Harman-style weighted MSE deviation score.
    Higher = better (we return negative deviation).
    """

    freq = df["Frequency"].values.astype(float)
    level = df["Level"].values.astype(float)

    # ================================
    # 1. BAND LIMIT: 100–10,000 Hz
    # ================================
    band = (freq >= 100) & (freq <= 10000)
    freq = freq[band]
    level = level[band]

    # ================================
    # 2. Smooth: ~1/6-oct smoothing
    # ================================
    # Window length based on your measured spacing (~20–30 points)
    window_size = 9
    kernel = np.ones(window_size) / window_size
    level_smooth = np.convolve(level, kernel, mode="same")

    # ================================
    # 3. Fit Harman target slope
    #    Target = m * log10(freq) + b
    # ================================
    x = np.log10(freq)
    A = np.vstack([x, np.ones_like(x)]).T
    m, b = np.linalg.lstsq(A, level_smooth, rcond=None)[0]

    target = m * x + b      # Ideal slope
    deviation = level_smooth - target

    # ================================
    # 4. Weighting (Harman / Toole):
    #    Midrange: 2–6 kHz = x2 weight
    # ================================
    weights = np.ones_like(freq)
    mid = (freq >= 2000) & (freq <= 6000)
    weights[mid] *= 2.0

    # ================================
    # 5. Weighted MSE deviation
    # ================================
    weighted_mse = np.mean(weights * (deviation ** 2))

    # ================================
    # 6. Score (negative so higher=better)
    # ================================
    score = -weighted_mse
    return score

def compute_bright_score(df):
    """
    Bright / detail mode:
    - Still anchored to a Harman-like slope
    - Less strict about smoothness
    - Rewards a moderate HF boost (4–10 kHz) vs midband
    Higher = better.
    """
    freq = df["Frequency"].values.astype(float)
    level = df["Level"].values.astype(float)

    # 1) Work in 100–10,000 Hz like before
    band = (freq >= 100) & (freq <= 10000)
    freq = freq[band]
    level = level[band]

    # 2) Light smoothing (~1/6 octave)
    window_size = 9
    kernel = np.ones(window_size) / window_size
    level_smooth = np.convolve(level, kernel, mode="same")

    # 3) Fit a simple downward target slope (Harman-like)
    x = np.log10(freq)
    A = np.vstack([x, np.ones_like(x)]).T
    m, b = np.linalg.lstsq(A, level_smooth, rcond=None)[0]
    target = m * x + b
    deviation = level_smooth - target

    # 4) Weighted MSE for "overall sanity"
    #    Midrange still matters, but less than in neutral mode
    weights = np.ones_like(freq)
    mid = (freq >= 2000) & (freq <= 6000)
    weights[mid] *= 1.5   # was 2.0 in neutral; now more relaxed

    mse = np.mean(weights * (deviation ** 2))

    # 5) HF boost term (reward some extra treble vs mid)
    mid_band = (freq >= 500) & (freq <= 2000)
    hf_band  = (freq >= 4000) & (freq <= 10000)

    if np.any(mid_band):
        mid_mean = np.mean(level_smooth[mid_band])
    else:
        mid_mean = np.mean(level_smooth)

    if np.any(hf_band):
        hf_mean = np.mean(level_smooth[hf_band])
    else:
        hf_mean = mid_mean  # fallback

    # positive = HF louder than mid
    hf_boost = hf_mean - mid_mean

    # We *like* something in, say, +3 to +6 dB range
    ideal_boost = 4.5  # "target" bright boost (dB)
    # Penalize being far from that target
    boost_error = (hf_boost - ideal_boost) ** 2

    # 6) Combine into a single cost
    #    - MSE keeps it from going wild
    #    - boost_error pushes toward brighter treble
    cost = 0.6 * mse + 0.4 * boost_error

    # Higher score = better
    return -cost





# ===========================================================
# 3. LOAD ALL FILES FROM ToeIN_data FOLDER
# ===========================================================
folder_path = r"C:\Users\anish\Music\ToeIN_data"

txt_files = sorted(glob.glob(os.path.join(folder_path, "ToeIN_*")))

print("FOUND FILES:")
for f in txt_files:
    print("   ", f)

if len(txt_files) == 0:
    raise ValueError("No ToeIN_* files found. Check folder path or extensions.")

angles = []
scores_balanced = []
scores_soundstaged = []

for file in txt_files:
    base = os.path.basename(file)

    # Remove extension, extract angle
    angle_str = os.path.splitext(base)[0].split("_")[1]
    angle = float(angle_str)

    print("\nLoading:", file)
    df = load_spectrum_txt(file)
    score = compute_harman_score(df)
    score2 = compute_bright_score(df)

    angles.append(angle)
    scores_balanced.append(score)
    scores_soundstaged.append(score2)

angles = np.array(angles).reshape(-1, 1)
scores = np.array(scores_balanced)
scores2 = np.array(scores_soundstaged)

print("\nAngles loaded:", angles.flatten())
print("Scores:", scores)
print("Scores:", scores2)



# ===========================================================
# 4. FIT GAUSSIAN PROCESS
# ===========================================================
kernel = ConstantKernel(1.0) * RBF(length_scale=10.0) + WhiteKernel(noise_level=0.1)

gp = GaussianProcessRegressor(kernel=kernel, normalize_y=True)
gp2 = GaussianProcessRegressor(kernel=kernel, normalize_y=True)
gp.fit(angles, scores)
gp2.fit(angles, scores2)


# ===========================================================
# 5. BAYESIAN OPTIMIZATION → NEXT BEST ANGLE
# ===========================================================
candidate_angles = np.linspace(0, 30, 400).reshape(-1, 1)
mean, std = gp.predict(candidate_angles, return_std=True)
mean2, std2 = gp2.predict(candidate_angles, return_std=True)

ucb = mean + 1.5 * std
ucb2 = mean2 + 3 * std2



next_angle = candidate_angles[np.argmax(ucb)][0]
next_angle2 = candidate_angles[np.argmax(ucb2)][0]



# Convert to float instead of array
next_angle2 = float(next_angle2)

# Minimum separation distance (degrees)
min_sep = 0

# If the next suggestion is too close to existing points, nudge it
for a in angles.flatten():
    if abs(next_angle2 - a) < min_sep:
        if next_angle2 < a:
            next_angle2 = a - min_sep    # nudge left
        else:
            next_angle2 = a + min_sep    # nudge right

print("\n===================================================")
print(" Recommended NEXT angle to measure:", round(float(next_angle), 2))
print("===================================================")

print("\n===================================================")
print(" Recommended NEXT angle to measure:", round(float(next_angle2), 2))
print("===================================================")


# ===========================================================
# 6. PLOTS FOR REPORT — GP MEAN vs UCB CURVES
# ===========================================================
import matplotlib.pyplot as plt

# ------------------------------
# FIGURE 4: Balanced Mode GP Mean vs UCB
# ------------------------------
plt.figure(figsize=(10, 6))
plt.plot(candidate_angles, mean, label="GP Mean Prediction", linewidth=2)
plt.plot(candidate_angles, ucb, label="UCB Acquisition Function", linestyle="--", linewidth=2)
plt.scatter(angles, scores, color="black", label="Measured Data Points", zorder=5)

plt.title("Figure 4. GP Mean Prediction Curve and UCB Acquisition Function")
plt.xlabel("Toe-In Angle (degrees)")
plt.ylabel("Score")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()

# ------------------------------
# FIGURE 5: Bright Mode GP Mean vs UCB
# ------------------------------
plt.figure(figsize=(10, 6))
plt.plot(candidate_angles, mean2, label="GP Mean Prediction (Bright Mode)", linewidth=2)
plt.plot(candidate_angles, ucb2, label="UCB Acquisition Function (Bright Mode)", linestyle="--", linewidth=2)
plt.scatter(angles, scores2, color="black", label="Measured Data Points", zorder=5)

plt.title("Figure 5. GP Mean Prediction Curve and UCB (Bright Mode)")
plt.xlabel("Toe-In Angle (degrees)")
plt.ylabel("Score")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()



