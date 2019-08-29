import threading

from gui.Interface import Interface
from server.Server import Server
from server.Database import Database


def main():
    host = ''
    port = 12800
    database = Database()
    server = Server(host, port, database)
    t = threading.Thread(target=server.launch)
    t.daemon = True
    print("Launching server...")
    t.start()
    print("Launching GUI...")
    inter = Interface(database)


if __name__ == '__main__':
    main()
