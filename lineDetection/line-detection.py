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
import os
import time
import traceback

global imagename 
imagename= "rightTurn3.png"

global turnCounter # total count of turns
turnCounter = 0
global prevTurn 
prevTurn = 0

global station 
#station = sys.argv[1]
# station = station.lower()
global Rthreshold
global Gthreshold
global Bthreshold
global im
global neighborRange
neighborRange = 10

Rthreshold = 100
Gthreshold = 50
Bthreshold = 180

global height
global width
global tr

global right
right = False

global saveDirectory
saveDirectory = "/home/fart/TeamFabulous/lineDetection/"
def tesseract(image):
    text = tr.ocr_image(image)
    #print text
    print "TESSERACT FINISHED"
    words = text.split()
    for word in words:
            if word == station:
                return True

def findStation():
    ret, frame = cap.read()
    cv2.waitKey(1)
    imgName = saveDirectory + "tessPic.png"
    cv2.imwrite(imgName,frame)
    tessImg = cv2.imread(imgName,1)
    tessImg = Image.fromarray(tessImg, 'RGB')
    stationFound = tesseract(tessImg)
    return stationFound

def findRed():
    global tessCallCounter
    array = maskRed.tolist()
    count = (sum(x.count(255) for x in array))
    print "red count is", count
    if count >= 2000:
        motor_socket.send_multipart([b'motor', b'0'])
        if tessCallCounter <= 3: # if we have called Tesseract under 5 times previously, call it again
            stationFound =  findStation()
            tessCallCounter += 1
            if stationFound:
                print "station found"
                if music:
                    player.pause()
                    found_noise.play()
                return True
            else: # station not found
                return False

        else: # tessCallCounter is greater than 5, jolt motors forward
            tessCallCounter = 0
            motor_socket.send_multipart([b'motor', b'5'])
            time.sleep(1)
            motor_socket.send_multipart([b'motor', b'0'])
            return False
    else: # no red found
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

             for i in range(0, neighborRange):
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
                 for i in range(0, neighborRange):
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

    im = cv2.imread(saveDirectory + "pic.png",1) # open the Image file
    # convert to HSV and mask to find blue and red
    hsv = cv2.cvtColor(im, cv2.COLOR_BGR2HSV)
    # Threshold the HSV image to get only red colors
    maskRed = cv2.inRange(hsv, lower_red, upper_red)
    maskBlue = cv2.inRange(hsv, lower_blue, upper_blue)

    height, width, channels = im.shape # get height and width of image
    #print width, height, channels



