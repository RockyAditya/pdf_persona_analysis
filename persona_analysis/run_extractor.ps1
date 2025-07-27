# PowerShell Script to Run Docker Container for PDF Outline Extractor

docker run --rm `
  -v "${PWD}\input:/app/input" `
  -v "${PWD}\output:/app/output" `
  --network none `
  pdf-outline-extractor



# run this in cmd =>  .\run_extractor.ps1