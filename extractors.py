from PIL import Image                                               #python imaging library
import pytesseract                                                  #ocr engine
import pdfplumber                                                   #pdf text extractor
import docx                                                         #docx file text extractor

#tesseract path
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

#image (ocr) function
def extract_text_from_image(image_path):
    try:
        image = Image.open(image_path)
        text = pytesseract.image_to_string(image)
        return text
    except Exception as e:
        print("Error extracting text from image:", e)
        return ""

#pdf text
def extract_text_from_pdf(pdf_path):
    try:
        text = ""
        with pdfplumber.open(pdf_path) as pdf:
            for page in pdf.pages:
                text += page.extract_text() + "\n"                              #reads all text from one page and adds it to 'text' which at first is an empty string
        return text
    except Exception as e:
        print("Error extracting text from PDF:", e)
        return ""

#word text
def extract_text_from_docx(docx_path):
    try:
        text = ""
        doc = docx.Document(docx_path)
        for para in doc.paragraphs:
            text += para.text + "\n"
        return text
    except Exception as e:
        print("Error extracting text from DOCX:", e)
        return ""
