from tesserwrap import Tesseract
from PIL import Image
tr = Tesseract("/usr/local/share") # this is slow
im = Image.open("test2.png")
text = tr.ocr_image(im)
print text
words = text.split()
for thing in words:
	if thing == "Arlington":
		print "found ittt" 