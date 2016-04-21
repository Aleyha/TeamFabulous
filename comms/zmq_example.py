'''
IGV_Raspberry_Pi_ZMQ_Server.py
Created by Team SNAPH Fall 2015

This program serves as an intermediary between the ZMQ server on the network node connected to 
the wheelchair base, and the IGV_Raspberry_Pi_Movement_Control.py program. 
This program creates a ZMQ poller that listens on the socket 2424 on the local machine. It will 
continue to poll for as long as the script is running without errors.
It also connects to the movement control program by connecting to the socket 2425 on the local 
machine.

This program has four main functions as a server on the Raspberry Pi.
1) This program continously polls for a Heartbeat signal. The network node connected to the Pi
should be sending a heartbeat signal in a loop. If this program goes the length of TIMEOUT_DURATION 
without receiving a signal, it will send an E-STOP signal to the movement program to stop the movement 
in the case of a network failure. As soon as it receives another packet from the network, it will allow 
for movement, until the Heartbeat signal is lost again. The TIMEOUT_DURATION is set at 1 second right
now. The Heartbeat signal should just be a single character "0", sent in a string packet over ZMQ. Any
data after the "0" will not be used. This program will reply with another "0" to the network node.
2) This program receives movement commands from the network node. The movement commands should start with 
the character "1", followed by a correct data packet that will be read by the movement program. If this
program encounters a packet that starts with "1", it will forward the rest of the packet on to the 
movement program, without checking the contents. The movment program will verify the packet, and if it
is correct, it will send a "1" back to this program, which will use that string as the reply to the network
node. If the packet is incorrect, the movement program will send a "0" back to this program, which will be 
the reply to the network node. To error check the status of the packet, the network node may verify the 
reply from this server (a "0" or "1") and handle that accordingly. This function also sets the vehicle_state 
to 1 (see next section).
3) This program receives status requests. The status request is a packet with the character "2", it will ignore
any data after the "2". The program maintains a state variable: vehicle_state. If the variable is set to 0
(0 on startup), that indicates that the vehicle is not executing a command, or the movement program is ready to
accept another command. When vehicle_state is set to 1, then the vehicle is still processing the previous 
command sent from the network. Technically, the movement program will accept commands at any time, and they will
override the current one, but that should only happen for a software E-STOP. The vehicle_state command is set 
to 1 when the command is passed through to the movement program, and it is set back to 0 when the movement 
program signals that it has completed (see next section). When this program receives a status request, it just 
sends the value of the variable to the requester. 
4) This program receives completion updates from the movement program. This packet is the character "3", it will
ignore all other data after. This data should never come from the network node, as it will disrupt the communication
between this server and the Raspberry Pi movement program, and could cause inaccurate readings when requesting the 
status of the vehicle. When the program receives this packet, it sets the vehicle_state variable back to 0 (see 
previous section). It then returns an empty string to the movement program. Again, the network node should 
NEVER send this command to this server. 

This program starts automatically when the Raspberry Pi boots up. It will continue to run as long as it doesn't crash.
If the program crashes, it can be run again at the command line in the correct directory with:
sudo python IGV_Raspberry_Pi_ZMQ_Server.py
This program will freeze if at any time it tries to send a ZMQ message but does not get a reply. This only happens 
when it sends commands to the vehicle movement program, and the program has crashed or is not functioning properly.
This can be resolved by simply restarting both of the programs, starting with the movement script first. This does 
not happen very often, and should not be a problem that another team should have to concern themselves with. The 
movement program should handle any problems gracefully, and not crash, meaning this program should not crash.

This program will only run on a computer that has zeromq correctly installed with the python bindings.

Additional information can be found in the user manual provided with the vehicle.
'''
#import statements
from random import randint
import time
import zmq

#the time in seconds that the program should go without a heartbeat before it sends the E-STOP command
TIMEOUT_DURATION = 1

#sets up the ZMQ for the server
context=zmq.Context()
worker=context.socket(zmq.REP)
worker.bind("tcp://*:2424")
#sets up the ZMQ to connect to the movement program
relay=context.socket(zmq.REQ)
relay.connect("tcp://localhost:2425")
#sets up the ZMQ poller to listen for messages on the socket
poller = zmq.Poller()
poller.register(worker,zmq.POLLIN)
base_time=time.time()
#vehicle_state is initialized to 0, or ready
vehicle_state=0
#estop is initialized to 0, or off
#this maintains the state of the estop from losing the heartbeat
estop = 0

'''
The main loop that polls on the socket. It will receive all messages and handle them accordingly
'''
while True:
	#look for message on socket
    try:
        socks = dict(poller.poll(1)) 
    except KeyboardInterrupt:
        break

	#if there is a message on the socket, handle it
    if worker in socks:
        frames = worker.recv()
		#the first character in the message should be the indicator (0 - 3)
        cmd=int(frames[0])
		#if the command is 0, it is the heartbeat signal
        if cmd==0:
			#if the program was frozen, unfreeze it until heartbeat lost again
			if(estop == 1):
				print "Heartbeat found"
				estop = 0
			#keep track of time between heartbeats, reset base time when signal received
            base_time=time.time()         
            worker.send(b"0")
		#if the command is 1, the movement command will be passed to the movement program
        if cmd==1:
			print "Command received"
			#vehicle is in busy state
            vehicle_state=1
			#get the rest of the message
            relaymsg=frames[1:]
			#send message to movement program, wait for reply
            relay.send(relaymsg)
            reply=relay.recv()
			#reply to the network node the command status received
            worker.send(b"%s"%reply)
		#if the command is 2, reply with the current state of the vehicle
        if cmd==2:
            print "Status received"
            msg=str(vehicle_state)
            worker.send(b"%s"%vehicle_state)
		#if the command is 3, set the vehicle state to ready (0)
        if cmd==3:
			print "Completion received"
            vehicle_state=0
            worker.send(b"")
	#while in the loop, check for the interval between heartbeats
	#if this interval is greater than TIMEOUT_DURATION, send E-STOP command
    else:
        current_time=time.time()
		#if interval is greater than TIMEOUT_DURATION
        if (current_time-base_time)>TIMEOUT_DURATION:
			#only send E-STOP command when program is not frozen
			if(estop == 0):
				print "Activate E-Stop"
				relay.send(b"00")
				reply=relay.recv()
				#mark program as frozen
				estop = 1
        
print "finished"       
