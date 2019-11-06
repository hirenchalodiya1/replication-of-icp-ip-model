import threading

# Variables for holding information about connections
connections = []
total_connections = 0


# Client class, new instance created for each connected client
# Each instance has the socket and address that is associated with items
# Along with an assigned ID and a name chosen by the client
class Client(threading.Thread):
    def __init__(self, sock, address, id_, name, signal):
        threading.Thread.__init__(self)
        self.socket = sock
        self.address = address
        self.id = id_
        self.name = name
        self.signal = signal

    def __str__(self):
        return str(self.id) + " " + str(self.address)

    # Attempt to get data from client
    # If unable to, assume client has disconnected and remove him from server data
    # If able to and we get data back, print it in the server and send it back to every
    # client aside from the client that has sent it
    # .decode is used to convert the byte data into a printable string
    def run(self):
        while self.signal:
            try:
                data = self.socket.recv(32)
                if data == b'':
                    raise
            except:
                print("Client " + str(self.address) + " has disconnected")
                self.signal = False
                self.socket.close()
                connections.remove(self)
                break

            if data != "":
                print("hello")
                print("ID " + str(self.id) + ": " + str(data.decode("utf-8")))
                for client in connections:
                    if client.id != self.id:
                        client.socket.sendall(data)


# Wait for new connections
def new_connections(sock):
    while True:
        c_sock, address = sock.accept()
        global total_connections
        connections.append(Client(c_sock, address, total_connections, "Name", True))
        connections[len(connections) - 1].start()
        print("New connection at ID " + str(connections[len(connections) - 1]))
        total_connections += 1