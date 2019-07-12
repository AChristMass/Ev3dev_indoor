#!/usr/bin/python3
import socket
from ev3dev2.motor import LargeMotor, SpeedPercent
from ev3dev import ev3 as ev3




def wait_running(mB, mC):
    mB.wait_while('running')
    mC.wait_while('running')


def rotation(mB, mC, degree):
    mB.run_to_rel_pos(position_sp=degree*2, speed_sp=100, stop_action="brake")
    mC.run_to_rel_pos(position_sp=-degree*2, speed_sp=100, stop_action="brake")
    wait_running(mB,mC)

def forward(mB, mC):
    mB.run_timed(time_sp = 3000, speed_sp = 900)
    mC.run_timed(time_sp = 3000, speed_sp = 900)
    wait_running(mB,mC)

def backward(mB, mC):
    mB.run_timed(time_sp = 3000, speed_sp = -900)
    mC.run_timed(time_sp = 3000, speed_sp = -900)
    wait_running(mB,mC)


#Set the wheels
mB = LargeMotor('outA')
mC = LargeMotor('outC')

#host = "192.168.43.208"
host="localhost"
port = 12800

server_connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_connection.connect((host, port))
server_connection.send(b"connection request")

print("Initialising...")
msg = server_connection.recv(1024)
msg = msg.decode()

print("first command receveid")

while msg != b"fin":
    if msg == 'z' :
        print("forward")
        forward(mB, mC)
    if msg == 's' :
        print("backward")
        backward(mB,mC)
    if msg == 'd' :
        print("right")
        rotation(mB, mC, 45)
    if msg == 'q' :
        print("left")
        rotation(mB, mC, -45)

    msg = server_connection.recv(1024)
    print("command received")
    msg = msg.decode()

server_connection.close()
