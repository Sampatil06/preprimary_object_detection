import streamlit as st
import os
from PIL import Image
from utils.database import register_user, login_user
from utils.object_detection import process_image
from utils.speech import text_to_speech
from utils.translation import translate_text
from utils.database import create_db

create_db()  



st.set_page_config(page_title="AdaptLearn-Hub", page_icon="📚", layout="wide")


st.markdown(
    """
    <style>
        .navbar {
            font-size: 24px;
            font-weight: bold;
            color: white;
            background-color: #4CAF50;
            text-align: center;
            padding: 10px;
            border-radius: 10px;
            margin-bottom: 20px;
        }
        .sidebar-content {
            font-size: 18px;
            padding: 10px;
            border-radius: 10px;
            background-color: #f4f4f4;
        }
        .stButton > button {
            width: 100%;
            padding: 10px;
            font-size: 18px;
        }
    </style>
    """,
    unsafe_allow_html=True,
)


st.markdown('<div class="navbar">AdaptLearn-Hub</div>', unsafe_allow_html=True)


if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.user_id = None
    st.session_state.username = None
    st.session_state.age = None
    st.session_state.gender = None
    st.session_state.camera_active = False
    st.session_state.captured_image = None
    st.session_state.language = "English"


def language_selection():
    st.sidebar.subheader("🌍 Select Language")
    languages = ["English", "Hindi", "Marathi", "Bengali", "Gujarati", "Tamil", "Telugu"]
    st.session_state.language = st.sidebar.selectbox("Choose Language", languages)


def login_page():
    st.subheader("Login or Register")
    option = st.radio("Select an option:", ["Login", "Register"])

    if option == "Login":
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")

        if st.button("Login"):
            user = login_user(username, password)
            if user:
                st.success("Login successful!")
                st.session_state.logged_in = True
                st.session_state.user_id = user[0]
                st.session_state.username = user[1]
                st.session_state.age = user[2]
                st.session_state.gender = user[3]
                st.rerun()
            else:
                st.error("Invalid username or password.")

    elif option == "Register":
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        age = st.number_input("Age", min_value=3, max_value=10, step=1)
        gender = st.selectbox("Gender", ["Male", "Female", "Other"])

        if st.button("Register"):
            if register_user(username, password, age, gender):
                st.success("Registration successful! You can now log in.")
            else:
                st.error("Username already exists. Try another.")


def capture_image():
    st.subheader("📷 Capture Image in Real-Time")
    
    camera_option = st.selectbox("📷 Camera", ["Off", "On"], key="camera_toggle")
    st.session_state.camera_active = camera_option == "On"

    if st.session_state.camera_active:
        captured_image = st.camera_input("Capture an Image", key="camera_input")

        if captured_image:
            image_path = "static/captured_image.jpg"
            os.makedirs("static", exist_ok=True)
            image = Image.open(captured_image)
            image.save(image_path)

            st.image(image_path, caption="Captured Image", width=400)
            detected_objects, description = process_image(image_path, st.session_state.user_id)
            translated_description = translate_text(description, st.session_state.language)
            st.write("### 📺 Detected Objects:", ", ".join(detected_objects))
            st.write("### 📚 Object Descriptions:", translated_description)
            audio_path = text_to_speech(translated_description, st.session_state.language)
            st.audio(audio_path, format="audio/mp3")


def main_page():
    language_selection()
    st.sidebar.markdown('<div class="sidebar-content"><b>User Profile</b></div>', unsafe_allow_html=True)
    st.sidebar.write(f"👤 **Username:** {st.session_state.username}")
    st.sidebar.write(f"🎂 **Age:** {st.session_state.age}")
    st.sidebar.write(f"♂️ **Gender:** {st.session_state.gender}")
    
    st.subheader("Upload or Capture Image")
    uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "png", "jpeg"])
    capture_image()

    if uploaded_file:
        image_path = f"static/{uploaded_file.name}"
        os.makedirs("static", exist_ok=True)
        with open(image_path, "wb") as f:
            f.write(uploaded_file.getbuffer())

        detected_objects, description = process_image(image_path, st.session_state.user_id)
        translated_description = translate_text(description, st.session_state.language)
        st.image(image_path, caption="Uploaded Image", width=400)
        st.write("### 📺 Detected Objects:", ", ".join(detected_objects))
        st.write("### 📚 Object Descriptions:", translated_description)
        audio_path = text_to_speech(translated_description, st.session_state.language)
        st.audio(audio_path, format="audio/mp3")


if not st.session_state.logged_in:
    login_page()
else:
    main_page()
