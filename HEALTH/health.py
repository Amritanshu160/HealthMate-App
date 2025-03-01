import streamlit as st
import google.generativeai as genai  # Gemini AI SDK
from PIL import Image
import base64
import os
from dotenv import load_dotenv

load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY")) # Replace with your API key


# Function to get AI response
def get_gemini_response(prompt):
    model = genai.GenerativeModel("gemini-pro")
    response = model.generate_content(prompt)
    return response.text

# Streamlit UI
st.header("🔍 AI-Powered Symptom Checker")
symptoms = st.text_area("Describe your symptoms:")
if st.button("Analyze Symptoms"):
    if symptoms:
        response = get_gemini_response(f"Analyze these symptoms and suggest possible conditions ,
        also tell further steps to be taken to cure the condition and also tell how 
        to prevent this to happen again in future: {symptoms}")
        st.success(response)
    else:
        st.warning("Please enter symptoms.")



