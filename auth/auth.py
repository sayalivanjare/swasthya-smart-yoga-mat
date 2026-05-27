import streamlit as st
import json
import re
import os
from datetime import datetime

USER_DB = "users.json"

# ==============================
#  Utility Functions
# ==============================

def load_users():
    if os.path.exists(USER_DB):
        with open(USER_DB, "r") as f:
            return json.load(f)
    return {}

def save_users(users):
    with open(USER_DB, "w") as f:
        json.dump(users, f, indent=4)

def valid_email(email):
    pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    return re.match(pattern, email) is not None

# ==============================
#  Registration
# ==============================

def register_user():
    st.subheader("📝 Create New Account")
    email = st.text_input("Email Address")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    confirm_password = st.text_input("Confirm Password", type="password")

    if st.button("Register"):
        users = load_users()

        if not valid_email(email):
            st.error("Invalid email format.")
            return None
        if username in users:
            st.error("Username already exists.")
            return None
        if password != confirm_password:
            st.error("Passwords do not match.")
            return None

        users[username] = {
            "email": email,
            "password": password,
            "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "sessions": []
        }
        save_users(users)
        st.success("✅ Registration successful! Please log in now.")
        return True

# ==============================
#  Login
# ==============================

def login_user():
    st.subheader("🔐 Login")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        users = load_users()
        if username in users and users[username]["password"] == password:
            st.session_state["user"] = username
            st.session_state["login_time"] = datetime.now().strftime("%H:%M:%S")
            st.success(f"Welcome back, {username} 👋")
            return True
        else:
            st.error("Invalid username or password.")
            return False

# ==============================
#  Password Recovery (Simulation)
# ==============================

def recover_password():
    st.subheader("🔑 Forgot Password?")
    email = st.text_input("Enter your registered email")

    if st.button("Recover Password"):
        users = load_users()
        for user, info in users.items():
            if info["email"] == email:
                st.info(f"Password recovery link has been sent to **{email}** (simulated).")
                return
        st.error("No account found with that email.")

# ==============================
#  Logout
# ==============================

def logout_user():
    if "user" in st.session_state:
        st.session_state.pop("user")
        st.session_state.pop("login_time", None)
        st.success("Logged out successfully.")
