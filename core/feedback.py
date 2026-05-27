# -------------------------
# FEEDBACK FUNCTION
# -------------------------

def pose_feedback(pose, feedback):

    """
    Voice / Console feedback
    """

    print(f"\nDetected Pose : {pose}")

    print(f"Feedback : {feedback}")


# -------------------------
# OPTIONAL CUSTOM FEEDBACK
# -------------------------

def get_pose_message(pose):

    messages = {

        "Tree Pose 🌳":
            "Maintain body balance and keep spine straight.",

        "Warrior Pose":
            "Keep your arms aligned and legs stable.",

        "Plank Pose":
            "Maintain a straight body posture.",

        "Cat Pose":
            "Move slowly and control breathing.",

        "Tadasana":
            "Stand upright with balanced posture."
    }

    return messages.get(
        pose,
        "Keep practicing yoga."
    )