import os
from dotenv import load_dotenv

# These are the correct imports
from google.adk.agents import Agent
from google.adk.apps.app import App

# We use a '.' to tell Python to look in the current folder for the 'tools' module.
from .tools.weather_tool import get_weather
from .tools.news_tool import get_top_news
from .tools.planner_tool import add_event, get_schedule
from .tools.memory_tool import save_memory, recall_memory
from .tools.summarizer_tool import summarize_text

# Load API keys from .env file (located two directories up)
dotenv_path = os.path.join(os.path.dirname(__file__), '..', '..', '.env')
load_dotenv(dotenv_path)

# Get the Gemini API key from the environment
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if not GEMINI_API_KEY:
    raise ValueError("GEMINI_API_KEY not found in .env file. Please add it.")

# 1. Define the Agent's System Prompt
system_prompt = """
You are a helpful and polite Personal Concierge Agent.
Your job is to assist the user with their daily tasks, planning, and information needs.
You have access to several tools.
- `get_weather`: To check the weather for a location.
- `get_top_news`: To get top news headlines for a category (e.g., 'technology', 'business').
- `get_schedule`: To check the user's personal planner for a specific date.
- `add_event`: To add events to the user's planner.
- `save_memory`: To remember personal facts (using a key-value pair).
- `recall_memory`: To recall personal facts (using a key).
- `summarize_text`: To summarize long pieces of text.
"""

# 2. Create the Agent
# The server will look for this *exact* variable name: 'root_agent'
root_agent = Agent(
    name="personal_concierge",
    instruction=system_prompt,
    # Use the model name that matches the ADK library's internal list
    model="gemini-2.5-flash",
    tools=[
        get_weather,
        get_top_news,
        add_event,
        get_schedule,
        save_memory,
        recall_memory,
        summarize_text
    ],
)

# 3. Create the ADK App
# The server will look for this *exact* variable name: 'adk_app'
adk_app = App(
    name="personal_concierge",
    root_agent=root_agent
)