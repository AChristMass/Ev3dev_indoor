import os.path
import sqlite3


class Database:
    def __init__(self):
        if not os.path.isfile("../bdd/fingerPrint.db"):
            self.bdd = sqlite3.connect('../bdd/fingerPrint.db')
            self.cmd = self.bdd.cursor()
            print("Initialising Database...")
            self.cmd.execute(
                "create table signals (x integer, y integer, bssid varchar, signal integer not null, type integer not null, PRIMARY KEY(x, y, bssid))")
            self.cmd.execute("CREATE TABLE data (zone integer default 0)")
            self.cmd.execute("create table fingerprints (x interger, y interger, PRIMARY KEY(x, y))")
        else:
            self.bdd = sqlite3.connect('../bdd/fingerPrint.db')
            self.cmd = self.bdd.cursor()
            print("Database detected")

        self.knownAPs = list()
        self.excludedAPs = set()
        self.excludedAPs.add("OnePlus")

    def scanFringerprint(self, lines, context):
        lines = lines.split("\n")
        address = list()
        signals = list()
        for i in range(0, int(len(lines) - 1), 3):
            addr = lines[i].split(" ")[1]
            address.append(lines[i].split(" ")[1])

            signal = lines[i + 1].split(" ")[1]
            signals.append(int(float(lines[i + 1].split(" ")[1])))

            name = lines[i + 2].split(" ")[1]
            if name == "OnePlus":
                continue
            self.addOnDataBase(context.x, context.y, addr, signal, 0)

    def addOnDataBase(self, x, y, bssid, signal, way):
        try:
            signal = int(float(signal))
            # The next 2 lines are here because you have to reconnect the bdd,
            # otherwize you'll get a "SqLite object created in an other Thread error,
            # that's a known error with sqlite3 "
            self.bdd = sqlite3.connect('../bdd/fingerPrint.db')
            self.cmd = self.bdd.cursor()
            self.cmd.execute(
                'insert into signals(x, y, bssid, signal, type) Values (' + str(x) + ', ' + str(y) + ',"' + str(
                    bssid) + '", ' + str(signal) + ', ' + str(way) + ')')

            print("db add : ",
                  '(' + str(x) + ', ' + str(y) + ',"' + str(bssid) + '", ' + str(signal) + ', ' + str(way) + ')')
            self.bdd.commit()
        except:
            print("Triplet X:" + str(x) + " Y:" + str(y) + " BSSID:" + bssid + " already exist.")

    def scan_fringerprint_with_area(self, lines, context):
        lines = lines.split("\n")
        address = list()
        signals = list()
        for i in range(0, int(len(lines) - 1), 3):
            name = lines[i + 2].split(" ")[1]
            if name in self.excludedAPs:
                continue

            address.append(lines[i].split(" ")[1])
            signals.append(int(float(lines[i + 1].split(" ")[1])))

        self.add_fingerprint_with_area(context.area, address, signals)

    def add_fingerprint_with_area(self, area, bssids, signals):

        try:
            # The next 2 lines are here because you have to reconnect the bdd,
            # otherwize you'll get a "SqLite object created in an other Thread error,
            # that's a known error with sqlite3 "
            self.bdd = sqlite3.connect('../bdd/fingerPrint.db')
            self.cmd = self.bdd.cursor()

            for bssid in bssids :
                if bssid not in self.knownAPs :
                    self.knownAPs.append(bssid)
                    self.cmd.execute('ALTER TABLE data ADD column' + str(bssid) + 'integer DEFAULT 0')


            self.cmd.execute(
                'insert into data('+",".join(bssids)+') Values ('+",".join(signals) +')')

            print("db add : " + ",".join(bssids))
            self.bdd.commit()
        except:
            print("Fingerprint already existing.")

    def printTable(self):
        print("Print table")
        self.cmd.execute('select * from signals')
        for i in self.cmd:
            print(i)

    def valAbs(self, x):
        return x if x > 0 else -x

    def getScans(self):
        scans = list()
        self.bdd = sqlite3.connect('../bdd/fingerPrint.db')
        self.cmd = self.bdd.cursor()
        self.cmd.execute('select * from signals ORDER BY x, y')
        for i in self.cmd:
            scans.append(i[:-1])
        return scans

    def get_fp_list(self):
        self.bdd = sqlite3.connect('../bdd/fingerPrint.db')
        self.cmd = self.bdd.cursor()
        self.cmd.execute('select DISTINCT x, y from signals')
        lst = []
        for i in self.cmd:
            lst.append(i)
        return lst

        return scans

    def getFingerprints(self):
        scans = self.getScans()
        fingerprints = list()
        x = y = -1

        for i in range(0, len(scans) - 1):
            if x != scans[i][0] or y != scans[i][1]:
                x = scans[i][0]
                y = scans[i][1]
                i += 1
                fg = [scans[i]]
                fingerprints.append(fg)

            else:
                fingerprints[len(fingerprints) - 1].append(scans[i])

        return fingerprints
