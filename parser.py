import re
import json

def parse_textbook(text_path, output_path):
    with open(text_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    data = []
    current_section = None
    paragraph_buffer = []

    # Regex to detect valid hierarchical section headers like "1", "1.2", "1.2.3"
    section_pattern = re.compile(r'^(\d+(?:\.\d+)*)(\s+)(.+)')

    # Function to clean and save a paragraph under a section
    def flush_paragraph(section, buffer):
        paragraph = ' '.join([line.strip() for line in buffer]).strip()
        if paragraph and re.match(r'^\d+(\.\d+)*$', section):  # Ensure it's a valid section id
            data.append({"section_id": section, "paragraph": paragraph})

    # Define a list of keywords or phrases to filter out non-content noise
    noise_phrases = [
        "Online edition", "List of Tables", "Author Index", "Bibliography",
        "Cambridge University Press", "©", "copyright", "feedback welcome"
    ]

    for line in lines:
        stripped = line.strip()

        # Skip noise lines
        if any(noise.lower() in stripped.lower() for noise in noise_phrases):
            continue

        # Check for section header
        match = section_pattern.match(line)
        if match:
            if paragraph_buffer and current_section:
                flush_paragraph(current_section, paragraph_buffer)
                paragraph_buffer = []

            current_section = match.group(1)  # Only the numeric part like "1.2.3"
        else:
            if stripped == '':
                if paragraph_buffer and current_section:
                    flush_paragraph(current_section, paragraph_buffer)
                    paragraph_buffer = []
            else:
                paragraph_buffer.append(line)

    if paragraph_buffer and current_section:
        flush_paragraph(current_section, paragraph_buffer)

    # Save to JSON
    with open(output_path, 'w', encoding='utf-8') as out_f:
        json.dump(data, out_f, ensure_ascii=False, indent=2)

    print(f"✅ Parsed {len(data)} clean paragraphs with valid section IDs saved to '{output_path}'")

if __name__ == "__main__":
    parse_textbook("/home/helena/text_mining/textbook_plain.txt", "structured_textbook.json")