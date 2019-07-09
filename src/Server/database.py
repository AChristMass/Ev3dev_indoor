import subprocess
import sqlite3
import os.path

class Database :
    def __init__(self):
        if not os.path.isfile("../bdd/fingerPrint.db"):
            self.bdd = sqlite3.connect('../bdd/fingerPrint.db')
            self.cmd = self.bdd.cursor()
            print("Initialising Database...")
            self.cmd.execute("create table signals (x integer, y integer, bssid varchar, signal integer not null, type integer not null, PRIMARY KEY(x, y, bssid))")
        else:
            self.bdd = sqlite3.connect('../bdd/fingerPrint.db')
            self.cmd = self.bdd.cursor()
            print("Database detected")
       
    #This one should only be implemnted into the client
    def scanFringerprint(self, lines) :
        print("adding scan to database")
        lines  = lines.decode('utf-8').split("\n")
        for i in range(0,int(len(lines)-1),3):
            addr = lines[i].split(" ")[1]
            signal = lines[i+1].split(" ")[1]
            name = lines[i+2].split(" ")[1]
            print(addr,signal,name)

 
        """for line in lines:
            values = line.rsplit(":", 1)
            values[0] = values[0].replace('\\',"")
            self.addOnDataBase(0, 0, values, 0)"""
             
    def addOnDataBase(self, x, y, values, way):
        try:
            self.cmd.execute('insert into signals(x, y, bssid, signal, type) Values (' +str(x)+', ' +str(y)+',"' +values[0]+'", ' +values[1]+', ' + str(way)+ ')')
            print("db add : ", '(' +str(x)+', ' +str(y)+',"' +values[0]+'", ' +values[1]+', ' + str(way)+ ')')
            self.bdd.commit()
        except:
            print("Triplet X:" + str(x) + " Y:" + str(y) + " BSSID:" + values[0] + " est deja existant.")


    def printTable(self, cmd):
        cmd.execute('select * from signals')
        for i in cmd:
            print(i)
