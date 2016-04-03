from time import sleep
import serial
ser = serial.Serial('COM4', 9600) # Establish the connection on a specific port
counter = 32 # Below 32 everything in ASCII is gibberish
while True:
    #counter +=1
    counter = input('Enter 1 or 0: ')
    ser.write(str(counter).encode()) # Convert the decimal number to ASCII then send it to the Arduino
    print (ser.readline()) # Read the newest output from the Arduino
    sleep(.1) # Delay for one tenth of a second
    #if counter == 255:
    #    counter = 32
            
