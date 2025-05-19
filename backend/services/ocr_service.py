import fitz
import docx
import pytesseract
from PIL import Image
import tempfile

def extract_text(file):
    filename = file.filename
    contents = file.file.read()
    paragraphs = []

    if filename.endswith(".pdf"):
        with tempfile.NamedTemporaryFile(delete=False,suffix=".pdf") as temp_pdf:
            temp_pdf.write(contents)
            temp_pdf.close()
            doc = fitz.open(temp_pdf.name)
            for i , page in enumerate(doc):
                blocks = page.get_text("blocks")
                for j, block in enumerate(blocks):
                    if block[4].strip():
                        paragraphs.append({"page":i+1,"para":j+1,"text":block[4].strip()})

    elif filename.endswith(".png",".jpg",".jpeg"):
        with tempfile.NamedTemporaryFile(delete=False,suffix=".pdf") as temp_img:
            temp_img.write(contents)
            temp_img.close()
            image = Image.open(temp_img.name)
            text = pytesseract.image_to_string(image)
            for i,para in enumerate(text.split("\n")):
                if para.strip():
                    paragraphs.append({"page":1,"para":i+1,"text":para.strip()})
    
    return paragraphs
