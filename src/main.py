import threading

from gui.Interface import Interface
from server.Server import Server


def main():
    host = ''
    port = 12800
    server = Server(host, port)
    t = threading.Thread(target=server.launch)
    t.daemon = True
    print("Launching server...")
    t.start()
    print("Launching GUI...")
    inter = Interface()
    inter.create_interface()




if __name__ == '__main__':
    main()
