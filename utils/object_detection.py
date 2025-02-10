from ultralytics import YOLO
import google.generativeai as genai
from utils.database import insert_history, get_user_age
from PIL import Image

yolo_model = YOLO("models/yolov8n.pt")

genai.configure(api_key="AIzaSyBfeSRXmhXJyX_CyP_dzlbtBLVxMJ8b88Q")

def detect_objects_yolo(image_path):
    results = yolo_model(image_path)

    detected_objects = []
    for result in results:
        for box in result.boxes:
            class_id = int(box.cls[0])
            confidence = float(box.conf[0])
            if confidence > 0.5:
                detected_objects.append(yolo_model.names[class_id])

    return detected_objects

def detect_objects_gemini(image_path):
    
    try:
        img = Image.open(image_path)
        model = genai.GenerativeModel("gemini-1.5-flash")
        response = model.generate_content(["Describe the objects in this image.", img])

        if response and response.text:
            detected_objects = response.text.split(", ")  
            return detected_objects
        else:
            return []
    except Exception as e:
        print(f"Error using Gemini API: {e}")
        return []

def get_object_descriptions(objects, user_age):
    if not objects:
        return [], "No objects detected."

    object_prompt = f"Only detect the object in the image and respond with only object names: {', '.join(objects)}."
    model = genai.GenerativeModel("gemini-1.5-flash")
    response_objects = model.generate_content(object_prompt)

    if response_objects and response_objects.text:
        short_objects = [obj.strip() for obj in response_objects.text.split(",") if obj.strip()]
    else:
        short_objects = objects  

    
    description_prompt = f"Explain the following objects in simple terms for a {user_age}-year-old: {', '.join(short_objects)}. as per age use complexity and keep it to 1-2 sentence"
    print(user_age)
    response_description = model.generate_content(description_prompt)

    description = response_description.text if response_description and response_description.text else "Description not available."

    return short_objects, description

def process_image(image_path, user_id, lang="en"):
    detected_objects = detect_objects_yolo(image_path)

    if not detected_objects:
        detected_objects = detect_objects_gemini(image_path)
        if isinstance(detected_objects, str):  
            detected_objects = [detected_objects]  

    user_age = get_user_age(user_id) or 4 

    short_objects, description = get_object_descriptions(detected_objects, user_age)

    insert_history(user_id, image_path, description)

    return short_objects, description
