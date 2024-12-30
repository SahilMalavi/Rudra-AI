import streamlit as st
from PIL import Image
import webbrowser
from gemini import gemini_response, gemini_IMGresponse, create_chat

create_chat()

# Function to handle chat-based interaction
def rudra(query):
    try:
        print("\n ==> Master : ", query)
        if 'current time' in query or 'todays date' in query:
            if 'time' in query and 'date' in query:
                time = datetime.datetime.now().strftime('%I:%M %p')
                current_date = datetime.datetime.now().date()
                return 'Current time is ' + time + ' and ' + 'Todays date is ' + str(current_date)
            elif 'time' in query:
                time = datetime.datetime.now().strftime('%I:%M %p')
                return 'Current time is ' + time
            elif 'date' in query:
                current_date = datetime.datetime.now().date()
                return 'Todays date is ' + str(current_date)

        elif 'open website' in query:
            if ".com" in query or ".in" in query or ".org" in query or ".online" in query or ".io" in query:
                openweb = query.replace("open", "")
                openweb = openweb.replace("website", "")
                webbrowser.open(openweb)
                return "opening " + openweb
            else:
                return "please say command like this. (example-open website youtube.com )"

        elif not query:
            return "please say command again.."
        else:
            response = gemini_response(query)
            print()
            return response
    except Exception as e:
        return f"Error occurred: {str(e)}"

# Main Streamlit app function
def main():
    st.title("Rudra AI")

    # Radio button to choose between chat and ask to image
    choice = st.radio("Select Mode", ("Chat", "Ask to Image"))

    if choice == "Chat":
        st.sidebar.title("Chat with Rudra")
        # Chat prompt
        prompt = "hey Rudra, I am Sahil, your task is to serve my queries or talk with me."
        first_response = gemini_response(prompt)

        # Display initial assistant message
        with st.chat_message('assistant'):
            st.markdown(first_response)

        # Collect and display chat messages
        if "messages" not in st.session_state:
            st.session_state.messages = []

        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

        # Handle user input
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

    elif choice == "Ask to Image":
        st.sidebar.title("Ask to Image")
        uploaded_image = st.sidebar.file_uploader("Upload an image", type=["jpg", "jpeg", "png"])

        if uploaded_image is not None:
            image = Image.open(uploaded_image)
            st.title("Rudra Image AI")
            st.image(image, caption="Uploaded Image")

            if prompt := st.chat_input("Ask to Image"):
                prompt = prompt.lower()
                with st.chat_message("user"):
                    st.markdown(prompt)
                with st.chat_message("assistant"):
                    message_placeholder = st.empty()
                    response = gemini_IMGresponse(prompt, image)
                    message_placeholder.markdown(response)
                print("\n ==> Rudra Image AI :", response)

        else:
            st.sidebar.write("Please upload an image to start 'Ask to Image'")

if __name__ == "__main__":
    main()
