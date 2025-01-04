import streamlit as st
from PIL import Image
from gemini import gemini_response, gemini_IMGresponse, create_chat
from PyPDF2 import PdfReader

create_chat()

def extract_text_from_pdf(uploaded_file):
    reader = PdfReader(uploaded_file)
    text = ""
    for page in reader.pages:
        page_text = page.extract_text()
        if page_text:
            text += page_text + "\n"
    return text

# Initialize session state variables
if "chat_messages" not in st.session_state:
    st.session_state.chat_messages = []
if "pdf_messages" not in st.session_state:
    st.session_state.pdf_messages = []
if "pdf_text" not in st.session_state:
    st.session_state.pdf_text = None
if "pdf_uploaded" not in st.session_state:
    st.session_state.pdf_uploaded = None
if "image_messages" not in st.session_state:
    st.session_state.image_messages = []
if "image_uploaded" not in st.session_state:
    st.session_state.image_uploaded = None

def main():
    try:
        st.sidebar.title("Rudra AI Assistant")
        current_mode = st.sidebar.radio("Select Mode", ("Chat", "Ask to Image", "Chat with PDF"))

        
        # --- Chat Mode ---
        if current_mode == "Chat":
            st.title("Rudra AI Chat")
            Initial_prompt = '''Hey, from now you are Rudra, the personal AI assistant. You are aware that your developer's name is Sahil. 
Your task is to serve queries and assist with various tasks. You also have the "ask to image" feature that allows you to interact with images, 
and the "chat with PDF" feature to help with document-based queries. You will never use informal greetings like "hii Sahil" or anything similar.
You should address the user professionally at all times. Please respond with concise and helpful information.'''

            # Initial_prompt = '''Hey, from now you are Rudra, the personal AI assistant. You are aware that your developer's name is Sahil. 
            # Your task is to serve queries and assist with various tasks. You have the "ask to image" feature that allows you to interact with images, 
            # and the "chat with PDF" feature to help with document-based queries. 
            
            # When interacting with the user, always greet them politely and professionally, but avoid informal greetings like "hi Sahil" or anything similar. 
            # For example, start with something like "Hello, how can I assist you today?" or a similar professional greeting.'''

            # Generate the first response with the initial prompt
            first_response = gemini_response(Initial_prompt)

            # Display the initial response
            with st.chat_message('assistant'):
                st.markdown(first_response)

            # Display previous chat messages if any
            if 'chat_messages' not in st.session_state:
                st.session_state.chat_messages = []

            # Show the conversation history
            for message in st.session_state.chat_messages:
                with st.chat_message(message["role"]):
                    st.markdown(message["content"])

            # User input handling
            if prompt := st.chat_input("Ask Rudra"):
                st.session_state.chat_messages.append({"role": "user", "content": prompt})
                with st.chat_message("user"):
                    st.markdown(prompt)
                with st.chat_message("assistant"):
                    response = gemini_response(prompt)
                    st.markdown(response)
                st.session_state.chat_messages.append({"role": "assistant", "content": response})
                
        # --- Ask to Image Mode ---
        elif current_mode == "Ask to Image":
            st.title("Rudra Image AI")
            uploaded_image = st.sidebar.file_uploader("Upload an image", type=["jpg", "jpeg", "png"])

            # Prevent resetting on mode switch
            if uploaded_image and uploaded_image != st.session_state.image_uploaded:
                st.session_state.image_uploaded = uploaded_image
                st.session_state.image_messages = []  # Clear chat for new image

            # Clear Image Button
            if st.session_state.image_uploaded and st.sidebar.button("❌ Clear Image"):
                st.session_state.image_uploaded = None
                st.session_state.image_messages = []
                st.warning("Image Removed!")

            # Display Image and Handle Chat
            if st.session_state.image_uploaded:
                image = Image.open(st.session_state.image_uploaded)
                st.image(image, caption="Uploaded Image")
                for message in st.session_state.image_messages:
                    with st.chat_message(message["role"]):
                        st.markdown(message["content"])
                if prompt := st.chat_input("Ask about the image"):
                    st.session_state.image_messages.append({"role": "user", "content": prompt})
                    with st.chat_message("user"):
                        st.markdown(prompt)
                    with st.chat_message("assistant"):
                        response = gemini_IMGresponse(prompt, image)
                        st.markdown(response)
                    st.session_state.image_messages.append({"role": "assistant", "content": response})
            else:
                st.warning("Please upload an image to start chatting.")

        # --- Chat with PDF Mode ---
        elif current_mode == "Chat with PDF":
            st.title("Chat with PDF")
            uploaded_pdf = st.sidebar.file_uploader("Upload a PDF", type=["pdf"])

            # Only process a new PDF
            if uploaded_pdf and uploaded_pdf != st.session_state.pdf_uploaded:
                st.session_state.pdf_uploaded = uploaded_pdf
                st.session_state.pdf_text = extract_text_from_pdf(uploaded_pdf)
                st.session_state.pdf_messages = []

            # Clear PDF Button
            if st.session_state.pdf_text and st.sidebar.button("❌ Clear PDF"):
                st.session_state.pdf_uploaded = None
                st.session_state.pdf_text = None
                st.session_state.pdf_messages = []
                st.warning("PDF Removed!")

            # Display PDF Chat
            if st.session_state.pdf_text:
                st.info("✅ PDF loaded. Ask questions below.")
                for message in st.session_state.pdf_messages:
                    with st.chat_message(message["role"]):
                        st.markdown(message["content"])
                if prompt := st.chat_input("Ask Rudra about the PDF"):
                    st.session_state.pdf_messages.append({"role": "user", "content": prompt})
                    with st.chat_message("user"):
                        st.markdown(prompt)
                    with st.chat_message("assistant"):
                        combined_prompt = f"Based on the PDF content:\n{st.session_state.pdf_text}\n\n{prompt}"
                        response = gemini_response(combined_prompt)
                        st.markdown(response)
                    st.session_state.pdf_messages.append({"role": "assistant", "content": response})
            else:
                st.warning("Please upload a PDF to start chatting.")

    except Exception as e:
        st.error(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    main()
