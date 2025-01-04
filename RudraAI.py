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

# Initialize session state only once
if "chat_messages" not in st.session_state:
    st.session_state.chat_messages = []
if "pdf_messages" not in st.session_state:
    st.session_state.pdf_messages = []
if "pdf_text" not in st.session_state:
    st.session_state.pdf_text = ""
if "image_messages" not in st.session_state:
    st.session_state.image_messages = []

# Main Streamlit app function
def main():
    try:
        st.sidebar.title("Rudra AI Assistant")

        # Mode selection with unique keys to avoid overlap
        choice = st.sidebar.radio("Select Mode", ("Chat", "Ask to Image", "Chat with PDF"))

        # --- Chat Mode ---
        if choice == "Chat":
            st.title("Rudra AI Chat")
            st.sidebar.title("Chat with Rudra")

            # Display previous chat messages
            for message in st.session_state.chat_messages:
                with st.chat_message(message["role"]):
                    st.markdown(message["content"])

            # Handle user input for chat mode
            if prompt := st.chat_input("Ask Rudra"):
                st.session_state.chat_messages.append({"role": "user", "content": prompt})
                with st.chat_message("user"):
                    st.markdown(prompt)
                with st.chat_message("assistant"):
                    response = gemini_response(prompt)
                    st.markdown(response)
                st.session_state.chat_messages.append({"role": "assistant", "content": response})

        # --- Ask to Image Mode ---
        elif choice == "Ask to Image":
            st.title("Rudra Image AI")
            uploaded_image = st.sidebar.file_uploader("Upload an image", type=["jpg", "jpeg", "png"])

            if uploaded_image:
                image = Image.open(uploaded_image)
                st.image(image, caption="Uploaded Image")

                # Display previous image-based messages
                for message in st.session_state.image_messages:
                    with st.chat_message(message["role"]):
                        st.markdown(message["content"])

                if prompt := st.chat_input("Ask about the image"):
                    st.session_state.image_messages.append({"role": "user", "content": prompt})
                    with st.chat_message("user"):
                        st.markdown(prompt)
                    with st.chat_message("assistant"):
                        try:
                            response = gemini_IMGresponse(prompt, image)
                            st.markdown(response)
                        except Exception as e:
                            response = f"Error: {str(e)}"
                            st.error(response)
                        st.session_state.image_messages.append({"role": "assistant", "content": response})

        # --- Chat with PDF Mode ---
        elif choice == "Chat with PDF":
            st.title("Chat with PDF")
            uploaded_pdf = st.sidebar.file_uploader("Upload a PDF", type=["pdf"])

            # Load PDF content once and store in session state
            if uploaded_pdf and st.session_state.pdf_text == "":
                st.session_state.pdf_text = extract_text_from_pdf(uploaded_pdf)

            # Display previous PDF chat messages
            for message in st.session_state.pdf_messages:
                with st.chat_message(message["role"]):
                    st.markdown(message["content"])

            # If PDF is uploaded and chat is active
            if st.session_state.pdf_text:
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
        st.error(f"An unexpected error occurred: {str(e)}")

if __name__ == "__main__":
    main()
