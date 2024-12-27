import socket
import threading
import argparse
import time

import keyboard
from utils.time_based_queue import TimeBasedQueue
class Peer:
    def __init__(self, shared_queue, peer_name, listen_port, connect_port, connect_address='localhost'):
        self.peer_name = peer_name
        self.listen_port = listen_port
        self.connect_port = connect_port
        self.connect_address = connect_address
        
        self.shared_queue = shared_queue
        self.player_list = TimeBasedQueue(expiry_time=5)
        
        # this flag changed to true if the player accepts to play
        self.accept = False
        
    def broadcast_existence(self, broadcast_port=12345):
        broadcast_addr = "255.255.255.255"
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
            s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
            while True:
                msg = f"{self.peer_name} is here."
                s.sendto(msg.encode(), (broadcast_addr, broadcast_port))
                time.sleep(2)   # broadcast every 2 seconds
        
    def discover_exposed_host(self, listen_port=12345):
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
            s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            s.bind(("", listen_port))
            while True:
                message, address = s.recvfrom(1024)
                # print(f"Received: {message.decode()} from {address}")
                
                # take the player's name from the message
                player_name = message.decode().split(" ")[0]
                
                # put player's name and ip into the queue
                self.player_list.add((player_name, address[0]))     # hosts are deleted every 5 secs, so this func has to be run every 5 secs

    def discover_choose_players(self):
        # discover other hosts playing the game -> ask the user to choose one to connect
        discover_thread = threading.Thread(target=self.discover_exposed_host, daemon=True)
        discover_thread.start()
        while True:
            player_list = self.player_list.get_all()
            if not player_list:
                print("No player is found. Continue searching for players...")
                time.sleep(5)
                continue
            else:
                print(f"List of players found:")
                for idx, player in enumerate(self.player_list.get_all()):
                    print(f"{idx+1}: {player}")
                print(f"Choose a player to connect (1-{len(self.player_list.get_all())})")
                
                while True:
                    key = keyboard.read_event()
                    if (key.name in [str(i) for i in range(1, len(self.player_list.get_all())+1)]):
                        print(f"Player chosen: {key.name}")
                        player_idx = int(key.name) - 1
                        # discover_thread.join()
                        print(f"Player chosen: {self.player_list.get_at(player_idx)}")
                        return player_idx
                    else:
                        print("Continue searching for players...")
                        break
                time.sleep(5)
            
    def attempt_connecting(self, client_socket):
        n_attempts = 3
        player_idx = self.discover_choose_players()
        
        self.connect_address = self.player_list.get_at(player_idx)[1]   # idx 0 is the player's name, idx 1 is the player's ip
        
        # try to connect to the server after every 10 seconds
        for _ in range(n_attempts):
            try:
                client_socket.connect((self.connect_address, self.connect_port))
                print(f"Connecting to server at {self.connect_address}:{self.connect_port}")
                client_socket.send(self.peer_name.encode())
                return True
                break
            except ConnectionRefusedError:
                print("Connection refused. Retrying in 10 seconds...")
                time.sleep(10)
                continue
        print(f"Cannot connect to {self.connect_address} after {n_attempts} attempts")
        return False
        
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
                
                # ask the player if they want to play with the other player, if no, close the connection
                print(f"Do you want to play with {self.other_peer_name}? (y/n)")
                while True:
                    key = keyboard.read_event()
                    if (key.name == "y"):
                        self.accept = True
                        break
                    elif (key.name == "n"):
                        self.accept = False
                        break
                
                if (self.accept == False):
                    client_socket.send(f"{self.peer_name} has refused to play".encode())
                    client_socket.close()
                    print(f"Close the connection with {self.other_peer_name}")
                    continue
                else:
                    print(f"Connected with {client_address}, player's name: {self.other_peer_name}")
                    while True:
                        message = client_socket.recv(1024)
                        if (message):
                            if (message.decode() == "e"):
                                print(f"{self.other_peer_name} has left the game")
                                server_socket.close()
                                print(f"Server is closed")
                            print(f"message put in shared queue of {self.peer_name} by {self.other_peer_name}: {message.decode()}")
                            self.shared_queue.put(message.decode())
                        else: 
                            print(f"Received obj is not a message (empty?)")
                            break
                        
        except Exception as e:
            print(f"Error: {e}")
            server_socket.close()
            print("Server is closed")
                    
    def connect(self):
        # for sending data
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        
        # specify the address and port this peer uses to connect
        # source_address = ("localhost", self.connect_port)     # turned on when using 2 machines
        # client_socket.bind(source_address)  
        
        # put connecting attempt in a loop because the player chosen can be offline right after -> need to choose player again
        while not self.attempt_connecting(client_socket):
            print("Continue searching for players...")
            continue     
            
        try:
            while True:
                key_pressed = keyboard.read_event()
                if (key_pressed.name == "up"):
                    message = key_pressed.name
                    client_socket.send(message.encode())
                elif (key_pressed.name == "down"):
                    message = key_pressed.name
                    client_socket.send(message.encode())
                elif (key_pressed.name == "e"):
                    client_socket.send(message.encode())
                    client_socket.close()
                    print("Client is closed")
                    break
        except Exception as e:
            print(f"Error: {e}")
            client_socket.close()
            print("Client is closed")
            
    def run(self):
        listen_thread = threading.Thread(target=self.listen, daemon=True)
        connect_thread = threading.Thread(target=self.connect, daemon=True)
        # broadcast existence, despite is playing or not
        broadcast_thread = threading.Thread(target=self.broadcast_existence, daemon=True)
        
        listen_thread.start()
        connect_thread.start()
        broadcast_thread.start()
        
        listen_thread.join()
        connect_thread.join()
        broadcast_thread.join()
        
if __name__ == "__main__":
    argparser = argparse.ArgumentParser(description="Peer to peer connection")
    argparser.add_argument("--peer_name", type=str, default="peer", help="Name of the peer")
    argparser.add_argument("--listen_port", type=int, default=29999, help="Port number for listening")
    argparser.add_argument("--connect_port", type=int, default=29998, help="Port number for connecting")
    
    # the connect address has to be founded (later)
    argparser.add_argument("--connect_address", type=str, default="localhost", help="Address for connecting")
    
    args = argparser.parse_args()
    
    peer = Peer(args.peer_name, args.listen_port, args.connect_port, args.connect_address)
    peer.run()