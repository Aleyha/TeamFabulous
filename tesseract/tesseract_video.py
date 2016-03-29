import numpy as np
import cv2
import subprocess
import threading
import sys
import os

# note to self: maybe there should be more connections if you save
# tesseract's output to a file
semaphore = threading.BoundedSemaphore();
#outfile_semaphore = threading.BoundedSemaphore();

def cleanup():
    print "CLEANING UP!"
    # removing the image file so the tesseract thread will stop calling tesseract!
    if os.path.isfile("./output.png"): 
        # only removes the link not the actual file.
        os.unlink("./output.png")

    # removing the output file
    if os.path.isfile("./out.txt"): 
        os.unlink("./out.txt")

'''
saves a video capture object to an image
'''
def save_image(frame):
    global semaphore

    # acquire the image for writing...
    semaphore.acquire()

    cv2.imwrite("output.png", frame)

    # making sure to release so another thread can use it.
    semaphore.release()

'''
this function just calls tesseract forever using a system call
it will stop if output.png is deleted
'''
def tesseract():
    global semaphore   
    while(True):
        if not os.path.exists("./output.png"):
            break

        semaphore.acquire()
        subprocess.call(["tesseract", "output.png","out"])
        semaphore.release()


'''
reads tesseract output file to
find the station name we are looking for.
'''
def find_station(station_name):
    # global semaphore
    while(True):
        if not os.path.isfile("./out.txt"):
            break
        f = open("out.txt", "r")
        for line in f:
            words = line.split()
            for word in words:
                if word.lower() == station_name:
                    print "STATION FOUND!!"
                    cleanup();
                    break
        f.close()

# creating a video capture object
cap = cv2.VideoCapture(0)

# creating output file??
f = open("out.txt", "w")
f.close()

# creating an output.png
ret, frame = cap.read()
cv2.imwrite("output.png", frame)

# threading objects
tesseract_thread = threading.Thread(target=tesseract)
station_finding_thread = threading.Thread(target=find_station, args=("save",))

# start threads
tesseract_thread.start()
station_finding_thread.start()


while(True):
    # Capture frame-by-frame
    ret, frame = cap.read()
    
    '''
    using another thread to save the frame to an image
    in order to keep the video from lagging
    because of the semaphores
    '''
    saving_thread = threading.Thread(target=save_image,args=(frame,))
    saving_thread.start()
    
    # Display the resulting frame
    cv2.imshow('frame', frame)
    if cv2.waitKey(1) & 0xFF == ord('q')  :
        break


cleanup()
tesseract_thread.join()
station_finding_thread.join()
# When everything is done, release the capture
cap.release()
cv2.destroyAllWindows()


    

