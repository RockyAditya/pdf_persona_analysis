# PDF Outline Extractor

This tool extracts structured outlines (Title, H1, H2) from PDFs using PyPDF2. Built for Adobe "Connecting the Dots" Challenge.

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

