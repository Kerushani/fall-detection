# from twilio.rest import Client
# from gps_location import start_gps_listener, findLocation
# import time


# def send_fall_alert():
#     """
#     Sends an SMS alert to the emergency contact using Twilio.
#     """
#     client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
#     message_body = f"ALERT: A fall has been detected. {EMERGENCY_CONTACT['name']} please check on {NECKLACE_WEARER} immediately. ->{LOCATION}"
#     try:
#         message = client.messages.create(
#             body=message_body,
#             from_=TWILIO_FROM_NUMBER,
#             to=EMERGENCY_CONTACT["number"]
#         )
#         print(f"Alert sent to {EMERGENCY_CONTACT['name']} at {EMERGENCY_CONTACT['number']}")
#         print(message_body)
#         return message.sid
#     except Exception as e:
#         print(f"Failed to send alert: {e}")
#         return None
    

# print(send_fall_alert())

from twilio.rest import Client
# from gps_location import start_gps_listener, findLocation
import time
import geocoder

EMERGENCY_CONTACT = {
    "name": "[EMERGENCY_CONTACT]",
    "number": ""
}

NECKLACE_WEARER = "[NECKLACE_WEARER]"

# ask Kerushani for Twilio credentials
TWILIO_ACCOUNT_SID = ""
TWILIO_AUTH_TOKEN = ""
TWILIO_FROM_NUMBER = ""

def send_fall_alert():
    """
    Sends an SMS alert to the emergency contact using Twilio.
    """
    # Start the GPS reader thread (safe to call multiple times)
    # start_gps_listener()

    # Wait for GPS to populate (up to 10s)
    location = geocoder.ip("me")

    lat, long = location.latlng[0], location.latlng[1]

    link = f"https://www.google.com/maps?q={lat},{long}"
    
    # for _ in range(10):
        # location = findLocation()
        # if location:
        #     break
        # time.sleep(1)  # Give GPS time to read something

    location = location or "location unavailable"

    client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
    message_body = (
        f"ALERT: A fall has been detected. {EMERGENCY_CONTACT['name']} please check on "
        f"{NECKLACE_WEARER} immediately. -> {link}"
    )

    try:
        message = client.messages.create(
            body=message_body,
            from_=TWILIO_FROM_NUMBER,
            to=EMERGENCY_CONTACT["number"]
        )
        print(f"Alert sent to {EMERGENCY_CONTACT['name']} at {EMERGENCY_CONTACT['number']}")
        return message.sid
    except Exception as e:
        print(message_body)
        print(f"Failed to send alert: {e}")
        return None

# Run alert if this script is run directly
if __name__ == "__main__":
    print(send_fall_alert())
