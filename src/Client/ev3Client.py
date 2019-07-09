#!/usr/bin/python3
import socket
import threading
import subprocess
import sys
import threading
sys.path.append('../')
from Common.request import Request
from uuid import getnode as get_mac


class Client:
    server_connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    def __init__(self, host, port):
        self.host = host
        self.port = port
        #self.server_connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_connection.connect((host, port))
        self.request = Request()
        self.state = Request.State.REFILL
        self.request.register(3, lambda x : self.scan(x))
        self.pending = ""
        self.launched = True
        self.macAdress = hex(get_mac())

    def launch(self) :
        self.server_connection.send(b"ev3")
        identification = self.server_connection.recv(1024)
        if identification == "refused" :
            print("Identification refused, please update your client...")
            return
        print("Connection established")
        self.server_connection.send( ("1" + self.macAdress + "`").encode() ) 
        while self.launched :
            self.doRead()
        
        self.server_connection.close()

    #Scan and send to the server RSSI signaturen
    def scan(self, request) :
        print("Launching scan...")
        scan = "nmcli -t -f BSSID,SIGNAL dev wifi".split(" ")
        rescan = "nmcli -t -f BSSID,SIGNAL dev wifi rescan".split(" ")
        subprocess.run(rescan)
        command = subprocess.run(scan, stdout=subprocess.PIPE)
        lines = command.stdout.decode("utf-8").split("\n")[:-1]
        self.server_connection.send(lines.encode())

    def doRead(self):
        recv = self.server_connection.recv(1024)
        print("Just recv : ", recv)
        last = str(recv.decode())
        recv = str(recv.decode()).split("`")

        if recv[0] == "" or recv[0] == '':
            print("ev3 client disconnected")
            self.launched = False
            return

        if self.pending != "" :
            recv[0] = self.pending + recv[0]
            self.pending = ""

        if last != "`" :
            self.pending = recv[-1]
            recv.pop()
            
        for request in recv :
            self.processIn(request)

    def processIn(self, request) :
        self.state = self.request.process(request)
        if self.state == Request.State.ERROR :
            print("Can't deal that kind of packets")
        

def main():
    host = "localhost"
    port = 12800
    client = Client(host, port)
    client.launch()


if __name__ == '__main__':
    main()

#msg = server_connection.recv(1024)
#msg = msg.decode()