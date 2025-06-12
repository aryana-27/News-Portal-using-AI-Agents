# AI-Powered News Dashboard

An intelligent news dashboard that provides real-time news updates, article summarization, translation, and interactive Q&A capabilities using advanced AI technologies.

## Features

- **Real-time News Updates**: Get the latest news from various categories including India, US, stock market, movies, health, sports, and technology
- **AI-Powered Summarization**: Get concise summaries of news articles using advanced language models
- **Multi-language Translation**: Translate articles into multiple languages
- **Interactive Q&A**: Ask questions about news articles and get AI-generated answers
- **Smart Question Generation**: Automatically generates relevant questions about articles
- **Modern UI**: Beautiful and responsive user interface with horizontal scrolling news cards

## Technologies Used

- **Frontend**: Streamlit
- **AI/ML**: 
  - Groq for text generation
  - Transformers for question generation
  - Deep Translator for language translation
- **News API**: Newspaper3k for article extraction
- **NLP**: NLTK for text processing

## Prerequisites

- Python 3.8 or higher
- Groq API key
- News API key

## 🚀 Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/news-dashboard.git
cd news-dashboard
```

2. Create and activate a virtual environment:
```bash
python -m venv myenv
source myenv/bin/activate  # On Windows, use: myenv\Scripts\activate
```

3. Install the required packages:
```bash
pip install -r requirements.txt
```

4. Set up your environment variables:
Create a `.env` file in the root directory and add your Groq API key:
```
GROQ_API_KEY=your_api_key_here
```

## 💻 Usage

1. Start the Streamlit app:
```bash
streamlit run app.py
```

2. Open your web browser and navigate to the URL shown in the terminal (typically http://localhost:8501)

3. Use the dashboard:
   - Browse news by category
   - Click on articles to read full content
   - Use the summarize button to get AI-generated summaries
   - Translate articles using the language selector
   - Ask questions about articles using the AI chatbot
   - Explore generated questions about each article

## 📁 Project Structure

- `app.py`: Main Streamlit application
- `api.py`: News API integration
- `summarise_agent.py`: Article summarization using Groq
- `translate.py`: Multi-language translation functionality
- `question_generator.py`: AI-powered question generation
- `bot.py`: Q&A chatbot implementation

