import streamlit as st
from database.yoga_poses import search_poses, get_pose, get_all_poses

def show():
    st.title("🔍 Search Yoga Poses")
    st.markdown("**Search by health need, body part, or difficulty!**")

    # Search bar
    query = st.text_input(
        "🔎 Search for yoga poses:",
        placeholder="e.g. back pain, balance, beginner, hips, stress..."
    )

    # Quick filter buttons
    st.markdown("**Quick Searches:**")
    col1, col2, col3, col4, col5 = st.columns(5)
    if col1.button("🔰 Beginner"):   query = "beginner"
    if col2.button("🦵 Legs"):       query = "legs"
    if col3.button("🧘 Back Pain"):  query = "back pain"
    if col4.button("⚖️ Balance"):    query = "balance"
    if col5.button("💪 Strength"):   query = "strength"

    st.markdown("---")

    # Get results
    if query:
        results = search_poses(query)
        if results:
            st.markdown(f"### Found **{len(results)}** poses for: *{query}*")
            for pose_name in results:
                pose_data = get_pose(pose_name)
                if not pose_data:
                    continue
                with st.expander(f"🧘 {pose_name} — {pose_data.get('difficulty','Beginner')}"):
                    col1, col2 = st.columns([2, 1])
                    with col1:
                        st.markdown(f"**Description:** {pose_data.get('description','')}")
                        st.markdown("**Benefits:**")
                        for b in pose_data.get("benefits", []):
                            if b:
                                st.markdown(f"- {b}")
                        st.markdown("**Steps:**")
                        for i, s in enumerate(pose_data.get("steps", []), 1):
                            if s:
                                st.markdown(f"{i}. {s}")
                    with col2:
                        st.markdown("**Details:**")
                        st.info(f"🏷️ Category: {pose_data.get('category','general')}")
                        st.info(f"⭐ Difficulty: {pose_data.get('difficulty','Beginner')}")
                        tags = pose_data.get("search_tags", [])
                        if tags:
                            st.markdown("**Tags:** " + ", ".join(tags))
        else:
            st.warning(f"No poses found for '{query}'. Try: beginner, back pain, balance, legs, strength")
    else:
        # Show all poses when no search
        st.markdown("### 📋 All Available Poses")
        all_poses = get_all_poses()
        cols = st.columns(4)
        for i, pose_name in enumerate(all_poses):
            pose_data = get_pose(pose_name)
            diff      = pose_data.get("difficulty", "Beginner") if pose_data else "Beginner"
            emoji     = "🔰" if diff == "Beginner" else "⭐" if diff == "Intermediate" else "🔥"
            cols[i % 4].markdown(f"{emoji} {pose_name}")