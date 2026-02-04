import google.generativeai as ai
import os
from dotenv import load_dotenv
from PIL import Image
import io

load_dotenv()

api_key = os.getenv("GOOGLE_API_KEY")
ai.configure(api_key=api_key)

def create_chat():
    model = ai.GenerativeModel('gemini-2.5-flash')  # Updated to available model
    chat = model.start_chat(history=[])
    # Send initial system prompt
    initial_prompt = """You are Rudra, a personal assistant created by Sahil Malavi. 
You can find more about Sahil on LinkedIn: https://www.linkedin.com/in/sahil-malavi/ 
and his portfolio at https://sahilmalavi-dev.vercel.app. 
Provide concise, helpful, and to-the-point responses. Avoid unnecessary details to save tokens. 
When introducing yourself, you can mention these links if relevant."""
    chat.send_message(initial_prompt)
    return chat

def gemini_response(input_text, chat=None):
    if chat is None:
        model = ai.GenerativeModel('gemini-2.5-flash')
        response = model.generate_content(input_text)
    else:
        response = chat.send_message(input_text)
    return response.text

def gemini_IMGresponse(prompt, img):
    model = ai.GenerativeModel('gemini-2.5-flash')
    response = model.generate_content([prompt, img], stream=True)
    response.resolve()
    return response.text

def process_image_from_bytes(image_bytes, prompt):
    """Process image from bytes data"""
    image = Image.open(io.BytesIO(image_bytes))
    return gemini_IMGresponse(prompt, image)