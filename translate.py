from phi.agent import Agent
from phi.model.groq import Groq
from dotenv import load_dotenv

import os
os.environ["GROQ_API_KEY"] = "YOUR_API_KEY"


# GROQ_API = "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"

# Initialize Phi agent with Groq model
agent = Agent(
    model=Groq(
        id="llama3-70b-8192",
        temperature=0.3,
        max_tokens=1000
    )
)

# Supported languages for translation
SUPPORTED_LANGUAGES = [
    "French", "Hindi", "German", "Gujarati", "Spanish",
    "Chinese", "Japanese", "Russian", "Tamil", "Telugu", "Malayalam"
]

def translate_text(text: str, target_language: str) -> str:
    """
    Translate text to the target language using Phi agent with Groq.
    Args:
        text (str): The text to translate
        target_language (str): The target language
    Returns:
        str: The translated text
    """
    if target_language not in SUPPORTED_LANGUAGES:
        return f"Translation to '{target_language}' is not supported yet."

    try:
        prompt = f"""You are an expert translator specializing in {target_language}.
        Translate the following text into {target_language}. 
        Maintain the original meaning and tone while ensuring natural language flow:
        
        {text}"""

        response = agent.run(prompt)
        return response.content.strip()

    except Exception as e:
        print(f"Error in translation: {str(e)}")
        return f"Error during translation: {str(e)}"