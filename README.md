# PDF Outline Persona Analyzer 🧠📄

A lightweight, offline tool to extract structured outlines from PDFs and rank them based on relevance to a specific user **persona** and **goal**. This project was built for **Adobe India's Connect the Dots Hackathon – Round 1A**.

---

## 🔍 Problem Statement

Given a persona (e.g., a student, researcher, or job seeker) and a collection of PDF documents, the system should:
1. Extract meaningful section headings
2. Understand the context of each document
3. Rank and present the most relevant sections based on the persona’s intent or job-to-be-done

---

## 🧠 Features

- ⚡ Fast and offline — processes PDFs locally using `pdfplumber`
- 🧾 Extracts structured outlines (headings) from each page
- 🎯 Uses persona and job context to rank relevance
- 🛠 Generates final ranked JSON output for easy consumption
- 📦 Docker-compatible for portability

---

## 📁 Project Structure

pdf_persona_analysis
├── input/ # Place your PDF files here
├── output/ # JSON outputs go here
├── persona_job.json # Persona definition file
├── persona_based_output.json # Final ranked output
├── extract_outline.py # Outline extractor logic
├── persona_relevance_extractor.py # Persona-based ranking script
├── run_extractor.ps1/.sh # Helper script
└── README.md


---

## 🧩 Sample Input: `persona_job.json`

```json
{
  "persona": {
    "role": "Undergraduate Computer Science Student",
    "focus_areas": [
      "Coding Skills",
      "Internship Eligibility",
      "Software Engineering Roles",
      "Location Preferences",
      "Required Qualifications"
    ]
  },
  "job_to_be_done": "Understand key eligibility criteria, roles, skills required, and opportunities provided in JPMorgan's 2026 SEP Program"
}
```
# PDF Outline Extractor + persona extraction

## How to Run

```bash
docker build --platform=linux/amd64 -t pdf-outline-extractor .
docker run --rm -v $(pwd)/input:/app/input -v $(pwd)/output:/app/output --network none pdf-outline-extractor

```
## How to run after this

.\run_extractor.ps1
## then output goes to outputfolder_name.json

## then run  
python persona_relevance_extractor.py


