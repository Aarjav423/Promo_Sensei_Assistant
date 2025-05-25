import os
from slack_bolt import App
from slack_bolt.adapter.flask import SlackRequestHandler
from flask import Flask, request
from rag_query import query_offers
from ingest_to_vector_db import ingest
from scraper import save_all_offers
from dotenv import load_dotenv
load_dotenv()

# Initialize Slack app
app = App(token=os.getenv("SLACK_BOT_TOKEN"), signing_secret=os.getenv("SLACK_SIGNING_SECRET"))

# Create Flask app
flask_app = Flask(__name__)
handler = SlackRequestHandler(app)

# Slash command handler
@app.command("/promosensei")
def handle_command(ack, respond, command):
    ack()
    text = command['text'].strip()
    print(f"Received: {text}")

    if text.startswith("search "):
        result = query_offers(text[7:])
    elif text == "summary":
        result = query_offers("top 3 latest deals")
    elif text.startswith("brand "):
        brand = text[6:].strip()
        result = query_offers(f"offers from {brand}")
    elif text == "refresh":
        save_all_offers()
        ingest()
        result = "✅ Refreshed offers from the web!"
    else:
        result = "❗ Invalid command. Try `/promosensei search [query]`"

    respond(result)

# Route for Slack events
@flask_app.route("/slack/events", methods=["POST"])
def slack_events():
    return handler.handle(request)

# Start Flask app
if __name__ == "__main__":
    flask_app.run(port=5000)

