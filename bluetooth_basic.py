import asyncio
from bleak import BleakScanner, BleakClient
import pandas as pd
import re


# UUID for the TX characteristic on Adafruit BLE UART service
# UART_TX_CHAR_UUID = "6E400001-B5A3-F393-­E0A9-­E50E24DCCA9E" 
RX_UUID = "6E400002-B5A3-F393-E0A9-E50E24DCCA9E"

TX_UUID = "6E400003-B5A3-F393-E0A9-E50E24DCCA9E"
# TX_UUID = "E439"

df = pd.DataFrame(columns=["xa", "ya", "za", "xg", "yg", "zg","bs"])
buffer = ""
callback = None  # Optional callback to send processed rows


# def handle_notification(sender, data):
#     # print(data.decode("utf-8"))
#     # print("\n break teehe")

#     global df, buffer

#     try:
#         decoded = data.decode("utf-8").strip()
#         buffer += decoded  # Keep adding to the buffer
#         print(f"Buffer: {buffer}")

#         # Check if we have all six values
#         matches = re.findall(r"(-?\d*\.?\d+)(?:([xyz][ag])|(bs))", buffer)

#         found_keys = {k for _, k in matches}
#         required_keys = {"xa", "ya", "za" ,"xg", "yg", "zg","bs"}

#         if required_keys.issubset(found_keys):
#             # Create dict from matches (will take the latest value for each key)
#             data_dict = {k: float(v) for v, k in matches if k in required_keys}

#             # Append to DataFrame
#             df.loc[len(df)] = {col: data_dict.get(col) for col in df.columns}
#             print(df.tail())

#             # Reset buffer to everything **after** the last match
#             # Find position of last axis match
#             last_match = list(re.finditer(r"(-?\d*\.?\d+)(?:([xyz][ag])|(bs))", buffer))[-1]
#             buffer = buffer[last_match.end():]  # keep what's leftover
#             print(df.head())

#     except Exception as e:
#         print(f"Error: {e}")


## <3 <3



def handle_notification(sender, data):
    global df, buffer

    try:
        decoded = data.decode("utf-8").strip()
        buffer += decoded
        #print(f"Buffer: {buffer}")

        # Keep looking for complete frames that start with '#'
        while "#" in buffer:
            start = buffer.find("#")
            next_start = buffer.find("#", start + 1)

            if next_start != -1:
                frame = buffer[start + 1:next_start]
                buffer = buffer[next_start:]  # trim fully
            else:
                # Maybe a complete final frame with no trailing #
                frame = buffer[start + 1:]

                # Attempt to parse, but don't trim unless it's good
                matches = re.findall(r"([xyz][ag]|bs)(-?\d*\.?\d+)", frame)
                keys = {k for k, _ in matches}
                if {"xa", "ya", "za", "xg", "yg", "zg", "bs"}.issubset(keys):
                    data_dict = {k: float(v) for k, v in matches}
                    df.loc[len(df)] = {col: data_dict.get(col) for col in df.columns}
                    print(df.tail())
                    buffer = ""  # Clear after full parse
                break  # Wait for more data

            # Parse normal frame if we had two #s
            matches = re.findall(r"([xyz][ag]|bs)(-?\d*\.?\d+)", frame)
            keys = {k for k, _ in matches}
            if {"xa", "ya", "za", "xg", "yg", "zg", "bs"}.issubset(keys):
                data_dict = {k: float(v) for k, v in matches}
                df.loc[len(df)] = {col: data_dict.get(col) for col in df.columns}
                print(df.tail())

    except Exception as e:
        print(f"Error: {e}")


async def main_ble():
    print("Scanning for sense_feather...")
    devices = await BleakScanner.discover(timeout=10)
    for d in devices:
        print(f"Found: {d.name} - {d.address}")
        if d.name and "sense_feather" in d.name:
            feather = d
            print("found sense!")
            break
    
    async with BleakClient(feather.address) as client:
        print(f"Connected to {feather.name}")
        
        for i in range(100):
            i = i+1 #this is neded or else it will work 50% of time - it's a cursed delay 
        # Subscribe to notifications from the TX characteristic
        print("at client")
        await client.start_notify(TX_UUID, handle_notification)
        print("Subscribed to notifications. Waiting...")

        # Wait for notifications for 60 seconds
        try: 
            while True:
                await asyncio.sleep(1)
        except KeyboardInterrupt:
            await client.stop_notify(TX_UUID)
            print ("Stopped")

asyncio.run(main_ble())


