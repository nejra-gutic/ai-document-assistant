import re

def build_qa_item(section: str, question: str, answer: str) -> dict:
    return {
        "section": section,
        "question": question.strip(),
        "answer": answer.strip(),
        "text": f"{question.strip()}\n{answer.strip()}"
    }

def split_text(text: str) -> list[str]:
    chunks = []

    numbered_pattern = r"(?m)^\s*(\d+)\.\s+(.+?)\n"

    all_matches = list(re.finditer(numbered_pattern, text))

    valid_matches = []
    expected_number = 1

    for match in all_matches:
        number = int(match.group(1))

        if number == expected_number:
            valid_matches.append(match)
            expected_number += 1

        if expected_number == 51:
            break

    for i, match in enumerate(valid_matches):
        question = match.group(0).strip()

        answer_start = match.end()

        if i + 1 < len(valid_matches):
            answer_end = valid_matches[i + 1].start()
        else:
            answer_end = len(text)

        answer = text[answer_start:answer_end].strip()

        item = build_qa_item(
            section="Hava Savunma Sistemleri Yarışması",
            question=question,
            answer=answer
        )

        chunks.append(item)

    return chunks


def extract_plain_qa(section_text: str) -> list[dict]:
    qa_pairs = []

    lines = [
        line.strip()
        for line in section_text.splitlines()
        if line.strip()
    ]

    current_question = None
    current_answer = []

    for line in lines:

        if line.endswith("?"):
            if current_question and current_answer:
                qa_pairs.append({
                    "question": current_question,
                    "answer": " ".join(current_answer).strip()
                })

            current_question = line
            current_answer = []

        else:
            if current_question:
                current_answer.append(line)

    if current_question and current_answer:
        qa_pairs.append({
            "question": current_question,
            "answer": " ".join(current_answer).strip()
        })

    return qa_pairs


def extract_long_qa_from_blocks(
    pages: list[dict],
    start_text: str
) -> list[dict]:

    qa_pairs = []
    blocks = []

    # 1. Iz svih stranica izvuci tekstualne blokove
    for page in pages:
        for block in page.get("blocks", []):
            if "lines" not in block:
                continue

            block_parts = []

            for line in block.get("lines", []):
                for span in line.get("spans", []):
                    text = span.get("text", "").strip()
                    size = span.get("size", 0)

                    if not text:
                        continue

                    # Ignoriši male reference / superscript brojeve
                    if size < 8:
                        continue

                    block_parts.append(text)

            block_text = " ".join(block_parts).strip()

            if block_text:
                blocks.append(block_text)

    # 2. Pronađi gdje počinje dugi Q&A dio
    start_index = None

    for i, block in enumerate(blocks):
        if start_text in block:
            start_index = i
            break

    if start_index is None:
        return []

    blocks = blocks[start_index:]

    # 3. Parsiraj pitanje -> odgovor
    current_question = None
    current_answer = []

    i = 0

    while i < len(blocks):
        block = blocks[i]

        # Ako blok sadrži ?, tretiramo ga kao pitanje
        if "?" in block:

            if current_question and current_answer:
                qa_pairs.append({
                    "question": current_question,
                    "answer": " ".join(current_answer).strip()
                })

            current_question = block
            current_answer = []

        # Poseban slučaj:
        # pitanje počne na kraju jedne stranice,
        # a završi u sljedećem bloku
        elif (
            i + 1 < len(blocks)
            and "?" in blocks[i + 1]
            and not block.endswith((".", "!", ":", ";"))
        ):
            combined_question = (
                block + " " + blocks[i + 1]
            ).strip()

            if current_question and current_answer:
                qa_pairs.append({
                    "question": current_question,
                    "answer": " ".join(current_answer).strip()
                })

            current_question = combined_question
            current_answer = []

            # Sljedeći blok smo već iskoristili
            i += 1

        else:
            if current_question:
                current_answer.append(block)

        i += 1

    # 4. Posljednji Q&A
    if current_question and current_answer:
        qa_pairs.append({
            "question": current_question,
            "answer": " ".join(current_answer).strip()
        })

    return qa_pairs