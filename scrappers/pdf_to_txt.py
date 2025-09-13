import pdfplumber
from pathlib import Path

# Path to your input PDF
pdf_path = Path(r"C:\Users\CODE CLASSES\nlp\Hiligaynon-Lexicon\resources\ceceilmotus.pdf")

# Path for the output TXT (auto-create directories if missing)
txt_path = Path(r"C:\Users\CODE CLASSES\nlp\Hiligaynon-Lexicon\output\output.txt")
txt_path.parent.mkdir(parents=True, exist_ok=True)

with pdfplumber.open(pdf_path) as pdf, open(txt_path, "w", encoding="utf-8") as out_file:
    for page_num, page in enumerate(pdf.pages, start=1):
        text = page.extract_text()
        if text:  # skip empty pages
            out_file.write(f"--- Page {page_num} ---\n")
            out_file.write(text)
            out_file.write("\n\n")  # extra spacing between pages

print(f"✅ Done! Extracted PDF text saved to: {txt_path}")
