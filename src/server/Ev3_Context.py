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
        N = 2.7  # N -> envorinemental factor.

        for i in range(0, int(len(scan) - 1), 3):
            addr = scan[i].split(" ")[1]
            signal = scan[i + 1].split(" ")[1]
            name = scan[i + 2].split(" ")[1]
            currentPos.append((name, addr, signal))
        for i in currentPos:
            signal = int(float(i[2]))

            distance = 10 ** ((MP - signal) / (10 * N))
            print("Distance from ", i[0], " is :", distance, "meters, dBm = ", i[2])

    """To find the position of the client."""

    def askScanForPosition(self):
        self.client.send(b"4scan`")

    """Callback functions for "askScanForPosition" """

    def askScanForPosition_Callback(self, scan):
        N = 7  # number of fingerprint used
        current_fingerprint = list()  # One scan from current_fingerprint =  ('70:28:8b:d4:53:49', -71)
        scan = scan.split("\n")
        print("Current fg = ")
        for i in range(0, int(len(scan) - 1), 3):
            addr = scan[i].split(" ")[1]
            signal = scan[i + 1].split(" ")[1]
            name = scan[i+2].split(" ")[1]
            if name == "OnePlus" :
                continue
            current_fingerprint.append((addr, signal))
            print("addr : ", addr)

        fingerprints = self.server.database.getFingerprints()  # One scan from fingerprints = (711, 110, '70:28:8b:d4:53:49', -71)

        self.print_difference_between_current_and_dbfg(current_fingerprint, fingerprints)

        fingerprint_with_value = list()
        for fg in fingerprints:
            fingerprint_with_value.append(self.fingerprintValue2(current_fingerprint, fg))

        sorted_fingerprints = sorted(fingerprint_with_value, key=lambda x: x[0])

        if len(sorted_fingerprints) > N:
            sorted_fingerprints = sorted_fingerprints[len(sorted_fingerprints) - N:]
        print(sorted_fingerprints)

        pos = self.relative_position(sorted_fingerprints)

        print("Relative position is : ", pos)
        self.x = pos[0]
        self.y = pos[1]

    """return the estimated position according to a set of positions"""

    def relative_position(self, positions):
        # One position --> (0.015215327576699661, 629, 114) -> Coef | x | y
        div = 0
        for pos in positions:
            if pos[0] > 0:
                div += pos[0]
        x = 0
        y = 0
        for pos in positions:
            x += pos[0] * pos[1]
            y += pos[0] * pos[2]
        if div > 0:
            return (x / div, y / div)
        return x, y

    def print_difference_between_current_and_dbfg(self, current_fingerprint, fingerprints):
        # One scan from current_fingerprint =  ('70:28:8b:d4:53:49', -71)
        # One scan from fingerprints = (711, 110, '70:28:8b:d4:53:49', -71)
        current_scan = dict()
        for scan in current_fingerprint:
            current_scan[scan[0]] = scan[1]
        diff = 0
        for fg in fingerprints:

            print("diff = ", diff)
            print("\nFingerprint , value is : ", self.fingerprintValue2(current_fingerprint, fg)[0])
            diff = 0
            for scan in fg:
                try:
                    if current_scan[scan[2]] is not None:
                        diff += self.valAbs(int(float(current_scan[scan[2]])) - scan[3])
                        print("Device :", scan[2], " | (", scan[0], ":", scan[1], ") | CurrentS : ",
                              current_scan[scan[2]],
                              " RegisterS : ", scan[3])
                except KeyError:
                    pass
        print("diff = ", diff)

    def fingerprintValue2(self, current_fingerprint, fingerprint):
        # One scan from current_fingerprint =  ('70:28:8b:d4:53:49', -71)
        # One scan from fingerprints = (711, 110, '70:28:8b:d4:53:49', -71)

        current_scan = dict()
        for scan in current_fingerprint:
            current_scan[scan[0]] = scan[1]

        count = 1
        value = 0

        for scan in fingerprint:
            try:
                if current_scan[scan[2]] is not None:
                    count +=1
                    value += self.valAbs(int(float(current_scan[scan[2]])) - scan[3])
            except KeyError:
                pass

        print("count = ", count)
        if value > 0:
            return (3 ** ((100 - self.valAbs(value)) / 10)) * count, fingerprint[0][0], fingerprint[0][1]
        return 0, fingerprint[0][0], fingerprint[0][1]

    """ Return a value corresponding to a fingerprint, this value is used to order fingerprints"""

    def fingerprintValue(self, current_fingerprint, fingerprint):
        # One scan from current_fingerprint =  ('70:28:8b:d4:53:49', -71)
        # One scan from fingerprints = (711, 110, '70:28:8b:d4:53:49', -71)
        current_scan = dict()
        for scan in current_fingerprint:
            current_scan[scan[0]] = 10 ** (int(float(scan[1])) / 10)

        value = 0
        for scan in fingerprint:
            try:
                if current_scan[scan[2]] is not None:
                    watt = 10 ** (int(float(scan[3])) / 10)
                    value += ((current_scan[scan[2]] - watt) * (current_scan[scan[2]] - watt)) / (
                            current_scan[scan[2]] * watt)
            except KeyError:
                pass
        return (value / len(fingerprint)), fingerprint[0][0], fingerprint[0][1]

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
