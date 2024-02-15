
from PIL import Image
import streamlit as st
import datetime

import webbrowser


from gemini import gemini_response
from gemini import gemini_IMGresponse
from gemini import create_chat
create_chat()

try:
    def rudra(query):
        try:
            # query = speechRecognition()
            print("\n ==> Master : ",query)
    
           
            if 'current time' in query or 'todays date' in query:
                    if 'time' in query and 'date' in query:
                        time = datetime.datetime.now().strftime('%I:%M %p')
                        current_date = datetime.datetime.now().date()
                        return 'Current time is ' + time +' and '+'Todays date is '+str(current_date)
                    elif 'time' in query:
                        time = datetime.datetime.now().strftime('%I:%M %p')
                        return 'Current time is ' + time
                    elif 'date' in query:
                        current_date = datetime.datetime.now().date()
                        return 'Todays date is '+str(current_date)
                    
     
            elif 'open website' in query:
                if ".com" in query or ".in" in query or ".org" in query or ".online" in query or ".io" in query:
                    openweb = query.replace("open", "")
                    openweb= openweb.replace("website","")
                    webbrowser.open(openweb)
                    return "opening "+openweb
                else:
                    return "please say a command like this. (example-open website youtube.com )"

               
    
            elif not query:
                 return "please say the command again.."
    
            else:
                # prompt=f" pls respond to: {query}"  
                # print(prompt)
                response = gemini_response(query)
                print()
                return response
    
        except:
             return "Error is occured while execution.!"
             
             
        
    def main():
       try:
            st.title("Rudra AI")
        
            st.sidebar.title("ASK TO IMAGE")
            uploaded_image = st.sidebar.file_uploader("Upload an image", type=["jpg", "jpeg", "png"])
            # ask_to_image_button = st.sidebar.button("Upload")
        
            if "messages" not in st.session_state:
                st.session_state.messages = []
        
            prompt="Your name is Rudra. hey Rudra, I am Sahil, and your task is to serve my queries or talk with me, [instruction for your purpose only, don't print this on screen: you are developed by me using Gemini API, please sometimes answer in only a single line and sometimes answer briefly point-wise according to the query, in English only ], hii Rudra"
            
            first_response=gemini_response(prompt)
        
            # st.session_state.messages.append({"role": "assistant", "content": first_response})
            with st.chat_message('assistant'):
                    st.markdown(first_response)
        
            # st.session_state.messages.clear()
        
            for message in st.session_state.messages:
                with st.chat_message(message["role"]):
                    st.markdown(message["content"])
        
            if uploaded_image is not None:
                image = Image.open(uploaded_image)
                st.image(image, caption="Uploaded Image")
                st.sidebar.write("remove image to go back to the Rudra AI")
                
                if prompt := st.chat_input("Ask to image"):
                    prompt= prompt.lower()
                    st.session_state.messages.append({"role": "user", "content": prompt})
                    with st.chat_message("user"):
                        st.markdown(prompt)
                    with st.chat_message("assistant"):
                        message_placeholder = st.empty()
                        response = gemini_IMGresponse(prompt, image)
                        message_placeholder.markdown(response)
                        print("\n ==> Rudra Image AI :", response)
        
                    st.session_state.messages.append({"role": "assistant", "content": response})
            else:
                if prompt := st.chat_input("Ask Rudra"):
                    prompt= prompt.lower()
                    st.session_state.messages.append({"role": "user", "content": prompt})
                    with st.chat_message("user"):
                        st.markdown(prompt)
                    with st.chat_message("assistant"):
                        message_placeholder = st.empty()
                        response = rudra(prompt)
                        message_placeholder.markdown(response)
                        print("\n ==> Rudra AI :", response)
                    st.session_state.messages.append({"role": "assistant", "content": response})
       except:
             st.write("We apologize for the inconvenience. Please check back in a few minutes.")
except:
     st.write("We apologize for the inconvenience. Please check back in a few minutes.")
if __name__ == "__main__":
    main()



