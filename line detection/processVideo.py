import Image
import numpy as np
import cv2 
 
 
def processVideo():
        cap = cv2.VideoCapture(0)
        while(True):
            ret, frame = cap.read()
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            cv2.imshow('frame',gray)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
            # rgb_im = cv2.cvtColor(frame, cv2.COLOR_BGR)
            # rgb_im = frame.convert('RGB') #convert the image to RGB type
            # width, height = frame.size # get height and width of image
            width = cap.get(3)
            height = cap.get(4)

            pix=frame.load()
            
        cap.release()
        cv2.destroyAllWindows()

processVideo()