from common.Request import Request


class Ev3Context:

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
        self.request.register(3, lambda x: self.server.database.scanFringerprint(x[1:], self))
        self.request.register(4, lambda x: self.askScanForPosition_Callback(x[1:]))
        self.request.register(5, lambda x: self.askDistance_Callback(x[1:]))
        self.x = 629
        self.y = 114
        self.macAddress = ""

    def doRead(self):
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
        self.state = self.request.process(request)
        if self.state == Request.State.ERROR:
            self.connected_clients.remove(self.client)

    def registerMacAdress(self, addr):
        self.macAddress = addr

    """To make a fingerprint."""

    def askScan(self):
        self.client.send(b"3scan`")

    def showScans(self):
        self.server.database.printTable()

    """Attempt to calculate the metric distance between the client and the AP's scanned"""

    def askDistance(self):
        self.client.send(b"5distance`")

    """Callback functions for "distance" """

    def askDistance_Callback(self, scan):
        currentPos = list()
        scan = scan.split("\n")
        MP = -45  # MP -> Expected measure for 1 meter distance.
        n = 2  # N -> envorinemental factor.

        for i in range(0, int(len(scan) - 1), 3):
            addr = scan[i].split(" ")[1]
            signal = scan[i + 1].split(" ")[1]
            name = scan[i + 2].split(" ")[1]
            currentPos.append((name, addr, signal))
        for i in currentPos:
            distance = 10 ** ((MP - int(float(i[2]))) / (10 * n))
            print("Distance from ", i[0], " is :", distance)

    """To find the position of the client."""

    def askScanForPosition(self):
        self.client.send(b"4scan`")

    """Callback functions for "askScanForPosition" """

    def askScanForPosition_Callback(self, scan):
        currentPos = list()
        scan = scan.split("\n")
        for i in range(0, int(len(scan) - 1), 3):
            addr = scan[i].split(" ")[1]
            signal = scan[i + 1].split(" ")[1]
            currentPos.append((addr, signal))

        scans = self.server.database.getScans()
        self.knn(3, currentPos, scans)

    def valAbs(self, x):
        return x if x > 0 else -x

    def knn(self, k, current_scan, scans):
        map_current = dict()
        map_relative = dict()
        for i in current_scan:
            map_current[i[0]] = int(float(i[1]))
            map_relative[i[0]] = None
        for j in scans:
            if not j[2] in map_relative:
                continue
            if map_relative[j[2]] is None:
                map_relative[j[2]] = (j[0], j[1], int(float(j[3])))
            else:
                if self.valAbs(j[3] - map_current[j[2]]) < self.valAbs(map_current[j[2]] - map_relative[j[2]][2]):
                    map_relative[j[2]] = (j[0], j[1], j[3])

        print(map_relative)

    def __str__(self):
        return "NAME : " + self.name + "     |     IP : " + self.ip + "     |     MacAddr : " + self.macAddress
