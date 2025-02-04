import streamlit as st
import requests
from utils.image_fetcher import get_recipe_image

# Set up page config
st.set_page_config(page_title="🔍 Search Recipes", page_icon="🔍")

# Custom CSS for overlap effect
st.markdown(
    """
    <style>
        .recipe-card {
            position: relative;
            padding: 10px;
            border-radius: 10px;
            background-color: #f8f9fa;
            margin-bottom: 20px;
            border-left: 5px solid #ff914d;
            box-shadow: 2px 2px 10px rgba(0, 0, 0, 0.1);
            display: flex;
            align-items: flex-start;
        }
        .recipe-image-container {
            position: relative;
            margin-right: -15px; /* Creates overlap */
            z-index: 2;
        }
        .recipe-info {
            flex-grow: 1;
            background: white;
            padding: 15px;
            border-radius: 10px;
            position: relative;
            z-index: 1;
            margin-left: -10px; /* Overlap effect */
            box-shadow: 2px 2px 5px rgba(0, 0, 0, 0.1);
        }
        .recipe-title {
            font-size: 20px;
            font-weight: bold;
            text-transform: uppercase;
            color: #ff914d;
            cursor: pointer;
        }
    </style>
    """,
    unsafe_allow_html=True
)

# Function to capitalize sentences properly
def capitalize_sentences(text):
    return ". ".join(sentence.capitalize() for sentence in text.split(". "))

# Title
st.title("🔍 Search Recipes")
st.write("Find the best recipes based on your preferences.")

search_col1, search_col2 = st.columns([0.8, 0.2])
with search_col1:
    # User input
    query = st.text_area("Enter your recipe idea:", "", height=80, help="Describe what you're looking for (e.g., 'Quick vegan lunch with avocado').")
with search_col2:
    # Number input for search results
    top_k = st.number_input("Number of results:", min_value=1, max_value=10, value=5, step=1)

# Search button
if st.button("Search") and query.strip():
    with st.spinner("Searching..."):
        api_url = f"http://127.0.0.1:8000/search?query={query.strip()}&top_k={top_k}"
        response = requests.get(api_url)

        if response.status_code == 200:
            results = response.json()["results"]
            
            if not results:
                st.warning("No results found. Try a different query.")
            else:
                for recipe in results:
                    # Capitalize all text fields
                    recipe["name"] = recipe["name"].upper()
                    recipe["description"] = capitalize_sentences(recipe["description"])
                    recipe["ingredients"] = [capitalize_sentences(ing) for ing in recipe["ingredients"]]
                    recipe["steps"] = [capitalize_sentences(step) for step in recipe["steps"]]

                    # Fetch recipe image
                    image_url = get_recipe_image(recipe["name"], recipe["id"])

                    with st.container():
                        col1, col2 = st.columns([0.3, 0.7])
                        with col1:
                            # Image inside an overlapping div
                            # Recipe image
                            st.image(image_url, caption="", use_container_width=True, output_format="auto")

                        with col2:

                            # Overlapping expander container
                            with st.expander(f"**🍽️ {recipe['name']} | ⏱️ {recipe['minutes']} min | 🛒 {len(recipe['ingredients'])} ingredients**", expanded=False):
                                st.markdown('<div class="recipe-info">', unsafe_allow_html=True)
                                st.write(f"**📖 Description:** {recipe['description']}")
                                
                                # Ingredients section
                                st.write("**🛒 Ingredients:**")
                                st.write(", ".join(recipe["ingredients"]))
                                
                                # Steps section (numbered list)
                                st.write("**👨‍🍳 Steps:**")
                                for i, step in enumerate(recipe["steps"], 1):
                                    st.write(f"{i}. {step}")
                                st.markdown("</div>", unsafe_allow_html=True)
                        
        else:
            st.error("Error fetching results.")
