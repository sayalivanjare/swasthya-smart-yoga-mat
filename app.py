import streamlit as st
import cv2
import mediapipe as mp
import time
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

from auth import login_user, register_user, logout_user, recover_password
from feedback import pose_feedback
from pose_detection import analyze_pose
from session_summary import init_session_state, record_session

# -------------------------
# SENSOR IMPORT
# -------------------------
try:
    from sensor_input import get_sensor_data
    SENSOR_AVAILABLE = True
except:
    SENSOR_AVAILABLE = False


# -------------------------
# CONFIG
# -------------------------
st.set_page_config(page_title="Swasthya Smart Yoga Mat", layout="wide")
init_session_state()

# -------------------------
# SESSION STATE
# -------------------------
if "running" not in st.session_state:
    st.session_state.running = False

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "start_time" not in st.session_state:
    st.session_state.start_time = 0

if "pose_history" not in st.session_state:
    st.session_state.pose_history = []


# -------------------------
# LOGIN SYSTEM
# -------------------------
def login_system():
    menu = st.sidebar.selectbox(
        "Authentication",
        ["Login", "Register", "Recover Password", "Logout"]
    )

    if menu == "Login":
        if login_user():
            st.session_state.logged_in = True

    elif menu == "Register":
        register_user()

    elif menu == "Recover Password":
        recover_password()

    elif menu == "Logout":
        logout_user()
        st.session_state.logged_in = False
        st.rerun()


login_system()

if not st.session_state.logged_in:
    st.warning("Please login first")
    st.stop()


# -------------------------
# HEATMAP
# -------------------------
def draw_heatmap(values):

    if len(values) < 13:
        st.warning("Waiting for sensor data...")
        return

    grid = np.array([
        [values[0], values[1], 0, values[2], values[3]],
        [values[4], values[5], values[6], values[7], values[8]],
        [values[9], values[10], 0, values[11], values[12]]
    ])

    fig, ax = plt.subplots(figsize=(5, 3))

    sns.heatmap(
        grid,
        annot=True,
        cmap="YlOrRd",
        linewidths=1,
        ax=ax
    )

    ax.set_title("Pressure Heatmap")

    st.pyplot(fig)
    plt.close(fig)


# -------------------------
# UI HEADER
# -------------------------
st.title("🧘 Swasthya Smart Yoga Mat")

st.sidebar.title("Control Panel")

selected_pose = st.sidebar.selectbox(
    "Select Pose",
    ["Tadasana", "Tree Pose", "Warrior Pose", "Plank Pose", "Cat Pose"]
)

start = st.sidebar.button("▶ Start Session")
stop = st.sidebar.button("⛔ Stop Session")


# -------------------------
# SESSION CONTROL
# -------------------------
if start:
    st.session_state.running = True
    st.session_state.start_time = time.time()
    st.session_state.pose_history = []

if stop:
    st.session_state.running = False
    record_session(st.session_state.pose_history)
    st.success("Session Saved")


# -------------------------
# LAYOUT
# -------------------------
col1, col2 = st.columns([2, 1])

frame_placeholder = col1.empty()
sensor_placeholder = col2.empty()
feedback_placeholder = col2.empty()


# -------------------------
# MEDIAPIPE
# -------------------------
mp_pose = mp.solutions.pose
pose = mp_pose.Pose(
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5
)


# -------------------------
# MAIN LOOP
# -------------------------
if st.session_state.running:

    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        st.error("Camera not detected")
        st.stop()

    while st.session_state.running:

        success, frame = cap.read()
        if not success:
            break

        frame = cv2.flip(frame, 1)

        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = pose.process(rgb)

        # ---------------- POSE ----------------
        detected_pose, feedback, score = analyze_pose(results)

        # overlay text
        cv2.putText(frame, f"{detected_pose}", (10, 40),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

        cv2.putText(frame, f"Score: {score:.2f}", (10, 80),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 255), 2)

        # ---------------- STORE SESSION ----------------
        elapsed = time.time() - st.session_state.start_time

        st.session_state.pose_history.append({
            "pose": detected_pose,
            "score": score,
            "time": elapsed
        })

        # ---------------- FRAME ----------------
        frame_placeholder.image(frame, channels="BGR")

        # ---------------- SENSOR ----------------
        sensor_values = []

        if SENSOR_AVAILABLE:
            try:
                raw = get_sensor_data()
                sensor_values = [min(v / 4000, 1.0) for v in raw]
            except:
                sensor_values = []

        # ---------------- SENSOR UI ----------------
        sensor_placeholder.empty()
        with sensor_placeholder.container():
            st.subheader("Sensor Heatmap")
            st.write(sensor_values)

            if len(sensor_values) >= 13:
                draw_heatmap(sensor_values)
            else:
                st.warning("Waiting for sensor data...")

        # ---------------- FEEDBACK UI ----------------
        feedback_placeholder.empty()
        with feedback_placeholder.container():
            st.subheader("AI Feedback")

            st.info(f"Detected Pose: {detected_pose}")
            st.warning(feedback)

            st.metric("Confidence", f"{score:.2f}")
            st.metric("Time (sec)", f"{int(elapsed)}")

        time.sleep(0.03)

    cap.release()
    cv2.destroyAllWindows()