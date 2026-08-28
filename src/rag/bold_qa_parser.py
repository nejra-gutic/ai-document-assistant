def looks_like_question(text: str) -> bool:
    text = text.strip()

    if len(text.split()) < 5:
        return False

    return (
        "?" in text
        or text.endswith("açıklayınız.")
        or text.endswith("analiz ediniz.")
        or text.endswith("nedir?")
        or text.endswith("nelerdir?")
    )


def extract_section_lines(
    pages: list[dict],
    start_title: str,
    end_title: str
) -> list[dict]:

    section_lines = []
    inside_section = False

    for page in pages:
        for block in page.get("blocks", []):
            for line in block.get("lines", []):

                line_text_parts = []

                for span in line.get("spans", []):
                    text = span.get("text", "").strip()

                    if text:
                        line_text_parts.append(text)

                line_text = " ".join(line_text_parts).strip()

                if not line_text:
                    continue

                if not inside_section and start_title in line_text:
                    inside_section = True

                # Pronašli smo početak sljedeće sekcije
                if inside_section and end_title in line_text:
                    return section_lines

                if inside_section:
                    section_lines.append(line)

    return section_lines


def extract_bold_qa(lines: list[dict]) -> list[dict]:
    qa_pairs = []

    current_bold_block = []
    current_answer = []
    current_question = None

    for line in lines:
        line_parts = []
        line_is_bold = True
        has_visible_text = False

        for span in line.get("spans", []):
            text = span.get("text", "").strip()
            font = span.get("font", "")
            size = span.get("size", 0)

            if not text:
                continue

            # Ignorišemo male reference / superscript brojeve
            if size < 8:
                continue

            has_visible_text = True
            line_parts.append(text)

            if "Bold" not in font:
                line_is_bold = False

        if not has_visible_text:
            continue

        line_text = " ".join(line_parts).strip()

        # Ako je linija bold, skupljamo je
        if line_is_bold:
            current_bold_block.append(line_text)
            continue

        # Došli smo do obične linije.
        # To znači da je prethodni bold blok završen.
        if current_bold_block:
            bold_text = " ".join(current_bold_block).strip()


            if looks_like_question(bold_text):

                # Sačuvaj prethodni Q&A
                if current_question and current_answer:
                    qa_pairs.append({
                        "question": current_question,
                        "answer": " ".join(current_answer).strip()
                    })

                # Novi bold blok postaje novo pitanje
                current_question = bold_text
                current_answer = []

            else:
                # Bold tekst koji nije pitanje
                # tretiramo kao dio odgovora
                if current_question:
                    current_answer.append(bold_text)

            current_bold_block = []

        # Običan tekst pripada odgovoru
        if current_question:
            current_answer.append(line_text)

    # Ako je na kraju ostao bold blok
    if current_bold_block:
        bold_text = " ".join(current_bold_block).strip()

        print("BOLD BLOCK:", bold_text)
        print(
            "LOOKS LIKE QUESTION:",
            looks_like_question(bold_text)
        )
        print("-" * 80)

        if looks_like_question(bold_text):

            if current_question and current_answer:
                qa_pairs.append({
                    "question": current_question,
                    "answer": " ".join(current_answer).strip()
                })

            current_question = bold_text
            current_answer = []

        else:
            if current_question:
                current_answer.append(bold_text)

    # Sačuvaj posljednji Q&A
    if current_question and current_answer:
        qa_pairs.append({
            "question": current_question,
            "answer": " ".join(current_answer).strip()
        })

    return qa_pairs