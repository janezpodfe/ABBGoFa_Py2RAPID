import socket

ROBOT_IP = "192.168.125.1" 
PORT = 5000

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((ROBOT_IP, PORT))

print("Connected! Enter coordinates as [x,y,z] or 'q' to quit.")

try:
    while True:
        cmd = input("Target Offset (e.g. [50,0,10]): ")
        if cmd.lower() == 'q':
            # Tell the robot to stop before we shut down
            s.send("EXIT".encode())
            break
            
        s.send(cmd.encode())
        raw_data = s.recv(1024).decode()

        if "ERROR" in raw_data:
            print(f"!!! {raw_data}")
        else:
            # Split Cartesian and Joint data
            cartesian, joints = raw_data.split('|')
            print(f"\n--- Robot Status ---")
            print(f"Position (X,Y,Z): {cartesian}")
            print(f"Joints (1-6):     {joints}")
            print(f"--------------------\n")
finally:
    s.close()
    print("Connection closed.")