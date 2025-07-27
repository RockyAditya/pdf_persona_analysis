# Dockerfile

FROM --platform=linux/amd64 python:3.12-slim

WORKDIR /app

# Copy and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy script
COPY extract_outline.py .
COPY persona_relevance_extractor.py .

# Create folders for input/output
RUN mkdir input output

# Run the script when container starts
CMD ["python", "extract_outline.py"]



