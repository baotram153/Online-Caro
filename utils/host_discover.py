import socket
from scapy.all import ARP, Ether, srp

def discover_devices_on_lan():
    """Discover devices on the LAN using ARP."""
    devices = []
    # Get the local IP and subnet
    local_ip = socket.gethostbyname(socket.gethostname())
    subnet = '.'.join(local_ip.split('.')[:-1]) + '.1/24'
    
    print(f"Scanning LAN for devices on subnet: {subnet}")
    
    # Create an ARP request packet
    arp = ARP(pdst=subnet)
    ether = Ether(dst="ff:ff:ff:ff:ff:ff")
    packet = ether / arp
    
    # Send the packet and capture the responses
    result = srp(packet, timeout=2, verbose=0)[0]
    
    for sent, received in result:
        devices.append({'ip': received.psrc, 'mac': received.hwsrc})
    
    return devices

def connect_to_device(ip, port=22, timeout=5):
    """Try to connect to a device on a specific port."""
    try:
        print(f"Attempting to connect to {ip}:{port}")
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.settimeout(timeout)
        client_socket.connect((ip, port))
        print(f"Connected to server at {ip}:{port}")
        
        data = "Hello, server!"
        client_socket.send(data.encode())
        
        response = client_socket.recv(1024).decode()
        print(f'Server says: {response}')
        
        client_socket.close()
            
    # return True
    except (socket.timeout, ConnectionRefusedError):
        print(f"Failed to connect to {ip}:{port}")
        return False
    except KeyboardInterrupt:
        print("User interrupted the program.")
        return False

if __name__ == "__main__":
    print("Discovering devices on the LAN...")
    devices = discover_devices_on_lan()
    
    if devices:
        print("\nDiscovered devices:")
        for i, device in enumerate(devices, 1):
            print(f"{i}. IP: {device['ip']}, MAC: {device['mac']}")
    else:
        print("No devices found.")
    
    # Example: Attempt to connect to devices on port 22 (SSH)
    for device in devices:
        connect_to_device(device['ip'], port=29999, timeout=10)
