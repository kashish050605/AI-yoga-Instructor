import cv2
import numpy as np

# Try new mediapipe API
import mediapipe as mp

# Suppress warnings
import os
import warnings
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
warnings.filterwarnings('ignore')

class PoseDetector:
    def __init__(self, detectionCon=0.5, trackCon=0.5):
        self.detectionCon = detectionCon
        self.trackCon = trackCon
        self.results = None
        self.lmList = []

        # Use the NEW mediapipe tasks API
        self.mp = mp
        BaseOptions = mp.tasks.BaseOptions
        PoseLandmarker = mp.tasks.vision.PoseLandmarker
        PoseLandmarkerOptions = mp.tasks.vision.PoseLandmarkerOptions
        VisionRunningMode = mp.tasks.vision.RunningMode

        self.options = PoseLandmarkerOptions(
            base_options=BaseOptions(
                model_asset_path='models/pose_landmarker.task'
            ),
            running_mode=VisionRunningMode.IMAGE,
            min_pose_detection_confidence=detectionCon,
            min_pose_presence_confidence=detectionCon,
            min_tracking_confidence=trackCon
        )

    def findPose(self, img, draw=True):
        with self.mp.tasks.vision.PoseLandmarker.create_from_options(self.options) as landmarker:
            imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            mp_image = self.mp.Image(
                image_format=self.mp.ImageFormat.SRGB,
                data=imgRGB
            )
            self.results = landmarker.detect(mp_image)

        if draw and self.results and self.results.pose_landmarks:
            h, w, _ = img.shape
            for landmarks in self.results.pose_landmarks:
                # Draw points
                for lm in landmarks:
                    cx, cy = int(lm.x * w), int(lm.y * h)
                    cv2.circle(img, (cx, cy), 5, (0, 255, 0), cv2.FILLED)
                # Draw connections manually
                CONNECTIONS = [
                    (11,12),(11,13),(13,15),(12,14),(14,16),
                    (11,23),(12,24),(23,24),(23,25),(24,26),
                    (25,27),(26,28),(27,29),(28,30),(29,31),(30,32)
                ]
                for p1, p2 in CONNECTIONS:
                    if p1 < len(landmarks) and p2 < len(landmarks):
                        x1,y1 = int(landmarks[p1].x*w), int(landmarks[p1].y*h)
                        x2,y2 = int(landmarks[p2].x*w), int(landmarks[p2].y*h)
                        cv2.line(img, (x1,y1), (x2,y2), (0,0,255), 2)
        return img

    def findPosition(self, img, draw=False):
        self.lmList = []
        if self.results and self.results.pose_landmarks:
            h, w, _ = img.shape
            for id, lm in enumerate(self.results.pose_landmarks[0]):
                cx, cy = int(lm.x * w), int(lm.y * h)
                self.lmList.append([id, cx, cy])
        return self.lmList

    def findAngle(self, img, p1, p2, p3, draw=True):
        if len(self.lmList) <= max(p1, p2, p3):
            return 0
        x1,y1 = self.lmList[p1][1], self.lmList[p1][2]
        x2,y2 = self.lmList[p2][1], self.lmList[p2][2]
        x3,y3 = self.lmList[p3][1], self.lmList[p3][2]
        angle = np.degrees(
            np.arctan2(y3-y2, x3-x2) - np.arctan2(y1-y2, x1-x2)
        )
        if angle < 0:
            angle += 360
        if draw:
            cv2.line(img, (x1,y1), (x2,y2), (255,255,255), 2)
            cv2.line(img, (x3,y3), (x2,y2), (255,255,255), 2)
            cv2.putText(img, str(int(angle)), (x2-30, y2-10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0,255,255), 2)
        return angle

    def isPoseDetected(self):
        return (self.results is not None and
                self.results.pose_landmarks is not None and
                len(self.results.pose_landmarks) > 0)

    def getAllLandmarks(self):
        if self.isPoseDetected():
            landmarks = []
            for lm in self.results.pose_landmarks[0]:
                landmarks.extend([lm.x, lm.y, lm.z, lm.presence])
            return landmarks
        return None