def find_direction(x1,y1,x2,y2):
	global im
    global right
	'''
	We will now draw a red cricle at the point where we have deteced a line
	draw = ImageDraw.Draw(im)
	# The circle will help us manually verify our algorithum
	cv2.imwrite("drawn.jpeg", im)
	drawnIm= cv2.imread("drawn.jpeg")
			   
	cv2.circle(drawnIm, (x1,y1),5,(0,0,255),-1 )
	cv2.circle(drawnIm, (x2,y2),5,(0,0,255),-1 )
	cv2.imwrite("drawn.jpeg",drawnIm)

	logic to see if line is turning right 

	
	if ( x2 >= x1 +20):
		print "turn right*************"
		return 2
		#logic to see if line is turning left 
	else:
		if ( x2 < x1 -20):
			print "!!!!!!!!!!!!!turn left"
			return 3
		#logic to see if line straight        
		else:                
			print "go straight"
			return 1

	'''

	# returns 1 - 9, 1-4 is left, 5 is straight, 6-9 is right
	xDiff = x2 - x1 # top x value - botom x value
	yDiff = abs(y2 - y1)  # difference between top and bottom values
	ratioYX = 3.0 * yDiff / float(width - 2 * neighborRange) # used to normalize ratio between width and height so that it seems like a 1:1 ratio (for easier mathing)
	rawTurn = xDiff * ratioYX / yDiff # closer to -1 is left turn, closer to 1 is right turn
	#print rawTurn
	normalizedTurn = int(rawTurn * 4.5) + 5
	if(normalizedTurn > 9):
		normalizedTurn = 9
	elif(normalizedTurn < 1):
		normalizedTurn = 1

	
	#comment this next block out for performance, it prints out the calculated direction
	turnAdjective = {0: "", 1: "slight", 2: "medium", 3: "heavy", 4: "max"}
	turnDirection = ["left", "straight", "right"]
	turnAdjectiveActual = abs(normalizedTurn - 5)
	if normalizedTurn > 5:
		turnDirectionActual = 2
	elif normalizedTurn < 5:
		turnDirectionActual = 0
	else:
		turnDirectionActual = 1
	print "%s %s" % (turnAdjective[turnAdjectiveActual], turnDirection[turnDirectionActual])

	return normalizedTurn # normalizes -1 to 1 to -4.5 to 4.5, which gets cast to -4 to 4, which gets shifted to 1 to 9:   1 is full left, 9 is full right, 5 is straight
				
	

    
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
    global direction
    direction = 0
    global tessCallCounter
    tessCallCounter = 0
    
    while(True):
        ret, frame = cap.read()
        # Display the resulting frame
	
        #cv2.imshow('frame', frame)
        if cv2.waitKey(1) & 0xFF == ord('q')  :
            break
        
	
        cv2.imwrite(saveDirectory + 'pic.png',frame)
        openimage()

        #look for red first
        foundStation = findRed()
        if foundStation:
            return

        #if red isn't found, start blue line detection
        y1=int (height-(height/4)) # Height 1 to start looking for line
       # print "y1 start "+ str(y1)
        linestarted1 = detect_line(x_start , y1)
        y2=int (height-(height*(0.75)))
       # print "y2 start "+ str(y2)
        linestarted2 = detect_line(x_start , y2)
       # print "linestarted1", linestarted1 , "linestarted2" , linestarted2
        if linestarted1 > -1 and linestarted2 > -1:  
            currTurn = find_direction(linestarted1,y1,linestarted2,y2)
            #motor_socket.send_multipart([b'motor', str(currTurn)])
            
            print "currTurn = ", currTurn
            print "prevTurn = ", prevTurn
            if currTurn == prevTurn:
                turnCounter += 1
            else:
                prevTurn = currTurn
                turnCounter = 1
            if turnCounter == 2 and currTurn != direction:
                # send turn to motors
                print "sending to motors"
                direction = currTurn
                if direction > 1 and direction < 5:
                    right = False
                if direction > 5 and direction < 10:
                    right = True
                if direction == 5:
                    right = True
                motor_socket.send_multipart([b'motor', str(currTurn)])
                turnCounter = 0
            # print "turnCounter = ", turnCounter
            
            
        else:
            print "Line NOT found"
            prevTurn = 0
            direction = 0
            if right:
                motor_socket.send_multipart([b'motor', b'b'])
            else:
                motor_socket.send_multipart([b'motor',b'c'])    
            motor_socket.send_multipart([b'motor', b'0'])
 


f = open(saveDirectory + "line_detection.txt", "w")

try:
  
    global music
    music = False # if music is working  
    


    tr = Tesseract("/usr/local/share") # this is slow 

    # Prepare our socket to talk to the motor
    context = zmq.Context()
    motor_socket = context.socket(zmq.ROUTER)
    motor_socket.setsockopt(zmq.IDENTITY, b'line')
    motor_socket.connect('tcp://localhost:5559')

    # prepare socket that talks to the main program
    main_socket = context.socket(zmq.DEALER)
    main_socket.setsockopt(zmq.IDENTITY, b'line')
    main_socket.connect('tcp://localhost:5550')




    try:
        # loading music files with pygame!
        pygame.mixer.init()

        # setting up the noise when it finds a station
        global found_noise 
        found_noise = pygame.mixer.Sound('secret.wav')

        player = pyglet.media.Player()
        
        # looking in the music directory for music to queue
        music_files = []
        for files in os.listdir("/home/fart/Music"):
            file = files.split(".")
        # if music:
            extension = file[1].lower() # in case file extension is uppercase
            if extension == "wav":
                music_files.append(files)

        print music_files
        # loading music from the music folder and queuing it up
        for i in range(len(music_files)):
            song = pyglet.media.load("/home/fart/Music/" + music_files[i])
            player.queue(song)

        music = True
    except:
         f.write("error opening music...")





    # clock = pygame.time.Clock()
    # clock.tick(10)
    # while pygame.mixer.music.get_busy():
    #     pygame.event.poll()
    #     clock.tick(10)

    while True:
        print "waiting for message..."
        msg = main_socket.recv_multipart()
        station = msg[0]
        
        print "running line detection with station " + station

        if music:
        	player.play()
        processimage(motor_socket)
        cap.release()
        cv2.destroyAllWindows()
        main_socket.send_multipart([b"finished"])
        motor_socket.send_multipart([b'motor', b'0'])
        
    motor_socket.close()
    main_socket.close()
    #pygame.mixer.quit()


except Exception as e:
    trace =  traceback.format_exc()
    print trace
    
    #traceback.print_stack(e)
    f.write(trace)
    f.close()
    time.sleep(300)
