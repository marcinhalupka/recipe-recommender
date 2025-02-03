import streamlit as st

def show_navbar():
    # Add a key to ensure the navbar doesn't duplicate
    if "navbar_shown" not in st.session_state:
        st.session_state["navbar_shown"] = True
        
        st.markdown(
            """
            <style>
                .css-18e3th9 {
                    padding-top: 2rem;
                }
                .css-1d391kg {
                    padding: 2rem;
                }
                .stApp {
                    background-color: #f8f9fa;
                }
            </style>
            """,
            unsafe_allow_html=True
        )
        st.markdown("<h1 style='text-align: center;'>🍽️ AI-Powered Recipe Explorer</h1>", unsafe_allow_html=True)
