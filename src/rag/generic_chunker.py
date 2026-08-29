def split_into_chunks(
    text: str,
    chunk_size: int = 800,
    overlap: int = 100
) -> list[str]:

    chunks = []
    start = 0

    while start < len(text):
        end = start + chunk_size

        # Avoid cutting a word at the end of a chunk
        if end < len(text):
            last_space = text.rfind(" ", start, end)

            if last_space != -1:
                end = last_space

        chunk = text[start:end].strip()

        if chunk:
            chunks.append(chunk)

        # Calculate the start of the next chunk
        next_start = max(end - overlap, 0)

        # Move to the next space if overlap starts inside a word
        if next_start > 0 and next_start < len(text):
            next_space = text.find(" ", next_start)

            if next_space != -1:
                next_start = next_space + 1

        if next_start <= start:
            next_start = end

        start = next_start

    return chunks