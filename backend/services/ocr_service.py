import fitz  # PyMuPDF for reading PDFs
import docx  # For reading DOCX files (not used here, but likely part of your full pipeline)
import pytesseract  # OCR for images
from PIL import Image  # Image processing
import tempfile  # For handling temporary files

def extract_text(file):
    """
    Extract text from a PDF or image file.
    Returns a list of dictionaries containing page number, paragraph number, and text.
    """
    filename = file.filename
    contents = file.file.read()  # Read the uploaded file contents
    paragraphs = []

    # If the uploaded file is a PDF
    if filename.endswith(".pdf"):
        # Save the uploaded PDF to a temporary file
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as temp_pdf:
            temp_pdf.write(contents)
            temp_pdf.close()

            # Open the PDF using PyMuPDF
            doc = fitz.open(temp_pdf.name)
            for i, page in enumerate(doc):  # Loop over pages
                blocks = page.get_text("blocks")  # Extract text blocks from the page
                for j, block in enumerate(blocks):
                    if block[4].strip():  # block[4] contains the actual text
                        paragraphs.append({
                            "page": i + 1,
                            "para": j + 1,
                            "text": block[4].strip()
                        })

    # If the uploaded file is an image
    elif filename.endswith((".png", ".jpg", ".jpeg")):  # Corrected tuple check
        # Save the image to a temporary file
        with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as temp_img:  # Use correct suffix for PIL
            temp_img.write(contents)
            temp_img.close()

            image = Image.open(temp_img.name)  # Open the image using PIL
            text = pytesseract.image_to_string(image)  # Extract text using OCR

            # Split text by lines and clean up
            for i, para in enumerate(text.split("\n")):
                if para.strip():
                    paragraphs.append({
                        "page": 1,
                        "para": i + 1,
                        "text": para.strip()
                    })

    return paragraphs  # Return the structured text output
