from pypdf import PdfReader

pdf_path = r"D:\MTech\Projects\LegalGPT-India\data\constitution.pdf"

reader = PdfReader(pdf_path)
    
print(f"Pages: {len(reader.pages)}")

text = ""

for page in reader.pages:
    page_text = page.extract_text()

    if page_text:
        text += page_text

print("\nFirst 2000 characters:\n")
print(text[:2000])