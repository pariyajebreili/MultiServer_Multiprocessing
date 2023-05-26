import socket
import time
import pickle
import select


HEADERSIZE = 10
IP = "127.0.0.1"
PORT = 1234

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

server_socket.bind((IP,PORT))

server_socket.listen(5)

sockets_list = [server_socket]

clients = {}

# Flag to keep track of whether a client is connected or not
client_connected = False


def receive_message(client_socket):
    try:
        message_header = client_socket.recv(HEADERSIZE)
        
        if not len(message_header):
            return False
        
        message_length = int(message_header.decode("utf-8").strip())
        return {"header":message_header,"data":client_socket.recv(message_length)}
    


    except:
        return False


while True:
    read_sockets, _, exception_sockets = select.select(sockets_list, [], sockets_list)
    for notified_socket in read_sockets : 
        if notified_socket== server_socket:
            if not client_connected:
                client_socket, client_address = server_socket.accept()

                user = receive_message(client_socket)

                if user is False :
                    continue
                sockets_list.append(client_socket)

                clients[client_socket] = user
                print(f"Accepted new connection from {client_address[0]}:{client_address[1]} username:{user['data'].decode('utf-8')}")

                # Set client_connected flag to True
                client_connected = True
            else:    
                # If a client is already connected, reject new connections
                client_socket, client_address = server_socket.accept()
                client_socket.send("Another client is already connected. Please try again later.".encode("utf-8"))
                client_socket.close()

        else:
            message = receive_message(notified_socket)

            if message is False :
                print(f"closed connection from {clients[notified_socket]['data'].decode('utf-8')}")
                sockets_list.remove(notified_socket)
                del clients[notified_socket]

                # Set client_connected flag to False
                client_connected = False
                continue
            user = clients[notified_socket]
            

            print(f"Receives message from {user['data'].decode('utf-8')}:{message['data'].decode('utf-8')}")

            for client_socket in clients :
                if client_socket != notified_socket:
                    client_socket.send(user['header']+user['data']+message['header']+message['data'])

    for notified_socket in exception_sockets :
        sockets_list.remove(notified_socket)
        del clients[notified_socket]

        # Set client_connected flag to False
        client_connected = False