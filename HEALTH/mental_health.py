from dotenv import load_dotenv
load_dotenv()

import streamlit as st
import os
import google.generativeai as genai

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

## Function to load Gemini Pro model and get response
model = genai.GenerativeModel("gemini-1.5-flash")
chat = model.start_chat(history=[])

def get_gemini_response(question):
    prompt = (
        "You are a mental health assistant. Provide supportive, empathetic, and non-judgmental responses "
        "to users' mental health concerns in a single, well-structured paragraph. Offer reassurance, coping strategies, "
        "and encouragement without giving medical advice. If needed, suggest seeking professional help in a gentle way.\n\n"
        f"User: {question}\nBot: "
    )
    response = chat.send_message(prompt, stream=False)  ## Single response instead of streaming
    return response.text

## Initialize our Streamlit app
st.set_page_config(page_title="Mental Health Assistant")

st.header("Mental Health Support Chat")
st.write("🧘 Welcome! Feel free to share your thoughts. I'm here to listen and support you.")

# Initialize session state for chat history if it doesn't exist
if 'chat_history' not in st.session_state:
    st.session_state['chat_history'] = []

input = st.text_input("How are you feeling today?", key="input")
submit = st.button("Talk")

if submit and input:
    response = get_gemini_response(input)
    
    # Add user query and response to session chat history
    st.session_state['chat_history'].append(("You", input))
    st.subheader("Response")
    st.write(response)  ## Display response as a single paragraph
    st.session_state['chat_history'].append(("Bot", response))

st.subheader("Chat History")
for role, text in st.session_state['chat_history']:
    st.write(f"**{role}:** {text}")
 
