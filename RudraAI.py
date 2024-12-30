import time
import datetime
from PIL import Image
import streamlit as st
import webbrowser

# Importing the necessary functions from gemini module
from gemini import gemini_response, gemini_IMGresponse, create_chat

# Initialize chat
create_chat()

def gemini_response_with_retry(input, retries=5, backoff=2):
    """
    Send a request to Gemini API with retries in case of ResourceExhausted error.
    
    Args:
        input (str): The input for generating content.
        retries (int): Number of retry attempts.
        backoff (int): The initial delay between retries (exponential backoff).
        
    Returns:
        str: The response from Gemini or a fallback message.
    """
    try:
        # Call the original gemini_response function to get the response from Gemini API
        response = gemini_response(input)
        return response
    
    except ResourceExhausted as e:
        # If ResourceExhausted error occurs, retry with exponential backoff
        if retries > 0:
            print(f"Rate limit exceeded. Retrying in {backoff} seconds...")
            time.sleep(backoff)  # Wait before retrying
            return gemini_response_with_retry(input, retries - 1, backoff * 2)  # Exponential backoff
        else:
            # If max retries are reached, return a fallback message
            print("Max retries reached. Please try again later.")
            return "Service temporarily unavailable. Please try again later."

def rudra(query):
    """
    Function to process user queries and return a response from Gemini or specific commands.
    
    Args:
        query (str): The user query or command.
        
    Returns:
        str: The response to the user's query.
    """
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
                return "Please say command like this. (example-open website youtube.com )"

        elif 'play on youtube' in query:
            song = query.replace("play", "")
            song = song.replace("on youtube", "")
            return f"Playing {song} on YouTube."

        elif not query:
            return "Please say command again.."

        else:
            # Use gemini_response_with_retry function to handle retries on failure
            response = gemini_response_with_retry(query)
            return response

    except Exception as e:
        return f"An error occurred: {str(e)}"

def main():
    """
    Main function to drive the Streamlit app.
    """
    st.title("Rudra AI")

    st.sidebar.title("ASK TO IMAGE")
    uploaded_image = st.sidebar.file_uploader("Upload an image", type=["jpg", "jpeg", "png"])

    if "messages" not in st.session_state:
        st.session_state.messages = []

    prompt = "Hey Rudra, I am Sahil. Your task is to serve my queries or talk with me. [Instruction: Please answer sometimes in a single line and sometimes briefly in points based on the query.]"

    first_response = gemini_response_with_retry(prompt)

    with st.chat_message('assistant'):
        st.markdown(first_response)

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

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
