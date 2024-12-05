import socket

import sys
import os
# caution: path[0] is reserved for script path (or '' in REPL)
# sys.path.append(os.getcwd())

import threading
import multiprocessing
import queue

sys.path.insert(5, 'D:\\projects\\uni_projects\\Pingpong_Online')
print(sys.path)

from game_proto import pingpong

class Server:
    def __init__(self,share_queue, port_number=29999):
        self.port_number = port_number
        self.share_queue = share_queue
    
    def run(self):
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print(f"Server is running on port {self.port_number}")
        server_socket.bind(("localhost", self.port_number))
        
        # listen to only 1 connection
        server_socket.listen(1)
        
        # reuse the address (ip + port) in case that address is already in use
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        try:
            while True:
                client_socket, client_address = server_socket.accept()
                print(f"Connection from {client_address}")
                
                while True:
                    data = client_socket.recv(1024)
                    print(f"Received data: {data.decode()}")
                    
                    self.share_queue.put(data.decode())
                    # message = input("Enter message: ")
                    # client_socket.send(message.encode())
                
        except KeyboardInterrupt:
            server_socket.close()
            print("Server is closed")
        except Exception as e:
            print(f"Error: {e}")
            server_socket.close()
            print("Server is closed")
            
if __name__ == "__main__":
    share_queue = queue.Queue()
    
    def run_server():
        server = Server(share_queue)
        server.run()
        
    def run_game():
        game = pingpong.GameEngine(share_queue)
        game.run()
        
    '''Multi-threading'''
    server_thread = threading.Thread(target=run_server, daemon=True)
    game_thread = threading.Thread(target=run_game, daemon=True)

    # Start both threads
    server_thread.start()
    game_thread.start()

    # Wait for the threads to complete (if necessary)
    server_thread.join()
    game_thread.join()
    
    # '''Multi-processing'''
    # server_process = multiprocessing.Process(target=server.run)
    # game_process = multiprocessing.Process(target=game.run)
    
    # server_process.start()
    # game_process.start()
    
    # server_process.join()
    # game_process.join()