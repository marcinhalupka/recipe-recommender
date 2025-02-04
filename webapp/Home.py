import streamlit as st
import sys
import os

# Force Python to recognize the 'webapp/' directory
sys.path.append(os.path.abspath(os.path.dirname(__file__)))

# Set Streamlit app config
st.set_page_config(
    page_title="🍽️ AI-Powered Recipe Explorer",
    page_icon="🍽️",
    layout="wide"
)

# Display Home Page
st.title("🍽️ AI-Powered Recipe Explorer")
st.write("Discover, explore, and generate amazing recipes with AI-driven insights.")
