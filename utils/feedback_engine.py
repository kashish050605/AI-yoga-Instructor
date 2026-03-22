from database.yoga_poses import get_pose

class FeedbackEngine:
    def __init__(self, pose_detector):
        self.detector = pose_detector

    def analyze(self, img, pose_name):
        pose_data = get_pose(pose_name)
        if not pose_data:
            return 0, ["Pose not found"], []

        lmList = self.detector.findPosition(img, draw=False)
        if len(lmList) == 0:
            return 0, ["No pose detected — stand in front of camera"], []

        angles_data    = pose_data.get("angles", {})
        corrections    = pose_data.get("corrections", {})
        correct_count  = 0
        total_count    = len(angles_data)
        correction_list = []
        correct_list    = []

        for part, data in angles_data.items():
            p1, p2, p3 = data["points"]
            target      = data["target"]
            tolerance   = data["tolerance"]

            if max(p1, p2, p3) >= len(lmList):
                continue

            actual = self.detector.findAngle(img, p1, p2, p3, draw=False)

            if abs(actual - target) <= tolerance:
                correct_count += 1
                correct_list.append(
                    f"✅ {part.replace('_', ' ').title()} — Good!"
                )
            else:
                correction_list.append(corrections.get(part, f"Adjust your {part}"))

        accuracy = int((correct_count / total_count) * 100) if total_count > 0 else 0
        return accuracy, correction_list, correct_list