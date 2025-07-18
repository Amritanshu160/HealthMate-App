import streamlit as st
import google.generativeai as genai
import os
from dotenv import load_dotenv
from PIL import Image
from io import BytesIO

# Load environment variables
load_dotenv()

# Configure Google Generative AI
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

generation_config = {
  "temperature": 0.7,
  "top_p": 0.9,
  "top_k": 40,
  "max_output_tokens": 2048,
  "response_mime_type": "text/plain",
}

model = genai.GenerativeModel(
  model_name="gemini-pro",
  generation_config=generation_config
)

# Page Configuration
st.set_page_config(layout="wide", page_title="CookEase", page_icon="👨‍🍳")

# App Title
st.title("👨‍🍳 CookEase: Your AI Cooking Assistant")
st.subheader("Enter your dish details and get step-by-step cooking instructions!")

# Sidebar for user input
with st.sidebar:
    st.title("🍽️ Recipe Generator")
    st.subheader("Provide details of the dish you want to cook")

    # User inputs
    dish_name = st.text_input("Dish Name", placeholder="Enter the dish name here")
    ingredients = st.text_area("Key Ingredients (comma-separated)", placeholder="e.g., Chicken, Garlic, Onion, Butter")

    prompt_parts = [
        f"Generate a detailed, step-by-step cooking recipe for {dish_name} using the key ingredients: {ingredients}. "
        "Specify the exact quantity of each ingredient required. "
        "Include detailed cooking instructions with precise cooking times and temperatures where necessary. "
        "Ensure clarity in each step, including preparation, cooking, and serving instructions."
    ]

    # Submit button
    submit_button = st.button("Generate Recipe")

if submit_button:
    response = model.generate_content(prompt_parts)
    st.subheader(f"🍳 Step-by-Step Recipe for {dish_name}")
    st.write(response.text)
  