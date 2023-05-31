import errno
import socket
import sys
import select
import time


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



def receive_message(client_socket):
    """
    Receive a message from the server and display the message data and the port it was received on.
    """

    message_header = b''
    while len(message_header) < HEADERSIZE:
        try:
            chunk = client_socket.recv(HEADERSIZE - len(message_header))
            if not chunk:
                return None
            message_header += chunk
        except BlockingIOError:
            # If there is no data available to read, wait for a short time before trying again
            time.sleep(0.1)

    message_length = int(message_header.decode("utf-8").strip())

    message_data = b''
    while len(message_data) < message_length:
        try:
            chunk = client_socket.recv(message_length - len(message_data))
            if not chunk:
                return None
            message_data += chunk
        except BlockingIOError:
            # If there isno data available to read, wait for a short time before trying again
            time.sleep(0.1)

    message_data = message_data.decode("utf-8")

    port = message_data.split(":")[0]
    data = message_data.split(":")[1]

    print(f"Received message from server on port {port}: {data}")

    return {
        "port": port,
        "data": data,
        "header": message_header
    }


while True:
    sockets_list = [client_socket]

    #read_sockets, write_socket, error_socket = select.select(sockets_list, [], [], 5.0)
    
    for socks in sockets_list:
        receive_message(socks)
        message = input(f"{my_username} > ")
        if message:
            message = message.encode("utf-8")
            message_header = f"{len(message):<{HEADERSIZE}}".encode("utf-8")
            client_socket.send(message_header + message)


#while True:
#    # Call the receive_message() function to receive messages from all client sockets
#    receive_message(client_sockets)

#    # Send a message to all client sockets
#    message = input(f"{my_username} > ")
#    if message:
#        for client_socket in client_sockets:
#            send_message_to_server(client_socket, message)