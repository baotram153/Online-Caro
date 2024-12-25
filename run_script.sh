# cd "D:\Bachelor\Projects\uni_projects\Pingpong_Online"
./env/Scripts/activate
python connect/peer_game.py --peer_name=peer1 --listen_port=29999 --connect_port=29998
python connect/peer_game.py --peer_name=peer2 --listen_port=29998 --connect_port=29999