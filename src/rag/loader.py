from pathlib import Path
import pymupdf


def clean_text(text: str) -> str:
    text = text.replace("+", "i")
    text = text.replace(
        "Hava Savunma S)stemler) Yarışması",
        "Hava Savunma Sistemleri Yarışması"
    )

    return text


def load_pdf(file_path: str) -> str:
    path = Path(file_path)

    if not path.exists():
        raise FileNotFoundError(f"PDF file not found: {file_path}")

    document = pymupdf.open(path)

    pages = []

    for page in document:
        text = page.get_text()

        if text:
            pages.append(clean_text(text))

    return "\n".join(pages)


def load_pdf_pages(file_path: str):
    document = pymupdf.open(file_path)

    pages = []

    for page in document:
        pages.append(page.get_text("dict"))

    return pages