import errno
import socket
import sys
import select


HEADERSIZE = 64

IP = "127.0.0.1"
PORTS = [8000, 8001, 8002, 8003, 8004]

my_username = input("Username : ")
#client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
#client_socket.connect((IP, PORT))
#print(f"Connected to server at {IP}:{PORT}")
#client_socket.setblocking(False)

client_sockets = []
for port in PORTS:
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((IP, port))
    client_socket.setblocking(False)
    client_sockets.append(client_socket)

username = my_username.encode("utf-8")
username_header = f"{len(username):<{HEADERSIZE}}".encode("utf-8")
client_socket.send(username_header + username)

while True:
    sockets_list = [client_socket]

    read_sockets, write_socket, error_socket = select.select(sockets_list, [], [])

    for socks in read_sockets:
        if socks == client_socket:
            message_header = client_socket.recv(HEADERSIZE)
            if not len(message_header):
                print("Connection closed by the server")
                sys.exit()
            try:
                message_length = int(message_header.decode("utf-8").strip())
                message = client_socket.recv(message_length).decode("utf-8")
                print(message)
            except ValueError:
                message = message_header.decode("utf-8").strip()
                print(message)

            #message = client_socket.recv(message_length).decode("utf-8")
            #print(message)
        else:
            message = input(f"{my_username} > ")
            if message:
                message = message.encode("utf-8")
                message_header = f"{len(message):<{HEADERSIZE}}".encode("utf-8")
                client_socket.send(message_header + message)
    
