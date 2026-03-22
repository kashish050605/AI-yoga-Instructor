import streamlit as st

st.set_page_config(
    page_title="AI Yoga Instructor",
    page_icon="🧘",
    layout="wide"
)

# Sidebar navigation
st.sidebar.title("🧘 AI Yoga Instructor")
st.sidebar.markdown("---")

page = st.sidebar.radio(
    "Navigate to:",
    ["🏠 Home", "📹 Live Mode", "🖼️ Image Upload Mode", "🔍 Search Mode"]
)

if page == "🏠 Home":
    st.title("🧘 Welcome to AI Yoga Instructor")
    st.markdown("""
    ### Your personal AI-powered yoga coach!
    This app uses **Computer Vision** and **AI** to help you
    practice yoga safely at home.
    ---
    ### 🚀 Features:
    | Mode | Description |
    |------|-------------|
    | 📹 **Live Mode** | Real-time posture correction using your webcam |
    | 🖼️ **Image Upload** | Upload a photo to identify your yoga pose |
    | 🔍 **Search Mode** | Search yoga poses by health need |
    ---
    ### 🏁 How to get started:
    1. Select a mode from the **left sidebar**
    2. In Live Mode — select a pose and click **Start**
    3. Stand in front of your camera and follow the feedback!
    """)
    col1, col2, col3 = st.columns(3)
    col1.metric("Poses Available", "20+")
    col2.metric("Detection", "Real-time")
    col3.metric("Accuracy", "Joint Angles")

elif page == "📹 Live Mode":
    from pages.live_mode import show
    show()

elif page == "🖼️ Image Upload Mode":
    from pages.image_upload_mode import show
    show()

elif page == "🔍 Search Mode":
    from pages.search_mode import show
    show()
    