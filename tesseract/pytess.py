import Image
import pytesseract
from pytesseract import image_to_string
print image_to_string(Image.open('words.jpg'))
