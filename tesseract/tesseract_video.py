import numpy as np
import cv2
import subprocess

cap = cv2.VideoCapture(0)

while(True):
    # Capture frame-by-frame
    station_name = "hello"
    ret, frame = cap.read()

    # Our operations on the frame come here
    #gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    cv2.imwrite("output.png", frame)
    subprocess.call("tesseract output.png out", shell=True)

    tesseract_output = open("out.txt", "r")

    for line in tesseract_output: 
    	output_array = line.split();
    	for word in output_array:
    		if(word.lower() == "hello"):
    			print "FOUND STATION!!!!!!!!!!!!"

    # Display the resulting frame
    cv2.imshow('frame', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()