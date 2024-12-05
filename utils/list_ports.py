import psutil

def get_listening_ports():
    """List all ports that the machine is actively listening to."""
    listening_ports = []
    for connection in psutil.net_connections(kind="inet"):
        if connection.status == psutil.CONN_LISTEN:
            listening_ports.append((connection.laddr.ip, connection.laddr.port))
    return listening_ports

if __name__ == "__main__":
    print("Listening Ports:")
    ports = get_listening_ports()
    for ip, port in ports:
        print(f"IP: {ip}, Port: {port}")