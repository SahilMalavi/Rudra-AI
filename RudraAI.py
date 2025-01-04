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
    st.session_state.pdf_text = None  # None indicates no PDF uploaded
if "pdf_uploaded" not in st.session_state:
    st.session_state.pdf_uploaded = None
if "image_messages" not in st.session_state:
    st.session_state.image_messages = []

def main():
    try:
        st.sidebar.title("Rudra AI Assistant")
        current_mode = st.sidebar.radio("Select Mode", ("Chat", "Ask to Image", "Chat with PDF"))

        # --- Chat Mode ---
        if current_mode == "Chat":
            st.title("Rudra AI Chat")
            for message in st.session_state.chat_messages:
                with st.chat_message(message["role"]):
                    st.markdown(message["content"])
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
            if uploaded_image:
                image = Image.open(uploaded_image)
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

        # --- Chat with PDF Mode ---
        elif current_mode == "Chat with PDF":
            st.title("Chat with PDF")

            # File uploader and persist the PDF
            uploaded_pdf = st.sidebar.file_uploader("Upload a PDF", type=["pdf"])

            # Only process new PDFs
            if uploaded_pdf and uploaded_pdf != st.session_state.pdf_uploaded:
                st.session_state.pdf_uploaded = uploaded_pdf
                st.session_state.pdf_text = extract_text_from_pdf(uploaded_pdf)
                st.session_state.pdf_messages = []  # Clear chat for the new PDF
                st.success("PDF Uploaded Successfully!")

            # Clear PDF button
            if st.session_state.pdf_text and st.sidebar.button("❌ Clear PDF"):
                st.session_state.pdf_uploaded = None
                st.session_state.pdf_text = None
                st.session_state.pdf_messages = []
                st.warning("PDF Removed!")

            # Show PDF chat if a PDF exists
            if st.session_state.pdf_text:
                st.info("✅ PDF loaded. Ask questions below.")
                for message in st.session_state.pdf_messages:
                    with st.chat_message(message["role"]):
                        st.markdown(message["content"])

                # Handle PDF-based conversation
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
