from game_proto.pingpong_client_server import GameEngine
from connect.peer_game import Peer
import threading
import queue

if __name__ == "__main__":
    shared_queue = queue.Queue()
    
    def run_game():
        game = GameEngine(shared_queue)
        game.run()
    
    def run_peer():
        peer = Peer(shared_queue)
        peer.run()
        
    game_thread = threading.Thread(target=run_game, daemon=True)
    peer_thread = threading.Thread(target=run_peer, daemon=True)
    
    game_thread.start()
    peer_thread.start()
    
    game_thread.join()
    peer_thread.join()