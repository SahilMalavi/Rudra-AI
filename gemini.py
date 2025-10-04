import streamlit
import google.generativeai as ai
import os
import pathlib
import textwrap
import PIL.Image

# image = PIL.Image.open('meal.png')

# from IPython.display import display
from IPython.display import Markdown

def to_markdown(text):
    text = text.replace('•', '  *')
    return Markdown(textwrap.indent(text, '> ', predicate=lambda _: True))

ai.configure(api_key="AIzaSyAP8M_8zf_Ks-KryXGSsXSEZlyL8wDocy0")

def create_chat():
    model = ai.GenerativeModel('gemini-2.0-flash')
    chat = model.start_chat(history=[])
    return chat

chat = create_chat()

def gemini_response(input):
    response = chat.send_message(input)    
    return response.text 

def gemini_IMGresponse(prompt, img):
    model = ai.GenerativeModel('gemini-2.5-flash')
    response = model.generate_content([prompt, img], stream=True)
    response.resolve()
    return response.text
