#!/usr/bin/python3
import subprocess
import sqlite3
import os.path

def createDataBase():
    if not os.path.isfile("../bdd/fingerPrint.db"):
        bdd = sqlite3.connect('../bdd/fingerPrint.db')
        cmd = bdd.cursor()
        print("Initialising Database...")
        cmd.execute("create table signals (x integer, y integer, bssid varchar, signal integer not null, type integer not null, PRIMARY KEY(x, y, bssid))")
    else:
        bdd = sqlite3.connect('../bdd/fingerPrint.db')
        cmd = bdd.cursor()
        print("Database detected")
    return (bdd, cmd)
        
def addOnDataBase(cmd, x, y, values, way):
    try:
        cmd.execute('insert into signals(x, y, bssid, signal, type) Values (' +str(x)+', ' +str(y)+',"' +values[0]+'", ' +values[1]+', ' + str(way)+ ')')
    except:
        print("Triplet X:" + str(x) + " Y:" + str(y) + " BSSID:" + values[0] + " est deja existant.")


def printTable(cmd):
    cmd.execute('select * from signals')
    for i in cmd:
        print(i)


def main():
    bdd, cmd = createDataBase()
    scan = "nmcli -t -f BSSID,SIGNAL dev wifi".split(" ")
    rescan = "nmcli -t -f BSSID,SIGNAL dev wifi rescan".split(" ")
    subprocess.run(rescan)
    command = subprocess.run(scan, stdout=subprocess.PIPE)
    lines = command.stdout.decode("utf-8").split("\n")[:-1]
    for line in lines:
        values = line.rsplit(":", 1)
        values[0] = values[0].replace('\\',"")
        addOnDataBase(cmd, 0, 0, values, 0)
    bdd.commit()
    printTable(cmd)
    bdd.close()

if __name__ == "__main__":
    main()