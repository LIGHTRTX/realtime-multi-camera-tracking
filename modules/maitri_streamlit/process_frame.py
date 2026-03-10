import cv2
import mediapipe as mp
import numpy as np

mp_pose = mp.solutions.pose
mp_drawing = mp.solutions.drawing_utils


def calculate_angle(a, b, c):
    a = np.array(a)
    b = np.array(b)
    c = np.array(c)
    ba = a - b
    bc = c - b
    cosine = np.dot(ba, bc) / (np.linalg.norm(ba) * np.linalg.norm(bc))
    angle = np.arccos(np.clip(cosine, -1.0, 1.0))
    return np.degrees(angle)


class ArmCurlAnalyzer:
    def __init__(self):
        self.pose = mp_pose.Pose(
            min_detection_confidence=0.3,
            min_tracking_confidence=0.3
        )
        self.angle_history = []
        self.rep_count = 0
        self.stage = None

    def process(self, frame):
        h, w, _ = frame.shape
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = self.pose.process(rgb)

        if results.pose_landmarks:
            landmarks = results.pose_landmarks.landmark

            shoulder = [
                landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].x * w,
                landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].y * h
            ]

            elbow = [
                landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].x * w,
                landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].y * h
            ]

            wrist = [
                landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].x * w,
                landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].y * h
            ]

            angle = calculate_angle(shoulder, elbow, wrist)
            self.angle_history.append(angle)

            if angle > 150:
                self.stage = "down"

            if angle < 50 and self.stage == "down":
                self.stage = "up"
                self.rep_count += 1

            cv2.putText(frame, f"Angle: {int(angle)}",
                        tuple(np.array(elbow, dtype=int)),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        0.8, (0, 255, 0), 2)

            cv2.putText(frame, f"Reps: {self.rep_count}",
                        (30, 50),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        1, (0, 0, 255), 2)

            mp_drawing.draw_landmarks(
                frame,
                results.pose_landmarks,
                mp_pose.POSE_CONNECTIONS
            )

        return frame

    def summary(self):
        if len(self.angle_history) == 0:
            return {
                "max_angle": 0,
                "min_angle": 0,
                "range_motion": 0,
                "reps": 0
            }

        max_angle = max(self.angle_history)
        min_angle = min(self.angle_history)
        range_motion = max_angle - min_angle

        return {
            "max_angle": max_angle,
            "min_angle": min_angle,
            "range_motion": range_motion,
            "reps": self.rep_count
        }
