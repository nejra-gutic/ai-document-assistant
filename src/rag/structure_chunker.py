from src.rag.generic_chunker import split_into_chunks


def split_by_paragraphs(
    text: str
) -> list[str]:

    paragraphs = text.split("\n\n")

    cleaned_paragraphs = []

    for paragraph in paragraphs:
        paragraph = paragraph.strip()

        if paragraph:
            cleaned_paragraphs.append(
                paragraph
            )

    return cleaned_paragraphs


def create_structured_chunks(
    text: str,
    max_chunk_size: int = 800
) -> list[str]:

    paragraphs = split_by_paragraphs(text)

    chunks = []
    current_chunk = ""

    for paragraph in paragraphs:

        # If one paragraph is too large,
        # split it using the old fixed-size chunker
        if len(paragraph) > max_chunk_size:

            if current_chunk:
                chunks.append(current_chunk)
                current_chunk = ""

            large_paragraph_chunks = split_into_chunks(
                paragraph,
                chunk_size=max_chunk_size
            )

            chunks.extend(large_paragraph_chunks)

            continue

        if len(current_chunk) + len(paragraph) <= max_chunk_size:
            if current_chunk:
                current_chunk += "\n\n"

            current_chunk += paragraph

        else:
            if current_chunk:
                chunks.append(current_chunk)

            current_chunk = paragraph

    if current_chunk:
        chunks.append(current_chunk)

    return chunks