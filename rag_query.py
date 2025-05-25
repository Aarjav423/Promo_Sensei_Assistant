import faiss
import pickle
from sentence_transformers import SentenceTransformer
from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY"),
    base_url=os.getenv("OPENROUTER_BASE_URL")
)

model = SentenceTransformer("all-MiniLM-L6-v2")

def query_offers(user_input: str) -> str:
    try:
        # 🔹 Load FAISS index
        index = faiss.read_index("offers_index.faiss")

        # 🔹 Load metadata
        with open("offers_metadata.pkl", "rb") as f:
            meta = pickle.load(f)

        # 🔹 Search vector DB
        vec = model.encode([user_input])
        _, idx = index.search(vec, 3)

        # 🔹 Build deal context
        context = "\n".join([
            f"🔸 {meta[i]['title']}\n{meta[i]['description']}\nDiscount: {meta[i]['discount']}\n"
            for i in idx[0]
        ])

        # 🔹 Call OpenRouter
        response = client.chat.completions.create(
            model="mistralai/mistral-7b-instruct",
            messages=[
                {"role": "system", "content": "You are Promo Sensei, a helpful shopping deals assistant."},
                {"role": "user", "content": f"Here are some deals:\n{context}\n\nUser query: {user_input}"}
            ]
        )

        return "\n Promo Sensei says:\n" + response.choices[0].message.content.strip()

    except FileNotFoundError as e:
        return f" Required file not found: {e.filename}"
    except Exception as e:
        return f" Unexpected error: {str(e)}"

# Entry point
if __name__ == "__main__":
    print(" Promo Sensei: Ask me about current shopping offers!\n")
    q = input("You: ")
    print(query_offers(q))
