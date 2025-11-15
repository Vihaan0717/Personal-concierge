import os
from google.adk.tools import FunctionTool
import google.generativeai as genai

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# --- THIS IS THE FIX ---
# We are now using the correct model names from your list.
PRIMARY_MODEL = "models/gemini-2.5-flash"
FALLBACK_MODEL = "models/gemini-2.5-pro"
# --- END OF FIX ---

if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)
    try:
        summarizer_model = genai.GenerativeModel(PRIMARY_MODEL)
    except Exception:
        try:
            summarizer_model = genai.GenerativeModel(FALLBACK_MODEL)
        except Exception:
            summarizer_model = None
else:
    summarizer_model = None

def summarize_text(text: str) -> str:
    """
    Summarizes a long piece of text into a concise paragraph.
    
    Args:
        text: The text to be summarized.
        
    Returns:
        A summary of the text or an error message.
    """
    global summarizer_model # Allow modifying the global variable
    if not summarizer_model:
        return "Error: Summarizer tool is not configured. Could not find a valid model or GEMINI_API_KEY is missing."

    if len(text) < 150:
        return "The provided text is already quite short."

    prompt = f"Please provide a concise, single-paragraph summary of the following text:\n\n---\n{text}\n---"
    
    try:
        response = summarizer_model.generate_content(prompt)
        return response.text
    except Exception as e:
        # If the primary model failed, try the fallback
        if summarizer_model.model_name == PRIMARY_MODEL:
            try:
                summarizer_model = genai.GenerativeModel(FALLBACK_MODEL)
                response = summarizer_model.generate_content(prompt)
                return response.text
            except Exception as e_pro:
                return f"Error: An error occurred during summarization with fallback model: {str(e_pro)}"
        
        # If it failed *even with* the fallback, then it's a real error.
        return f"Error: An error occurred during summarization: {str(e)}"

summarize_text = FunctionTool(
    func=summarize_text
)