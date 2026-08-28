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


LONG_QA_START = (
    "Bir takım, Kaggle aşamasında %95'lik bir doğruluk skoru elde ederek"
)


def build_qa_dataset(pdf_path: str) -> list[dict]:

    # Učitaj PDF
    text = load_pdf(pdf_path)
    pages = load_pdf_pages(pdf_path)
    sections = split_into_sections(text)

    # --------------------------------------------------
    # HSS - numerisani Q&A
    # --------------------------------------------------

    numbered_hss_qa = split_text(text)

    # --------------------------------------------------
    # HSS - bold Q&A
    # --------------------------------------------------

    hss_lines = extract_section_lines(
        pages,
        "Hava Savunma Sistemleri (HSS) yarışmasının görev aşamaları",
        "Genel Kurallar"
    )

    bold_hss_qa = extract_bold_qa(hss_lines)

    formatted_bold_hss_qa = [
        build_qa_item(
            section="Hava Savunma Sistemleri Yarışması",
            question=qa["question"],
            answer=qa["answer"]
        )
        for qa in bold_hss_qa
    ]

    all_hss_qa = numbered_hss_qa + formatted_bold_hss_qa

    # --------------------------------------------------
    # Genel Kurallar
    # --------------------------------------------------

    general_lines = extract_section_lines(
        pages,
        "Genel Kurallar",
        "E-Ticaret Hackathonu"
    )

    general_qa = extract_bold_qa(general_lines)

    formatted_general_qa = [
        build_qa_item(
            section="Genel Kurallar",
            question=qa["question"],
            answer=qa["answer"]
        )
        for qa in general_qa
    ]

    # --------------------------------------------------
    # E-Ticaret Hackathonu
    # --------------------------------------------------

    ecommerce_lines = extract_section_lines(
        pages,
        "E-Ticaret Hackathonu",
        "Yapay Zeka Destekli Adres Çözümleme Yarışması"
    )

    ecommerce_qa = extract_bold_qa(ecommerce_lines)

    formatted_ecommerce_qa = [
        build_qa_item(
            section="E-Ticaret Hackathonu",
            question=qa["question"],
            answer=qa["answer"]
        )
        for qa in ecommerce_qa
    ]

    # --------------------------------------------------
    # Address - kratki Q&A
    # --------------------------------------------------

    address_text = sections[
        "Yapay Zeka Destekli Adres Çözümleme Yarışması"
    ]

    short_address_text, _ = address_text.split(
        LONG_QA_START,
        1
    )

    address_short_qa = extract_plain_qa(
        short_address_text
    )

    formatted_address_short_qa = [
        build_qa_item(
            section="Yapay Zeka Destekli Adres Çözümleme Yarışması",
            question=qa["question"],
            answer=qa["answer"]
        )
        for qa in address_short_qa
    ]

    # --------------------------------------------------
    # Address - dugi Q&A
    # --------------------------------------------------

    address_long_qa = extract_long_qa_from_blocks(
        pages,
        LONG_QA_START
    )

    formatted_address_long_qa = [
        build_qa_item(
            section="Yapay Zeka Destekli Adres Çözümleme Yarışması",
            question=qa["question"],
            answer=qa["answer"]
        )
        for qa in address_long_qa
    ]

    # --------------------------------------------------
    # Spoji cijeli dataset
    # --------------------------------------------------

    all_qa = (
        all_hss_qa
        + formatted_general_qa
        + formatted_ecommerce_qa
        + formatted_address_short_qa
        + formatted_address_long_qa
    )

    return all_qa