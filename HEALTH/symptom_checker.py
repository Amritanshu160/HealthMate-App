import streamlit as st
import google.generativeai as genai  # Gemini AI SDK
from PIL import Image
import base64
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))  # Load Gemini API key

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
        prompt = (
            f"Analyze these symptoms and suggest possible conditions. "
            f"Also, suggest further steps to be taken to cure the condition, "
            f"and how to prevent this from happening again in the future: {symptoms}"
        )
        response = get_gemini_response(prompt)
        st.success(response)
    else:
        st.warning("Please enter symptoms.")







