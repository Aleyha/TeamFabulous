#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright 2012-2013 Zdenko Podobný
# Author: Zdenko Podobný
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""
Simple python demo script of tesseract-ocr 3.02 c-api and filehandle
"""

import os
import sys
import ctypes
from ctypes import pythonapi, util, py_object

# Demo variables
lang = "eng"
output = "dump.config"
filename = "../phototest.tif"
libpath = "/usr/local/lib64/"
libpath_w = "../vs2008/DLL_Release/"
tessdata = "/usr/src/tesseract-ocr/"

if sys.platform == "win32":
	libname = libpath_w + "libtesseract302.dll"
	libname_alt = "libtesseract302.dll"
	os.environ["PATH"] += os.pathsep + libpath_w
else:
	libname = libpath + "libtesseract.so.3.0.2"
	libname_alt = "libtesseract.so.3"

try:
	tesseract = ctypes.cdll.LoadLibrary(libname)
except:
	try:
		tesseract = ctypes.cdll.LoadLibrary(libname_alt)
	except WindowsError, err:
		print("Trying to load '%s'..." % libname)
		print("Trying to load '%s'..." % libname_alt)
		print(err)
		exit(1)

tesseract.TessVersion.restype = ctypes.c_char_p
tesseract_version = tesseract.TessVersion()

# We need to check library version because libtesseract.so.3 is symlink
# and can point to other version than 3.02
if float(tesseract_version) < 3.02:
	print("Found tesseract-ocr library version %s." % tesseract_version)
	print("C-API is present only in version 3.02!")
	exit(2)

api = tesseract.TessBaseAPICreate()

rc = tesseract.TessBaseAPIInit3(api, tessdata, lang);
if (rc):
	tesseract.TessBaseAPIDelete(api)
	print("Could not initialize tesseract.\n")
	exit(3)

# Tested in linux - may cause problems on Windows.
fh = open(output,'wb')
PyFile_AsFile = pythonapi.PyFile_AsFile
PyFile_AsFile.argtypes = [ctypes.py_object]
PyFile_AsFile.restype = ctypes.c_void_p

tesseract.TessBaseAPIPrintVariables(api, PyFile_AsFile(fh));
fh.close()