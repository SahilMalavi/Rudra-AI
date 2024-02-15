from PIL import Image
# import pywhatkit
import streamlit as st
import datetime
# import pyttsx3
# import speech_recognition as sr
import webbrowser
# import pywhatkit
# import pyaudio

from gemini import gemini_response
from gemini import gemini_IMGresponse
from gemini import create_chat
create_chat()


# def speak(text):
#     print("\n ==> Rudra AI :",text)
#     print("")
#     engi.say(text)
#     engi.runAndWait()

# def hello():
#     hour = int(datetime.datetime.now().hour)
#     if 0 <= hour < 12:
#         speak("Good Morning master")

#     elif hour >= 12 and hour < 18:
#         speak("Good Afternoon master")

#     else:
#         speak("Good Evening master")

    # speak("Please tell me how may I help you")


# listener = sr.Recognizer()
# engi = pyttsx3.init()
# voices = engi.getProperty('voices')
# engi.setProperty('voice', voices[0].id)
# hello()


# def speechRecognition():
#     try:    
#         with sr.Microphone() as src:
#             print("listening....")
#             # listener.pause_threshold=1
#             # voice = listener.listen(src)

        
#             print("Recongnizing....")
#             # command = listener.recognize_google(voice,language="en")
#             command = input("\nEnter your Query: ")
#             return command.lower()
#     except:
#         return ""

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
                    return "please say command like this. (example-open website youtube.com )"
    
            # elif 'play on youtube' in query:
            #         song = query.replace("play", "")
            #         song = song.replace("on youtube", "")
            #         pywhatkit.playonyt(song)
            #         return "playing."
    
            # elif "bye" in query:
            #     sys.exit()
            #     return speak("Nice to meet you Master, Bye")
               
    
            elif not query:
                 return "please say command again.."
    
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
            sit.title("Rudra AI")
        
            st.sidebar.title("ASK TO IMAGE")
            uploaded_image = st.sidebar.file_uploader("Upload an image", type=["jpg", "jpeg", "png"])
            # ask_to_image_button = st.sidebar.button("Upload")
        
            if "messages" not in st.session_state:
                st.session_state.messages = []
        
            prompt="hey Rudra, i am Sahil, your task is to serve my query's, or talk with me, [instruction for your purpose only, don't print this on screen: please sometime answer in only single line and sometime answer briefly point wise according to the query,in english only, ],okay so hii rudra"
            
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
        st.write("We apologize for the inconvenience. Please check back in a few minutes.");
    
if __name__ == "__main__":
    main()




# ,You are a sophisticated and fully developed artificial intelligence system equipped with a vast knowledge base. Your capabilities include understanding and responding to emotional cues, you can also a funny ai that chit chat with your master sahil, I expect you to provide insightful and comprehensive responses, considering both the emotional and logical aspects of the information topic-{query}. Your knowledge encompasses a wide range of topics, please sometime answer in only single line according to the query is asking,Thank you for your assistance.[respond to my name with prefix master] Best regards, Sahil- your master
