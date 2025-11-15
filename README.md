# Personal Concierge Agent (Google ADK Capstone Project)

This project is a "Personal Concierge Agent" built for the Google ADK Capstone, submitted for the **Concierge Agents** track.

It's a Python-based AI agent that uses the Google ADK framework and the Gemini model to help users manage their daily lives. It's connected to live APIs for real-time data and can remember personal information and schedule events.

## ✨ Features

This agent is built with five custom tools:

1.  **Weather Tool:** Connects to the [OpenWeatherMap API](https://openweathermap.org/api) to fetch real-time weather for any city.
2.  **News Tool:** Connects to the [NewsAPI](https://newsapi.org/) to get the latest headlines in categories like technology, business, or sports.
3.  **Personal Planner:** A stateful tool that can `add_event` and `get_schedule`. It saves events to a local `data/schedule.json` file, persisting the user's schedule.
4.  **Personal Memory:** A stateful tool that can `save_memory` and `recall_memory`. It saves key-value pairs (like "wife's birthday": "October 25th") to a local `data/memory.json` file.
5.  **Summarizer Tool:** Uses the `google-generativeai` library directly to summarize long pieces of text.

## 🚀 Capstone: Key Concepts Used

This project successfully demonstrates **3 key concepts** required by the capstone:

1.  **Agent powered by an LLM:** The `root_agent` is an `Agent` class powered by the `gemini-2.5-flash` model.
2.  **Custom Tools:** All five tools (`get_weather`, `get_top_news`, `save_memory`, etc.) are custom-built Python functions registered with the agent as `FunctionTool` objects.
3.  **Sessions & Memory (State Management):** The agent uses the ADK's default `InMemorySessionService` to maintain conversational state. The custom `memory_tool` and `planner_tool` demonstrate long-term, stateful memory by reading/writing to the local file system.

## 📁 Project Structure

The project uses the required `adk web` directory structure:personal-concierge/
├── agents/
└── personal_concierge/
    ├── init.py  
    ├── agent.py and 'adk_app'
    └── tools/ 
├── init.py
├── memory_tool.py
├── news_tool.py
├── planner_tool.py
├── summarizer_tool.py 
└── weather_tool.py 
├── data/
├── .env
└── venv/