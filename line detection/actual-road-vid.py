import Image, ImageDraw, ImageFont
import numpy as np
import cv2 
from time import sleep
import serial

global imagename 
imagename= "pic"

global Rthreshold
global Gthreshold
global Bthreshold
global im
Rthreshold = 100
Gthreshold = 50
Bthreshold = 180

global pix

global height
global width

def detect_line(start_x,y):
        global Rthreshold
        global Gthreshold
        global Bthreshold
        for x in range (start_x,width):
             # We will extract r,g,b values of pixels at x, y to x,y+10
             r=[]
             g=[]
             b=[]
             for i in range(0, 10):
                 r_value,g_value,b_value=(pix[x,y+i])
                 r.append(r_value)
                 g.append(g_value)
                 b.append(b_value)
             
             Cr = int(np.mean(r))
             Cg = int(np.mean(g))
             Cb = int(np.mean(b))
             
             # First condition for line detection
             if (Cr < Rthreshold ) and (Cg > Gthreshold) and (Cb > Bthreshold ):
                 #when in this if statement we will perfrom another check
                 #This time we will extract r,g,b values of pixels from x,y to x+10, y    
                 
                 r=[]
                 g=[]
                 b=[]
                 for i in range(0, 10):
                    r_value,g_value,b_value=(pix[x,y+i])
                    r.append(r_value)
                    g.append(g_value)
                    b.append(b_value)
             
                 Cr = int(np.mean(r))
                 Cg = int(np.mean(g))
                 Cb = int(np.mean(b))
                 #Second condition for line detection       
                 if (Cr < Rthreshold ) and (Cg > Gthreshold) and (Cb > Bthreshold ):
                         #If this condition is true, we have detected a line
                         print "Line found " + str(x) +" , "+ str(y)
                         return (x)
                           

def openimage(frame):
    global imagename
    global pix
    global height
    global width
    global im
    im = Image.open(imagename +".png") # open the Image file
    # im = Image.fromarray(frame)
    rgb_im = im.convert('RGB') #convert the image to RGB type
    width, height = rgb_im.size # get height and width of image
    pix=im.load()  # load all pixels of image in an list called "pix"
    print width, height

def annotate_image(x1,y1,x2,y2):
            global im
            # We will now draw a red cricle at the point where we have deteced a line
            draw = ImageDraw.Draw(im)
            # The circle will help us manually verify our algorithum
            draw.ellipse((x1, y1, x1+10, y1+10), fill=(255, 0, 0)) # Draw a circle    
            draw.ellipse((x2, y2, x2+10, y2+10), fill=(255, 0, 0)) # Draw a circle    
            im.save(imagename+".jpeg","JPEG")

            # logic to see if line is turning right 
            if ( x2 >= x1 +20):
               print "turn right*************"
               draw.text( (width/2,height/2), "Turn Right")    
               im.save(imagename+".jpeg","JPEG")
               #logic to see if line is turning left 
               return 2
            else:
                    if ( x2 < x1 -20):
                       draw.text( (width/2,height/2), "Turn Left", )        
                       im.save(imagename+".jpeg","JPEG")
                       print "!!!!!!!!!!!!!turn left"
                       return 3
                   #logic to see if line straight        
                    #if ( roadstarted2 + 19 > roadstarted1 > roadstarted2 - 20 ):
                    else:                
                       draw.text( (width/2,height/2), "Go Straight", )  
                       im.save(imagename+".jpeg","JPEG")
                       print "go straight"
                       return 1

    
def processimage():
        global height
        global width
        linestarted1 =-1
        linestarted2 =-1
        x_start= 10
        cap = cv2.VideoCapture(0)
        # cap = cv2.VideoCapture("lineVid.mov") 
        # ser = serial.Serial('COM4', 9600) # Establish the connection on a specific port
        counter = 32 # Below 32 everything in ASCII is gibberish
        while(True):
            ret, frame = cap.read()
            cv2.imshow('frame',frame)
            cv2.imwrite('pic.png',frame)
            imagename = "pic"
            openimage(frame)
            if cv2.waitKey(10) & 0xFF == ord('q'):
                break
            y1=int (height-(height/4)) # Height 1 to start looking for line
            print "y1 start "+ str(y1)
            linestarted1 = detect_line(x_start , y1)
            y2=int (height-(height*(0.75)))
            print "y2 start "+ str(y2)
            linestarted2 = detect_line(x_start , y2)
            if linestarted1 > -1 and linestarted2 > -1:
                
                counter = annotate_image(linestarted1,y1,linestarted2,y2)
                # ser.write(str(counter).encode()) # Convert the decimal number to ASCII then send it to the Arduino
                # print (ser.readline()) # Read the newest output from the Arduino
                # sleep(.1) # Delay for one tenth of a second
                print counter
            else:
                print " Line NOT found"
	cap.release()
 		      

processimage()
