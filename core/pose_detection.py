import cv2
import mediapipe as mp
import numpy as np
import math
import time

# ---------------- MEDIAPIPE SETUP ----------------
mp_pose = mp.solutions.pose
mp_drawing = mp.solutions.drawing_utils

pose = mp_pose.Pose(
    static_image_mode=False,
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5
)

# ---------------- POSE LIST ----------------
POSES = [
    "Tadasana 🧘‍♀️",
    "Tree Pose 🌳",
    "Warrior Pose ⚔️",
    "Plank Pose 💪",
    "Cat Pose 🐈"
]

# ---------------- ANGLE CALCULATION ----------------
def calculate_angle(a, b, c):
    a = np.array(a)
    b = np.array(b)
    c = np.array(c)

    radians = np.arctan2(
        c[1] - b[1],
        c[0] - b[0]
    ) - np.arctan2(
        a[1] - b[1],
        a[0] - b[0]
    )

    angle = np.abs(radians * 180.0 / np.pi)

    if angle > 180:
        angle = 360 - angle

    return angle

# ---------------- POSE ANALYSIS ----------------
def analyze_pose(results):

    if not results.pose_landmarks:
        return "No Person", "Please stand in frame", 0.0

    lm = results.pose_landmarks.landmark

    # ---------------- LANDMARKS ----------------
    LEFT_SHOULDER = [
        lm[mp_pose.PoseLandmark.LEFT_SHOULDER.value].x,
        lm[mp_pose.PoseLandmark.LEFT_SHOULDER.value].y
    ]

    RIGHT_SHOULDER = [
        lm[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].x,
        lm[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].y
    ]

    LEFT_ELBOW = [
        lm[mp_pose.PoseLandmark.LEFT_ELBOW.value].x,
        lm[mp_pose.PoseLandmark.LEFT_ELBOW.value].y
    ]

    RIGHT_ELBOW = [
        lm[mp_pose.PoseLandmark.RIGHT_ELBOW.value].x,
        lm[mp_pose.PoseLandmark.RIGHT_ELBOW.value].y
    ]

    LEFT_WRIST = [
        lm[mp_pose.PoseLandmark.LEFT_WRIST.value].x,
        lm[mp_pose.PoseLandmark.LEFT_WRIST.value].y
    ]

    RIGHT_WRIST = [
        lm[mp_pose.PoseLandmark.RIGHT_WRIST.value].x,
        lm[mp_pose.PoseLandmark.RIGHT_WRIST.value].y
    ]

    LEFT_HIP = [
        lm[mp_pose.PoseLandmark.LEFT_HIP.value].x,
        lm[mp_pose.PoseLandmark.LEFT_HIP.value].y
    ]

    RIGHT_HIP = [
        lm[mp_pose.PoseLandmark.RIGHT_HIP.value].x,
        lm[mp_pose.PoseLandmark.RIGHT_HIP.value].y
    ]

    LEFT_KNEE = [
        lm[mp_pose.PoseLandmark.LEFT_KNEE.value].x,
        lm[mp_pose.PoseLandmark.LEFT_KNEE.value].y
    ]

    RIGHT_KNEE = [
        lm[mp_pose.PoseLandmark.RIGHT_KNEE.value].x,
        lm[mp_pose.PoseLandmark.RIGHT_KNEE.value].y
    ]

    LEFT_ANKLE = [
        lm[mp_pose.PoseLandmark.LEFT_ANKLE.value].x,
        lm[mp_pose.PoseLandmark.LEFT_ANKLE.value].y
    ]

    RIGHT_ANKLE = [
        lm[mp_pose.PoseLandmark.RIGHT_ANKLE.value].x,
        lm[mp_pose.PoseLandmark.RIGHT_ANKLE.value].y
    ]

    # ---------------- ANGLES ----------------
    left_knee_angle = calculate_angle(
        LEFT_HIP,
        LEFT_KNEE,
        LEFT_ANKLE
    )

    right_knee_angle = calculate_angle(
        RIGHT_HIP,
        RIGHT_KNEE,
        RIGHT_ANKLE
    )

    left_elbow_angle = calculate_angle(
        LEFT_SHOULDER,
        LEFT_ELBOW,
        LEFT_WRIST
    )

    right_elbow_angle = calculate_angle(
        RIGHT_SHOULDER,
        RIGHT_ELBOW,
        RIGHT_WRIST
    )

    left_body_angle = calculate_angle(
        LEFT_SHOULDER,
        LEFT_HIP,
        LEFT_ANKLE
    )

    right_body_angle = calculate_angle(
        RIGHT_SHOULDER,
        RIGHT_HIP,
        RIGHT_ANKLE
    )

    # ---------------- TADASANA ----------------
    if (
        160 < left_knee_angle < 180 and
        160 < right_knee_angle < 180 and
        160 < left_body_angle < 180 and
        160 < right_body_angle < 180
    ):

        return (
            "Tadasana 🧘‍♀️",
            "Stand tall and relax shoulders.",
            0.92
        )

    # ---------------- TREE POSE ----------------
    elif (
        (
            left_knee_angle < 100 or
            right_knee_angle < 100
        ) and
        LEFT_WRIST[1] < LEFT_SHOULDER[1] and
        RIGHT_WRIST[1] < RIGHT_SHOULDER[1]
    ):

        return (
            "Tree Pose 🌳",
            "Maintain balance and engage core.",
            0.95
        )

    # ---------------- WARRIOR POSE ----------------
    elif (
        (
            abs(LEFT_WRIST[1] - LEFT_SHOULDER[1]) < 0.1 and
            abs(RIGHT_WRIST[1] - RIGHT_SHOULDER[1]) < 0.1
        ) and
        (
            left_knee_angle < 140 or
            right_knee_angle < 140
        )
    ):

        return (
            "Warrior Pose ⚔️",
            "Keep arms straight and chest open.",
            0.90
        )

    # ---------------- PLANK POSE ----------------
    elif (
        160 < left_body_angle < 180 and
        160 < right_body_angle < 180 and
        abs(LEFT_SHOULDER[1] - LEFT_ANKLE[1]) < 0.15
    ):

        return (
            "Plank Pose 💪",
            "Keep your body straight.",
            0.93
        )

    # ---------------- CAT POSE ----------------
    elif (
        left_body_angle < 140 and
        right_body_angle < 140
    ):

        return (
            "Cat Pose 🐈",
            "Curve your spine gently.",
            0.88
        )

    else:
        return (
            "Adjust Posture",
            "Please align your body properly.",
            0.50
        )

