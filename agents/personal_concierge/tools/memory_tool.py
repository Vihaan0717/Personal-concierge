import json
import os
from google.adk.tools import FunctionTool

# Corrected path to be relative to this file, then go up to project root
DATA_DIR = os.path.join(os.path.dirname(__file__), '..', '..', '..', 'data')
MEMORY_FILE = os.path.join(DATA_DIR, "memory.json")

def _ensure_data_dir():
    """Ensures the data directory exists."""
    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR)

def _load_memory() -> dict:
    """Loads the memory from the JSON file."""
    _ensure_data_dir()
    if not os.path.exists(MEMORY_FILE):
        return {}
    try:
        with open(MEMORY_FILE, 'r') as f:
            return json.load(f)
    except json.JSONDecodeError:
        return {}

def _save_memory(memory: dict):
    """Saves the memory to the JSON file."""
    _ensure_data_dir()
    with open(MEMORY_FILE, 'w') as f:
        json.dump(memory, f, indent=2)

def save_memory(key: str, value: str) -> str:
    """
    Saves a piece of information to personal memory (a key-value store).
    
    Args:
        key: The key for the memory (e.g., "wife's birthday", "favorite_color").
        value: The value of the memory (e.g., "October 25th", "blue").
        
    Returns:
        A confirmation string.
    """
    memory = _load_memory()
    memory[key] = value
    _save_memory(memory)
    return f"Got it. I'll remember that '{key}' is '{value}'."

def recall_memory(key: str) -> str:
    """
    Recalls a piece of information from personal memory using its key.
    
    Args:
        key: The key of the memory to recall.
        
    Returns:
        The remembered value or a 'not found' message.
    """
    memory = _load_memory()
    value = memory.get(key)
    
    if value:
        return f"I recall that '{key}' is '{value}'."
    else:
        return f"I'm sorry, I don't have any memory stored for the key '{key}'."


# We wrap the functions *with the same name*
save_memory = FunctionTool(
    func=save_memory
)

recall_memory = FunctionTool(
    func=recall_memory
)