import Image, ImageDraw, ImageFont
import numpy as np
import cv2 
from tesserwrap import Tesseract
from PIL import Image 
import threading
import zmq
import sys
import pyglet
import pygame

global position

global imagename 
imagename= "rightTurn3.png"

global turnCounter # total count of turns
turnCounter = 0
global prevTurn 
prevTurn = 0

global station 
# station = sys.argv[1]
# station = station.lower()
global Rthreshold
global Gthreshold
global Bthreshold
global im
Rthreshold = 100
Gthreshold = 50
Bthreshold = 180

global height
global width
global tr
tr = Tesseract("/usr/local/share") # this is slow


def tesseract(image):
    text = tr.ocr_image(image)
    print text
    print "TESSERACT FINISHED"
    words = text.split()
    for word in words:
            if word == station:
                return True

def findStation():
    ret, frame = cap.read()
    cv2.waitKey(100)
    imgName = "tessPic.png"
    cv2.imwrite(imgName,frame)
    tessImg = cv2.imread(imgName,1)
    tessImg = Image.fromarray(tessImg, 'RGB')
    stationFound = tesseract(tessImg)
    return stationFound

def findRed():
    array = maskRed.tolist()
    count = (sum(x.count(255) for x in array))
    print "count is", count
    if count >= 400:
       # motor_socket.send_multipart([b'motor', str(0))
       if findStation():
        print "station found"
        # position = pygame.mixer.music.get_pos()
        pygame.mixer.music.pause()
        return True
    else:
        return False


def detect_line(start_x,y):
        global Rthreshold
        global Gthreshold
        global Bthreshold
        foundBlue = False
        
        for x in range (start_x,width):
             # We will extract r,g,b values of pixels at x, y to x,y+10
             r=[]
             g=[]
             b=[]

             for i in range(0, 10):
                 b_value,g_value,r_value=(im[y+i,x])
                 r.append(r_value)
                 g.append(g_value)
                 b.append(b_value)
                #look for red. If found, take 5 pictures and run tesseract() on them to see if correct station was reached
                 # if(maskRed[y+i,x] ==  255):
                 #    print "found red"
                    # foundStation = findStation()
                    # if foundStation == True:
                    #     print "FOUND STATION!!"
                    #     # motor_socket.send_multipart([b'motor', str(0))

                    #     exit()
                    # else:
                    #     break     
                 if(maskBlue[y+i,x] ==  255):
                    foundBlue = True
                    break
                                   
             
             Cr = int(np.mean(r))
             Cg = int(np.mean(g))
             Cb = int(np.mean(b))
   

             # First condition for line detection
             if ((Cr < Rthreshold ) and (Cg > Gthreshold) and (Cb > Bthreshold )) or (foundBlue == True):
                 foundBlue = False
                 #when in this if statement we will perfrom another check
                 #This time we will extract r,g,b values of pixels from x,y to x+10, y    
                 r=[]
                 g=[]
                 b=[]
                 for i in range(0, 10):
                    b_value,g_value,r_value=(im[y+i,x])
                    r.append(r_value)
                    g.append(g_value)
                    b.append(b_value)
                    if(maskBlue[y+i,x] ==  255):
                        #print "foundblue"
                        foundBlue = True
                        break
                    
             
                 Cr = int(np.mean(r))
                 Cg = int(np.mean(g))
                 Cb = int(np.mean(b))

                 #Second condition for line detection       
                 if ((Cr < Rthreshold ) and (Cg > Gthreshold) and (Cb > Bthreshold )) or (foundBlue == True):
                         #If this condition is true, we have detected a line

                         #print "Line found " + str(x) +" , "+ str(y)
                         return (x)
                           

def openimage():
    global imagename
    global pix
    global height
    global width
    global im
    global maskRed
    global maskBlue

    lower_green = np.array([50,100,100])
    upper_green = np.array([70,255,255])
    lower_blue = np.array([110,100,100])
    upper_blue = np.array([130,255,255])
    lower_red = np.array([0,100,100])
    upper_red = np.array([10,255,255])

    im = cv2.imread("pic.png",1) # open the Image file
    # convert to HSV and mask to find blue and red
    hsv = cv2.cvtColor(im, cv2.COLOR_BGR2HSV)
    # Threshold the HSV image to get only red colors
    maskRed = cv2.inRange(hsv, lower_red, upper_red)
    maskBlue = cv2.inRange(hsv, lower_blue, upper_blue)

    height, width, channels = im.shape # get height and width of image
    #print width, height, channels



