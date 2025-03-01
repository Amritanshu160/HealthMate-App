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

# Set page config once at the beginning
st.set_page_config(
    page_title="Health App Suite",
    page_icon="🏥",
    layout="wide"
)

def front():
    import streamlit as st

    # Title and description
    st.title("🏥 HealthMate - Your Health Companion")
    st.write("Welcome to **HealthMate**! Your one-stop solution for health, wellness, and lifestyle management. Explore the following tools to take control of your health.")

    # App descriptions
    st.subheader("Available Features")
    st.write("""
    1. **Medical Image Analysis**: Analyze medical images (e.g., X-rays, MRIs) with AI-powered tools for insights and diagnostics.
    2. **Symptom Checker**: Get preliminary health assessments based on your symptoms.
    3. **Mental Health Assistant**: Access tools and resources to support your mental well-being.
    4. **Calories Advisor**: Track your daily calorie intake and get personalized recommendations.
    5. **Recipe Generator**: Discover healthy recipes tailored to your dietary preferences and calorie goals.
    6. **BMI Calculator**: Calculate your Body Mass Index (BMI) and understand your health status.
    """)
    
    # Footer
    st.write("---")
    st.write("Made with ❤️ by Amritanshu Bhardwaj")
    st.write("© 2025 HealthMate. All rights reserved.")


# Function to get Gemini response for text prompts
def get_gemini_response(prompt):
    model = genai.GenerativeModel("gemini-2.0-flash")
    response = model.generate_content(prompt)
    return response.text

# Function to get Gemini response for image prompts
def get_gemini_response_image(input_prompt, image):
    model = genai.GenerativeModel("gemini-2.0-flash")
    response = model.generate_content([input_prompt, image[0]])
    return response.text

# Function to prepare the uploaded image for Google Gemini
def input_image_setup(uploaded_file):
    if uploaded_file is not None:
        bytes_data = uploaded_file.getvalue()
        image_parts = [
            {
                "mime_type": uploaded_file.type,
                "data": bytes_data
            }
        ]
        return image_parts
    else:
        raise FileNotFoundError("No file uploaded")

# BMI Calculator
def bmi_calculator():
    st.title("BMI Calculator")
    height = st.slider("Enter your height (in cm):", 100, 250, 175)
    weight = st.slider("Enter your weight (in kg):", 40, 200, 70)
    bmi = weight / ((height / 100) ** 2)
    st.write(f"Your BMI is {bmi:.2f}")
    st.write(" ### BMI Categories ###")
    st.write("--Underweight: BMI less than 18.5")
    st.write("--Normal weight: BMI between 18.5 and 24.9")
    st.write("--Overweight: BMI between 24 and 29.9")
    st.write("--Obesity: BMI 30 or greater")

# Calories Advisor App
def calories_advisor():
    st.header("Calories Advisor App")
    uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])
    image = ""
    if uploaded_file is not None:
        image = Image.open(uploaded_file)
        st.image(image, caption="Uploaded Image.", use_column_width=True)

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
        response = get_gemini_response_image(input_prompt, image_data)
        st.header("The Response is")
        st.write(response)

# Recipe Generator
def recipe_generator():
    st.title("👨‍🍳 CookEase: Your AI Cooking Assistant")
    st.subheader("Enter your dish details and get step-by-step cooking instructions!")

    with st.sidebar:
        st.subheader("Provide details of the dish you want to cook")

        dish_name = st.text_input("Dish Name", placeholder="Enter the dish name here")
        ingredients = st.text_area("Key Ingredients (comma-separated)", placeholder="e.g., Chicken, Garlic, Onion, Butter")

        prompt_parts = [
            f"Generate a detailed, step-by-step cooking recipe for {dish_name} using the key ingredients: {ingredients}. "
            "Specify the exact quantity of each ingredient required. "
            "Include detailed cooking instructions with precise cooking times and temperatures where necessary. "
            "Ensure clarity in each step, including preparation, cooking, and serving instructions."
        ]

        submit_button = st.button("Generate Recipe")

    if submit_button:
        response = get_gemini_response(prompt_parts)
        st.subheader(f"🍳 Step-by-Step Recipe for {dish_name}")
        st.write(response)

# Medical Image Analysis
def medical_image_analysis():
    st.header("🩺 Medical Image Analysis App")
    st.subheader("Upload a medical image, and our AI will help diagnose potential issues and provide recommendations.")

    uploaded_file = st.file_uploader("Upload a medical image for analysis...", type=["jpg", "jpeg", "png"])
    image = ""

    if uploaded_file is not None:
        image = Image.open(uploaded_file)
        st.image(image, caption="Uploaded Medical Image", use_column_width=True)

    submit = st.button("Analyze the Medical Image")

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
            response = get_gemini_response_image(input_prompt, image_data)
            st.header("Analysis Results")
            st.write(response)
        except Exception as e:
            st.error(f"An error occurred: {e}")

# Symptom Checker
def symptom_checker():
    st.header("🔍 AI-Powered Symptom Checker")
    symptoms = st.text_area("Describe your symptoms:")
    if st.button("Analyze Symptoms"):
        if symptoms:
            response = get_gemini_response(f"Analyze these symptoms and suggest possible conditions, also tell further steps to be taken to cure the condition and also tell how to prevent this to happen again in future: {symptoms}")
            st.success(response)
        else:
            st.warning("Please enter symptoms.")

# Mental Health Assistant
def mental_health_assistant():
    st.header("Mental Health Support Chat")
    st.write("🧘 Welcome! Feel free to share your thoughts. I'm here to listen and support you.")

    if 'chat_history' not in st.session_state:
        st.session_state['chat_history'] = []

    input = st.text_input("How are you feeling today?", key="input")
    submit = st.button("Talk")

    if submit and input:
        response = get_gemini_response(f"You are a mental health assistant. Provide supportive, empathetic, and non-judgmental responses to users' mental health concerns in a single, well-structured paragraph. Offer reassurance, coping strategies, and encouragement without giving medical advice. If needed, suggest seeking professional help in a gentle way.\n\nUser: {input}\nBot: ")
        st.session_state['chat_history'].append(("You", input))
        st.subheader("Response")
        st.write(response)
        st.session_state['chat_history'].append(("Bot", response))

    st.subheader("Chat History")
    for role, text in st.session_state['chat_history']:
        st.write(f"**{role}:** {text}")

# Main App
def main():
    st.sidebar.title("Navigation")
    app_mode = st.sidebar.selectbox("Choose the app", ["Home Page","Symptom Checker", "Calories Advisor", "Recipe Generator", "Medical Image Analysis", "BMI Calculator", "Mental Health Assistant"])
    
    if app_mode == "Home Page":
        front()
    elif app_mode == "Symptom Checker":
        symptom_checker()
    elif app_mode == "Calories Advisor":
        calories_advisor()
    elif app_mode == "Recipe Generator":
        recipe_generator()
    elif app_mode == "Medical Image Analysis":
        medical_image_analysis()
    elif app_mode == "BMI Calculator":
        bmi_calculator()
    elif app_mode == "Mental Health Assistant":
        mental_health_assistant()

if __name__ == "__main__":
    main()