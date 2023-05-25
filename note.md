
## https://www.youtube.com/watch?v=t331lKVrJ00&ab_channel=Linode

## https://www.youtube.com/watch?v=CV7_stUWvBQ&ab_channel=sentdex

## https://www.digitalocean.com/community/tutorials/python-socket-programming-server-client

## https://docs.python.org/3/howto/sockets.html

## https://gist.github.com/berendiwema/1816201


## https://cppsecrets.com/users/136289711011711297109979711510511010310449545464103109971051084699111109/Python-Multiprocessing-Listeners-and-Clients.php


explanation

<p>

```python
# create an INET, STREAMing socket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# now connect to the web server on port 80 - the normal http port
s.connect(("www.python.org", 80))
```
This is a code snippet in Python that creates a socket object `s` using the `socket` module. The `socket.AF_INET` parameter specifies that this is an IPv4 socket, and `socket.SOCK_STREAM` specifies that it will use the TCP protocol for reliable, ordered communication. 

The next line of code uses the `connect()` method to establish a connection to the web server running on the "www.python.org" domain, on port 80. Port 80 is the default port used for HTTP traffic, so this connection is likely intended for a web request. 

Overall, this code creates a TCP socket and connects it to the Python.org web server, allowing for further communication between the client and server.

<p>

<p>
What happens in the web server is a bit more complex. First, the web server creates a “server socket”:

```python
# create an INET, STREAMing socket
serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# bind the socket to a public host, and a well-known port
serversocket.bind((socket.gethostname(), 80))
# become a server socket
serversocket.listen(5)
```

<p>

<p>

```python
while True:
    # accept connections from outside
    (clientsocket, address) = serversocket.accept()
    # now do something with the clientsocket
    # in this case, we'll pretend this is a threaded server
    ct = client_thread(clientsocket)
    ct.run()
```

This is a code snippet in Python that implements a simple multi-threaded server that listens for incoming connections from clients using the `serversocket` object created in the previous code snippet.

The code is wrapped in an infinite loop using `while True`, which means that the server will continuously listen for incoming connections until it is stopped. 

The `accept()` method is used to accept incoming connections from clients. When a connection is accepted, the method returns a tuple containing a new socket object `clientsocket` that represents the connection to the client, and the remote `address` of the client.

The next line of code creates a new thread to handle the incoming client connection using the `client_thread` class. This allows the server to handle multiple client connections simultaneously. 

Finally, the `run()` method of the `client_thread` object is called to start the new thread and handle the client connection.

Overall, this code implements a multi-threaded server that listens for incoming connections from clients and handles them in separate threads, allowing the server to handle multiple connections simultaneously.
<p>

