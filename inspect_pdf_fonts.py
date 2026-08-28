import fitz


document = fitz.open("data/rag-example-qa.pdf")

page = document[8]  # 9. stranica PDF-a, jer indeks kreće od 0

page_dict = page.get_text("dict")


for block in page_dict["blocks"]:
    if "lines" not in block:
        continue

    for line in block["lines"]:
        for span in line["spans"]:
            text = span["text"].strip()

            if not text:
                continue

            print("TEXT:", text)
            print("FONT:", span["font"])
            print("SIZE:", span["size"])
            print("FLAGS:", span["flags"])
            print("-" * 50)