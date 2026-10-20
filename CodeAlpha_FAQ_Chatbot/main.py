from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import re

app = FastAPI(title="FAQ Chatbot", description="A simple FAQ chatbot using TF-IDF and cosine similarity.")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Restrict this to your frontend domain when deploying.
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Sample FAQ knowledge base. Edit these questions and answers for your chosen topic.
FAQS = [
    {
        "question": "What is this chatbot?",
        "answer": "This is an FAQ chatbot that matches your question with the closest question in its knowledge base."
    },
    {
        "question": "How can I contact customer support?",
        "answer": "You can contact customer support by emailing support@example.com. Replace this sample email with your real support address."
    },
    {
        "question": "What are your working hours?",
        "answer": "Our sample support hours are Monday to Friday, 9 AM to 5 PM."
    },
    {
        "question": "How do I create an account?",
        "answer": "Choose the Sign Up option on the website and complete the registration form."
    },
    {
        "question": "I forgot my password. How can I reset it?",
        "answer": "Select Forgot Password on the login page and follow the instructions sent to your registered email."
    },
    {
        "question": "Is the service free?",
        "answer": "This demo chatbot is free to run locally. Add your own pricing details if you are using it for a real product."
    },
    {
        "question": "How can I track my order?",
        "answer": "Open your account, go to My Orders, and select the order you want to track. This is an example answer you can customize."
    },
    {
        "question": "Can I cancel an order?",
        "answer": "If an order has not shipped, open My Orders and check whether a cancellation option is available."
    },
    {
        "question": "Which languages does this chatbot support?",
        "answer": "This starter version matches English questions. You can extend the FAQ data and add multilingual NLP support later."
    },
    {
        "question": "How does the chatbot find an answer?",
        "answer": "It cleans the text, converts FAQ questions into TF-IDF vectors, and uses cosine similarity to find the closest match."
    },
    {
        "question": "What should I do if I do not get a useful answer?",
        "answer": "Try rephrasing your question or contact support. You can also add more relevant questions and answers to the FAQ list in main.py."
    },
]

def preprocess(text: str) -> str:
    """Basic NLP text cleaning: lowercase, remove URLs/punctuation, and normalize spaces."""
    text = text.lower()
    text = re.sub(r"https?://\S+|www\.\S+", " ", text)
    text = re.sub(r"[^a-z0-9\s]", " ", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text

faq_questions = [preprocess(item["question"]) for item in FAQS]
vectorizer = TfidfVectorizer(ngram_range=(1, 2), stop_words="english")
faq_matrix = vectorizer.fit_transform(faq_questions)

class ChatRequest(BaseModel):
    message: str = Field(min_length=1, max_length=1000)

@app.get("/api/faqs")
def get_faqs():
    return {"faqs": [{"question": f["question"]} for f in FAQS]}

@app.post("/api/chat")
def chat(request: ChatRequest):
    user_message = preprocess(request.message)
    if not user_message:
        return {
            "answer": "Please type a question using a few words so I can find a matching FAQ.",
            "matched_question": None,
            "confidence": 0.0
        }

    user_vector = vectorizer.transform([user_message])
    scores = cosine_similarity(user_vector, faq_matrix).flatten()
    best_index = int(scores.argmax())
    best_score = float(scores[best_index])

    # Similarity threshold prevents unrelated questions from receiving a misleading answer.
    if best_score < 0.12:
        return {
            "answer": "Sorry, I couldn't find a close FAQ for that question. Try rephrasing it, or contact customer support.",
            "matched_question": None,
            "confidence": round(best_score, 3)
        }

    return {
        "answer": FAQS[best_index]["answer"],
        "matched_question": FAQS[best_index]["question"],
        "confidence": round(best_score, 3)
    }

app.mount("/", StaticFiles(directory="static", html=True), name="static")
