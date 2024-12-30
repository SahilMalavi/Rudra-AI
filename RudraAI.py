def main():
    try:
        st.title("Rudra AI")
        print("Initialized Rudra AI title in Streamlit.")
        
        if "messages" not in st.session_state:
            st.session_state.messages = []
            print("Initialized session state.")

        prompt = ("From now, your name is Rudra. Hey Rudra, I am Sahil, and your task is to serve my queries or talk with me. "
                  "[Instruction for your purpose only, don't print this on screen: You are developed by me using Gemini API. "
                  "Please sometimes answer in only a single line and sometimes answer briefly point-wise according to the query, in English only.] Hi Rudra.")
        
        first_response = gemini_response(prompt)
        print(f"Received first response from Gemini: {first_response}")

        with st.chat_message('assistant'):
            st.markdown(first_response)

        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

        if prompt := st.chat_input("Ask Rudra"):
            print(f"User input received: {prompt}")
            prompt = prompt.lower()
            st.session_state.messages.append({"role": "user", "content": prompt})
            with st.chat_message("user"):
                st.markdown(prompt)
            with st.chat_message("assistant"):
                message_placeholder = st.empty()
                try:
                    response = rudra(prompt)
                    print(f"Rudra AI response: {response}")
                    message_placeholder.markdown(response)
                except Exception as e:
                    print(f"Error in processing Rudra query: {e}")
                    message_placeholder.markdown("An error occurred while processing your query.")
            st.session_state.messages.append({"role": "assistant", "content": response})

    except Exception as e:
        st.write("We apologize for the inconvenience. Please check back in a few minutes.")
        print(f"An error occurred in 'main': {e}")
