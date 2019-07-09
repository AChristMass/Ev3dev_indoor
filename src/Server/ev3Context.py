import sys
from Common.request import Request

class Ev3Context :

    def __init__(self, client, server, ipAddr):
        self.name = "ev3"
        self.client = client
        self.ip = ipAddr
        self.server = server
        self.connected_clients = server.connected_clients
        self.request = Request()
        self.state = Request.State.REFILL
        self.pending = "" #Use to store data from an incompleted frame (Like a from who would take two calls to SOCKET.recv() to be completed)
        self.request.register(1, lambda x : self.registerMacAdress(x[3:]))
        self.request.register(2, lambda x : print(x[1:]))
        self.request.register(3, lambda x : self.server.database.scanFringerprint(x) )
        self.x = 629
        self.y = 114
        self.macAddress = ""


    def doRead(self):
        recv = self.client.recv(1024)
        last = str(recv.decode())
        recv = str(recv.decode()).split("`")
        print("recv : ", recv)

        if recv[0] == "" or recv[0] == '':
            print("ev3 client disconnected")
            self.connected_clients.remove(self.client)
            self.server.logged.remove(self)
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
            self.connected_clients.remove(self.client)

    def registerMacAdress(self, addr) :
        self.macAddress = addr   

    def askScan(self):
        self.client.send(b"3scan`")

           
    def __str__(self):
        return "NAME : " + self.name + "     |     IP : " + self.ip +  "     |     MacAddr : " + self.macAddress
    

