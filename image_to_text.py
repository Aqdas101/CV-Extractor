from PIL import Image
import pytesseract
import io
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
def image_to_text(images):
    print('Start -- Extracting text from image...')
    img_bytes = io.BytesIO()
    images.save(img_bytes, format='PNG')  
    text = pytesseract.image_to_string(Image.open(img_bytes))
    print('End -- Extracting text from image\n\n')
    return text