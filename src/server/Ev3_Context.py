from common.Request import Request


class Ev3Context:
    """An Ev3Context is associated to a client identified as an ev3.
    It is used to manage communication with this ev3 client.
    It manage every packet sended and received between him and the client associated"""

    def __init__(self, client, server, ipAddr):
        self.name = "ev3"
        self.client = client
        self.ip = ipAddr
        self.server = server
        self.connected_clients = server.connected_clients
        self.request = Request()
        self.state = Request.State.REFILL
        self.pending = ""  # Use to store data from an incompleted frame (Like a from who would take two calls to SOCKET.recv() to be completed)
        self.request.register(1, lambda x: self.registerMacAdress(x[3:]))
        self.request.register(2, lambda x: print(x[1:]))
        self.request.register(3, lambda x: self.server.database.scan_fingerprint_with_area(x[1:], self))
        self.request.register(4, lambda x: self.askScanForPosition_Callback(x[1:]))
        self.x = 629
        self.y = 114
        self.xc = None
        self.yc = None
        self.area = None
        self.macAddress = ""

    def doRead(self):
        """Read the buffer in order to extract packets"""
        recv = self.client.recv(1024)
        last = str(recv.decode())
        recv = str(recv.decode()).split("`")

        if recv[0] == "" or recv[0] == '':
            print("ev3 client disconnected")
            self.connected_clients.remove(self.client)
            self.server.logged.remove(self)
            return
        if self.pending != "":
            recv[0] = self.pending + recv[0]
            self.pending = ""
        if last != "`":
            self.pending = recv[-1]
            recv.pop()
        for request in recv:
            self.processIn(request)

    def processIn(self, request):
        """Call the function associated to the opcode contain in the head of @request"""
        self.state = self.request.process(request)
        if self.state == Request.State.ERROR:
            self.connected_clients.remove(self.client)

    def registerMacAdress(self, addr):
        """register a macAddress (bssid or ssid) """
        self.macAddress = addr

    def askScan(self):
        """Ask the client to send a scan containing the RSSI values of every APs in his reach,
        the client will respond with a packet of opcode 3, check out the function currently
        associated to opcode 3 in @self.__init__() to know what it does or change it"""
        self.client.send(b"3scan`")

    def showScans(self):
        """Print in the command line the scans"""
        self.server.database.printTable()

    def askScanForPosition_Callback(self, lines):
        """Demand a unique fingerprint to the client which will be processed and use to
        determined where the client is located"""
        print("askScanForPosition_Callback")
        lines = lines.split("\n")
        address = list()
        signals = list()
        for i in range(0, int(len(lines) - 1), 3):
            name = lines[i + 2].split(" ")[1]
            address.append(lines[i].split(" ")[1])
            signals.append(int(float(lines[i + 1].split(" ")[1])))

        self.server.database.store_and_flat_current_scan(address, signals)

    def __str__(self):
        return "NAME : " + self.name + "     |     IP : " + self.ip + "     |     MacAddr : " + self.macAddress
