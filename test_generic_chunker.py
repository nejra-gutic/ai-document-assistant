from src.rag.generic_chunker import split_into_chunks


text = """
This is the first part of the document. It contains some information
about the company and its internal rules.

This is the second paragraph. It contains additional details about
employees, responsibilities, and company policies.

This is the third paragraph. It contains information about vacation,
working hours, and remote work.
"""

chunks = split_into_chunks(
    text,
    chunk_size=100,
    overlap=20
)

print("Broj chunkova:", len(chunks))

for i, chunk in enumerate(chunks, start=1):
    print(f"\n--- CHUNK {i} ---")
    print(chunk)