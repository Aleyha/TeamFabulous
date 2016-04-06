import cv2
import numpy as np
from matplotlib import pyplot as plt

img = cv2.imread('test2.png',0)
ret,thresh1 = cv2.threshold(img,127,255,cv2.THRESH_BINARY)
ret,thresh2 = cv2.threshold(img,127,255,cv2.THRESH_BINARY_INV)
ret,thresh3 = cv2.threshold(img,127,255,cv2.THRESH_TRUNC)
ret,thresh4 = cv2.threshold(img,127,255,cv2.THRESH_TOZERO)
ret,thresh5 = cv2.threshold(img,127,255,cv2.THRESH_TOZERO_INV)

images = [img, thresh1, thresh2, thresh3, thresh4, thresh5]

cv2.imwrite("binary.png", images[1])
cv2.imwrite("binary_inv.png", images[2])
cv2.imwrite("trunc.png", images[3])
cv2.imwrite("tozero.png", images[4])
cv2.imwrite("tozero_inv.png", images[5])

'''
titles = ['Original Image','BINARY','BINARY_INV','TRUNC','TOZERO','TOZERO_INV']


for i in xrange(6):
  plt.subplot(2,3,i+1),plt.imshow(images[i],'gray')
  plt.title(titles[i])
  plt.xticks([]),plt.yticks([])

plt.show()
'''