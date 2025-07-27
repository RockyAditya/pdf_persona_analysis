import os
import json
import re
from datetime import datetime

# --- Load persona and job context ---
with open("persona_job.json", "r", encoding="utf-8") as f:
    context = json.load(f)

persona_focus = context["persona"]["focus_areas"]
job_goal = context["job_to_be_done"]

# --- Initialize output structure ---
outline_dir = "./output"
output = {
    "metadata": {
        "documents": [],
        "persona": context["persona"]["role"],
        "job_to_be_done": job_goal,
        "timestamp": datetime.now().isoformat()
    },
    "extracted_sections": [],
    "sub_section_analysis": []
}

# --- Enhanced scoring logic ---
def relevance_score(text):
    score = 0
    text_lower = text.lower()

    for keyword in persona_focus:
        keyword_lower = keyword.lower()
        if keyword_lower in text_lower:
            score += 3  # full phrase match
        elif any(word in text_lower for word in keyword_lower.split()):
            score += 1  # partial match

    return score

# --- Process outline files ---
seen_titles = set()

for file in os.listdir(outline_dir):
    if not file.endswith(".json"):
        continue

    # Only process the specific job description PDF
    if "837880940-JPMorganChase-SEP-FT-Job-Description" not in file:
        continue

    with open(os.path.join(outline_dir, file), "r", encoding="utf-8") as f:
        doc = json.load(f)

    output["metadata"]["documents"].append(file)

    for entry in doc.get("outline", []):
        section_title = entry["text"].replace('\n', ' ').strip()

        if section_title in seen_titles:
            continue
        seen_titles.add(section_title)

        score = relevance_score(section_title)
        if score >= 2:  # Filter low relevance
            output["extracted_sections"].append({
                "document": file,
                "page": entry["page"],
                "section_title": section_title,
                "importance_rank": score
            })

            output["sub_section_analysis"].append({
                "document": file,
                "page": entry["page"],
                "refined_text": section_title
            })

# --- Sort sections by importance descending ---
output["extracted_sections"] = sorted(
    output["extracted_sections"], key=lambda x: -x["importance_rank"]
)

# --- Save result ---
with open("persona_based_output.json", "w", encoding="utf-8") as f:
    json.dump(output, f, indent=2, ensure_ascii=False)

print("✅ Persona-based extraction completed: persona_based_output.json")
