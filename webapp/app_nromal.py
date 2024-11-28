import streamlit as st
import pdfplumber
import os
import google.generativeai as genai
from difflib import unified_diff
from dotenv import load_dotenv
import spacy
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer

# Load environment variables
load_dotenv()

# Configure Google Gemini-Pro AI Model
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

generation_config = {
    "temperature": 1,
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

# Initialize the Google Gemini Model
model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    generation_config=generation_config,
    safety_settings=safety_settings
)

# Function to extract text from uploaded file
def extract_text_from_file(file):
    if file.type == "application/pdf":
        try:
            with pdfplumber.open(file) as pdf:
                return " ".join([page.extract_text() for page in pdf.pages if page.extract_text()])
        except Exception as e:
            st.error(f"Error reading PDF file: {e}")
            return None
    elif file.type == "text/plain":
        try:
            return file.read().decode("utf-8")
        except Exception as e:
            st.error(f"Error reading text file: {e}")
            return None
    else:
        st.error("Unsupported file type. Please upload a PDF or TXT file.")
        return None

# Generate a plain text comparison
def generate_comparison_text(generated_report, ground_truth):
    diff = unified_diff(
        ground_truth.splitlines(), 
        generated_report.splitlines(), 
        fromfile="Ground Truth", 
        tofile="Generated Report", 
        lineterm=""
    )
    return "\n".join(diff)

# Streamlit page configuration
st.set_page_config(page_title="Radiology Report Analysis", page_icon="🧬", layout="wide")
st.title("Visualize Radiology Report and Correction 🌡")
st.subheader("An App to help with Radiology Analysis using AI")

# File uploader
uploaded_file = st.file_uploader("Upload a Radiology Report (PDF or TXT)", type=["pdf", "txt"])

if uploaded_file:
    report_text = extract_text_from_file(uploaded_file)
    if report_text:
        st.text_area("Extracted Report", value=report_text, height=300)
        
        # Placeholder for the AI-generated report
        generated_report = "Patient has a normal chest X-ray. No abnormalities detected."
        
        # Placeholder for the ground truth
        ground_truth = "Patient has a normal chest X-ray. No fractures or lesions."
        
        # Generate and display the comparison as plain text
        comparison_text = generate_comparison_text(generated_report, ground_truth)
        st.text_area("Comparison", value=comparison_text, height=300)

nlp = spacy.load("en_core_web_sm")

def find_errors(generated_report,ground_truth):
    gen_doc = nlp(generated_report)
    truth_doc = nlp(ground_truth)
    return [(ent.text, "Missed") for ent in truth_doc.ents if ent.text not in generated_report]

errors = find_errors(generated_report,ground_truth)
st.write("Identified Errors:", errors)
