#!/usr/bin/env python3
from ev3dev2.motor import LargeMotor
from ev3dev2.sensor.lego import TouchSensor, UltrasonicSensor
from ev3dev2.sensor import INPUT_1, INPUT_2, INPUT_3, INPUT_4
from ev3dev2.led import Leds
from ev3dev2.sound import Sound
from time import sleep



def wait_running(mB, mC):
    mB.wait_while('running')
    mC.wait_while('running')


def rotation(mB, mC, degree):
    mB.run_to_rel_pos(position_sp=degree*2, speed_sp=100, stop_action="brake")
    mC.run_to_rel_pos(position_sp=-degree*2, speed_sp=100, stop_action="brake")
    
def forward(mB, mC):
    mB.run_forever(speed_sp=540)
    mC.run_forever(speed_sp=540)


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

#leds.all_off() # stop the LEDs flashing (as well as turn them off)


#while not ts.is_pressed :
while True:
    while usMiddle.distance_centimeters<= 35 : 
        leds.set_color('LEFT',  'RED')
        leds.set_color('RIGHT', 'RED')

        dRight = usRight.distance_centimeters
        dLeft = usLeft.distance_centimeters

        if dRight <= 10 : 
            rotation(mB, mC, -1)
            continue

        if dLeft <= 10 :
            rotation(mB, mC, 1)
            continue
        
        rotation(mB, mC, 1)

    if usRight.distance_centimeters < 10 : 
        rotation(mB, mC, -1)
        continue

    if usLeft.distance_centimeters < 10 : 
        rotation(mB, mC,  1)
        continue

    forward(mB, mC)
    leds.set_color('LEFT',  'GREEN')
    leds.set_color('RIGHT', 'GREEN')

