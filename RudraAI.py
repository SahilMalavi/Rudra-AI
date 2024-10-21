from PIL import Image
import streamlit as st
import datetime
import webbrowser
from gemini import gemini_response, gemini_IMGresponse
from gemini import create_chat

create_chat()

def rudra(query):
    try:
        # Logging the query
        print("\n ==> Master : ", query)
    
        if 'current time' in query or 'todays date' in query:
            if 'time' in query and 'date' in query:
                time = datetime.datetime.now().strftime('%I:%M %p')
                current_date = datetime.datetime.now().date()
                return f'Current time is {time} and Todays date is {current_date}'
            elif 'time' in query:
                time = datetime.datetime.now().strftime('%I:%M %p')
                return f'Current time is {time}'
            elif 'date' in query:
                current_date = datetime.datetime.now().date()
                return f'Todays date is {current_date}'

        elif 'open website' in query:
            if ".com" in query or ".in" in query or ".org" in query or ".online" in query or ".io" in query:
                openweb = query.replace("open", "").replace("website", "").strip()
                webbrowser.open(openweb)
                return f"Opening {openweb}"
            else:
                return "Please say a command like this: (example - open website youtube.com)"

        elif not query:
            return "Please say the command again."

        else:
            # Fetching response from Gemini
            response = gemini_response(query)
            print("\n ==> Rudra AI: ", response)
            return response

    except Exception as e:
        # Logging the exception to understand what went wrong
        print(f"Error occurred in 'rudra' function: {e}")
        return "An error occurred while executing the command."

def main():
    try:
        st.title("Rudra AI")
        #st.sidebar.title("ASK TO IMAGE")
        #uploaded_image = st.sidebar.file_uploader("Upload an image", type=["jpg", "jpeg", "png"])

        if "messages" not in st.session_state:
            st.session_state.messages = []

        prompt = ("From now, your name is Rudra. Hey Rudra, I am Sahil, and your task is to serve my queries or talk with me. "
                  "[Instruction for your purpose only, don't print this on screen: You are developed by me using Gemini API. "
                  "Please sometimes answer in only a single line and sometimes answer briefly point-wise according to the query, in English only.] Hi Rudra.")

        first_response = gemini_response(prompt)

        with st.chat_message('assistant'):
            st.markdown(first_response)

        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

        if uploaded_image is not None:
            image = Image.open(uploaded_image)
            st.image(image, caption="Uploaded Image")
            st.sidebar.write("Remove the image to go back to Rudra AI.")

            if prompt := st.chat_input("Ask to image"):
                prompt = prompt.lower()
                st.session_state.messages.append({"role": "user", "content": prompt})
                with st.chat_message("user"):
                    st.markdown(prompt)
                with st.chat_message("assistant"):
                    message_placeholder = st.empty()
                    try:
                        response = gemini_IMGresponse(prompt, image)
                        message_placeholder.markdown(response)
                        print("\n ==> Rudra Image AI:", response)
                    except Exception as e:
                        message_placeholder.markdown("An error occurred while processing the image query.")
                        print(f"Error with image AI: {e}")

                st.session_state.messages.append({"role": "assistant", "content": response})
        else:
            if prompt := st.chat_input("Ask Rudra"):
                prompt = prompt.lower()
                st.session_state.messages.append({"role": "user", "content": prompt})
                with st.chat_message("user"):
                    st.markdown(prompt)
                with st.chat_message("assistant"):
                    message_placeholder = st.empty()
                    try:
                        response = rudra(prompt)
                        message_placeholder.markdown(response)
                        print("\n ==> Rudra AI:", response)
                    except Exception as e:
                        message_placeholder.markdown("An error occurred while processing your query.")
                        print(f"Error occurred with text query: {e}")

                st.session_state.messages.append({"role": "assistant", "content": response})

    except Exception as e:
        st.write("We apologize for the inconvenience. Please check back in a few minutes.")
        print(f"An error occurred in 'main': {e}")

if __name__ == "__main__":
    main()
