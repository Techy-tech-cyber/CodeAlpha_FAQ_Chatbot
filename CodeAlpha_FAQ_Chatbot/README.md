# CodeAlpha Task 2 — FAQ Chatbot

A responsive FAQ chatbot built with FastAPI, HTML, CSS, JavaScript, and scikit-learn.

## Features
- Sample FAQ questions and answers in `main.py`
- Text preprocessing (lowercase, URL/punctuation cleanup, whitespace normalization)
- TF-IDF vectorization with unigram and bigram features
- Cosine similarity to select the closest FAQ
- Similarity threshold for questions with no close match
- Chat UI with suggested questions, conversation bubbles, and clear-chat button
- JSON API endpoint and interactive API docs

## Run locally (Windows / VS Code)

Open a terminal in this project folder and run:

```powershell
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
python -m uvicorn main:app --reload
```

Then open:
- Chat UI: http://127.0.0.1:8000
- API documentation: http://127.0.0.1:8000/docs
- FAQ list: http://127.0.0.1:8000/api/faqs

## API example

`POST /api/chat`

```json
{
  "message": "I can't remember my password"
}
```

Example response:

```json
{
  "answer": "Select Forgot Password on the login page and follow the instructions sent to your registered email.",
  "matched_question": "I forgot my password. How can I reset it?",
  "confidence": 0.5
}
```

The confidence number depends on the question and the fitted FAQ data, so the exact value can vary.

## Customize the FAQs
Edit the `FAQS` list in `main.py`. Each item needs a `question` and an `answer`. Keep the questions relevant to the topic/product you choose.

## Notes
This is a small retrieval-based FAQ chatbot, not a generative AI chatbot. It chooses the closest stored answer and does not invent new answers. For deployment, restrict CORS to your frontend domain and consider adding rate limits and a real support contact.
