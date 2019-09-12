import os.path
import sqlite3

"""This class is used to create a Database, it contains every methods needed 
to add, alter or delete data on the database."""


class Database:
    def __init__(self):
        if not os.path.isfile("../bdd/fingerPrint.db"):
            self.bdd = sqlite3.connect('../bdd/fingerPrint.db')
            self.cmd = self.bdd.cursor()
            print("Initialising Database...")
            # self.cmd.execute("create table signals (x integer, y integer,
            # bssid varchar, signal integer not null, type integer not null, PRIMARY KEY(x, y, bssid))")
            self.cmd.execute(
                "create table FG (x integer, y integer, xc integer, yc integer)")
            self.cmd.execute("create table cases (x integer, y integer, area integer default -1)")
        else:
            self.bdd = sqlite3.connect('../bdd/fingerPrint.db')
            self.cmd = self.bdd.cursor()
            print("Database detected")

        self.knownAPs = list()
        self.excludedAPs = set()
        self.excludedAPs.add("OnePlus")
        self.excludedAPs.add("Redmi")
        self.excludedAPs.add("AndroidAP2815")
        self.excludedAPs.add("AndroidAP7398")
        self.excludedAPs.add("Huawei P8 lite 2017")
        self.excludedAPs.add("DIRECT-5B-HP ENVY 5000 series")

        self.data_to_predict = None

        self.cmd.execute("PRAGMA table_info(FG)")
        self.cursors = [e for e in self.cmd]
        for i in self.cursors[4:]:
            self.knownAPs.append(i[1])

    """Store a scan into @self.data_to_predict after adding undetected APs to this scan"""

    def store_and_flat_current_scan(self, address, signals):
        data = list()

        for ap in self.knownAPs:
            if ap in address:
                data.append(signals[address.index(ap)])
            else:
                data.append(0)
        print(data)
        self.data_to_predict = data

        return

    """Interpret data from a scan ,then call @self.add_fingerprint_with_area"""

    def scan_fingerprint_with_area(self, lines, context):
        lines = lines.split("\n")
        address = list()
        signals = list()
        for i in range(0, int(len(lines) - 1), 3):
            name = lines[i + 2].split(" ")[1]
            if name in self.excludedAPs:
                continue
            if str(name) == "eduroam" or str(name) == "umlv-sf-captif":

                address.append(lines[i].split(" ")[1])
                signals.append(int(float(lines[i + 1].split(" ")[1])))
                if signals[len(signals) - 1] < -79:
                    signals[len(signals) - 1] = 0
            else:
                continue

        self.add_fingerprint_with_area(context, address, signals)

    """Add new fingerprint to the database, also change 
    the table by adding new column for each unknown new APs"""

    def add_fingerprint_with_area(self, context, bssids, signals):
        # The next 3 lines are here because you have to reconnect the bdd,
        # otherwize you'll get a "SqLite object created in an other Thread error,
        # that's a known error with sqlite3 "
        self.bdd = sqlite3.connect('../bdd/fingerPrint.db')
        self.cmd = self.bdd.cursor()

        x = context.x
        y = context.y
        xc = context.xc
        yc = context.yc

        for bssid in bssids:
            if bssid not in self.knownAPs:
                self.knownAPs.append(bssid)
                self.cmd.execute('ALTER TABLE FG ADD column' + '\'' + str(bssid) + '\'' + 'integer DEFAULT 0')

        self.cmd.execute('SELECT * FROM  FG')
        for i in self.cmd:
            print(i)

        self.cmd.execute(
            'INSERT INTO FG(x, y, xc, yc,\'' + "','".join(bssids) + '\' ) VALUES (' + str(x) + ',' + str(
                y) + ',' + str(xc) + ',' + str(yc) + "," + ", ".join(str(signal) for signal in signals) + ')')

        self.bdd.commit()
        return

    """Return every fingerprint with the area where each 
    fingerprints as been done for Machine Learning training"""

    def get_fp_for_training(self):
        self.bdd = sqlite3.connect('../bdd/fingerPrint.db')
        self.cmd = self.bdd.cursor()

        self.cmd.execute(
            'SELECT * FROM CASES JOIN FG WHERE CASES.x = FG.xc AND CASES.y = FG.yc')

        data = list()
        for i in self.cmd:

            temp = list()

            for j in range(7, len(i)):
                temp.append(i[j])
            temp.append(i[2])
            data.append(temp)

        return data

    """Return the fingerprints stored in the database"""

    def getScans(self):
        scans = list()
        self.bdd = sqlite3.connect('../bdd/fingerPrint.db')
        self.cmd = self.bdd.cursor()
        self.cmd.execute('select * from FG ORDER BY x, y')
        for i in self.cmd:
            scans.append(i[:-1])
        return scans

    """Return the position of every fingerprints in the database 
    if they are in the same location only one set of coordinate is send"""

    def get_fp_list(self):
        self.bdd = sqlite3.connect('../bdd/fingerPrint.db')
        self.cmd = self.bdd.cursor()
        self.cmd.execute('select DISTINCT x, y from FG')
        lst = []
        for i in self.cmd:
            lst.append(i)
        return lst

        return scans

    """Add a box to the database with his position and the area the box is inside"""

    def add_new_box(self, x, y, area):
        try:
            self.bdd = sqlite3.connect('../bdd/fingerPrint.db')
            self.cmd = self.bdd.cursor()
            self.cmd.execute('insert into cases(x, y, area) Values (' + str(x) + ', ' + str(y) + ',' + str(
                area) + ')')
            print('insert into cases(x, y, area) Values (' + str(x) + ', ' + str(y) + ',' + str(
                area) + ')')
            self.bdd.commit()
        except:
            print("Already exist")

    """Get the number of area stored in the database"""

    def load_id_area(self):
        self.bdd = sqlite3.connect('../bdd/fingerPrint.db')
        self.cmd = self.bdd.cursor()
        self.cmd.execute('select max(area) from cases')
        id = 0
        for i in self.cmd:
            id = i
        return id[0]

    """Remove an area linked to a Box"""

    def delete_area_from_case(self, x, y):
        self.bdd = sqlite3.connect('../bdd/fingerPrint.db')
        self.cmd = self.bdd.cursor()
        self.cmd.execute('update cases set area = -1 where x =' + str(x) + ' and ' + str(y))
        self.bdd.commit()

    """Get Boxes stored int the database"""

    def load_cases(self):
        self.bdd = sqlite3.connect('../bdd/fingerPrint.db')
        self.cmd = self.bdd.cursor()
        self.cmd.execute('select x, y, area from cases')
        return self.cmd

    """Get areas stored in the database"""

    def load_areas(self):
        self.bdd = sqlite3.connect('../bdd/fingerPrint.db')
        self.cmd = self.bdd.cursor()
        self.cmd.execute('select distinct area from cases')
        lst = []
        for i in self.cmd:
            lst.append(i[0])
        return lst
