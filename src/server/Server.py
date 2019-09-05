import select
import socket
import threading

from database.Database import Database
from server.Ev3_Context import Ev3Context


class Server:
    contextsAvailable = list("ev3")
    lock = threading.Lock()
    logged = list()  # Store connected client with an active context

    def __init__(self, host, port, database):
        self.host = host
        self.port = port
        self.server_connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_connection.bind((host, port))
        self.server_connection.listen()
        self.server_connection.setblocking(False)
        self.server_launched = True
        self.connected_clients = []  # Used to store each client who have requested a connection
        self.contexts = dict()  # Used to store one context for every client identified , a contexts is a class use to store data and action for a specific client.
        self.database = database
        print("Server launched on port : {}".format(port))

    # Main loop, can register new clients and call processKey for each clients who can be read or write
    def launch(self):
        nb_clients = 0
        while threading.current_thread().is_alive():
            if (len(self.connected_clients) != nb_clients):
                print("Connected clients : ", len(self.connected_clients))
                nb_clients = len(self.connected_clients)

            connections_asked, wlist, xlist = select.select([self.server_connection], [], [], 0.05)
            for connection in connections_asked:
                connection_client, infos_connection = connection.accept()
                if connection not in self.connected_clients:
                    self.connected_clients.append(connection_client)
                    self.contexts[
                        str(infos_connection)] = None  # Add an entry according to the ip addr and port of a client

            if len(self.connected_clients) > 0:
                self.processClients()

        for client in self.connected_clients:
            client.close()

        self.server_connection.close()

    def processClients(self):
        try:
            clients_toRead, wlist, xlist = select.select(self.connected_clients, [], [], 0.05)
        except select.error:
            pass
        else:
            for client in clients_toRead:
                try:
                    addr = (str(client).split()[7] + " " + str(client).split()[8])[:-1].split("=")[
                        1]  # Extract the ip addr and port
                    if self.contexts[addr] is None:  # if no context is attached to a client
                        Server.lock.acquire()
                        full_recv = str(client.recv(1024).decode()).split("`")
                        recv = full_recv[0]
                        if recv == "ev3":
                            self.contexts[addr] = Ev3Context(client, self, addr)
                            Server.logged.append(self.contexts[addr])
                            client.send("accepted".encode())
                        else:
                            self.connected_clients.remove(client)
                            client.send("refused".encode())
                        Server.lock.release()
                    else:
                        self.contexts[addr].doRead()
                except ConnectionResetError:
                    self.connected_clients.remove(client)
                    continue
