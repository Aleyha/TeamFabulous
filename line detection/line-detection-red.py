import Image, ImageDraw, ImageFont
import numpy as np
import cv2 
from tesserwrap import Tesseract
from PIL import Image 
import threading

global imagename 
imagename= "rightTurn3.png"

global station 
station = "DEW"
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
                 if(maskRed[y+i,x] ==  255):
                    print "found red"
                    
                    ret, frame = cap.read()
                    cv2.waitKey(100)
                    #imgName = 'tessPic' + str(f+1) +".png"
                    imgName = "tessPic.png"
                    cv2.imwrite(imgName,frame)
                    tessImg = cv2.imread(imgName,1)
                    tessImg = Image.fromarray(tessImg, 'RGB')
                    stationFound = tesseract(tessImg) 
                    if stationFound == True:
                        print "FOUND STATION!!"
                        exit()
                    else:
                        break     
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

    
def processimage():
    global height
    global width
    global cap
    linestarted1 =-1
    linestarted2 =-1
    x_start= 10
    cap = cv2.VideoCapture(1)
    # cap = cv2.VideoCapture("lineVid.mov") 
    cap.set(3, 320)
    cap.set(4, 240)

    # ser = serial.Serial('COM4', 9600) # Establish the connection on a specific port
    counter = 32 # Below 32 everything in ASCII is gibberish
    while(True):
        ret, frame = cap.read()
        # Display the resulting frame
        cv2.imshow('frame', frame)
        if cv2.waitKey(100) & 0xFF == ord('q')  :
            break
        cv2.imwrite('pic.png',frame)
        openimage()

        y1=int (height-(height/4)) # Height 1 to start looking for line
       # print "y1 start "+ str(y1)
        linestarted1 = detect_line(x_start , y1)
        y2=int (height-(height*(0.75)))
       # print "y2 start "+ str(y2)
        linestarted2 = detect_line(x_start , y2)
       # print "linestarted1", linestarted1 , "linestarted2" , linestarted2
        if linestarted1 > -1 and linestarted2 > -1:
            
            counter = annotate_image(linestarted1,y1,linestarted2,y2)
            #print counter
        else:
            print " Line NOT found"
    cap.release()
    cv2.destroyAllWindows()
		      

processimage()
