import streamlit as st
from PIL import Image
import webbrowser
from gemini import gemini_response, gemini_IMGresponse, create_chat

create_chat()
def rudra(query):
    try:
        query = query.strip().lower()  # Normalize the query
        
        if query.startswith("open website"):
            # Extract the website from the query
            openweb = query[len("open website"):].strip()
            
            # Check if the user specified a valid URL
            if openweb:
                # Add 'https://' if not already present
                if not openweb.startswith(("http://", "https://")):
                    openweb = "https://" + openweb

                # Use the preferred browser for better compatibility
                try:
                    webbrowser.open_new_tab(openweb)
                    return f"Opening {openweb}"
                except:
                    return "Failed to open the browser. Please try manually."

            else:
                return "Please specify a valid website (e.g., 'open website youtube.com')"

        elif not query:
            return "Please write your command again."

        else:
            response = gemini_response(query)
            return response

    except Exception as e:
        print(f"Error in rudra function: {str(e)}")
        return "An error occurred while processing your query. Please try again later. " + str(e)
        
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
            Initial_prompt='''hey Rudra, I am Sahil your developer, your task is to serve my queries, or talk with me,
            you can also open any webpages on the internet, and your "ask to image" feature, powers you to interact with images, okay so hii Rudra [reply with 2-3 lines only]'''
            
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
                    response = rudra(prompt)
                    message_placeholder.markdown(response)
                st.session_state.messages.append({"role": "assistant", "content": response})

        elif choice == "Ask to Image":
            st.title("Rudra Image AI")
            st.sidebar.title("Ask to Image")
            uploaded_image = st.sidebar.file_uploader("Upload an image", type=["jpg", "jpeg", "png"])

            if uploaded_image is not None:
                image = Image.open(uploaded_image)
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
