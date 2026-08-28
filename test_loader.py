from src.rag.loader import load_pdf, load_pdf_pages
from src.rag.chunker import split_text, build_qa_item
from src.rag.bold_qa_parser import extract_section_lines, extract_bold_qa


# 1. Učitaj obični tekst
text = load_pdf("data/rag-example-qa.pdf")

# 2. Prvih 50 numerisanih Q&A
numbered_qa = split_text(text)

# 3. Učitaj strukturirani PDF sadržaj
pages = load_pdf_pages("data/rag-example-qa.pdf")

# 4. Uzmi samo dugi bold dio HSS sekcije
hss_lines = extract_section_lines(
    pages,
    "Hava Savunma Sistemleri (HSS) yarışmasının görev aşamaları",
    "Genel Kurallar"
)

# 5. Izvuci 9 bold Q&A
bold_qa = extract_bold_qa(hss_lines)

# 6. Prebaci bold Q&A u isti format kao prvih 50
formatted_bold_qa = []

for qa in bold_qa:
    item = build_qa_item(
        section="Hava Savunma Sistemleri Yarışması",
        question=qa["question"],
        answer=qa["answer"]
    )

    formatted_bold_qa.append(item)

# 7. Spoji ih
all_hss_qa = numbered_qa + formatted_bold_qa


print("Numerisana Q&A:", len(numbered_qa))
print("Bold Q&A:", len(formatted_bold_qa))
print("Ukupno:", len(all_hss_qa))

print("\n--- PRVI ELEMENT ---")
print(all_hss_qa[0])

print("\n--- ELEMENT 51 ---")
print(all_hss_qa[50])

print("\n--- POSLJEDNJI ELEMENT ---")
print(all_hss_qa[-1])