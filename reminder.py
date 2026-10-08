import os
import sqlite3
import webbrowser
from datetime import datetime
from urllib.parse import quote
from dotenv import load_dotenv
from openai import OpenAI

# Load secrets from .env
load_dotenv()

# Initialize OpenAI client
api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=api_key) if api_key and api_key != "your_actual_openai_api_key_here" else None


def generate_ai_message(name, relation, occasion):
    """Generates a personalized greeting message using OpenAI API or fallback logic."""
    if not client:
        return f"Hey {name}! Happy {occasion}! Hope you have an incredible day filled with joy."

    prompt = (
        f"Write a warm, personalized, short SMS message (under 60 words) "
        f"wishing my {relation}, {name}, a Happy {occasion}."
    )

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a thoughtful message composer."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.7,
        max_tokens=60
    )

    return response.choices[0].message.content.strip()


def send_whatsapp_message(phone_number, message):
    """Encodes the message and opens a pre-filled WhatsApp web link."""
    encoded_message = quote(message)
    clean_phone = phone_number.replace("+", "").replace("-", "").replace(" ", "")
    whatsapp_url = f"https://wa.me/{clean_phone}?text={encoded_message}"
    
    print(f"   🔗 Generated WhatsApp Link: {whatsapp_url}")
    print("   🚀 Opening WhatsApp in your browser...")
    webbrowser.open(whatsapp_url)


def check_special_days():
    """Queries the SQLite database for contacts whose special_day matches today."""
    today = datetime.now().strftime("%m-%d")
    print(f"Checking database for special days today ({today})...\n")

    # Connect to database
    conn = sqlite3.connect("contacts.db")
    cursor = conn.cursor()

    # Query contacts matching today's date
    cursor.execute("""
        SELECT name, relation, occasion, phone, delivery_pref 
        FROM contacts 
        WHERE special_day = ?
    """, (today,))

    matching_contacts = cursor.fetchall()
    conn.close()

    if not matching_contacts:
        print("No special days found for today!")
        return

    # Process each matched record from the database
    for row in matching_contacts:
        name, relation, occasion, phone, delivery_pref = row
        print(f"🎉 TODAY IS A SPECIAL DAY FOR {name.upper()} ({relation})!")

        message = generate_ai_message(name, relation, occasion)
        print(f"   Drafted Message: \"{message}\"")

        if delivery_pref == "WhatsApp":
            send_whatsapp_message(phone, message)
        elif delivery_pref == "SMS":
            print(f"   Action: Ready for Twilio SMS integration to {phone}...\n")


if __name__ == "__main__":
    check_special_days()
    import os
import sqlite3
import webbrowser
from datetime import datetime
from urllib.parse import quote
from dotenv import load_dotenv
from openai import OpenAI
from twilio.rest import Client

# Load secrets from .env
load_dotenv()

# Initialize OpenAI client
api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=api_key) if api_key and api_key != "your_actual_openai_api_key_here" else None

# Twilio Configuration
TWILIO_ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID")
TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")
TWILIO_PHONE_NUMBER = os.getenv("TWILIO_PHONE_NUMBER")

# Initialize Twilio Client safely
twilio_client = None
if TWILIO_ACCOUNT_SID and TWILIO_AUTH_TOKEN and TWILIO_ACCOUNT_SID != "your_twilio_account_sid":
    try:
        twilio_client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
    except Exception as e:
        print(f"⚠️ Could not initialize Twilio client: {e}")


def generate_ai_message(name, relation, occasion):
    """Generates a personalized greeting message using OpenAI API or fallback logic."""
    if not client:
        return f"Hey {name}! Happy {occasion}! Hope you have an incredible day filled with joy."

    prompt = (
        f"Write a warm, personalized, short SMS message (under 30 words) "
        f"wishing my {relation}, {name}, a Happy {occasion}."
    )

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a thoughtful message composer."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.7,
        max_tokens=60
    )

    return response.choices[0].message.content.strip()


def send_whatsapp_message(phone_number, message):
    """Encodes the message and opens a pre-filled WhatsApp web link."""
    encoded_message = quote(message)
    clean_phone = phone_number.replace("+", "").replace("-", "").replace(" ", "")
    whatsapp_url = f"https://wa.me/{clean_phone}?text={encoded_message}"
    
    print(f"   🔗 Generated WhatsApp Link: {whatsapp_url}")
    print("   🚀 Opening WhatsApp in your browser...")
    webbrowser.open(whatsapp_url)


def send_sms_message(phone_number, message):
    """Sends an automated SMS via Twilio API, or prints mock logs if missing credentials."""
    if not twilio_client or not TWILIO_PHONE_NUMBER or TWILIO_PHONE_NUMBER == "+1234567890":
        print(f"   📱 [MOCK SMS to {phone_number}]: \"{message}\"")
        print("   ⚠️ Twilio credentials missing in .env — simulated sending completed.")
        return

    try:
        sms = twilio_client.messages.create(
            body=message,
            from_=TWILIO_PHONE_NUMBER,
            to=phone_number
        )
        print(f"   📱 SMS successfully dispatched via Twilio! Message SID: {sms.sid}")
    except Exception as e:
        print(f"   ❌ Failed to send Twilio SMS: {e}")


def check_special_days():
    """Queries the SQLite database for contacts whose special_day matches today."""
    today = datetime.now().strftime("%m-%d")
    print(f"Checking database for special days today ({today})...\n")

    # Connect to database
    conn = sqlite3.connect("contacts.db")
    cursor = conn.cursor()

    # Query contacts matching today's date
    cursor.execute("""
        SELECT name, relation, occasion, phone, delivery_pref 
        FROM contacts 
        WHERE special_day = ?
    """, (today,))

    matching_contacts = cursor.fetchall()
    conn.close()

    if not matching_contacts:
        print("No special days found for today!")
        return

    # Process each matched record from the database
    for row in matching_contacts:
        name, relation, occasion, phone, delivery_pref = row
        print(f"🎉 TODAY IS A SPECIAL DAY FOR {name.upper()} ({relation})!")

        message = generate_ai_message(name, relation, occasion)
        print(f"   Drafted Message: \"{message}\"")

        if delivery_pref == "WhatsApp":
            send_whatsapp_message(phone, message)
        elif delivery_pref == "SMS":
            send_sms_message(phone, message)


if __name__ == "__main__":
    check_special_days()