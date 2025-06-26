import re
import json

def parse_textbook(text_path, output_path):
    with open(text_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    data = []
    current_section = None
    paragraph_buffer = []

    # Patterns
    chapter_pattern = re.compile(r'^Chapter\s+(\d+)\b')
    section_pattern = re.compile(r'^(\d+\.\d+)\b')

    def flush_paragraph(section, buffer):
        paragraph = ' '.join([line.strip() for line in buffer]).strip()
        if paragraph and section:
            data.append({"section_id": section, "paragraph": paragraph})

    for line in lines:
        stripped = line.strip()

        # Skip empty header/footer artifacts
        if any(bad in stripped.lower() for bad in ["copyright", "green tea press", "http", "license"]):
            continue

        # Check for chapter
        chap_match = chapter_pattern.match(stripped)
        if chap_match:
            if paragraph_buffer and current_section:
                flush_paragraph(current_section, paragraph_buffer)
                paragraph_buffer = []
            current_section = chap_match.group(1)  # e.g., "1"
            continue

        # Check for section like 1.1, 1.2
        sec_match = section_pattern.match(stripped)
        if sec_match:
            if paragraph_buffer and current_section:
                flush_paragraph(current_section, paragraph_buffer)
                paragraph_buffer = []
            current_section = sec_match.group(1)  # e.g., "1.2"
            continue

        # Paragraph logic
        if stripped == "":
            if paragraph_buffer and current_section:
                flush_paragraph(current_section, paragraph_buffer)
                paragraph_buffer = []
        else:
            paragraph_buffer.append(line)

    # Flush final paragraph
    if paragraph_buffer and current_section:
        flush_paragraph(current_section, paragraph_buffer)

    with open(output_path, 'w', encoding='utf-8') as out_f:
        json.dump(data, out_f, ensure_ascii=False, indent=2)

    print(f"✅ Parsed {len(data)} paragraphs with section IDs into '{output_path}'")

if __name__ == "__main__":
    parse_textbook("/home/helena/text_mining/textbook_plain.txt", "structured_thinkpython.json")