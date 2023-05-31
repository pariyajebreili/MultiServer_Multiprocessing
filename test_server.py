import random
import socket
import time
import select
from collections import deque
import multiprocessing

HEADERSIZE = 64
IP = "127.0.0.1"
MAX_CONNECTIONS = 1

# List of port numbers to use for each server
ports = [8000, 8001, 8002, 8003, 8004]

# Create a list of dictionaries to store the number of connected clients and the availability of each server
server_info = [{"port": port, "capacity": MAX_CONNECTIONS, "connected_clients": 0} for port in ports]

def server(port):

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    server_socket.bind((IP,port))

    server_socket.listen()

    sockets_list = [server_socket]
    print(sockets_list)

    clients = {}

    # List to store waiting clients
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
        #read_sockets, _, exception_sockets = select.select(sockets_list, [], sockets_list)
        for notified_socket in sockets_list : 
            if notified_socket== server_socket:
                for server in reversed(server_info):
                    if server["port"] == port and server["connected_clients"] < server["capacity"]:
                        # If the current server is the same as the server for this process and there is available capacity, accept the new client
                        client_socket, client_address = server_socket.accept()

                        user = receive_message(client_socket)

                        if user is False :
                            continue
                        sockets_list.append(client_socket)

                        clients[client_socket] = user
                        
                        print(f"Accepted new connection from {client_address[0]}:{client_address[1]} username:{user['data'].decode('utf-8')} port:{port}")
                        server["connected_clients"] += 1
                        #client_socket.send(f"You are connected to server on port:{port}".encode("utf-8"))
                        start_time = time.time()
                        #print(server["connected_clients"])
                        break
                    elif server["connected_clients"] < server["capacity"]:
                        # If the current serverContinuing from where we left off:has available capacity, accept the new client
                        client_socket, client_address = server_socket.accept()

                        user = receive_message(client_socket)

                        if user is False :
                            continue
                        sockets_list.append(client_socket)

                        clients[client_socket] = user

                        #print(f"Accepted new connection from {client_address[0]}:{client_address[1]} username:{user['data'].decode('utf-8')}port:{server['port']}")
                                  # Update the number of connected clients for the current server
                        server["connected_clients"] += 1
                        

                        # Encode the message and calculate its length
                        message1 = "heelooo"
                        username = message1.encode("utf-8")
                        username_header = f"{len(username):<{HEADERSIZE}}".encode("utf-8")
                        client_socket.send(username_header + username)


                        #message = receive_message(client_socket)
                        #port = message["port"]
                        #message_data = message["data"]
                        # Send a message to the client indicating which server it is connected to
                        
                        #client_socket.send(message["header"] + message_data.encode("utf-8"))
                        # Break out of the loop since we've connected to a server
                        break
                    else:
                        # If the current server is full, add the client to the waiting list
                        waiting_clients.append((client_socket, client_address))
                        #print(f"Client {port}: is waiting for an available server")

                # If we've gone through all the servers and haven't found an available one, wait for one to become available
                if len(waiting_clients) > 0:
                    #print("All servers are full, waiting for an available one...")
                    # Wait for up to 10 seconds for a server to become available
                    read_sockets, _, _ = select.select(sockets_list, [], [], 10)

                    for notified_socket in read_sockets:
                        random.shuffle(server_info)
                        for server in server_info:
                            if server["connected_clients"] < server["capacity"]:
                                # If the current server has available capacity, accept the new client
                                client_socket, client_address = server_socket.accept()

                                user =receive_message(client_socket)

                                if user is False:
                                    continue

                                sockets_list.append(client_socket)
                                clients[client_socket] = user

                                #print(f"Accepted new connection from {client_address[0]}:{client_address[1]} username:{user['data'].decode('utf-8')} port:{server['port']}")
                                server["connected_clients"] += 1
                                #print(server["connected_clients"])
                                break
                        else:
                            # If no servers have available capacity, add the client to the waiting list
                            waiting_clients.append((client_socket, client_address))
                            print(f"Client {client_address[0]}:{client_address[1]} is waiting for an available server")
            else:
                # If the notified socket is not the server socket, receive andprocess the message from the client
                message = receive_message(notified_socket)

                # If the message is False, remove the client socket from the list of sockets and the dictionary of clients
                if message is False:
                    sockets_list.remove(notified_socket)
                    del clients[notified_socket]

                    # Find the server that the disconnected client was connected to and update the number of connected clients
                    for server in server_info:
                        if server["port"] == port:
                            server["connected_clients"] -= 1
                            end_time = time.time()
                            duration = end_time - start_time
                            print(f"Client {client_address[0]}:{client_address[1]} username:{user['data'].decode('utf-8')} port:{port} the duration : {duration}")
                            break

                else:
                    # If the message is not False, broadcast it to all clients except the sender
                    for client_socket in clients:
                        if client_socket != notified_socket:
                            message = receive_message(notified_socket)
                            port = message["port"]
                            message_data = message["data"]
                            # Send a message to the client indicating which server it is connected to
                            client_socket.send(f"You are connected to server on port {port}\n".encode("utf-8"))
                            client_socket.send(message["header"] + message_data.encode("utf-8"))
                            
        #server_socket.close()


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