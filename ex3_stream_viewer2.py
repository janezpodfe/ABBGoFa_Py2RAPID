import socket
import csv
import datetime
import time

# --- Configuration ---
ROBOT_IP = "192.168.125.1"
STREAM_PORT = 5001
LOG_FILE = "robot_telemetry_log.csv"

def start_logging():
    print("--- GOFA LIVE TELEMETRY & LOGGING ---")
    print(f"[*] Target: {ROBOT_IP}:{STREAM_PORT}")
    
    while True:
        try:
            # Create socket with a timeout
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(5.0) 
            
            print(f"[*] Attempting to connect...")
            s.connect((ROBOT_IP, STREAM_PORT))
            print("[+] Connected! Streaming data...")

            with open(LOG_FILE, mode='a', newline='') as file:
                writer = csv.writer(file)
                # Write header if file is empty
                if file.tell() == 0:
                    writer.writerow(["Timestamp", "X", "Y", "Z", "J1", "J2", "J3", "J4", "J5", "J6"])

                while True:
                    data = s.recv(1024).decode().strip()
                    if not data:
                        print("\n[!] Robot closed connection.")
                        break
                    
                    # Print to console
                    print(f"\r[LIVE] {data}                                ", end="", flush=True)
                    
                    # Parse and Log
                    timestamp = datetime.datetime.now().strftime("%H:%M:%S.%f")[:-3]
                    if '|' in data:
                        cart, jnt = data.split('|')
                        writer.writerow([timestamp] + cart.split(',') + jnt.split(','))
                        file.flush() # Forces data to be saved immediately

        except (socket.timeout, ConnectionRefusedError, socket.error) as e:
            print(f"[!] Connection failed: {e}. Retrying in 2s...")
            time.sleep(2)
        except KeyboardInterrupt:
            print("\n[*] Stopping logger at user request.")
            break
        finally:
            s.close()

if __name__ == "__main__":
    start_logging()