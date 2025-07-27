import os
import json
import pdfplumber
from collections import defaultdict
import re

# --- Utility Functions ---

def is_bold(fontname):
    return fontname and any(weight in fontname.lower() for weight in ["bold", "bd", "black"])

def is_valid_heading(text):
    if not text or len(text.strip()) < 4:
        return False
    if re.match(r"^\d+$", text.strip()):
        return False
    if "@" in text or re.search(r"\.com|\.(org|edu|net)", text):
        return False
    return True

def prettify_heading(text):
    # Add spacing between glued words and handle numeric-word boundaries
    text = re.sub(r'(?<=[a-z])(?=[A-Z])', ' ', text)
    text = re.sub(r'(?<=[A-Z])(?=[A-Z][a-z])', ' ', text)
    text = re.sub(r'([a-z])([A-Z0-9])', r'\1 \2', text)
    text = re.sub(r'([A-Z])([A-Z][a-z])', r'\1 \2', text)
    text = re.sub(r'(?<=[A-Za-z])(?=\d)', ' ', text)
    text = re.sub(r'(?<=\d)(?=[A-Za-z])', ' ', text)
    return re.sub(r'\s+', ' ', text).strip()

# --- Core Outline Extraction ---

def extract_outline_from_pdf(file_path):
    outline = []
    font_counter = defaultdict(int)
    text_blocks = []

    with pdfplumber.open(file_path) as pdf:
        for page_num, page in enumerate(pdf.pages, 1):
            for char in page.chars:
                text = char.get("text", "").strip()
                fontname = char.get("fontname", "").lower()
                font_size = round(char.get("size", 0), 1)
                x0 = round(char.get("x0", 0), 1)
                top = round(char.get("top", 0), 1)

                if not text:
                    continue

                text_blocks.append({
                    "text": text,
                    "size": font_size,
                    "fontname": fontname,
                    "x0": x0,
                    "top": top,
                    "page": page_num
                })

    # Group text by (page, line_top)
    grouped_lines = defaultdict(list)
    for block in text_blocks:
        key = (block["page"], round(block["top"] / 2) * 2)
        grouped_lines[key].append(block)

    lines = []
    for (page, top), group in grouped_lines.items():
        group_sorted = sorted(group, key=lambda x: x["x0"])
        line_text = "".join([w["text"] for w in group_sorted]).strip()
        if not is_valid_heading(line_text):
            continue

        size = group_sorted[0].get("size", 0)
        fontname = group_sorted[0].get("fontname", "")

        if is_bold(fontname):
            lines.append({
                "text": line_text,
                "size": size,
                "fontname": fontname,
                "page": page
            })
            font_counter[size] += 1

    # Heading size thresholds
    sorted_fonts = sorted(font_counter.items(), key=lambda x: (-x[1], -x[0]))
    h1_size = sorted_fonts[0][0] if sorted_fonts else 14.0
    h2_size = sorted_fonts[1][0] if len(sorted_fonts) > 1 else h1_size - 1

    for line in lines:
        level = "H1" if line["size"] >= h1_size else "H2" if line["size"] >= h2_size else None
        if level:
            outline.append({
                "level": level,
                "text": prettify_heading(line["text"]),
                "page": line["page"]
            })

    title = outline[0]["text"] if outline else os.path.basename(file_path)
    return {
        "title": prettify_heading(title),
        "outline": outline
    }

# --- File System Integration (Docker compatible) ---
# --- File System Integration (LOCAL RUN) ---

input_dir = "input"
output_dir = "output"

if not os.path.exists(output_dir):
    os.makedirs(output_dir)

for filename in os.listdir(input_dir):
    if filename.lower().endswith(".pdf"):
        filepath = os.path.join(input_dir, filename)
        try:
            result = extract_outline_from_pdf(filepath)
            out_path = os.path.join(output_dir, filename.replace(".pdf", ".json"))
            with open(out_path, "w", encoding="utf-8") as f:
                json.dump(result, f, indent=2, ensure_ascii=False)
            print(f"✅ Processed: {filename}")
        except Exception as e:
            print(f"❌ Failed: {filename} | Error: {e}")


