from phi.agent import Agent
from phi.model.groq import Groq
from dotenv import load_dotenv

import os
os.environ["GROQ_API_KEY"] = "YOUR_API_KEY"

# Initialize Phi agent with Groq model
agent = Agent(
    model=Groq(
        id="llama3-70b-8192",
        temperature=0.3,
        max_tokens=500
    )
)

def summarize_text(text: str) -> str:
    """
    Summarize the given text using Phi agent with Groq.
    Args:
        text (str): The text to summarize
    Returns:
        str: The summarized text
    """
    try:
        prompt = f"""Please provide a clear and concise summary of the following text. 
        Focus on the main points and key information:
        
        {text}"""

        response = agent.run(prompt)
        return response.content.strip()
    except Exception as e:
        print(f"Error in summarization: {str(e)}")
        return "Error generating summary. Please try again."
