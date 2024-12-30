from PIL import Image
import streamlit as st
import datetime
import webbrowser
from gemini import gemini_response
from gemini import gemini_IMGresponse
from gemini import create_chat

create_chat()

# Handling the ResourceExhausted error and retry logic
def gemini_response_with_retry(input, retries=3):
    try:
        return gemini_response(input)
    except Exception as e:
        if retries > 0 and 'ResourceExhausted' in str(e):
            return gemini_response_with_retry(input, retries - 1)
        else:
            return "Service temporarily unavailable. Please try again later."

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
                return "Opening " + openweb
            else:
                return "Please say command like this: (example-open website youtube.com )"

        elif 'play on youtube' in query:
            song = query.replace("play", "")
            song = song.replace("on youtube", "")
            # Commented out the pywhatkit dependency
            # pywhatkit.playonyt(song)
            return "Playing."

        elif not query:
            return "Please say command again.."

        else:
            # Using the gemini_response_with_retry to handle resource exhaustion
            response = gemini_response_with_retry(query)
            return response

    except Exception as e:
        return f"Error occurred: {str(e)}"

# Handling exceptions during "Ask to Image" feature
def ask_to_image_with_retry(uploaded_image, prompt):
    try:
        image = Image.open(uploaded_image)
        # Using the gemini_IMGresponse function to get response for the image and prompt
        return gemini_IMGresponse(prompt, image)
    except Exception as e:
        return f"An error occurred while processing the image: {str(e)}"

def main():
    st.title("Rudra AI")

    st.sidebar.title("ASK TO IMAGE")
    uploaded_image = st.sidebar.file_uploader("Upload an image", type=["jpg", "jpeg", "png"])

    if "messages" not in st.session_state:
        st.session_state.messages = []

    prompt = "Hey Rudra, I am Sahil, your task is to serve my queries or talk with me. Please respond concisely or in detail based on the query."

    first_response = gemini_response_with_retry(prompt)

    with st.chat_message('assistant'):
        st.markdown(first_response)

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if uploaded_image is not None:
        try:
            st.title("Rudra Image AI")
            st.image(uploaded_image, caption="Uploaded Image")
            st.sidebar.write("Remove image to go back to Rudra AI")
            
            if prompt := st.chat_input("Ask to image"):
                prompt = prompt.lower()
                st.session_state.messages.append({"role": "user", "content": prompt})
                
                with st.chat_message("user"):
                    st.markdown(prompt)

                with st.chat_message("assistant"):
                    message_placeholder = st.empty()
                    response = ask_to_image_with_retry(uploaded_image, prompt)
                    message_placeholder.markdown(response)
                
                st.session_state.messages.append({"role": "assistant", "content": response})
        
        except Exception as e:
            st.sidebar.write(f"Error: {str(e)}")
            st.sidebar.write("There was an issue processing the image. Please try again.")

    else:
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

if __name__ == "__main__":
    main()
