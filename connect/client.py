import socket
import pygame

class Client:
    def __init__(self, port_number=29998, server_address="localhost", server_port=29999):
        self.port_number = port_number
        self.server_address = server_address
        self.server_port = server_port
    
    def run(self):
        pygame.init()
        pygame.display.set_mode((100, 100))
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.bind(("localhost", self.port_number))
        client_socket.connect((self.server_address, self.server_port))
        print(f"Enter data:")
        try:
            while True:
                for event in pygame.event.get():
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_UP:
                            print("UP")
                            client_socket.send("UP".encode())
                        if event.key == pygame.K_DOWN:
                            print("Down")
                            client_socket.send("DOWN".encode())
                # response = client_socket.recv(1024)
                # print(f"Received: {response.decode()}")
                
        except KeyboardInterrupt:
            client_socket.close()
            print("Client is closed")
        except Exception as e:
            print(f"Error: {e}")
            client_socket.close()
            print("Client is closed")
            
if __name__ == "__main__":
    client = Client()
    client.run()