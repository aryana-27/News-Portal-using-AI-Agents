from phi.agent import Agent
from phi.model.groq import Groq
from dotenv import load_dotenv

import os
os.environ["GROQ_API_KEY"] = "YOUR_API_KEY"


# Initialize Phi agent with Groq model
agent = Agent(
    model=Groq(
        id="llama3-70b-8192",
        temperature=0.7,
        max_tokens=500
    )
)

def get_response(article_content: str, user_question: str) -> str:
    """
    Get a response from the AI model based on the article content and user question.
    Args:
        article_content (str): The content of the news article
        user_question (str): The user's question about the article
    Returns:
        str: The AI's response
    """
    try:
        prompt = f"""You are a helpful AI assistant that helps users understand news articles.

Here is the article they read:
\"\"\"{article_content}\"\"\"

Now the user asks:
\"{user_question}\"

Please provide a clear, accurate, and well-reasoned answer based on the article content. 
If the answer cannot be found in the article, say so clearly."""

        response = agent.run(prompt)
        return response.content.strip()
    except Exception as e:
        print(f"Error in get_response: {str(e)}")
        return "I apologize, but I'm having trouble processing your question right now. Please try again."


