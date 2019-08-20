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
            self.cmd.execute("create table data (zone integer, bssid varchar, signal integer)")
            self.cmd.execute("create table fingerprints (x interger, y interger, PRIMARY KEY(x, y))")
        else:
            self.bdd = sqlite3.connect('../bdd/fingerPrint.db')
            self.cmd = self.bdd.cursor()
            print("Database detected")

    def scanFringerprint(self, lines, context):
        lines = lines.split("\n")
        for i in range(0, int(len(lines) - 1), 3):
            addr = lines[i].split(" ")[1]
            signal = lines[i + 1].split(" ")[1]
            name = lines[i + 2].split(" ")[1]
            if name == "OnePlus":
                continue
            self.addOnDataBase(context.x, context.y, addr, signal, 0)

    def addOnDataBase(self, x, y, bssid, signal, way):
        try:
            signal = int(float(signal))
            # You have to reconnect the bdd, otherwize you'll get a "SqLite object created in an other Thread error"
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

    def addOnDataBaseWithArea(self, area, bssid, signal):
        try:
            signal = int(float(signal))
            # You have to reconnect the bdd, otherwize you'll get a "SqLite object created in an other Thread error"
            self.bdd = sqlite3.connect('../bdd/fingerPrint.db')
            self.cmd = self.bdd.cursor()
            self.cmd.execute(
                'insert into data(area, bssid, signal) Values (' + str(area) + ',"' + str(bssid) + '", ' + str(signal) + ')')

            print("db add : ",
                  '(' + str(area) + ',"' + str(bssid) + '", ' + str(signal) + ')')
            self.bdd.commit()
        except:
            print("Triplet zone:" + str(area) + " bssid:" + bssid + " signal " + signal + " already exist.")

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