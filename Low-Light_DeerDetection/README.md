#  Low-Light Deer Detection using Image Enhancement

This project explores improving object detection performance in **low-light and nighttime environments** using image preprocessing techniques.

---

##  Approach

A YOLOv8-based object detection model was used as the baseline. Several preprocessing methods were evaluated to improve detection under poor visibility conditions:

- **Gamma Correction** – global brightness enhancement  
- **CLAHE (Contrast Limited Adaptive Histogram Equalization)** – local contrast enhancement  
- **Gaussian Smoothing** – noise reduction prior to enhancement
- **Baseline Dataset** - https://www.kaggle.com/datasets/winnerbishal/deer-cameratraps

---

##  Key Insight

In extremely low-light conditions, **gamma correction significantly improves detection**, while CLAHE alone can fail due to amplification of background noise.

> Global brightness enhancement is more effective than local contrast enhancement in severely underexposed scenes.

---

##  Example Result

### Raw Image (No Detection)
- Extremely low visibility  
- Deer is barely distinguishable  

![Raw Image](raw_input.jpg)

---

### Gamma / Enhanced Image (Detection)
- Deer successfully detected  
- Confidence improved under low-light conditions  

![Enhanced Image](gamma_gaussian_clahe_input.jpg)

---

##  Observations

- Low-light images primarily suffer from **lack of signal**, not just contrast  
- CLAHE can degrade performance in noisy scenes by amplifying irrelevant features  
- Gaussian smoothing can help stabilize CLAHE, but **does not replace brightness correction**  
- Detection performance is highly sensitive in edge-case scenarios  

---

##  Future Work

- Evaluate preprocessing on a **low-light subset of the dataset**  
- Develop **adaptive preprocessing pipelines** based on scene conditions  
- Improve robustness under **occlusion and partial visibility**  
- Explore temporal methods (video-based detection)  

---

##  Tech Stack

- Python  
- OpenCV  
- Ultralytics YOLOv8  

---

## 📁 Files

- `Base_train.py` – baseline YOLO training  
- `Clahe_train.py` – CLAHE preprocessing experiments  
- `test.py` – inference and evaluation  

---

##  Summary

This project demonstrates how targeted preprocessing can convert a **failure case into a successful detection**, highlighting the importance of handling real-world conditions such as low visibility and noise in computer vision systems.
