from src.rag.embedder import Embedder
from test_loader import all_qa
from src.rag.vector_store import VectorStore


embedder = Embedder()

# Uzimamo "text" iz svakog Q&A dictionaryja
texts = [qa["text"] for qa in all_qa]

# Pravimo embedding za svaki Q&A
embeddings = embedder.embed_texts(texts)

print("Broj Q&A:", len(all_qa))
print("Broj tekstova:", len(texts))
print("Shape embeddings:", embeddings.shape)

vector_store = VectorStore(dimension=384)

vector_store.add(embeddings)

print("Broj vektora u FAISS-u:", vector_store.index.ntotal)


query = "Bir takım kaç kişiden oluşabilir?"

query_embedding = embedder.embed_text(query)

distances, indices = vector_store.search(
    query_embedding,
    k=3
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

