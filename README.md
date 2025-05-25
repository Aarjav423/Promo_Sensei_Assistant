# Promo Sensei

Promo Sensei is a Slack-based or web-based assistant that helps users find current promotional offers across e-commerce sites using scraping, vector search, and LLMs.

## Features

- Scrapes real-time offers
- FAISS-powered vector search
- OpenAI GPT-based responses
- Slackbot & web UI

## How to Run

1. `python scraper.py`
2. `python ingest_to_vector_db.py`
3. `python rag_query.py` OR `python slackbot.py` OR `python app.py`

## Sample Queries

- "Flat 50% deals on cosmetics?"
- "Any Puma sportswear offers?"
- "Latest mobile deals from Flipkart?"

## Setup Instructions

1. Clone the repo and install dependencies:
   pip install -r requirements.txt

2. Add your API keys to [.env](http://_vscodecontentref_/11) (see sample in repo).

3. Scrape and ingest offers:
   python [scraper.py](http://_vscodecontentref_/12)
   python [ingest_to_vector_db.py](http://_vscodecontentref_/13)

4. Run the web app:
   python [app.py](http://_vscodecontentref_/14)

5. Or run the Slack bot:
   python [slackbot.py](http://_vscodecontentref_/15)

## Key Design Decisions

- **Retrieval-Augmented Generation (RAG):** Uses FAISS for semantic search over offers, then LLM (OpenAI via OpenRouter) for natural language answers.
- **Extensible Scraping:** Each brand/site can have its own scraping function.
- **Multi-Interface:** Supports both web and Slack interfaces for user queries.
