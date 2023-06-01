## best version

import random
import socket
import time
import select
from collections import deque
import multiprocessing

HEADERSIZE = 64
IP = "127.0.0.1"
MAX_CONNECTIONS = 1

#List of port numbers to use for each server
ports = [8000, 8001, 8002, 8003, 8004]

#Create a list of dictionaries to store the number of connected clients, the availability of each server, and whether the server is currently occupied
server_info = [{"port": port, "capacity": MAX_CONNECTIONS, "connected_clients": 0, "occupied": False} for port in ports]

#Create a list to track the current load of each server
server_loads = [0] * len(ports)


def server(port):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    server_socket.bind((IP,port))

    server_socket.listen()

    sockets_list = [server_socket]
    print(sockets_list)

    clients = {}

    # List tostore waiting clients
    waiting_clients = deque()

    def receive_message(client_socket):
        try:
            message_header = client_socket.recv(HEADERSIZE)
            
            if not len(message_header):
                return False
            
            message_length = int(message_header.decode("utf-8").strip())
            return {"header":message_header,"data":client_socket.recv(message_length)}
        
        except:
            pass
        return False

    while True:
        read_sockets, _, exception_sockets = select.select(sockets_list, [], sockets_list)
        for notified_socket in read_sockets:
            if notified_socket == server_socket:
                for server in server_info:
                    if server["occupied"] == False:
                        # If the current server is not occupied, accept the new client
                        client_socket, client_address = server_socket.accept()

                        user = receive_message(client_socket)

                        if user is False:
                            continue

                        sockets_list.append(client_socket)
                        clients[client_socket] = user

                        server["occupied"] = True
                        start_time = time.time()
                        server["connected_clients"] += 1

                        print(f"Accepted new connection from {client_address[0]}:{client_address[1]} username:{user['data'].decode('utf-8')} port:{server['port']}")

                        # Send a messageto the client indicating which server it is connected to
                        client_socket.send(f"You are connected to server on port {server['port']}\n".encode("utf-8"))

                        # Add the client to the clients dictionary
                        clients[client_socket] = {"user": user["data"].decode("utf-8"), "port": server['port']}

                        break
                else:
                    # If all servers are occupied, add the client to the waiting list
                    client_socket, client_address = server_socket.accept()

                    user = receive_message(client_socket)

                    if user is False:
                        continue

                    sockets_list.append(client_socket)
                    clients[client_socket] = user

                    waiting_clients.append(client_socket) # Store the socket of the waiting client

                    print(f"Client {client_address[0]}:{client_address[1]} username:{user['data'].decode('utf-8')} is waiting for an available server")

            else:
                # If the notified socket is not the server socket, it must be a client socket
                message = receive_message(notified_socket)

                if message is False:
                    print(f"Closed connection from {clients[notified_socket]['user']} port:{clients[notified_socket]['port']}")
                    end_time = time.time()
                    duration = end_time - start_time
                    print(f"duration : {duration}")
                    server = next(s for s in server_info if s['port'] == clients[notified_socket]['port'])
                    server['occupied'] = False
                    server['connected_clients'] -= 1
                    sockets_list.remove(notified_socket)
                    del clients[notified_socket]

                    # Check if there are any waiting clients
                    if len(waiting_clients) > 0:
                        # If there are waiting clients, accept the firstone and assign it to an available server
                        waiting_client_socket = waiting_clients.popleft()
                        server = next(s for s in server_info if s['occupied'] == False)
                        server['occupied'] = True
                        server['connected_clients'] += 1

                        print(f"Accepted new connection from {client_address[0]}:{client_address[1]} username:{user['data'].decode('utf-8')} port:{server['port']}")

                        # Send a messageto the client indicating which server it is connected to
                        waiting_client_socket.send(f"You are connected to server on port {server['port']}\n".encode("utf-8"))

                        # Add the client to the clients dictionary
                        clients[waiting_client_socket] = {"user": user["data"].decode("utf-8"), "port": server['port']}

                else:
                    # If there are no waiting clients, close the connection
                    print(f"Closed connection from {clients[notified_socket]['user']} port:{clients[notified_socket]['port']}")
                    server = next(s for s in server_info if s['port'] == clients[notified_socket]['port'])
                    server['occupied'] = False
                    server['connected_clients'] -= 1
                    sockets_list.remove(notified_socket)
                    del clients[notified_socket]


if __name__ == '__main__':
    # List of port numbers to use for each server
    ports = [8000, 8001, 8002, 8003, 8004]

    # Create a process for each server
    processes = []
    for port in ports:
        p = multiprocessing.Process(target=server, args=(port,))
        processes.append(p)

    # Start each process
    for p in processes:
        print(p)
        p.start()

    # Wait for all processes to finish
    for p in processes:
        p.join()