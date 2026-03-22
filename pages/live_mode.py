import streamlit as st
import cv2
import time
from utils.pose_detector import PoseDetector
from utils.feedback_engine import FeedbackEngine
from database.yoga_poses import get_all_poses, get_pose

def show():
    st.title("📹 Live Yoga Mode")
    st.markdown("**Stand in front of your camera and select a pose to practice!**")

    pose_names    = get_all_poses()
    selected_pose = st.selectbox("Select a Yoga Pose to Practice:", pose_names)

    pose_data = get_pose(selected_pose)
    if pose_data:
        with st.expander(f"📖 About {selected_pose}"):
            st.write(pose_data.get("description", ""))
            st.markdown("**Difficulty:** " + pose_data.get("difficulty", "Beginner"))
            st.markdown("**Benefits:**")
            for b in pose_data.get("benefits", []):
                st.markdown(f"- {b}")
            st.markdown("**Steps:**")
            steps = pose_data.get("steps", [])
            for i, s in enumerate(steps, 1):
                if s:
                    st.markdown(f"{i}. {s}")

    col1, col2 = st.columns(2)
    start = col1.button("▶️ Start Live Detection", type="primary")
    stop  = col2.button("⏹️ Stop")

    frame_placeholder    = st.empty()
    accuracy_placeholder = st.empty()
    feedback_placeholder = st.empty()

    if start:
        detector = PoseDetector()
        feedback = FeedbackEngine(detector)
        cap      = cv2.VideoCapture(0)

        if not cap.isOpened():
            st.error("❌ Cannot open camera! Check your webcam.")
            return

        st.info("📷 Camera started! Press **Stop** to end session.")

        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                st.error("Cannot read camera!")
                break

            frame = detector.findPose(frame, draw=True)
            detector.findPosition(frame, draw=False)

            accuracy, corrections, corrects = feedback.analyze(frame, selected_pose)

            # Accuracy bar
            filled  = accuracy // 10
            empty   = 10 - filled
            accuracy_placeholder.markdown(
                f"### 🎯 Accuracy: {accuracy}%\n"
                f"{'🟢' * filled}{'⚪' * empty}"
            )

            # Feedback
            feedback_text = ""
            if corrects:
                feedback_text += "**✅ What's correct:**\n"
                for c in corrects:
                    feedback_text += f"{c}\n\n"
            if corrections:
                feedback_text += "**🔴 What to fix:**\n"
                for c in corrections:
                    feedback_text += f"- {c}\n"
            if accuracy == 100:
                feedback_text = "🎉 **Perfect pose! Amazing work!**"

            feedback_placeholder.markdown(feedback_text)

            # Show frame
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            frame_placeholder.image(
                frame_rgb,
                channels="RGB",
                use_container_width=True
            )

            time.sleep(0.03)

            if stop:
                break

        cap.release()
        st.success("✅ Session ended!")