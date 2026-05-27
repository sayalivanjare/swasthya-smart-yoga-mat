import streamlit as st
import time

def init_session_state():
    defaults = {
        "username": "Guest",
        "session_log": [],
        "start_time": None
    }
    for key, val in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = val


def record_session(pose_history):
    init_session_state()

    if not pose_history:
        return

    total_time = time.time() - st.session_state.get("start_time", time.time())
    avg_score = sum([x["score"] for x in pose_history]) / len(pose_history)
    best_pose = max(pose_history, key=lambda x: x["score"])["pose"]

    session_data = {
        "username": st.session_state.username,
        "duration_min": round(total_time / 60, 2),
        "avg_score": round(avg_score, 2),
        "best_pose": best_pose,
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
    }

    st.session_state.session_log.append(session_data)
    st.session_state.pose_history = []


def show_summary():
    init_session_state()

    st.title("📊 Yoga Session Dashboard")

    if not st.session_state.session_log:
        st.info("No sessions recorded yet.")
        return

    sessions = st.session_state.session_log

    st.subheader("📈 Performance Trend")
    scores = [s["avg_score"] for s in sessions]
    st.line_chart(scores)

    for session in reversed(sessions):
        st.write(session)