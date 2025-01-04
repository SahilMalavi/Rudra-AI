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

# Main Streamlit app function
def main():
    try:
        st.sidebar.title("Rudra AI Assistant")

        # Mode selection
        choice = st.sidebar.radio("Select Mode", ("Chat", "Ask to Image", "Chat with PDF"), index=0)  # Default is "Chat"

        if choice == "Chat":
            st.title("Rudra AI Chat")
            st.sidebar.title("Chat with Rudra")
            Initial_prompt='''hey Rudra, I am Sahil your developer, your task is to serve my queries, or talk with me,
            and your "ask to image" feature, powers you to interact with images, okay so hii Rudra [reply with 2-3 lines only]'''
            
            # Display initial assistant message
            with st.chat_message('assistant'):
                st.markdown(Initial_prompt)

            if "messages" not in st.session_state:
                st.session_state.messages = []

            # Collect and display chat messages
            for message in st.session_state.messages:
                with st.chat_message(message["role"]):
                    st.markdown(message["content"])

            # Handle user input
            if prompt := st.chat_input("Ask Rudra"):
                st.session_state.messages.append({"role": "user", "content": prompt})
                with st.chat_message("user"):
                    st.markdown(prompt)
                with st.chat_message("assistant"):
                    response = gemini_response(prompt)
                    st.markdown(response)
                st.session_state.messages.append({"role": "assistant", "content": response})

        elif choice == "Ask to Image":
            st.title("Rudra Image AI")
            st.sidebar.title("Ask to Image")
            uploaded_image = st.sidebar.file_uploader("Upload an image", type=["jpg", "jpeg", "png"])

            if uploaded_image:
                image = Image.open(uploaded_image)
                st.image(image, caption="Uploaded Image")

                if prompt := st.chat_input("Ask to Image"):
                    with st.chat_message("user"):
                        st.markdown(prompt)
                    with st.chat_message("assistant"):
                        try:
                            response = gemini_IMGresponse(prompt, image)
                            st.markdown(response)
                        except Exception as e:
                            st.markdown(f"Error: {str(e)}")

        elif choice == "Chat with PDF":
            st.title("Chat with PDF")
            uploaded_pdf = st.sidebar.file_uploader("Upload a PDF", type=["pdf"])
            pdf_text = ""

            if uploaded_pdf:
                pdf_text = extract_text_from_pdf(uploaded_pdf)
                st.sidebar.success("PDF uploaded successfully!")

                if prompt := st.chat_input("Ask Rudra about the PDF"):
                    combined_prompt = f"Based on the provided PDF content:\n{pdf_text}\n\n{prompt}"
                    response = gemini_response(combined_prompt)
                    st.markdown(response)
            else:
                st.warning("Please upload a PDF file to start chatting with it.")

    except Exception as e:
        print(f"Error in main function: {str(e)}")
        st.error(f"An unexpected error occurred. Please try again later. {str(e)}")

if __name__ == "__main__":
    main()
