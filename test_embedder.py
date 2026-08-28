from src.rag.pipeline import build_qa_dataset
from src.rag.embedder import Embedder
from src.rag.vector_store import VectorStore

import json


PDF_PATH = "data/rag-example-qa.pdf"


# 1. Napravi Q&A dataset
all_qa = build_qa_dataset(PDF_PATH)


# 2. Uzmi tekst iz svakog Q&A
texts = [
    qa["text"]
    for qa in all_qa
]


# 3. Napravi embeddings
embedder = Embedder()

embeddings = embedder.embed_texts(texts)


# 4. Napravi FAISS index
vector_store = VectorStore(
    dimension=embeddings.shape[1]
)

vector_store.add(embeddings)

vector_store.save("data/faiss.index")

with open(
    "data/metadata.json",
    "w",
    encoding="utf-8"
) as file:
    json.dump(
        all_qa,
        file,
        ensure_ascii=False,
        indent=2
    )


# 5. Test semantic searcha
query = "Bir takım kaç kişiden oluşabilir?"

query_embedding = embedder.embed_text(query)

distances, indices = vector_store.search(
    query_embedding,
    k=3
)


# 6. Ispis rezultata
print("Broj Q&A:", len(all_qa))
print("Shape embeddings:", embeddings.shape)
print(
    "Broj vektora u FAISS-u:",
    vector_store.index.ntotal
)

print("\nQUERY:")
print(query)

print("\n--- TOP 3 RESULTS ---")

for distance, index in zip(distances, indices):
    qa = all_qa[index]

    print("\nDistance:", distance)
    print("Section:", qa["section"])
    print("Question:", qa["question"])
    print("Answer:", qa["answer"])