def annotate_image(x1,y1,x2,y2):
            global im
            # We will now draw a red cricle at the point where we have deteced a line
            # draw = ImageDraw.Draw(im)
            # # The circle will help us manually verify our algorithum
            font = cv2.FONT_HERSHEY_SIMPLEX
            cv2.imwrite("drawn.jpeg", im)
            drawnIm= cv2.imread("drawn.jpeg")
                       
            cv2.circle(drawnIm, (x1,y1),5,(0,0,255),-1 )
            cv2.circle(drawnIm, (x2,y2),5,(0,0,255),-1 )
            cv2.imwrite("drawn.jpeg",drawnIm)
            
            # logic to see if line is turning right 
            if ( x2 >= x1 +20):
               print "turn right*************"
               return 2
               #logic to see if line is turning left 
            else:
                    if ( x2 < x1 -20):
                       print "!!!!!!!!!!!!!turn left"
                       cv2.putText(drawnIm, "turn left", (width/2, height/2),font,4,(255,255,255),2,cv2.LINE_AA )
                       return 3
                   #logic to see if line straight        
                    else:                
                       print "go straight"
                       return 1

    
def processimage(motor_socket):
    global height
    global width
    global cap
    linestarted1 =-1
    linestarted2 =-1
    x_start= 10
    cap = cv2.VideoCapture(0)
    cap.set(3, 320)
    cap.set(4, 240)
    prevTurn = 0

    
    while(True):
        ret, frame = cap.read()
        # Display the resulting frame
        cv2.imshow('frame', frame)
        if cv2.waitKey(100) & 0xFF == ord('q')  :
            break
        cv2.imwrite('pic.png',frame)
        openimage()

        #look for red first
        foundStation = findRed()
        if foundStation:
            return
        else:
            pygame.mixer.music.unpause()

        #if red isn't found, start blue line detection
        y1=int (height-(height/4)) # Height 1 to start looking for line
       # print "y1 start "+ str(y1)
        linestarted1 = detect_line(x_start , y1)
        y2=int (height-(height*(0.75)))
       # print "y2 start "+ str(y2)
        linestarted2 = detect_line(x_start , y2)
       # print "linestarted1", linestarted1 , "linestarted2" , linestarted2
        if linestarted1 > -1 and linestarted2 > -1:  
            currTurn = annotate_image(linestarted1,y1,linestarted2,y2)
            # print "currTurn = ", currTurn
            # print "prevTurn = ", prevTurn
            if currTurn == prevTurn:
                turnCounter += 1
            else:
                prevTurn = currTurn
                turnCounter = 1
            if turnCounter == 5:
                # send turn to motors
                print "sending to motors"
                motor_socket.send_multipart([b'motor', str(currTurn)])
                turnCounter = 0
            # print "turnCounter = ", turnCounter
        else:
            print " Line NOT found"
    

# Prepare our socket to talk to the motor
context = zmq.Context()
motor_socket = context.socket(zmq.ROUTER)
motor_socket.setsockopt(zmq.IDENTITY, b'line')
motor_socket.connect('tcp://localhost:5559')

# prepare socket that talks to the main program
# main_socket = context.socket(zmq.DEALER)
# main_socket.setsockopt(zmq.IDENTITY, b'line')
# main_socket.connect('tcp://localhost:5550')

# song = pyglet.media.load('onedance.wav')
# player = pyglet.media.Player()
# player.queue(song)

pygame.mixer.init()
# pygame.display.set_mode((200,100))
pygame.mixer.music.load("onedance.wav")
position= 0
pygame.mixer.music.play()
pygame.mixer.music.pause()
# pygame.mixer.music.set_pos(position)
# pygame.mixer.music.play(0)

# clock = pygame.time.Clock()
# clock.tick(10)
# while pygame.mixer.music.get_busy():
#     pygame.event.poll()
#     clock.tick(10)

# while True:
#     msg = main_socket.recv_multipart()
while True:
    station = raw_input("enter station: ")
    # player.play()
    # pygame.mixer.music.set_pos(position)
    pygame.mixer.music.unpause()
    processimage(motor_socket)
    cap.release()
    cv2.destroyAllWindows()
    
motor_socket.close()
