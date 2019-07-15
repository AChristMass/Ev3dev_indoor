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
        else:
            self.bdd = sqlite3.connect('../bdd/fingerPrint.db')
            self.cmd = self.bdd.cursor()
            print("Database detected")

    def scanFringerprint(self, lines, context):
        lines = lines.split("\n")
        for i in range(0, int(len(lines) - 1), 3):
            addr = lines[i].split(" ")[1]
            signal = lines[i + 1].split(" ")[1]
            # name = lines[i+2].split(" ")[1]
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
        self.cmd.execute('select * from signals')
        for i in self.cmd:
            scans.append(i[:-1])
        return scans