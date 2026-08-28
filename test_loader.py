from src.rag.loader import load_pdf, load_pdf_pages
from src.rag.chunker import (
    split_text,
    build_qa_item,
    extract_plain_qa,
    extract_long_qa_from_blocks,
)
from src.rag.bold_qa_parser import (
    extract_section_lines,
    extract_bold_qa,
)
from src.rag.section_parser import split_into_sections
import random


PDF_PATH = "data/rag-example-qa.pdf"

LONG_QA_START = (
    "Bir takım, Kaggle aşamasında %95'lik bir doğruluk skoru elde ederek"
)


# --------------------------------------------------
# 1. Učitaj PDF
# --------------------------------------------------

text = load_pdf(PDF_PATH)
pages = load_pdf_pages(PDF_PATH)
sections = split_into_sections(text)


# --------------------------------------------------
# 2. HSS - prvih 50 numerisanih Q&A
# --------------------------------------------------

numbered_hss_qa = split_text(text)


# --------------------------------------------------
# 3. HSS - dugi bold Q&A
# --------------------------------------------------

hss_long_lines = extract_section_lines(
    pages,
    "Hava Savunma Sistemleri (HSS) yarışmasının görev aşamaları",
    "Genel Kurallar"
)

bold_hss_qa = extract_bold_qa(hss_long_lines)

formatted_bold_hss_qa = []

for qa in bold_hss_qa:
    formatted_bold_hss_qa.append(
        build_qa_item(
            section="Hava Savunma Sistemleri Yarışması",
            question=qa["question"],
            answer=qa["answer"]
        )
    )

all_hss_qa = numbered_hss_qa + formatted_bold_hss_qa


# --------------------------------------------------
# 4. Genel Kurallar
# --------------------------------------------------

general_lines = extract_section_lines(
    pages,
    "Genel Kurallar",
    "E-Ticaret Hackathonu"
)

general_qa = extract_bold_qa(general_lines)

formatted_general_qa = []

for qa in general_qa:
    formatted_general_qa.append(
        build_qa_item(
            section="Genel Kurallar",
            question=qa["question"],
            answer=qa["answer"]
        )
    )


# --------------------------------------------------
# 5. E-Ticaret Hackathonu
# --------------------------------------------------

ecommerce_lines = extract_section_lines(
    pages,
    "E-Ticaret Hackathonu",
    "Yapay Zeka Destekli Adres Çözümleme Yarışması"
)

ecommerce_qa = extract_bold_qa(ecommerce_lines)

formatted_ecommerce_qa = []

for qa in ecommerce_qa:
    formatted_ecommerce_qa.append(
        build_qa_item(
            section="E-Ticaret Hackathonu",
            question=qa["question"],
            answer=qa["answer"]
        )
    )


# --------------------------------------------------
# 6. Yapay Zeka Destekli Adres Çözümleme
#    - odvoji kratki i dugi dio
# --------------------------------------------------

address_text = sections[
    "Yapay Zeka Destekli Adres Çözümleme Yarışması"
]

short_address_text, _ = address_text.split(
    LONG_QA_START,
    1
)


# --------------------------------------------------
# 7. Address - kratkih 30 Q&A
# --------------------------------------------------

address_short_qa = extract_plain_qa(short_address_text)

formatted_address_short_qa = []

for qa in address_short_qa:
    formatted_address_short_qa.append(
        build_qa_item(
            section="Yapay Zeka Destekli Adres Çözümleme Yarışması",
            question=qa["question"],
            answer=qa["answer"]
        )
    )


# --------------------------------------------------
# 8. Address - dugi Q&A
# --------------------------------------------------

address_long_qa = extract_long_qa_from_blocks(
    pages,
    LONG_QA_START
)

formatted_address_long_qa = []

for qa in address_long_qa:
    formatted_address_long_qa.append(
        build_qa_item(
            section="Yapay Zeka Destekli Adres Çözümleme Yarışması",
            question=qa["question"],
            answer=qa["answer"]
        )
    )


# --------------------------------------------------
# 9. Spoji sve Q&A iz dokumenta
# --------------------------------------------------

all_qa = (
    all_hss_qa
    + formatted_general_qa
    + formatted_ecommerce_qa
    + formatted_address_short_qa
    + formatted_address_long_qa
)


# --------------------------------------------------
# 10. Test ispisi
# --------------------------------------------------

print("HSS numerisana Q&A:", len(numbered_hss_qa))
print("HSS bold Q&A:", len(formatted_bold_hss_qa))
print("Ukupno HSS:", len(all_hss_qa))

print("Genel Kurallar Q&A:", len(formatted_general_qa))
print("E-Ticaret Hackathonu Q&A:", len(formatted_ecommerce_qa))

print("Address kratki Q&A:", len(formatted_address_short_qa))
print("Address dugi Q&A:", len(formatted_address_long_qa))

print("UKUPNO SVI Q&A:", len(all_qa))


print("\n--- PRVI Q&A U DOKUMENTU ---")
print(all_qa[0]["question"])


print("\n--- PRVI DUGI ADDRESS Q&A ---")
print(formatted_address_long_qa[0]["question"])


print("\n--- POSLJEDNJI Q&A U DOKUMENTU ---")
print(all_qa[-1]["question"])


random_qa = random.choice(all_qa)

print("\n--- RANDOM Q&A ---")
print("SECTION:")
print(random_qa["section"])

print("\nQUESTION:")
print(random_qa["question"])

print("\nANSWER:")
print(random_qa["answer"])