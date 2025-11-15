import json
import os
from google.adk.tools import FunctionTool
from datetime import datetime

# Corrected path to be relative to this file, then go up to project root
DATA_DIR = os.path.join(os.path.dirname(__file__), '..', '..', '..', 'data')
SCHEDULE_FILE = os.path.join(DATA_DIR, "schedule.json")

def _ensure_data_dir():
    """Ensures the data directory exists."""
    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR)

def _load_schedule() -> dict:
    """Loads the schedule from the JSON file."""
    _ensure_data_dir()
    if not os.path.exists(SCHEDULE_FILE):
        return {}
    try:
        with open(SCHEDULE_FILE, 'r') as f:
            return json.load(f)
    except json.JSONDecodeError:
        return {}

def _save_schedule(schedule: dict):
    """Saves the schedule to the JSON file."""
    _ensure_data_dir()
    with open(SCHEDULE_FILE, 'w') as f:
        json.dump(schedule, f, indent=2)

def add_event(date: str, time: str, description: str) -> str:
    """
    Adds an event to the personal planner.
    
    Args:
        date: The date of the event (YYYY-MM-DD).
        time: The time of the event (HH:MM).
        description: A description of the event.
        
    Returns:
        A confirmation string.
    """
    try:
        # Validate date format
        datetime.strptime(date, '%Y-%m-%d')
        # Validate time format
        datetime.strptime(time, '%H:%M')
    except ValueError:
        return "Error: Invalid date or time format. Please use YYYY-MM-DD and HH:MM."

    schedule = _load_schedule()
    
    if date not in schedule:
        schedule[date] = []
        
    schedule[date].append({"time": time, "description": description})
    
    # Sort events by time
    schedule[date] = sorted(schedule[date], key=lambda e: e['time'])
    
    _save_schedule(schedule)
    return f"Event added: On {date} at {time}, '{description}'."

def get_schedule(date: str) -> str:
    """
    Gets the schedule for a specific date. 'today' is a valid date.
    
    Args:
        date: The date to get the schedule for (YYYY-MM-DD or 'today').
        
    Returns:
        A string with the schedule for that day.
    """
    if date.lower() == 'today':
        date = datetime.now().strftime('%Y-%m-%d')
    else:
        try:
            datetime.strptime(date, '%Y-%m-%d')
        except ValueError:
            return "Error: Invalid date format. Please use YYYY-MM-DD or 'today'."

    schedule = _load_schedule()
    
    if date not in schedule or not schedule[date]:
        return f"No events found for {date}."
    
    events = [f"- {e['time']}: {e['description']}" for e in schedule[date]]
    return f"Your schedule for {date}:\n" + "\n".join(events)


# We wrap the functions *with the same name*
add_event = FunctionTool(
    func=add_event
)

get_schedule = FunctionTool(
    func=get_schedule
)