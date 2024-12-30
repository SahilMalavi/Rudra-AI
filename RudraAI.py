from PIL import Image
import streamlit as st
import datetime
import webbrowser
from gemini import gemini_response
from gemini import gemini_IMGresponse
from gemini import create_chat

create_chat()  # Initializes the chat with the Gemini API

# Function for responding to user queries
def rudra(query):
    try:
        print("\n ==> Master: ", query)

        # Handle queries for current time and today's date
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

        # Handle the open website command
        elif 'open website' in query:
            if ".com" in query or ".in" in query or ".org" in query or ".online" in query or ".io" in query:
                openweb = query.replace("open", "").replace("website", "").strip()
                webbrowser.open(openweb)
                return f"Opening {openweb}"
            else:
                return "Please specify a valid website. Example: open website youtube.com"

        # Commented out pywhatkit-dependent code for playing song on YouTube
        # elif 'play on youtube' in query:
        #     song = query.replace("play", "").replace("on youtube", "").strip()
        #     pywhatkit.playonyt(song)
        #     return "Playing your song on YouTube."

        # Default response for unrecognized commands
        elif not query:
            return "Please enter a command or ask a question."

        # If the query is valid, pass it to Gemini API for processing
        else:
            response = gemini_response(query)
            return response

    except Exception as e:
        print(f"Error: {e}")
        return "An error occurred while processing your request."

# Main function to handle Streamlit interface
def main():
    st.title("Rudra AI")

    # Sidebar for image upload
    st.sidebar.title("ASK TO IMAGE")
    uploaded_image = st.sidebar.file_uploader("Upload an image", type=["jpg", "jpeg", "png"])

    # Initialize session state for messages if not already done
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Instruction to start the chat (prompt for the AI)
    prompt = """Hey Rudra, I am Sahil. Your task is to serve my queries, or talk with me. [Instruction for you purpose only: 
                Please sometimes answer in only a single line and sometimes answer briefly in a point-wise format 
                according to the query. Answer only in English. You can also open any websites on the internet. 
                For example, you can respond to the command [open website youtube.com] or play a song with [play on youtube 'song'].
                Please respond to the command [what is current time] to know the current time, and [what is today's date] to know today's date.]"""
    
    # Get the first response based on the prompt
    first_response = gemini_response(prompt)
    with st.chat_message('assistant'):
        st.markdown(first_response)

    # Display previous messages from the chat history
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Handle image upload and interaction
    if uploaded_image is not None:
        image = Image.open(uploaded_image)
        st.title("Rudra Image AI")
        st.image(image, caption="Uploaded Image")
        st.sidebar.write("Remove image to go back to Rudra AI")

        # Process user input for image-based queries
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
    
    # Handle text-based queries for AI
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
