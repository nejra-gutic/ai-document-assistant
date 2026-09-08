from src.rag.structure_chunker import create_structured_chunks


text = """
This is a short first paragraph.

This is a very long paragraph that contains a lot of information about the company and its artificial intelligence system. The company developed a retrieval system for searching documents and finding relevant information. The system processes documents, creates chunks, generates embeddings, and stores them inside a vector database. When the user asks a question, the application converts the question into an embedding and searches for similar chunks. The retrieved information is then sent to a large language model which generates the final answer for the user. This paragraph is intentionally very long because we want to test what happens when a single paragraph is larger than the maximum allowed chunk size.

This is a short final paragraph.
"""


chunks = create_structured_chunks(
    text,
    max_chunk_size=220
)

print(f"Total chunks: {len(chunks)}")

for i, chunk in enumerate(chunks, start=1):
    print(f"\n--- CHUNK {i} ({len(chunk)} characters) ---")
    print(chunk)