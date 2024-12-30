import streamlit as st
from PIL import Image

# Define gemini_response and gemini_IMGresponse functions (you may need to replace these with your actual functions)
def gemini_response(prompt):
    # Placeholder function for Gemini response (AI)
    return "This is the response to your prompt: " + prompt

def gemini_IMGresponse(prompt, image):
    # Placeholder function for Gemini Image response
    return "This is the response based on the image and prompt: " + prompt

def rudra(prompt):
    # Placeholder for the rudra AI response
    return "This is Rudra's response: " + prompt

def main():
    st.title("Rudra AI")

    # Sidebar: Added options for navigating between different modes
    st.sidebar.title("Navigation")
    mode = st.sidebar.radio("Choose Mode", ["Chat with Rudra", "Ask to Image"])

    if "messages" not in st.session_state:
        st.session_state.messages = []

    prompt = "Hey Rudra, I am Sahil. Your task is to serve my queries, or talk with me. You can answer in a single line or point-wise, and you can also open web pages. Enter commands like [open website youtube.com], [play on youtube 'song'], [what is current time], or [what is today's date]."

    if mode == "Chat with Rudra":
        # First interaction with the AI
        first_response = gemini_response(prompt)

        with st.chat_message('assistant'):
            st.markdown(first_response)

        # Displaying previous messages
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

        # Regular chat input
        if prompt := st.chat_input("Ask Rudra"):
            prompt = prompt.lower()
            st.session_state.messages.append({"role": "user", "content": prompt})
            with st.chat_message("user"):
                st.markdown(prompt)
            with st.chat_message("assistant"):
                message_placeholder = st.empty()
                response = rudra(prompt)
                message_placeholder.markdown(response)
                st.session_state.messages.append({"role": "assistant", "content": response})

    elif mode == "Ask to Image":
        # Ask to image section
        uploaded_image = st.sidebar.file_uploader("Upload an image", type=["jpg", "jpeg", "png"])

        if uploaded_image is not None:
            image = Image.open(uploaded_image)
            st.title("Rudra Image AI")
            st.image(image, caption="Uploaded Image")
            st.sidebar.write("Remove image to go back to Rudra AI")

            if prompt := st.chat_input("Ask to image"):
                prompt = prompt.lower()
                st.session_state.messages.append({"role": "user", "content": prompt})
                with st.chat_message("user"):
                    st.markdown(prompt)
                with st.chat_message("assistant"):
                    message_placeholder = st.empty()
                    response = gemini_IMGresponse(prompt, image)
                    message_placeholder.markdown(response)
                    st.session_state.messages.append({"role": "assistant", "content": response})
        else:
            st.sidebar.write("Please upload an image to ask about it.")
    

if __name__ == "__main__":
    main()
