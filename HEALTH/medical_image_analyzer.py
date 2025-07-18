import streamlit as st
import google.generativeai as genai
import os
from dotenv import load_dotenv
from PIL import Image

# Load environment variables
load_dotenv()

# Configure Google Generative AI
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Function to get a response from Gemini
def get_gemini_response(input_prompt, image):
    model = genai.GenerativeModel("gemini-1.5-flash")
    response = model.generate_content([input_prompt, image[0]])
    return response.text

# Function to prepare the uploaded image for Google Gemini
def input_image_setup(uploaded_file):
    if uploaded_file is not None:
        bytes_data = uploaded_file.getvalue()
        # Prepare the image in the format required by Gemini
        image_parts = [
            {
                "mime_type": uploaded_file.type,
                "data": bytes_data
            }
        ]
        return image_parts
    else:
        raise FileNotFoundError("No file uploaded")

# Initialize Streamlit app
st.set_page_config(page_title="Medical Image Analysis App", page_icon="🩺")

st.header("🩺 Medical Image Analysis App")
st.subheader("Upload a medical image, and our AI will help diagnose potential issues and provide recommendations.")

uploaded_file = st.file_uploader("Upload a medical image for analysis...", type=["jpg", "jpeg", "png"])
image = ""

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Medical Image", use_column_width=True)

# Submit button
submit = st.button("Analyze the Medical Image")

# Input prompt for the Gemini model
input_prompt = """
You are a medical expert trained to analyze medical images. Your task is to:
1. Identify abnormalities or issues in the provided medical image.
2. Explain the findings in simple terms for a layperson to understand.
3. Provide recommendations for further tests, treatment, or lifestyle adjustments based on the analysis.
4. Your response should be structured as follows:

   - Observations: 
     - Observation 1: ...
     - Observation 2: ...
   - Recommendations:
     - Recommendation 1: ...
     - Recommendation 2: ...

"""

if submit:
    try:
        image_data = input_image_setup(uploaded_file)
        response = get_gemini_response(input_prompt, image_data)
        st.header("Analysis Results")
        st.write(response)
    except Exception as e:
        st.error(f"An error occurred: {e}")