import requests
from bs4 import BeautifulSoup
import urllib.parse

def extract_image_url(pinterest_url: str) -> str:
    """Extracts the image URL from a Pinterest sharing link."""
    if not pinterest_url:
        return None
    parsed_url = urllib.parse.urlparse(pinterest_url)
    query_params = urllib.parse.parse_qs(parsed_url.query)
    return query_params.get("media", [None])[0]

def get_recipe_image(recipe_name: str, recipe_id: int) -> str:
    """
    Given a recipe name and ID, fetches the recipe page and extracts the image URL.
    
    Args:
        recipe_name (str): The name of the recipe.
        recipe_id (int): The unique ID of the recipe.
    
    Returns:
        str: The extracted image URL or a placeholder if not found.
    """
    # Construct the recipe URL
    page_id = '-'.join(recipe_name.lower().split()) + '-' + str(recipe_id)
    page_url = f"https://www.food.com/recipe/{page_id}"

    # Fetch the webpage
    response = requests.get(page_url)
    if response.status_code != 200:
        return "https://3f4c2184e060ce99111b-f8c0985c8cb63a71df5cb7fd729edcab.ssl.cf2.rackcdn.com/media/1012/recipe-placeholder.jpg"

    # Parse the webpage content
    soup = BeautifulSoup(response.text, "html.parser")

    # Find the media URL
    media_url = None
    for el in soup.find_all("a", href=True):
        if "img.sndimg.com" in el["href"]:
            media_url = el["href"]
            break  # Stop at the first valid image URL
    
    return extract_image_url(media_url) if media_url else "https://3f4c2184e060ce99111b-f8c0985c8cb63a71df5cb7fd729edcab.ssl.cf2.rackcdn.com/media/1012/recipe-placeholder.jpg"
