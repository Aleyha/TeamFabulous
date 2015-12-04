import Image, ImageDraw, ImageFont
import numpy as np

def processimage():
        start_off_set = 10
        im = Image.open('leftTurn.png') # open the Image file
        rgb_im = im.convert('RGB') #convert the image to RGB type
        width, height = rgb_im.size # get height and width of image
        pix=im.load()  # load all pixels of image in an list called "pix"
        print width, height
        
        y=int (height-(height/4)) # Height 1 to start looking for line
        r,g,b=pix[start_off_set,y]  # Get the RBG value at this height
        averagecolorvalue=r+g+b # Use these values to initialize the average color value at this point
        roadstarted1=0 #variable used to store the starting point of line at height 1
        # We will loop through the width of image at height 1 and get the average color value
        pr=[]
        pg=[]
        pb=[]
        for x in range (start_off_set,width):
             r,g,b= pix[x,y] # rbg value of pixel
             pr.append(r)
             pg.append(g)
             pb.append(b)

        Ar = np.mean(pr)
        Ag = np.mean(pg)
        Ab = np.mean(pb)

        # we will loop through the width again this time searching for start of line 
        for x in range (start_off_set,width):
             # We will extract r,g,b values of pixels at x, y to x,y+10
             prgb=[]
             for i in range(0, 10):
                 prgb.append(pix[x,y+i])
             Cr = np.mean(prgb[0])
             Cg = np.mean(prgb[1])
             Cb = np.mean(prgb[2])
          
             diff = (abs(Cr - Ar) + abs(Cg-Ag) + abs(Cb - Ab))
             # First condition for line detection
             if (diff > 100 ):
                 #when in this if statement we will perfrom another check
                 #This time we will extract r,g,b values of pixels from x,y to x+10, y    
                 prgb = []
                 for i in range(0, 10):
                     prgb.append(pix[x+i,y])
                 
                 Cr = np.mean(prgb[0])
                 Cg = np.mean(prgb[1])
                 Cb = np.mean(prgb[2])
                 diff = (abs(Cr - Ar) + abs(Cg-Ag) + abs(Cb - Ab))
                 #Second condition for line detection       
                 if (diff > 100 ):
                         #If this condition is true, we have detected a line
                         roadstarted1=x # store the x value of line
                         break # Break out of loop
        # We will now draw a red cricle at the point where we have deteced a line
        draw = ImageDraw.Draw(im)
        # The circle will help us manually verify our algorithum
        draw.ellipse((roadstarted1, y, roadstarted1+10, y+10), fill=(255, 0, 0)) # Draw a circle    
        im.save("output.jpg","JPEG") #Save the changes to circile in a new image file
        # Now we will repeat the whole process at a different height 2
        # We will not calculate the average again but use the average calculated above
        y=int (height-(height*(0.75)))
        roadstarted2=0
        for x in range (start_off_set,width):
             prgb =[]
             # We will extract r,g,b values of pixels at x, y to x,y+10
             for i in range(0, 10):
                prgb.append(pix[x,y+i])

             Cr = np.mean(prgb[0])
             Cg = np.mean(prgb[1])
             Cb = np.mean(prgb[2])

             diff = (abs(Cr - Ar) + abs(Cg-Ag) + abs(Cb - Ab))
             if (diff > 100 ):
                #when in this if statement we will perfrom another check
                 #This time we will extract r,g,b values of pixels from x,y to x+10, y    
                 prgb = []
                 for i in range(0, 10):
                     prgb.append(pix[x+i,y])

                 Cr = np.mean(prgb[0])
                 Cg = np.mean(prgb[1])
                 Cb = np.mean(prgb[2])
                 diff = (abs(Cr - Ar) + abs(Cg-Ag) + abs(Cb - Ab))
                 #Second condition for line detection
                 if (diff > 100 ):
                         #If this condition is true, we have detected a line
                         roadstarted2=x # store the x value of line
                         break # Break out of loop
        # We will now draw a red cricle at the point where we have deteced a line
        
        draw = ImageDraw.Draw(im)
        draw.ellipse((roadstarted2, y, roadstarted2+10, y+10), fill=(255, 0, 0)) # Draw a circle    
        im.save("output.jpg","JPEG")

        # logic to see if line is turning right 
        if ( roadstarted2 >= roadstarted1 +20):
               print "turn right"
               draw.text( (width/2,height/2), "Turn Right")    
               im.save("output.jpg","JPEG")
           #logic to see if line is turning left 
        else:
                if ( roadstarted2 < roadstarted1 -20):
                   draw.text( (width/2,height/2), "Turn Left", )        
                   im.save("output.jpg","JPEG")
                   print "turn left"
               #logic to see if line straight        
                #if ( roadstarted2 + 19 > roadstarted1 > roadstarted2 - 20 ):
                else:                 
                       draw.text( (width/2,height/2), "Go Straight", )  
                       im.save("output.jpg","JPEG")
                       print "go straight"
processimage()
