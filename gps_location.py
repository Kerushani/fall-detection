import re
import threading
import time
from serial import Serial

port = "/dev/cu.usbmodem11201"
baudrate = 115200

_latest_raw_line = None
_reader_thread_started = False  

def _serial_reader():
    global _latest_raw_line
    try:
        with Serial(port=port, baudrate=baudrate, timeout=1) as port_serie:
            if port_serie.isOpen():
                port_serie.flush()
                print(f"Listening on {port}...")

                while True:
                    try:
                        line = port_serie.readline().decode('utf-8').strip()
                        if "Lat:" in line and "Lon:" in line:
                            _latest_raw_line = line
                            print(f"RAW {_latest_raw_line}")  # we don't need this line but prints out if needed
                    except Exception as e:
                        print(f"GPS Read error: {e}")
    except Exception as e:
        print(f"GPS Could not open serial port: {e}")

def start_gps_listener():
    global _reader_thread_started
    if not _reader_thread_started:
        threading.Thread(target=_serial_reader, daemon=True).start()
        _reader_thread_started = True

def findLocation():
# grab the google maps link
    if not _latest_raw_line:
        return None

    match = re.search(r"Lat:\s*([\d\.\-]+)\s+Lon:\s*([\d\.\-]+)", _latest_raw_line)
    if match:
        lat, lon = match.groups()
        return f"https://www.google.com/maps?q={lat},{lon}"
    return None

# run script itself
if __name__ == "__main__":
    start_gps_listener()
    print("from main... Listening for GPS... Ctrl+C to stop.")
    try:
        while True:
            location = findLocation()
            if location:
                print(location)
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nMain: Stopped by user.")
