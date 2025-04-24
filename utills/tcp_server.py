import socket

# UE's IP address (replace with actual IP from UERANSIM)
host = "0.0.0.0"  # Listen on all interfaces
port = 8080       # TCP port

# Create a TCP socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_socket.bind((host, port))
server_socket.listen(5)

print(f"Listening on {host}:{port}...")

while True:
    client_socket, client_address = server_socket.accept()
    print(f"Connection from {client_address}")
    data = client_socket.recv(1024).decode()
    print(f"Received: {data}")
    client_socket.send(b"Hello from UE!\n")
    client_socket.close()