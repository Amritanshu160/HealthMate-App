import streamlit as st
from google import genai
import os
from dotenv import load_dotenv
from PIL import Image
from io import BytesIO

# Load environment variables
load_dotenv()

# Configure Google Generative AI
client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))

# Set page config once at the beginning
st.set_page_config(
    page_title="HealthMate",
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
    6. **Nutri Navigator**: Get personalized diet, health and workout recommendation.
    7. **Multilanguage Medical Document Analyzer**: Analyze and get recommendations based on your medical documents effortlessly.                  
    8. **BMI Calculator**: Calculate your Body Mass Index (BMI) and understand your health status.
    """)
    
    # Footer
    st.write("---")
    st.write("Made with ❤️ by Amritanshu Bhardwaj")
    st.write("© 2025 HealthMate. All rights reserved.")


# Function to get Gemini response for text prompts
def get_gemini_response(prompt):
    response = client.models.generate_content(
        model= "gemini-2.5-flash",
        contents= prompt
    )
    return response.text

# Function to get Gemini response for image prompts
def get_gemini_response_image(input_prompt, image):
    response = client.models.generate_content(
        model= "gemini-2.5-flash",
        contents= [input_prompt, image]
    )
    return response.text

# Function to prepare the uploaded image for Google Gemini
def input_image_setup(uploaded_file):
    if uploaded_file is not None:
        image = Image.open(uploaded_file)
        return image
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
         - Further Observations...
       - Recommendations:
         - Recommendation 1: ...
         - Recommendation 2: ...
         - Further Recommendations... 
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

    if "messages" not in st.session_state:
        st.session_state["messages"] = [
            {"role": "assistant", "content": "Hi, I'm here to support you. How are you feeling today?"}
        ]

    # Display chat history in st.chat_message style
    for msg in st.session_state.messages:
        st.chat_message(msg["role"]).write(msg["content"])

    user_input = st.chat_input("How are you feeling today?")
    if user_input:
        st.session_state.messages.append({"role": "user", "content": user_input})
        st.chat_message("user").write(user_input)

        response = get_gemini_response(
            f"You are a mental health assistant. Provide supportive, empathetic, and non-judgmental responses to users' mental health concerns in a single, well-structured paragraph. "
            f"Offer reassurance, coping strategies, and encouragement without giving medical advice. If needed, suggest seeking professional help in a gentle way.\n\n"
            f"User: {user_input}\nBot: "
        )

        st.chat_message("assistant").write(response)
        st.session_state.messages.append({"role": "assistant", "content": response})

def nutri_navigator():
    import streamlit as st

    st.title("🥗 Nutri Navigator: Personalized Diet & Fitness AI")
    st.markdown("AI-powered health assistant for personalized meal plans, restaurants & workouts.")

    # User Inputs
    age = st.number_input("Age", min_value=5, max_value=100, step=1)
    weight = st.number_input("Weight (kg)", min_value=20.0, max_value=200.0, step=0.5)
    height = st.number_input("Height (cm)", min_value=80.0, max_value=250.0, step=0.5)
    gender = st.selectbox("Gender", ["Male", "Female", "Other"])
    diet_type = st.selectbox("Diet Preference", ["Vegetarian", "Non-Vegetarian"])
    region = st.text_input("Region (e.g., South India, North America, etc.)")
    food_type = st.multiselect("Preferred Food Types", ["Low Carb", "High Protein", "Ayurvedic", "Ketogenic", "Balanced"])
    disease = st.text_area("Existing Disease(s) (optional)")
    allergies = st.text_area("Food Allergies (optional)")

    if st.button("Generate Personalized Plan"):
        with st.spinner("Generating your personalized nutrition & fitness plan..."):
            prompt = f"""
            Generate a personalized health and fitness plan for the following user:
            Age: {age}
            Weight: {weight} kg
            Height: {height} cm
            Gender: {gender}
            Diet Type: {diet_type}
            Region: {region}
            Food Preferences: {', '.join(food_type)}
            Disease(s): {disease if disease else 'None'}
            Allergies: {allergies if allergies else 'None'}

            Return the response in the following format:
            1. **Breakfast** (time & items)
            2. **Lunch** (time & items)
            3. **Evening Snacks** (if applicable)
            4. **Dinner** (time & items)
            5. **Workout Recommendations** (type, duration, and timing based on goals and health)
            6. **Nearby Restaurant Suggestions** (based on diet type and region - only mention if popular options)
            """

            response = get_gemini_response(prompt)
            st.info("Here’s your personalized plan:")
            st.success(response.text)

    st.markdown("---")
    st.caption("🔒 Your data is private and only used to generate personalized recommendations.")

def medical_doc_analyzer():
    from dotenv import load_dotenv
    load_dotenv()

    import os
    from PIL import Image
    from google import genai
    import pathlib

    # Initialize Gemini client
    client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))

    # Function to get Gemini response
    def get_gemini_response(input_prompt, file_data, user_input=None):
        # If file is not an image (PDF), upload it first
        if not isinstance(file_data, Image.Image):
            # Determine MIME type based on file extension
            file_extension = pathlib.Path(uploaded_file.name).suffix.lower()
            mime_type = {
                '.pdf': 'application/pdf'
            }.get(file_extension, 'application/octet-stream')
            
            # Upload the file
            uploaded_file_obj = client.files.upload(
                file=file_data,
                config=dict(mime_type=mime_type)
            )
            contents = [input_prompt, uploaded_file_obj]
            if user_input:  # Only add user input if it exists
                contents.append(user_input)
        else:
            contents = [input_prompt, file_data]
            if user_input:  # Only add user input if it exists
                contents.append(user_input)
        
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=contents
        )
        return response.text

    st.header("📃 Multilanguage Medical Document Analyzer")

    # Chat memory initialization
    if "message" not in st.session_state:
        st.session_state["message"] = [
            {"role": "assistant", "content": "Hello! Upload a medical document or image and I'll help you understand or answer questions about it."}
        ]

    # File upload section
    uploaded_file = st.file_uploader("Upload a medical document (PDF or Image)", type=["pdf", "jpg", "jpeg", "png"])

    # Display file preview
    file_data = None
    if uploaded_file is not None:
        file_type = uploaded_file.type

        if "image" in file_type:
            file_data = Image.open(uploaded_file)
            st.image(file_data, caption="Uploaded Image", use_column_width=True)
        else:
            st.success(f"Uploaded file: {uploaded_file.name}")
            file_data = uploaded_file

    # Submit button for initial analysis
    submit = st.button("Analyze")

    # Gemini prompt for document analysis
    input_prompt = """
    You are an expert in understanding medical documents like prescriptions, lab reports, discharge summaries, and radiology reports.
    A user will upload an image or document, and you'll be asked to extract, summarize, or answer questions based on it.
    """

    # Initial analysis response (without user input)
    if submit and uploaded_file is not None:
        response = get_gemini_response(input_prompt, file_data)
        # Add to chat history
        st.session_state.message.append({"role": "assistant", "content": response})

    # Chat UI for Q&A
    st.divider()
    st.subheader("💬 Ask Questions About the Document")

    # Display chat history
    for msg in st.session_state.message:
        st.chat_message(msg["role"]).write(msg["content"])

    # Chat input
    if prompt := st.chat_input("Ask a question about your uploaded document..."):
        st.session_state.message.append({"role": "user", "content": prompt})
        st.chat_message("user").write(prompt)

        # Generate Gemini response (with user input)
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                try:
                    response = get_gemini_response(input_prompt, file_data, prompt)
                except Exception as e:
                    response = f"Error: {e}"

            st.session_state.message.append({"role": "assistant", "content": response})
            st.write(response)  
        

# Main App
def main():
    st.sidebar.title("Navigation")
    app_mode = st.sidebar.selectbox("Choose the app", ["Home Page","Symptom Checker", "Calories Advisor", "Recipe Generator", "Nutri Navigator", "Medical Document Analyzer", "Medical Image Analysis", "BMI Calculator", "Mental Health Assistant"])
    
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
    elif app_mode == "Nutri Navigator":
        nutri_navigator()
    elif app_mode == "Medical Document Analyzer":
        medical_doc_analyzer()        
    elif app_mode == "BMI Calculator":
        bmi_calculator()
    elif app_mode == "Mental Health Assistant":
        mental_health_assistant()

if __name__ == "__main__":
    main()