import sys
import signal
import socket

NUM_TRANSMISSIONS = 10
if len(sys.argv) < 2:
    print("Usage: python3 " + sys.argv[0] + " server_port")
    sys.exit(1)
assert len(sys.argv) == 2
server_port = int(sys.argv[1])

# TODO: Create a socket for the server
server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Function to check if a number is prime
def is_prime(n):
    if n <= 1:
        return False
    for i in range(2, int(n**0.5) + 1):
        if n % i == 0:
         return False
    return True

# Setup signal handler to exit gracefully
def cleanup(sig, frame):
    # TODO Close server's socket
    print("Shutting down server...")
    server_socket.close()
    sys.exit(0)

# SIGINT is sent when you press ctrl + C, SIGTERM if you use 'kill' or leave the shell
signal.signal(signal.SIGINT, cleanup)
signal.signal(signal.SIGTERM, cleanup)


# TODO: Bind it to server_port
server_socket.bind(('', server_port))
print(f"Server listening on port {server_port}")

while True:
    pass
    # TODO: Receive RPC request from client
    data, client_address = server_socket.recvfrom(1024)
    rpc_data = data.decode()

    # TODO: Turn byte array that you received from client into a string variable called rpc_data
    try:
        _, number_str = rpc_data.split('(')
        number = int(number_str[:-1])  # Remove the closing parenthesis and convert to int
        print(f"Received prime check request for: {number}")
    except ValueError as e:
        print("Error parsing request:", e)
        continue

    # TODO: Parse rpc_data to get the argument to the RPC.
    # Remember that the RPC request string is of the form prime(NUMBER)

    # TODO: Print out the argument for debugging

    # TODO: Compute if the number is prime (return a 'yes' or a 'no' string)
    result = "yes" if is_prime(number) else "no"

    # TODO: Send the result of primality check back to the client who sent the RPC request
    server_socket.sendto(result.encode(), client_address)
    print(f"Sent '{result}' to {client_address}")

# TODO: Close server's socket
    server_socket.close()