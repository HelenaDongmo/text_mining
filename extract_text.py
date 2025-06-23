import fitz  # PyMuPDF
import re

def extract_text_from_pdf(pdf_path):
    doc = fitz.open(pdf_path)
    full_text = ""

    for page_num in range(len(doc)):
        page = doc[page_num]
        text = page.get_text()
        full_text += text + "\n"

    return full_text

def clean_text(text):
    # Remove multiple newlines and trim spaces
    text = re.sub(r'\n{2,}', '\n\n', text)
    return text.strip()

if __name__ == "__main__":
    pdf_file = "/home/helena/text_mining/irbookonlinereading.pdf"
    raw_text = extract_text_from_pdf(pdf_file)
    cleaned_text = clean_text(raw_text)

    with open("textbook_plain.txt", "w", encoding="utf-8") as f:
        f.write(cleaned_text)

    print("✅ Text extracted and saved to 'textbook_plain.txt'")