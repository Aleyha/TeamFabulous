import numpy as np
import cv2
import subprocess
import threading
import os

semaphore = threading.BoundedSemaphore();

def video():
    global semaphore
    cap = cv2.VideoCapture(0)

    while(True):
        # Capture frame-by-frame
        ret, frame = cap.read()

        # Our operations on the frame come here
        #gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        saving_thread = threading.Thread(target=save_image,args=(frame,))
        saving_thread.start()
        
        # Display the resulting frame
        cv2.imshow('frame', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # When everything done, release the capture
    cap.release()
    cv2.destroyAllWindows()
def save_image(frame):
    print "saving image is started..."
    semaphore.acquire()
    cv2.imwrite("output.png", frame)
    semaphore.release()
    print "saving image is done..."
def tesseract():

    while(True):
        semaphore.acquire()
        subprocess.call("tesseract output.png stdin", shell=True)
        semaphore.release()


def find_station(station_name):
    global semaphore

    #semaphore.acquire()
    tesseract_output = input()
    print tesseract_output

    for line in tesseract_output: 
        output_array = line.split();
        for word in output_array:
            if(word.lower() == station_name):
                print "FOUND STATION!!!!!!!!!!!!"
    tesseract_output.close()
    #semaphore.release()

video_thread = threading.Thread(target=video)
tesseract_thread = threading.Thread(target=tesseract)
station_finding_thread = threading.Thread(target=find_station, args="packet")

video_thread.start()
tesseract_thread.start()