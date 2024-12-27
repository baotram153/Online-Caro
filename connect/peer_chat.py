import socket
import threading
import argparse
import time

class Peer:
    def __init__(self, peer_name, listen_port, connect_port, connect_address):
        self.peer_name = peer_name
        self.listen_port = listen_port
        self.connect_port = connect_port
        self.connect_address = connect_address
    
        
    def listen(self):
        # for receiving data
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print(f"Server is running on port {self.listen_port}")
        server_socket.bind(("localhost", self.listen_port))
        
        # listen to only 1 connection
        server_socket.listen(1)
        
        # reuse the address (ip + port) in case that address is already in use
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        
        try:
            while True:
                client_socket, client_address = server_socket.accept()
                self.other_peer_name = client_socket.recv(1024).decode()
                print(f"Connection from {client_address}, name: {self.other_peer_name}")
                while True:
                    message = client_socket.recv(1024)
                    if (message):
                        if (message.decode() == "\exit"):
                            print(f"{self.other_peer_name} has left the chat")
                            server_socket.close()
                            print(f"Server is closed")
                        print(f"{self.other_peer_name}: {message.decode()}")
                    else: 
                        break
        except Exception as e:
            print(f"Error: {e}")
            server_socket.close()
            print("Server is closed")
                    
    def connect(self):
        # for sending data
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        while True:
            # try to connect to the server after every 10 seconds
            try:
                client_socket.connect((self.connect_address, self.connect_port))
                print(f"Connected to server at {self.connect_address}:{self.connect_port}")
                client_socket.send(self.peer_name.encode())
                break
            except ConnectionRefusedError:
                print("Connection refused. Retrying in 10 seconds...")
                time.sleep(10)
                continue
        try:
            while True:
                message = input()
                if (message == "\exit"):
                    client_socket.send(message.encode())
                    client_socket.close()
                    print("Client is closed")
                    break
                else:
                    client_socket.send(message.encode())
        except Exception as e:
            print(f"Error: {e}")
            client_socket.close()
            print("Client is closed")
            
    def run(self):
        listen_thread = threading.Thread(target=self.listen, daemon=True)
        connect_thread = threading.Thread(target=self.connect, daemon=True)
        
        listen_thread.start()
        connect_thread.start()
        
        listen_thread.join()
        connect_thread.join()
        
if __name__ == "__main__":
    argparser = argparse.ArgumentParser(description="Peer to peer connection")
    argparser.add_argument("--peer_name", type=str, default="peer", help="Name of the peer")
    argparser.add_argument("--listen_port", type=int, default=29998, help="Port number for listening")
    argparser.add_argument("--connect_port", type=int, default=29999, help="Port number for connecting")
    argparser.add_argument("--connect_address", type=str, default="localhost", help="Address for connecting")
    
    args = argparser.parse_args()
    
    peer = Peer(args.peer_name, args.listen_port, args.connect_port, args.connect_address)
    peer.run()