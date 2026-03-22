import streamlit as st
import cv2
import numpy as np
from PIL import Image
from utils.pose_detector import PoseDetector
from utils.feedback_engine import FeedbackEngine
from database.yoga_poses import get_all_poses, get_pose

def show():
    st.title("🖼️ Image Upload Mode")
    st.markdown("**Upload a photo of yourself doing yoga to get feedback!**")

    pose_names    = get_all_poses()
    selected_pose = st.selectbox("Which pose are you attempting?", pose_names)

    uploaded_file = st.file_uploader(
        "Upload your yoga photo:",
        type=["jpg", "jpeg", "png"]
    )

    if uploaded_file is not None:
        # Convert uploaded file to OpenCV image
        image     = Image.open(uploaded_file).convert("RGB")
        img_array = np.array(image)
        img_bgr   = cv2.cvtColor(img_array, cv2.COLOR_RGB2BGR)

        col1, col2 = st.columns(2)

        with col1:
            st.markdown("### 📸 Your Photo")
            st.image(image, use_container_width=True)

        # Run pose detection
        detector = PoseDetector(detectionCon=0.3)
        img_bgr  = detector.findPose(img_bgr, draw=True)
        detector.findPosition(img_bgr, draw=False)

        feedback = FeedbackEngine(detector)
        accuracy, corrections, corrects = feedback.analyze(img_bgr, selected_pose)

        with col2:
            st.markdown("### 🤖 AI Analysis")

            # Convert back to RGB for display
            img_rgb = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2RGB)
            st.image(img_rgb, use_container_width=True)

        # Results
        st.markdown("---")
        st.markdown(f"## 🎯 Accuracy Score: {accuracy}%")

        # Progress bar
        st.progress(accuracy / 100)

        if accuracy >= 80:
            st.success("🎉 Excellent! Your pose looks great!")
        elif accuracy >= 50:
            st.warning("👍 Good attempt! A few things to fix:")
        else:
            st.error("💪 Keep practicing! Here's what to improve:")

        col3, col4 = st.columns(2)

        with col3:
            if corrects:
                st.markdown("### ✅ What's correct:")
                for c in corrects:
                    st.markdown(c)

        with col4:
            if corrections:
                st.markdown("### 🔴 What to fix:")
                for c in corrections:
                    st.markdown(f"- {c}")

        # Show pose reference info
        pose_data = get_pose(selected_pose)
        if pose_data:
            with st.expander("📖 Correct Pose Instructions"):
                st.markdown("**Steps to perform correctly:**")
                for i, s in enumerate(pose_data.get("steps", []), 1):
                    if s:
                        st.markdown(f"{i}. {s}")