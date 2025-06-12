from dotenv import load_dotenv
import os
from phi.agent import Agent
from phi.model.groq import Groq

# Load key and initialize agent
os.environ["GROQ_API_KEY"] = "YOUR_API_KEY"

agent = Agent(
    model=Groq(id="llama3-70b-8192"),
    markdown=True
)

def generate_questions(article_content: str) -> list:
    prompt = f"""
You are a thoughtful and futuristic AI question generator that helps users reflect deeply on news articles.

Your job is to read the article and generate 5 insightful questions that:
- Encourage the reader to think about long-term consequences
- Draw connections to historical events or similar trends
- Highlight potential risks, opportunities, or ethical concerns
- Encourage curiosity and deeper thought

Here is the article:
\"\"\"{article_content}\"\"\"

Generate 5 such questions:
"""
    response = agent.run(prompt)
    return [q.strip("12345. ") for q in response.content.strip().split("\n") if q.strip()]
