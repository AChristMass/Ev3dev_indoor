import select
import socket

host = ''
port = 12800

server_connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_connection.bind((host, port))
server_connection.listen(5)
print("Le serveur écoute à présent sur le port {}".format(port))

server_launched = True
connected_clients = []
while server_launched:

    connections_asked, wlist, xlist = select.select([server_connection], [], [], 1)

    clients_toRead = []

    for connexion in connections_asked:
        connection_client, infos_connexion = connexion.accept()
        if connexion not in connected_clients:
            connected_clients.append(connection_client)
        else:
            print("One client has something to say")
            clients_toRead.append(connexion)

    print("nombre de client = ", len(connected_clients))
    for client in clients_toRead:

        try:
            msg_recv = client.recv(1024)
        except ConnectionResetError:
            connected_clients.remove(client)
            continue

        msg_recv = msg_recv.decode()
        print("Reçu {}".format(msg_recv))
        try:
            client.send(b"received")
            if msg_recv == "fin":
                server_launched = False
        except BrokenPipeError:
            connected_clients.remove(client)
            continue

print("Fermeture des connexions")
for client in connected_clients:
    client.close()

server_connection.close()
