# backend/services/twilio_client.py

import os
from twilio.rest import Client
from twilio.base.exceptions import TwilioRestException

# Get your Twilio credentials from environment variables (safe)
TWILIO_ACCOUNT_SID = os.environ.get("TWILIO_ACCOUNT_SID")
TWILIO_AUTH_TOKEN = os.environ.get("TWILIO_AUTH_TOKEN")

# Room config
ROOM_TYPE = "group"  # or "group-small" / "go"
ROOM_STATUS_COMPLETED = "completed"

client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

def create_twilio_room(consultation):
    """
    Create a Twilio video room using consultation ID.
    Returns the room SID if successful.
    """
    try:
        room = client.video.rooms.create(
            unique_name=f"consult-{consultation.id}",
            type=ROOM_TYPE,
            record_participants_on_connect=False
        )
        return room.sid
    except TwilioRestException as e:
        print(f"[Twilio Error] Could not create room: {e}")
        return None

def end_twilio_room(room_sid):
    """
    Marks a Twilio room as completed (ends it).
    """
    try:
        room = client.video.rooms(room_sid).update(status=ROOM_STATUS_COMPLETED)
        return room.status == ROOM_STATUS_COMPLETED
    except TwilioRestException as e:
        print(f"[Twilio Error] Could not end room: {e}")
        return False
