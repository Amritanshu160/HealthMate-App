import streamlit as st
import google.generativeai as genai
import os
from dotenv import load_dotenv
load_dotenv() # Loading all the environment variables
from PIL import Image

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

def get_gemini_response(input_prompt,image):
    model = genai.GenerativeModel('gemini-1.5-flash')
    response = model.generate_content([input_prompt,image[0]])
    return response.text

def input_image_setup(uploaded_file):
    if uploaded_file is not None:
        bytes_data = uploaded_file.getvalue()
        # This image part is the format in which google gemini pro vision takes image
        image_parts = [
            {
                "mime_type":uploaded_file.type,
                "data":bytes_data
            }
        ]
        return image_parts
    else:
        raise FileNotFoundError("No file uploaded")
    
## Initialize our streamlit app

st.set_page_config(page_title="Calories Advisor App")

st.header("Calories Advisor App")
uploaded_file = st.file_uploader("Choose an image...",type=["jpg","jpeg","png"])
image=""
if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image,caption="Uploaded Image.",use_column_width=True)

sumbit = st.button("Tell me about the total calories")

input_prompt = """
You are an expert in nutritionist where you need to see the food items from the image
               and calculate the total calories, also provide the details of
               every food items with calories intake
               in below format

               1. Item 1 - no of calories
               2. Item 2 - no of calories
               ----
               ----
        Finally you can also mention whether the food is healthy or not and also
        mention the
        percentage split of the ratio of carbohydrates,fats,fibers,sugars and other important
        things required in our diet



"""

if sumbit:
    image_data = input_image_setup(uploaded_file)
    response = get_gemini_response(input_prompt,image_data)
    st.header("The Response is")
    st.write(response)