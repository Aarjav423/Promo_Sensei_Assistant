import json, faiss, pickle
from sentence_transformers import SentenceTransformer
import numpy as np

def ingest():
    with open("all_offers.json") as f:
        offers = json.load(f)

    model = SentenceTransformer('all-MiniLM-L6-v2')
    texts = [f"{o['title']} {o['description']} {o['discount']}" for o in offers]
    embeddings = model.encode(texts, convert_to_numpy=True)

    index = faiss.IndexFlatL2(embeddings.shape[1])
    index.add(embeddings)

    with open("offers_metadata.pkl", "wb") as f:
        pickle.dump(offers, f)

    faiss.write_index(index, "offers_index.faiss")

if __name__ == "__main__":
    ingest()
