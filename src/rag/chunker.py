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