# ---------------- MAIN CAMERA LOOP ----------------
def run_pose_detection():

    cap = cv2.VideoCapture(0)

    while cap.isOpened():

        success, frame = cap.read()

        if not success:
            print("Camera not detected")
            break

        # Flip frame
        frame = cv2.flip(frame, 1)

        # Convert to RGB
        image_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # Process pose
        results = pose.process(image_rgb)

        # Analyze pose
        detected_pose, feedback, confidence = analyze_pose(results)

        # Draw skeleton
        if results.pose_landmarks:

            mp_drawing.draw_landmarks(
                frame,
                results.pose_landmarks,
                mp_pose.POSE_CONNECTIONS
            )

        # Display pose
        cv2.putText(
            frame,
            f"Pose: {detected_pose}",
            (20, 40),
            cv2.FONT_HERSHEY_SIMPLEX,
            1,
            (0, 255, 0),
            2
        )

        # Display confidence
        cv2.putText(
            frame,
            f"Confidence: {confidence:.2f}",
            (20, 80),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.8,
            (255, 255, 0),
            2
        )

        # Display feedback
        cv2.putText(
            frame,
            feedback,
            (20, 120),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.7,
            (0, 255, 255),
            2
        )

        # Show frame
        cv2.imshow("Swathya Smart Yoga Detection", frame)

        # Exit with Q
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

# ---------------- RUN ----------------
if __name__ == "__main__":
    run_pose_detection()