# Real-Time Multi-Camera Tracking System (110+ FPS)

Production-oriented computer vision pipeline for real-time tracking, re-identification, and activity analysis.
The system is designed to remain stable under occlusion, motion blur, and camera transitions while supporting additional analytics modules such as **exercise repetition analysis**.

This is not a demo-only system. It is built for continuous inference.

---

# Key Capabilities

* Sustained **95–110+ FPS** on RTX-class GPUs
* Stable identity tracking under partial and full occlusion
* Multi-camera compatible (synchronized or near-synchronized feeds)
* Explicit handling of ID drift and tracker degradation
* Modular, inspectable pipeline (detector → tracker → re-ID → association)
* Integrated **exercise repetition analysis** using pose estimation

---

# Architecture Overview

Input Video(s)
→ YOLOv8 Detection
→ ByteTrack Association
→ Appearance-Based Re-ID
→ Pose Estimation (Keypoint Extraction)
→ Exercise Repetition Analyzer
→ Temporal Consistency & Gating
→ Stable Track Output

---

# Performance Benchmarks

| Scenario                     | FPS   |
| ---------------------------- | ----- |
| Single camera (1080p)        | 110   |
| Multi-camera (2 streams)     | 95    |
| Occlusion-heavy scenes       | 90+   |
| Tracking + Exercise Analysis | 85–95 |

Benchmarks measured on **RTX 4060**, batch size = 1, FP16 inference.

See `benchmarks/fps_results.md` for detailed measurements.

---

# Exercise Repetition Analyzer

**Objective:**
Detect and count repetitions of common exercises (e.g., squats, push-ups, bicep curls) from video streams in real time.

**Approach**

* Pose estimation to detect body keypoints
* Joint angle computation from keypoints
* Movement phase detection
* Repetition counting using threshold-based state transitions

**Key Steps**

1. Detect human pose keypoints
2. Compute joint angles (e.g., elbow, knee, shoulder)
3. Track motion phases (up / down / contraction / extension)
4. Increment repetition count when a full cycle is detected

**Supported Exercises**

* Squats
* Push-ups
* Bicep curls
* Shoulder press
* Sit-ups

**Outputs**

* Real-time rep counter
* Motion phase visualization
* Joint angle graphs
* Per-person exercise statistics

**Applications**

* Fitness monitoring systems
* Personal training assistants
* Sports performance analysis
* Rehabilitation tracking

---

# Failure Modes (Explicitly Documented)

This system may degrade under:

* Extreme camera desynchronization
* Long-term full occlusion (> N frames)
* Severe motion blur at low shutter speeds
* Partial body visibility during exercise movements

**Mitigations implemented**

* Confidence gating
* Track aging logic
* Re-ID refresh under uncertainty
* Pose smoothing filters

See `failure_modes.md` for detailed discussion.

---

# Why This Exists

Most tracking repositories optimize for demos.
This system focuses on **runtime reliability, modularity, and real-world analytics integration**, including exercise movement analysis.

---

# Technologies Used

* Python
* PyTorch
* Ultralytics YOLOv8
* ByteTrack
* OpenCV
* NumPy
* Pose estimation frameworks (e.g., YOLO-Pose / OpenPose / MediaPipe)

---

# Repository Structure

```
project/
│
├── run.py
├── requirements.txt
│
├── detectors/
│   └── yolo_detector.py
│
├── tracking/
│   └── bytetrack_tracker.py
│
├── reid/
│   └── appearance_model.py
│
├── pose/
│   └── pose_estimator.py
│
├── exercise_analysis/
│   └── repetition_counter.py
│
├── benchmarks/
│   └── fps_results.md
│
└── failure_modes.md
```

---

# How to Run

```bash
pip install -r requirements.txt
python run.py --input demo/input.mp4
```

Example with multi-camera input:

```bash
python run.py --input cam1.mp4 cam2.mp4
```

---

# Future Improvements

* Cross-camera identity re-identification
* Transformer-based motion understanding
* 3D pose estimation for better exercise analysis
* Real-time analytics dashboard
* Edge-device optimization

---
