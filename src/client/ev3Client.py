#!/usr/bin/python3
import socket
import subprocess
from uuid import getnode as get_mac

from client.Request import Request

# sudo -S iw dev wlx4494fcf51bd0 scan | grep -o 'BSS ..\:..\:..\:..\:..\:..\|SSID: .*\|signal\: .*'


"""This script is use to run the Lego Mindstorm ev3, this client wait for instruction from the server and respond acocrdingly"""


class Client:
    # server_connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.server_connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print("Init connection...")
        self.server_connection.connect((host, port))
        print("Connection established")
        self.request = Request()
        self.state = Request.State.REFILL
        self.request.register(3, lambda x: self.server_connection.send(("3" + self.scan(x) + "`").encode()))
        self.request.register(4, lambda x: self.server_connection.send(("4" + self.scan(x) + "`").encode()))
        self.request.register(5, lambda x: self.server_connection.send(("5" + self.scan(x) + "`").encode()))
        self.pending = ""
        self.launched = True
        self.macAdress = hex(get_mac())

    """indentify the client to the server"""

    def launch(self):
        self.server_connection.send(b"ev3")
        identification = self.server_connection.recv(1024)
        if identification == "refused":
            print("Identification refused, please update your client...")
            return
        print("Identification succed")
        self.server_connection.send(("1" + self.macAdress + "`").encode())
        while self.launched:
            self.doRead()

        self.server_connection.close()

    # Scan and send to the server RSSI signaturen
    def scan(self, request):
        scan = subprocess.check_output(
            "echo maker | sudo -S iw dev wlx4494fcf51bd0 scan | grep -o 'BSS ..\:..\:..\:..\:..\:..\|SSID: .*\|signal\: .*'",
            shell=True)
        # self.server_connection.send(("3" + scan.decode("utf-8") + "`").encode())
        print("Sending scan...")
        return scan.decode("utf-8")

    """Read packet from the sever"""

    def doRead(self):
        recv = self.server_connection.recv(1024)
        last = str(recv.decode())
        recv = str(recv.decode()).split("`")

        if recv[0] == "" or recv[0] == '':
            print("ev3 client disconnected")
            self.launched = False
            return

        if self.pending != "":
            recv[0] = self.pending + recv[0]
            self.pending = ""

        if last != "`":
            self.pending = recv[-1]
            recv.pop()

        for request in recv:
            self.processIn(request)

    """Process the server request contained in a packet"""

    def processIn(self, request):
        self.state = self.request.process(request)
        if self.state == Request.State.ERROR:
            print("Can't deal that kind of packets")


def main():
    host = "192.168.43.208"
    port = 12800
    client = Client(host, port)
    print("Launching...")
    client.launch()


if __name__ == '__main__':
    main()

# msg = server_connection.recv(1024)
# msg = msg.decode()
