import asyncio
from bleak import BleakScanner, BleakClient

# UUID for the TX characteristic on Adafruit BLE UART service
# UART_TX_CHAR_UUID = "6E400001-B5A3-F393-­E0A9-­E50E24DCCA9E" 
RX_UUID = "6E400002-B5A3-F393-E0A9-E50E24DCCA9E"

TX_UUID = "6E400003-B5A3-F393-E0A9-E50E24DCCA9E"
# TX_UUID = "E439"

def handle_notification(sender, data):
    # print(f"Notification from {sender}: {data.decode()}")

    print(data.decode("utf-8"))
    print("\n")

async def main():
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

asyncio.run(main())
