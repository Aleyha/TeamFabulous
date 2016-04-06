import os
import ctypes

lang = "eng"
filename = "test2.png"
libname = "/usr/local/lib/libtesseract.so.3"
TESSDATA_PREFIX = os.environ.get('TESSDATA_PREFIX')
if not TESSDATA_PREFIX:
    print "can't find TESSDATA_PREFIX"
    TESSDATA_PREFIX = "../"

tesseract = ctypes.cdll.LoadLibrary(libname)
tesseract.TessVersion.restype = ctypes.c_char_p
tesseract_version = tesseract.TessVersion()
api = tesseract.TessBaseAPICreate()
print "creating api"
rc = tesseract.TessBaseAPIInit3(api, TESSDATA_PREFIX, lang)
print "init api"
if (rc):
    tesseract.TessBaseAPIDelete(api)
    print("Could not initialize tesseract.\n")
    exit(3)
 
print "setting image"

img = tesseract.pixRead(filename)
tesseract.TessBaseAPISetImage2(api, img)
print "recognizing"
if(tesseract.TessBaseAPIRecognize(api, None) != 0):
    exit(3)
print "getting text"
text = tesseract.TessBaseAPIGetUTF8Text(api)
if text == None:
	exit(3)

print ctypes.string_at(text)
