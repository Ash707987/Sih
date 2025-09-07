
import streamlit as st
import google.generativeai as genai
import os
from PIL import Image

# API key configuration
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY") or "AIzaSyCkBw_tbgw686LFDzy4dqD4daA6vsNp-38"
genai.configure(api_key=GEMINI_API_KEY)

# Load model - use an appropriate model for image support
# Corrected model name: gemini-1.5-pro or gemini-1.5-pro-latest
model = genai.GenerativeModel("gemini-1.5-flash")

st.title("🐄 Cattle Breed Identifier for Farmers- Pashudhan App")
st.write("Enter cattle details (in Hindi, Hinglish, Tamil, etc.) or upload a cattle image.")

# User input
user_text = st.text_area("Describe your cattle (color, size, features, etc.)")
uploaded_image = st.file_uploader("📷 Upload a cattle image", type=["jpg", "jpeg", "png"])

if st.button("🔍 Identify Cattle"):
    if not uploaded_image and not user_text.strip():
        st.warning("Please provide text or upload an image.")
    else:
        with st.spinner("Analyzing cattle..."):
            prompt_parts = [
                "You are a cattle expert. Analyze the given cattle description/image and answer in 2 languages:",
                "1. The same language as the farmer's input (if possible).",
                "2. Always also in English.",
                "Give details: Breed, approximate weight, predicted sex, predicted age.",
            ]
            
            if uploaded_image:
                image = Image.open(uploaded_image)
                prompt_parts.append(image)
            
            if user_text.strip():
                prompt_parts.append(user_text)

            try:
                response = model.generate_content(prompt_parts)
                response.resolve()
                st.success("✅ Cattle Analysis:")
                st.write(response.text)
            except Exception as e:
                st.error(f"Error during analysis: {str(e)}")