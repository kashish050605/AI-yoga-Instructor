import cv2
from utils.pose_detector import PoseDetector

# Initialize detector
detector = PoseDetector()

# Open webcam (0 = default camera)
cap = cv2.VideoCapture(0)

print("Press Q to quit")

while True:
    success, img = cap.read()
    if not success:
        print("Cannot read camera!")
        break

    # Detect pose and draw landmarks
    img = detector.findPose(img)
    
    # Get landmark positions
    lmList = detector.findPosition(img, draw=False)

    # Show if pose is detected
    if detector.isPoseDetected():
        cv2.putText(img, "POSE DETECTED!", (10, 50),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        
        # Show elbow angle as example
        if len(lmList) > 15:
            angle = detector.findAngle(img, 11, 13, 15)  # Left elbow

    else:
        cv2.putText(img, "No pose detected", (10, 50),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

    # Show the video
    cv2.imshow("Pose Detection Test", img)

    # Press Q to quit
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()