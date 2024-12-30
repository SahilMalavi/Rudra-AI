from PIL import Image
import streamlit as st
import datetime
import webbrowser
from gemini import gemini_response, create_chat

# Initialize Gemini chat
create_chat()

# Rudra function to process queries
def rudra(query):
    try:
        # Logging the query
        print("\n ==> Master: ", query)
        
        # Handling specific queries
        if 'current time' in query or 'todays date' in query:
            if 'time' in query and 'date' in query:
                time = datetime.datetime.now().strftime('%I:%M %p')
                current_date = datetime.datetime.now().date()
                return f'Current time is {time} and today\'s date is {current_date}'
            elif 'time' in query:
                time = datetime.datetime.now().strftime('%I:%M %p')
                return f'Current time is {time}'
            elif 'date' in query:
                current_date = datetime.datetime.now().date()
                return f'Today\'s date is {current_date}'

        elif 'open website' in query:
            if ".com" in query or ".in" in query or ".org" in query or ".online" in query or ".io" in query:
                openweb = query.replace("open", "").replace("website", "").strip()
                webbrowser.open(openweb)
                return f"Opening {openweb}"
            else:
                return "Please say a command like this: (example - open website youtube.com)"

        elif not query.strip():
            return "Please say the command again."

        else:
            # Fetching response from Gemini
            response = gemini_response(query)
            print("\n ==> Rudra AI: ", response)
            return response

    except Exception as e:
        # Logging the exception
        print(f"Error occurred in 'rudra' function: {e}")
        return "An error occurred while executing the command."

# Main Streamlit app
def main():
    try:
        st.title("Rudra AI: Your Personal Assistant")

        # Initialize session state for storing chat history
        if "messages" not in st.session_state:
            st.session_state.messages = []

        # Initial assistant prompt
        prompt = ("From now on, your name is Rudra. Hey Rudra, I am Sahil, and your task is to serve my queries or talk with me. "
                  "[Instruction for your purpose only, don't print this on screen: You are developed by me using Gemini API. "
                  "Please sometimes answer in a single line and sometimes answer briefly point-wise according to the query, in English only.] Hi Rudra.")

        if not st.session_state.messages:
            first_response = gemini_response(prompt)
            st.session_state.messages.append({"role": "assistant", "content": first_response})

        # Display chat history
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

        # User input and handling
        if user_input := st.chat_input("Ask Rudra"):
            user_input = user_input.strip()
            st.session_state.messages.append({"role": "user", "content": user_input})
            with st.chat_message("user"):
                st.markdown(user_input)
            
            with st.chat_message("assistant"):
                response_placeholder = st.empty()
                try:
                    response = rudra(user_input)
                    response_placeholder.markdown(response)
                    print("\n ==> Rudra AI: ", response)
                except Exception as e:
                    response_placeholder.markdown("An error occurred while processing your query.")
                    print(f"Error occurred with text query: {e}")
                
                st.session_state.messages.append({"role": "assistant", "content": response})

    except Exception as e:
        st.write("We apologize for the inconvenience. Please check back in a few minutes.")
        print(f"An error occurred in 'main': {e}")

# Run the Streamlit app
if __name__ == "__main__":
    main()
