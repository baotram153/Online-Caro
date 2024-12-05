import socket

def start_server(port=8080):
    try:    
        local_ip = socket.gethostbyname(socket.gethostname())
        host = "0.0.0.0"
        """Start a server that listens on the specified host and port."""
        # Create a socket (IPv4, TCP)
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        
        # # Reuse the socket address (avoid "Address already in use" error)
        # server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        
        # Bind the socket to the specified address and port
        server_socket.bind((host, port))
        print(f"Server is listening on {host}:{port}...")
        
        # Start listening for incoming connections
        server_socket.listen(5)  # Allow up to 5 pending connections
        while True:
            # Accept a connection
            client_socket, client_address = server_socket.accept()
            print(f"Connection established with {client_address}")
            
            # Receive data from the client
            data = client_socket.recv(1024).decode()
            print(f"Received: {data}")
            
            # Send a response back to the client
            response = "Acknowledged\n"
            client_socket.sendall(response.encode())
            
            # Close the client connection
            # client_socket.close()
            # print("Connection closed.")
    
    except KeyboardInterrupt:
        print("Server shutting down.")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        server_socket.close()

if __name__ == "__main__":
    # Start the server on port 8080
    start_server(port=29999)
