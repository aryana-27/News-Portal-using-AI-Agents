import streamlit as st
import hashlib
import api
import summarise_agent
import translate
import question_generator
import bot

# --- Page Configuration ---
st.set_page_config(
    page_title="News Dashboard",
    page_icon="📰",
    layout="wide"
)

# --- Custom CSS (keeping your existing CSS as it's good) ---
st.markdown("""
<style>
    /* Main styling */
    .main-title {
        text-align: center;
        color: #1f2937;
        font-size: 2.5rem;
        font-weight: 700;
        margin-bottom: 2rem;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.1);
    }
    
    .category-section {
        margin-bottom: 3rem;
    }
    
    .category-title {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 1rem 1.5rem;
        border-radius: 12px;
        font-size: 1.5rem;
        font-weight: 600;
        margin-bottom: 1.5rem;
        text-align: center;
        box-shadow: 0 4px 12px rgba(102, 126, 234, 0.3);
    }
    
    .news-grid {
        display: grid;
        grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
        gap: 1.5rem;
        margin: 1.5rem 0;
    }
    
    .news-card {
        background: white;
        border-radius: 16px;
        overflow: hidden;
        box-shadow: 0 8px 24px rgba(0, 0, 0, 0.1);
        transition: all 0.3s ease;
        border: 1px solid #e5e7eb;
        height: 100%;
        display: flex;
        flex-direction: column;
    }
    
    .news-card:hover {
        transform: translateY(-8px);
        box-shadow: 0 16px 32px rgba(0, 0, 0, 0.15);
        border-color: #667eea;
    }
    
    .news-image {
        width: 100%;
        height: 200px;
        object-fit: cover;
        transition: transform 0.3s ease;
    }
    
    .news-card:hover .news-image {
        transform: scale(1.05);
    }
    
    .news-content {
        padding: 1.25rem;
        flex-grow: 1;
        display: flex;
        flex-direction: column;
    }
    
    .news-title {
        font-size: 1.1rem;
        font-weight: 600;
        color: #1f2937;
        line-height: 1.4;
        margin-bottom: 0.75rem;
        display: -webkit-box;
        -webkit-line-clamp: 3;
        -webkit-box-orient: vertical;
        overflow: hidden;
        flex-grow: 1;
    }
    
    .news-date {
        color: #6b7280;
        font-size: 0.875rem;
        margin-top: auto;
        padding-top: 0.75rem;
        border-top: 1px solid #f3f4f6;
    }
    
    .no-articles {
        text-align: center;
        padding: 2rem;
        color: #6b7280;
        font-size: 1.1rem;
        background: #f9fafb;
        border-radius: 12px;
        border: 2px dashed #d1d5db;
    }
    
    .sidebar-title {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 1rem;
        border-radius: 12px;
        text-align: center;
        font-weight: 600;
        margin-bottom: 1.5rem;
    }

    /* New styles for question section (optional, but good for visual separation) */
    .question-section {
        background-color: #f0f2f6; /* Light grey background */
        border-radius: 10px;
        padding: 20px;
        margin-top: 20px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.05);
    }
    .question-title-text {
        font-size: 1.25rem;
        font-weight: 600;
        color: #333;
        margin-bottom: 1rem;
    }
</style>
""", unsafe_allow_html=True)

# --- Session State ---
if "selected_article" not in st.session_state:
    st.session_state.selected_article = None
if "translated_text" not in st.session_state:
    st.session_state.translated_text = None
if "selected_question" not in st.session_state:
    st.session_state.selected_question = None
if "Youtube" not in st.session_state:
    st.session_state.Youtube = None

# --- Sidebar: AI Chatbot ---
st.sidebar.markdown('<div class="sidebar-title">🤖 AI News Bot</div>', unsafe_allow_html=True)
headline_input = st.sidebar.text_input("Enter news headline")
user_question = st.sidebar.text_input("Ask your question")

if st.sidebar.button("Get Answer") and headline_input and user_question:
    articles = api.fetch_news(headline_input)
    if articles:
        response = bot.get_response(articles[0]['content'], user_question)
        st.sidebar.markdown(f"Answer: {response}")
    else:
        st.sidebar.warning("No article found for that headline.")

# --- Main Page ---
if st.session_state.selected_article is None:
    st.markdown('<h1 class="main-title">📰 News Dashboard</h1>', unsafe_allow_html=True)
    
    categories = ["India", "US", "stock market", "Movies", "health", "sports", "technology"]

    for category in categories:
        st.markdown(f'<div class="category-section">', unsafe_allow_html=True)
        st.markdown(f'<div class="category-title">{category.upper()}</div>', unsafe_allow_html=True)
        
        articles = api.fetch_news(category)

        if articles:
            num_articles = min(len(articles), 6)
            cols_per_row = 3
            
            for i in range(0, num_articles, cols_per_row):
                cols = st.columns(cols_per_row)
                
                for j in range(cols_per_row):
                    if i + j < num_articles:
                        article = articles[i + j]
                        with cols[j]:
                            with st.container():
                                if article.get('image'):
                                    st.image(article['image'], use_column_width=True)
                                else:
                                    st.image("https://via.placeholder.com/300x200?text=No+Image", use_column_width=True)
                                
                                st.markdown(f"**{article['title'][:100]}{'...' if len(article['title']) > 100 else ''}**")
                                
                                if article.get('publishedAt'):
                                    st.caption(f"📅 {article['publishedAt']}")
                                
                                unique_key = hashlib.md5((category + article['title'] + str(i + j)).encode()).hexdigest()
                                
                                if st.button("Read Full Article", key=unique_key, type="primary"):
                                    st.session_state.selected_article = article
                                    st.rerun()
                            
                            st.markdown("<br>", unsafe_allow_html=True)
        else:
            st.markdown('<div class="no-articles">📭 No articles found for this category</div>', unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)
        st.markdown("---")

# --- Article View ---
else:
    article = st.session_state.selected_article

    # Article Header
    if article.get('image'):
        st.image(article['image'], use_column_width=True)
    st.title(article['title'])

    col1, col2 = st.columns(2)

    with col1:
        if st.button("Summarize"):
            summary = summarise_agent.summarize_text(article['content'])
            st.markdown("Summary:")
            st.markdown("\n".join([f"- {line}" for line in summary.split(". ") if line.strip()]))

    with col2:
        lang = st.selectbox("Select target language", translate.SUPPORTED_LANGUAGES, key="translate_lang")
        if st.button("Translate"):
            if lang:
                st.session_state.translated_text = translate.translate_text(article['content'], lang)
                st.rerun()

    # Display article content
    st.markdown("Full Article:")
    content_to_display = st.session_state.translated_text or article['content']
    st.write(content_to_display)

    st.markdown('<div class="question-section">', unsafe_allow_html=True)
    st.markdown('<div class="question-title-text">🤔 Related Questions</div>', unsafe_allow_html=True)

    questions = question_generator.generate_questions(article['content'])[:5] # Get up to 5 questions

    if questions:
        for i, q in enumerate(questions):
            # Use st.expander for a clean "Click to reveal answer" experience
            with st.expander(f"**{i+1}. {q}**"):
                # Generate and display the answer when the expander is opened
                answer = bot.get_response(article['content'], q)
                st.write(answer)
    else:
        st.info("No related questions could be generated for this article.")
    
    st.markdown('</div>', unsafe_allow_html=True) # Close question-section div

    # Back Button
    if st.button("🔙 Back to All News"):
        st.session_state.selected_article = None
        st.session_state.translated_text = None
        st.session_state.selected_question = None
        st.session_state.Youtube = None
        st.rerun()