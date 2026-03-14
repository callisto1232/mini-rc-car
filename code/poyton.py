import socket
import subprocess
import time
import sys

# Configuration
ESP32_IP = "192.168.1.100"
PORT = 4210
TARGET_SSID = "Fox-17"

def get_current_ssid():
    try:
        if sys.platform.startswith("linux"):
            # Modern Linux: uses nmcli
            cmd = ["nmcli", "-t", "-f", "active,ssid", "dev", "wifi"]
            result = subprocess.check_output(cmd).decode('utf-8')
            # nmcli output looks like: "yes:LAGARIMEDYA\nno:OtherSSID"
            for line in result.split('\n'):
                if line.startswith("yes:"):
                    return line.split(":")[1].strip()
                    
        elif sys.platform == "darwin":
            # macOS: uses networksetup
            cmd = ["networksetup", "-getairportnetwork", "en0"]
            result = subprocess.check_output(cmd).decode('utf-8')
            return result.split(": ")[-1].strip()
    except Exception as e:
        print(f"Error detecting SSID: {e}")
    return None

def send_data():
    current_ssid = get_current_ssid()
    
    if current_ssid != TARGET_SSID:
        print(f"❌ Error: Connected to '{current_ssid}', but need '{TARGET_SSID}'")
        # During testing, you can comment the 'return' out if you are on Ethernet
        return

    print(f"✅ Verified: Connected to {TARGET_SSID}")
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    
    try:
        while True:
            # Placeholder for Gamepad data
            message = "F255" 
            sock.sendto(message.encode(), (ESP32_IP, PORT))
            time.sleep(0.02) # 50Hz
            
    except KeyboardInterrupt:
        print("\nStopping...")
    finally:
        sock.close()

if __name__ == "__main__":
    send_data()
