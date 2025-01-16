import os
import streamlit as st
from langchain_openai import ChatOpenAI
from educhain import Educhain, LLMConfig
from dotenv import load_dotenv
# Fetch the GROQ API key from the environment
load_dotenv()  

# Initialize the ChatOpenAI model with Groq API configuration
llama3_groq = ChatOpenAI(
    model="llama3-70b-8192",  # The model you want to use
    openai_api_base="https://api.groq.com/openai/v1",  # Custom API base for Groq
    openai_api_key=os.getenv("GROQ_API_KEY")  # The API key for accessing the Groq service
)

flash_config = LLMConfig(custom_model="llama3-70b-8192")

# Initialize Educhain with LLM
client = Educhain(flash_config)

# Function to generate mnemonics based on user input, favorite movie, style, and language
def generate_mnemonic(answer, favorite_movie, style, language):
    try:
        # Define the style-specific prompt
        style_prompt = {
            "Acronym": "Create a mnemonic acronym",
            "Rhyme": "Create a rhyming mnemonic",
            "Storytelling": "Create a storytelling mnemonic"
        }

        # Construct the prompt
        prompt = (
            f"{style_prompt[style]} to help remember: '{answer}', "
            f"using references and themes from the movie '{favorite_movie}'. "
            f"Generate the response in {language}."
        )

        # Invoke the model with the prompt
        response = llama3_groq.invoke(prompt)
        mnemonic = response.content.strip()  # Access content attribute and strip unnecessary whitespace
        return mnemonic
    except Exception as e:
        st.error(f"Error generating mnemonic: {type(e).__name__}: {str(e)}")
        return None


# Study Assistant Functionality
def study_assistant():
    st.title("📚 AI Study Assistant")
    st.write("Enhance your study experience with personalized mnemonics based on your favorite movie!")

    # Input fields for the study assistant
    favorite_movie = st.text_input("What's your favorite movie?", key="favorite_movie")
    answer_to_study = st.text_input("What do you want to remember?", key="answer_to_study")

    # Dropdown for mnemonic style
    mnemonic_style = st.selectbox(
        "Choose your mnemonic style:",
        ["Acronym", "Rhyme", "Storytelling"],
        key="mnemonic_style"
    )

    # Dropdown for language selection
    mnemonic_language = st.selectbox(
        "Choose your preferred language:",
        ["English", "Spanish", "French", "German", "Chinese", "Hindi"],
        key="mnemonic_language"
    )

    if st.button("Generate Mnemonic"):
        if not favorite_movie or not answer_to_study:
            st.error("Please provide both the answer to study and your favorite movie.")
        else:
            mnemonic = generate_mnemonic(answer_to_study, favorite_movie, mnemonic_style, mnemonic_language)
            if mnemonic:
                st.success("Mnemonic generated successfully!")
                st.write(f"### Mnemonic ({mnemonic_style} - {mnemonic_language}): {mnemonic}")

# Main App
def main():
    st.sidebar.title("⚙️ Settings")
    st.sidebar.subheader("App Modes")
    mode = st.sidebar.radio("Choose a Mode:", ["Study Assistant"])

    if mode == "Study Assistant":
        study_assistant()

if __name__ == "__main__":
    st.set_page_config(page_title="AI Study Assistant", layout="wide")
    main()
