'''
 Main program for FART (test)

 This program talks to the server backend and line detection

 Tells the line program to start and stop. It also sends the station name

 Tells the server backend if the line detection started and sends the station name to the main program
'''

import zmq
import pyglet
import traceback
import time


try:


    music = False

    try:
        song = pyglet.media.load("/home/fart/TeamFabulous/comms/R2D2a.wav")
        music = True
    except:
        pass

    context = zmq.Context()

    # creating a socket for the line detection
    # and server to talk to
    socket = context.socket(zmq.ROUTER)
    socket.setsockopt(zmq.IDENTITY, b'main')
    socket.bind('tcp://*:5550')


    # Initialize poll set
    poller = zmq.Poller()
    poller.register(socket, zmq.POLLIN)

    if music:
        song.play()

    line_detection_running= False
    while True:
        print "recieving message"

        msg = socket.recv_multipart()
        print msg
        if msg[0] == "server":
            if not line_detection_running:
                socket.send_multipart([b'server', b'bet'])
                socket.send_multipart([b'line', msg[1]]) 

                line_detection_running = True
        if msg[0] == "line":
            print "assuming line is done..."
            line_detection_running = False
    


    socket.close()

except Exception as e:
    trace =  traceback.format_exc()
    print trace
    f = open("/home/fart/TeamFabulous/comms/main_program.txt", "w")
    #traceback.print_stack(e)
    f.write(trace)
    f.close()
    time.sleep(300)
