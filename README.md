# Real-Time Multi-Camera Tracking System (110+ FPS)

Production-oriented computer vision pipeline for real-time tracking and re-identification,
designed to remain stable under occlusion, motion blur, and camera transitions.

This is not a demo-only system. It is built for continuous inference.

---

## Key Capabilities

- Sustained **95–110+ FPS** on RTX-class GPUs
- Stable identity tracking under partial and full occlusion
- Multi-camera compatible (synchronized or near-synchronized feeds)
- Explicit handling of ID drift and tracker degradation
- Modular, inspectable pipeline (detector → tracker → re-ID → association)

---

## Architecture Overview

Input Video(s)
→ YOLOv8 Detection
→ ByteTrack Association
→ Appearance-Based Re-ID
→ Temporal Consistency & Gating
→ Stable Track Output

---

## Performance Benchmarks

| Scenario                     | FPS |
|-----------------------------|-----|
| Single camera (1080p)       | 110 |
| Multi-camera (2 streams)    | 95  |
| Occlusion-heavy scenes      | 90+ |

Benchmarks measured on RTX 4060, batch=1, FP16 inference.

See `benchmarks/fps_results.md` for details.

---

## Failure Modes (Explicitly Documented)

This system degrades under:
- Extreme camera desynchronization
- Long-term full occlusion (> N frames)
- Severe motion blur at low shutter speeds

Mitigations implemented:
- Confidence gating
- Track aging logic
- Re-ID refresh under uncertainty

See `failure_modes.md`.

---

## Why This Exists

Most tracking repos optimize for demos.
This system optimizes for **runtime reliability**.

---

## How to Run

```bash
pip install -r requirements.txt
python run.py --input demo/input.mp4
