import sys
import select
from socket import *

import builtins

# Redefine print for autograder -- do not modify
def print(*args, **kwargs):
    builtins.print(*args, **kwargs, flush=True)

bad_words = ["virus", "worm", "malware"]
good_words = ["groot", "hulk", "ironman"]

def replace_bad_words(s):
    for j in range(3):
        s = s.replace(bad_words[j], good_words[j])
    return s

if len(sys.argv) != 2:
    print("Usage: python3 " + sys.argv[0] + " port")
    sys.exit(1)
port = int(sys.argv[1])

# Create a TCP socket to listen on port for new connections
listener_socket = socket(AF_INET, SOCK_STREAM)
listener_socket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)

# Bind the server's socket to port
listener_socket.bind(('', port))

# Put listener_socket in LISTEN mode
listener_socket.listen(5)
print(f"Listening on port {port}")

# Accept a connection first from two clients
# OR 
# implement accepting connections from multiple clients
# by including listener_socket in event handling 
sockets_list = [listener_socket]
clients = {}

def broadcast(message, sender_socket):
    for socket in clients:
        if socket != sender_socket:
            try:
                socket.send(message.encode())
            except:
                socket.close()
                sockets_list.remove(socket)
                del clients[socket]


active = True

while active:
    pass
    # Use select to see which socket is available to read from
    read_sockets, _, exception_sockets = select.select(sockets_list, [], sockets_list)

    # recv on socket that is ready to read

    # Check to see if connection is closed

    # Filter and replace bad words

    # Forward to other sockets
    for notified_socket in read_sockets:
        if notified_socket == listener_socket:
            client_socket, client_address = listener_socket.accept()
            sockets_list.append(client_socket)
            clients[client_socket] = client_address
            print(f"Accepted new connection from {client_address[0]}:{client_address[1]}")
        else:
            try:
                message = notified_socket.recv(1024).decode()
                if message:
                    message = replace_bad_words(message)
                    broadcast(message, notified_socket)
                else:
                    sockets_list.remove(notified_socket)
                    del clients[notified_socket]
            except Exception as e:
                print(f"Error: {e}")
                sockets_list.remove(notified_socket)
                del clients[notified_socket]
                continue

    for notified_socket in exception_sockets:
        sockets_list.remove(notified_socket)
        del clients[notified_socket]

# Close sockets
for socket in sockets_list:
    socket.close()