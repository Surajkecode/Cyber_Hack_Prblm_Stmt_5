import subprocess
import re
import sys

def extract_metadata(file_path):
    exiftool_path = r"E:/Project_CyberHack/exiftool-13.18_64/exiftool-13.18_64/exiftool.exe"
    command = [exiftool_path, file_path]
    
    result = subprocess.run(command, capture_output=True, text=True)
    metadata = result.stdout

    print(f"📸 Metadata for: {file_path}")
    print(metadata)

    # Extract GPS coordinates
    gps_info = re.findall(r"GPS Position/s*:/s*([/d.]+)/s*([NS]),/s*([/d.]+)/s*([EW])", metadata)
    if gps_info:
        lat, lat_dir, lon, lon_dir = gps_info[0]
        latitude = f"{lat} {lat_dir}"
        longitude = f"{lon} {lon_dir}"
        print("🌍 GPS Location:", latitude, longitude)
    else:
        print("❌ GPS data not found.")

# Run only if file argument is provided
if __name__ == "__main__":
    if len(sys.argv) > 1:
        extract_metadata(sys.argv[1])
    else:
        print("❌ No file provided! Usage: python metadata.py <file_path>")
