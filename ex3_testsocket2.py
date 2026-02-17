import socket
import threading
import time

# --- Configuration ---
ROBOT_IP = "192.168.125.1"  # Adjust to your GoFa's actual IP
CMD_PORT = 5000             # Matches T_ROB1
STREAM_PORT = 5001          # Matches T_BACK

def position_listener():
    print(f"[*] Starting Live Stream Listener on port {STREAM_PORT}...")
    while True:
        try:
            stream_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            # Short timeout to keep the script responsive
            stream_sock.settimeout(2.0) 
            stream_sock.connect((ROBOT_IP, STREAM_PORT))
            
            while True:
                try:
                    data = stream_sock.recv(1024).decode()
                    if not data:
                        break
                    print(f"\r[LIVE FEED] {data}                    ", end="", flush=True)
                except socket.timeout:
                    # Just a hiccup, keep trying to receive
                    continue
        except Exception:
            # If the robot isn't there, wait and try to reconnect
            time.sleep(1)
            continue
        finally:
            stream_sock.close()

def main_commander():
    """Main function to send move commands to T_ROB1."""
    print(f"[*] Connecting to Command Port {CMD_PORT}...")
    try:
        cmd_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        cmd_sock.connect((ROBOT_IP, CMD_PORT))
        
        print("\n--- GOFA COMMAND CONSOLE ---")
        print("Format: [x,y,z]  (e.g., [20,0,10])")
        print("Type 'q' to exit safely.")
        print("----------------------------\n")

        while True:
            user_input = input("\nEnter Offset: ")
            
            if user_input.lower() == 'q':
                cmd_sock.send("EXIT".encode())
                break
            
            # Send the coordinate string
            cmd_sock.send(user_input.encode())
            
            # Wait for the "ACK" or "ERROR" from the robot's main task
            response = cmd_sock.recv(1024).decode()
            print(f"\n[ROBOT RESPONSE] {response}")

    except Exception as e:
        print(f"[!] Command Error: {e}")
    finally:
        cmd_sock.close()
        print("[*] Command Connection Closed.")

if __name__ == "__main__":
    # # 1. Start the Background Listener Thread
    # listener_thread = threading.Thread(target=position_listener, daemon=True)
    # listener_thread.start()

    # 2. Run the Main Commander in the foreground
    main_commander()