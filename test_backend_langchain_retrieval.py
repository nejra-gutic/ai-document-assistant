from backend.main import rag_service


query = "Bir takım kaç kişiden oluşabilir?"

documents = rag_service.retrieve(query)

print("QUERY:")
print(query)

print("\nRESULTS:")

for i, document in enumerate(documents, start=1):
    print(f"\n--- RESULT {i} ---")
    print("CONTENT:")
    print(document.page_content)

    print("\nMETADATA:")
    print(document.metadata)