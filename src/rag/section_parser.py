SECTION_TITLES = [
    "Hava Savunma Sistemleri Yarışması",
    "Genel Kurallar",
    "E-Ticaret Hackathonu",
    "Yapay Zeka Destekli Adres Çözümleme Yarışması",
]


def split_into_sections(text: str) -> dict[str, str]:
    sections = {}

    positions = []

    for title in SECTION_TITLES:
        index = text.find(title)

        if index != -1:
            positions.append((index, title))

    positions.sort()

    for i, (start_index, title) in enumerate(positions):
        content_start = start_index + len(title)

        if i + 1 < len(positions):
            content_end = positions[i + 1][0]
        else:
            content_end = len(text)

        section_text = text[content_start:content_end].strip()

        sections[title] = section_text

    return sections