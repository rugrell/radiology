import streamlit as st
from pdfplumber import open as open_pdf
import os
import google.generativeai as genai
from PIL import Image
from dotenv import load_dotenv
load_dotenv()

#Configure Google Gemini-Pro AI Model
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

generation_config = {
    "temprature": 1,
    "top_p": 0.95,
    "top_k": 0,
    "max_output_tokens": 8129,
}


# Safety settings 
safety_settings = [
    {
        "category": "HARM_CATEGORY_HARASSMENT",
        "threshold": "BLOCK_MEDIUM_AND_ABOVE"
    },
    {
        "category": "HARM_CATEGORY_HARASSMENT",
        "threshold": "BLOCK_MEDIUM_AND_ABOVE"
    },
    {
        "category": "HARM_CATEGORY_HARASSMENT",
        "threshold": "BLOCK_MEDIUM_AND_ABOVE"
    },
]

#Initialize the Model
model = genai.GenerativeModel(
    #model_name="models/gemini-1.5-flash",
    model_name="gemini-1.5-flash",
    generation_config=generation_config,
    safety_settings=safety_settings
)

#streamlit page configuration

st.set_page_config(page_title="Radiology", page_icon="🧬", layout="wide")
st.title("Visualize Radiology Report and Correction 🌡")
st.subheader("An App to help with Radiology Analysis using AI")













