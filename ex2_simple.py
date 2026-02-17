import socket
import threading
import time

# Function to handle the high-speed background stream
def position_listener():
    stream_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    stream_sock.connect(("192.168.125.1", 5001))
    while True:
        try:
            data = stream_sock.recv(1024).decode()
            if data:
                print(f"\r[LIVE POS] {data}", end="")
        except:
            break

# Start the listener in a separate thread
listener_thread = threading.Thread(target=position_listener, daemon=True)
listener_thread.start()

# Main logic for sending commands (Port 5000)
cmd_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
cmd_sock.connect(("192.168.125.1", 5000))

try:
    while True:
        offset = input("\nMove Offset [x,y,z]: ")
        cmd_sock.send(offset.encode())
        # The main thread just sends commands; the background thread shows pos
        time.sleep(1) 
finally:
    cmd_sock.close()