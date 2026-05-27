import time
import random
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import confusion_matrix, accuracy_score

# ---------------- CONFIG ----------------
POSES = ['Tadasana', 'Tree Pose']
CONFIDENCE_THRESHOLD = 0.7
NUM_USERS = 3
POSES_PER_USER = 30  # simulate a full session
RESULT_CSV = "software_full_session_test.csv"


# ---------------- SIMULATE SENSOR INPUT ----------------
def simulate_sensor_input():
    """
    Simulate inputs for software-only AI testing.
    Includes normal poses and edge cases (missing data)
    """
    actual_pose = random.choice(POSES + [None])  # None simulates missing input
    sensor_data = {"fake_sensor": random.random()}
    return sensor_data, actual_pose


# ---------------- MODEL PREDICTION ----------------
def predict_pose(sensor_data):
    """


    Example:
    predicted_pose, confidence = your_model.predict(sensor_data)
    return predicted_pose, confidence
    """
    actual_pose = sensor_data.get("actual_pose", random.choice(POSES))

    # Handle missing input
    if actual_pose is None:
        return "Uncertain", 0.0

    # Simulate AI prediction (~85% correct)
    if random.random() < 0.85:
        predicted_pose = actual_pose
    else:
        predicted_pose = [p for p in POSES if p != actual_pose][0]

    confidence = round(random.uniform(0.6, 0.99), 2)
    return predicted_pose, confidence


# ---------------- TEST LOOP ----------------
results = []
consecutive_errors = 0
max_consecutive_errors = 0
test_id = 1

for user_id in range(1, NUM_USERS + 1):
    user_errors = 0
    for _ in range(POSES_PER_USER):
        start_time = time.time()

        sensor_data, actual_pose = simulate_sensor_input()
        sensor_data["actual_pose"] = actual_pose

        predicted_pose, confidence = predict_pose(sensor_data)
        latency = round((time.time() - start_time) * 1000, 2)  # ms

        # Apply confidence threshold
        if confidence < CONFIDENCE_THRESHOLD or actual_pose is None:
            predicted_pose = "Uncertain"

        # Track consecutive misclassifications
        if predicted_pose != actual_pose:
            consecutive_errors += 1
            user_errors += 1
        else:
            consecutive_errors = 0
        max_consecutive_errors = max(max_consecutive_errors, consecutive_errors)

        results.append({
            "Test_ID": test_id,
            "User_ID": user_id,
            "Actual_Pose": actual_pose if actual_pose else "Missing",
            "Predicted_Pose": predicted_pose,
            "Confidence": confidence,
            "Latency_ms": latency
        })
        test_id += 1

# ---------------- RESULTS ----------------
df = pd.DataFrame(results)
print(df)

# Overall accuracy excluding uncertain predictions
valid_predictions = df[df["Predicted_Pose"] != "Uncertain"]
accuracy = accuracy_score(valid_predictions["Actual_Pose"], valid_predictions["Predicted_Pose"])
print(f"\nSoftware-only Model Accuracy: {accuracy * 100:.2f}%")
print(f"Max Consecutive Misclassifications: {max_consecutive_errors}")

# Per-user accuracy
user_accuracy = valid_predictions.groupby("User_ID").apply(
    lambda x: accuracy_score(x["Actual_Pose"], x["Predicted_Pose"])
)
print("\nPer-User Accuracy:")
print(user_accuracy)

# Confusion matrix
cm = confusion_matrix(valid_predictions["Actual_Pose"], valid_predictions["Predicted_Pose"], labels=POSES)
cm_df = pd.DataFrame(cm, index=POSES, columns=POSES)
print("\nConfusion Matrix:")
print(cm_df)

# Average latency
avg_latency = df["Latency_ms"].mean()
print(f"\nAverage Prediction Latency: {avg_latency:.2f} ms")

# Save results
df.to_csv(RESULT_CSV, index=False)
print(f"\nResults saved to {RESULT_CSV}")

# ---------------- VISUALIZATION ----------------
sns.set(style="whitegrid")

# 1. Confusion matrix heatmap
plt.figure(figsize=(6, 5))
sns.heatmap(cm_df, annot=True, fmt="d", cmap="Blues")
plt.title("Confusion Matrix")
plt.ylabel("Actual Pose")
plt.xlabel("Predicted Pose")
plt.show()

# 2. Latency distribution
plt.figure(figsize=(6, 4))
sns.histplot(df["Latency_ms"], bins=10, kde=True)
plt.title("Prediction Latency Distribution (ms)")
plt.xlabel("Latency (ms)")
plt.ylabel("Frequency")
plt.show()

# 3. Per-user accuracy bar chart
plt.figure(figsize=(6, 4))
sns.barplot(x=user_accuracy.index, y=user_accuracy.values)
plt.ylim(0, 1)
plt.title("Per-User Accuracy")
plt.xlabel("User ID")
plt.ylabel("Accuracy")
plt.show()
