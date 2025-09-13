
import streamlit as st
import google.generativeai as genai
import os
from PIL import Image

# API key configuration
GEMINI_API_KEY = "AIzaSyCkBw_tbgw686LFDzy4dqD4daA6vsNp-38"
genai.configure(api_key=GEMINI_API_KEY)

# Load model - use an appropriate model for image support
# Corrected model name: gemini-1.5-pro or gemini-1.5-pro-latest
model = genai.GenerativeModel("gemini-1.5-flash")

st.title("🐄 Cattle Breed Identifier and AI Assistant for Farmers- Pashudhan App")
st.write("Enter cattle details (in Hindi, Hinglish, Tamil, etc.) or upload a cattle image to get started.")

# User input
user_text = st.text_area("Describe your cattle (color, size, features, etc.)")
uploaded_image = st.file_uploader("📷 Upload a cattle image", type=["jpg", "jpeg", "png"])

if st.button("🔍 Analyse"):
    if not uploaded_image and not user_text.strip():
        st.warning("Please provide text or upload an image.")
    else:
        with st.spinner("Analyzing cattle..."):
            prompt_parts = [
                "You are a cattle expert and a vetrinary. Analyze the given cattle description/image and answer in 2 languages, If the farmer has uploaded an image, analyze the image and provide your best guess.",
                "1. The same language as the farmer's input (if possible).",
                "2. Always also in English.",
                "3. Help the farmer out if any of its cattle has any diseases and symptoms, tell the farmer why is it caused and how to get it fixed.",
                "4. If the cattle is pregnant, tell the farmer how many months it has been pregnant and when is the expected delivery date.",
                "5. If the farmer decides to take the cattle to a vet and get it treated, provide a list of 3 best vets near the farmer's location (if location is provided by the farmer)(use google maps).",
                "6. If the farmer wants to sell the cattle, help the farmer with the best price for the cattle(always show the price in Indian rupees).",
                "7. If the farmer wants to buy a new cattle, help the farmer with the best breed for his farm(always show the price in Indian rupees).",
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

