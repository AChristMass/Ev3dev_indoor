#!/usr/bin/python3
from ev3dev2.button import Button
import os
from time import sleep
os.system('setfont Lat15-TerminusBold14') 
    
def main():
    print("MAIN DEMARRE")
    but =  Button()
    while(True):
        if(but.left):
            os.system("clear")
            print("left")
        elif but.up:
            os.system("clear")
            print("up")
        elif but.right:
            os.system("clear")
            print("right")
        elif but.down:
            os.system("clear")
            print("down")
        sleep(0.1)

if __name__ == "__main__":
    main()
