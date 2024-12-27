# from game_proto.pingpong_client_server import GameEngine
from game_proto.pingpong_peer import GameEngine
from connect.peer_game import Peer
import threading
import queue
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("--listen_port", default=29999, type=int, help="Port to listen")
parser.add_argument("--connect_port", default=29998, type=int, help="Port to connect")
parser.add_argument("--peer_name", type=str, help="Name of player")
args = parser.parse_args()

if __name__ == "__main__":
    shared_queue = queue.Queue()
    
    def run_game():
        game = GameEngine(shared_queue)
        game.run()
    
    def run_peer():
        peer = Peer(shared_queue, args.peer_name, args.listen_port, args.connect_port)
        peer.run()
        
    game_thread = threading.Thread(target=run_game, daemon=True)
    peer_thread = threading.Thread(target=run_peer, daemon=True)
    
    game_thread.start()
    peer_thread.start()
    
    game_thread.join()
    peer_thread.join()