import subprocess

def monitor_network(interface="Wi-Fi"):
    # Use raw string format for Windows path
    tshark_path = "C:/Program Files/Wireshark/tshark.exe"

    print(f"📡 Monitoring network traffic on interface: {interface}")
    
    try:
        # Run TShark with correct parameters
        process = subprocess.Popen(
            [tshark_path, "-i", interface, "-Y", "tor OR http OR https", "-T", "fields", "-e", "ip.src", "-e", "ip.dst"],
            stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True
        )

        print("🟢 Listening for Tor traffic and suspicious patterns... Press Ctrl+C to stop.")
        
        # Read the output line by line
        for line in process.stdout:
            print(line.strip())

    except FileNotFoundError:
        print(f"❌ Error: TShark not found at {tshark_path}. Check your installation.")
    except Exception as e:
        print(f"❌ Unexpected error: {e}")

# Example Usage
monitor_network("Wi-Fi")
