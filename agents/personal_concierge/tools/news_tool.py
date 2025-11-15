import requests
import os
from google.adk.tools import FunctionTool

NEWSAPI_KEY = os.getenv("NEWSAPI_KEY")
BASE_URL = "https://newsapi.org/v2/top-headlines"

def get_top_news(category: str = "general") -> str:
    """
    Gets the top 5 news headlines for a specific category from NewsAPI.
    
    Args:
        category: The category to fetch news for (e.g., 'business', 'technology', 
                  'entertainment', 'health', 'science', 'sports', 'general').
                  
    Returns:
        A formatted string of the top 5 headlines or an error message.
    """
    if not NEWSAPI_KEY:
        return "Error: NEWSAPI_KEY is not configured in your .env file."

    valid_categories = ['business', 'entertainment', 'general', 'health', 'science', 'sports', 'technology']
    if category.lower() not in valid_categories:
        return f"Error: Invalid category. Please choose from: {', '.join(valid_categories)}"

    params = {
        "category": category,
        "apiKey": NEWSAPI_KEY,
        "language": "en",
        "pageSize": 5
    }
    
    try:
        response = requests.get(BASE_URL, params=params)
        response.raise_for_status() # This will raise an error for 4xx or 5xx responses
        data = response.json()
        
        if data.get("articles") and len(data["articles"]) > 0:
            articles = data["articles"]
            headlines = [f"{i+1}. {a['title']}" for i, a in enumerate(articles)]
            return f"Top 5 headlines for '{category}':\n" + "\n".join(headlines)
        else:
            return f"No top headlines found for '{category}'."
            
    except requests.exceptions.HTTPError as e:
        # This will now print the *actual* error from the API to your console
        print(f"NewsAPI HTTP Error: {e.response.text}")
        return f"Error: Could not retrieve news. HTTP Error: {e.response.status_code}. Check console for details."
    except Exception as e:
        print(f"NewsAPI General Error: {str(e)}")
        return f"Error: An unexpected error occurred: {str(e)}"

get_top_news = FunctionTool(
    func=get_top_news
)