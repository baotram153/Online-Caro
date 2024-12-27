import socket 
import time
import threading

'''
Can discover other hosts in LAN who are broadcasting their existence.
'''

def broadcast(port=12345):
    broadcast_addr = "255.255.255.255"
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
        # socket.SOL_SOCKET: socket level option
        # socket.SO_BROADCAST: socket option to allow broadcasting
        s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        while True:
            # s.sendto(b"Hello, broadcast world!", ('<broadcast>', port))
            s.sendto(b"Hello, broadcast world!", (broadcast_addr, port))
            time.sleep(2)   # broadcast every 2 seconds
        
        
def listen(port=12345):
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
        # bind the socket to a specific port so that the socket can listen to that port
        # "" means listen to all available interfaces
        s.bind(("", port))
        while True:
            message, address = s.recvfrom(1024)
            print(f"Received: {message.decode()} from {address}")

if (__name__ == "__main__"):
    # create 2 threads: one for broadcasting and one for listening
    broadcast_thread = threading.Thread(target=broadcast)
    listen_thread = threading.Thread(target=listen)
    
    broadcast_thread.start()
    listen_thread.start()
    
    broadcast_thread.join()
    listen_thread.join()