from twilio.rest import Client

EMERGENCY_CONTACT = {
    "name": "Aman Serhan",
    "number": "+16477635666"
}

NECKLACE_WEARER = "Kerushani"

# ask Kerushani for Twilio credentials
TWILIO_ACCOUNT_SID = ""
TWILIO_AUTH_TOKEN = ""
TWILIO_FROM_NUMBER = ""


def send_fall_alert():
    """
    Sends an SMS alert to the emergency contact using Twilio.
    """
    client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
    message_body = f"ALERT: A fall has been detected. {EMERGENCY_CONTACT['name']} please check on {NECKLACE_WEARER} immediately."
    try:
        message = client.messages.create(
            body=message_body,
            from_=TWILIO_FROM_NUMBER,
            to=EMERGENCY_CONTACT["number"]
        )
        print(f"Alert sent to {EMERGENCY_CONTACT['name']} at {EMERGENCY_CONTACT['number']}")
        return message.sid
    except Exception as e:
        print(f"Failed to send alert: {e}")
        return None

