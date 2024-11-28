import streamlit as st
from pdfplumber import open as open_pdf
import os
import google.generativeai as genai
from PIL import Image
from dotenv import load_dotenv
load_dotenv()
import difflib  
from difflib import SequenceMatcher
from difflib import HtmlDiff

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

def extract_text_from_file(file):
    if file.type == "application/pdf":
        with open_pdf(file) as pdf:
            return " ".join([page.extract_text() for page in pdf.pages])
    elif file.type == "text/plain":
        return file.read().decode("utf-8")
    else:
        st.error("Unsupported File !")
        return None
        

##########################################################################################

#streamlit page configuration
st.set_page_config(page_title="Radiology", page_icon="🧬", layout="wide")
st.title("Visualize Radiology Report and Correction 🌡")
st.subheader("An App to help with Radiology Analysis using AI")

uploaded_file = st.file_uploader("Upload a Radiology Report (PDF or Text)", type=["pdf","text"]) 


if uploaded_file:
    report_text = extract_text_from_file(uploaded_file)
    if report_text:
        st.text_area("Extracted Report", value=report_text, height=300)

#submit = st.button("Generate Analysis")

def generate_comparison_html(generated_report, ground_truth):
    differ = HtmlDiff()
    return differ.make_file(ground_truth.splitlines(), generated_report.splitlines(),context=True)

generated_report = "Patient has a normal chest X-ray. No abnormalities detected."
ground_truth = "Patient has a normal chest X-ray. No fractures or lesions."

comparison_html = generate_comparison_html(generated_report,ground_truth)
st.markdown(comparison_html, unsafe_allow_html=True)


















