import streamlit as st
from PIL import Image
import webbrowser
from gemini import gemini_response, gemini_IMGresponse, create_chat

create_chat()

# Function to handle chat-based interaction with error handling
# def rudra(query):
    # try:
    #     print("\n ==> Master : ", query)
    #     if 'current time' in query or 'todays date' in query:
    #         if 'time' in query and 'date' in query:
    #             time = datetime.datetime.now().strftime('%I:%M %p')
    #             current_date = datetime.datetime.now().date()
    #             return 'Current time is ' + time + ' and ' + 'Todays date is ' + str(current_date)
    #         elif 'time' in query:
    #             time = datetime.datetime.now().strftime('%I:%M %p')
    #             return 'Current time is ' + time
    #         elif 'date' in query:
    #             current_date = datetime.datetime.now().date()
    #             return 'Todays date is ' + str(current_date)

#         elif 'open website' in query:
#             if ".com" in query or ".in" in query or ".org" in query or ".online" in query or ".io" in query:
#                 openweb = query.replace("open", "")
#                 openweb = openweb.replace("website", "")
#                 webbrowser.open(openweb)
#                 return "Opening " + openweb
#             else:
#                 return "Please specify the website (e.g., open website youtube.com)"

#         elif not query:
#             return "Please write your command again."
#         else:
#             response = gemini_response(query)
#             return response
#     except Exception as e:
#         print(f"Error in rudra function: {str(e)}")
#         return "An error occurred while processing your query. Please try again later."

# Main Streamlit app function 
def main():
    try:

        # Radio button in the sidebar to choose between chat and ask to image
        choice = st.sidebar.radio("Select Mode", ("Chat", "Ask to Image"), index=0)  # Default to "Chat"

        if choice == "Chat":
            st.title("Rudra AI")
            st.sidebar.title("Chat with Rudra")
            # Chat prompt
            # prompt = "Hey Rudra, I am Sahil, your task is to serve my queries or talk with me."
            Initial_prompt='''hey Rudra, i am Sahil, your task is to serve my query's, or talk with me,
            [instruction for you purpose only: please sometime answer in only single line and sometime answer briefly point wise according to the query,in english 
            only, you can also able to open any webpages on the internet, you only tell user to enter [open website youtube.com] this command, 
            play any song on youtube when user enter command [play on youtube],you only tell user to enter [play on youtube 'song'] this command.
            only tell user to enter [what is current time] this command to know current time,only tell user to enter [what is todays date] this command, 
            to know todays date],okay so hii rudra'''
            
            first_response = gemini_response(Initial_prompt)

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
                    response = gemini_response(prompt)
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
                        try:
                            response = gemini_IMGresponse(prompt, image)
                            message_placeholder.markdown(response)
                        except Exception as e:
                            print(f"Error in Ask to Image: {str(e)}")
                            message_placeholder.markdown("An error occurred while processing the image. Please try again.")
                else:
                    st.warning("Please type a query to proceed with the 'Ask to Image' mode.")

            else:
                st.sidebar.write("Please upload an image to start 'Ask to Image'")

    except Exception as e:
        print(f"Error in main function: {str(e)}")
        st.error("An unexpected error occurred. Please try again later.",str(e))

if __name__ == "__main__":
    main()
