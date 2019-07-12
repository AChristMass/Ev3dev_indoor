import socket
from ev3dev2.motor import LargeMotor
from ev3dev2.sensor.lego import TouchSensor, UltrasonicSensor
from ev3dev2.sensor import INPUT_1, INPUT_2, INPUT_3, INPUT_4
from ev3dev2.led import Leds
from ev3dev2.sound import Sound

def wait_running(mB, mC):
    mB.wait_while('running')
    mC.wait_while('running')


def rotation(mB, mC, degree):
    mB.run_to_rel_pos(position_sp=degree*2, speed_sp=100, stop_action="brake")
    mC.run_to_rel_pos(position_sp=-degree*2, speed_sp=100, stop_action="brake")

def forward(mB, mC):
    mB.run_forever(speed_sp=540)
    mC.run_forever(speed_sp=540)

def backward(mB, mC):
    mB.run_forever(speed_sp=-540)
    mC.run_forever(speed_sp=-540)


#Set the wheels
mB = LargeMotor('outA')
mC = LargeMotor('outC')

# Connect ultrasonic and touch sensors to any sensor port
usRight = UltrasonicSensor(INPUT_3)
usMiddle = UltrasonicSensor(INPUT_4)
usLeft = UltrasonicSensor(INPUT_1)
#ts = TouchSensor()
leds = Leds()
sound = Sound()


host = "169.254.208.101"
port = 12800

server_connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_connection.connect((host, port))



msg = server_connection.recv(1024)
msg = msg.decode()
while msg != b"fin":
    if msg == 'z' :
        forward(mB, mC)
    if msg == 's' :
        backward(mB,mC)
    if msg == 'd' :
        rotation(mB, mC, 45)
    if msg == 'q' :
        rotation(mB, mC, -45)
    msg = server_connection.recv(1024)
    msg = msg.decode()



server_connection.close()