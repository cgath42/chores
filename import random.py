import random
from datetime import datetime
import schedule
import time
from twilio.rest import Client

# Twilio credentials (replace these with your actual credentials)
TWILIO_ACCOUNT_SID = "your_account_sid"
TWILIO_AUTH_TOKEN = "your_auth_token"
TWILIO_PHONE_NUMBER = "+1234567890"  # Your Twilio phone number
SHELBY_PHONE = "+11234567890"       # Shelby's phone number
DAWSON_PHONE = "+19876543210"       # Dawson's phone number

# Inspirational quotes
QUOTES = [
    "Believe you can and you're halfway there. – Theodore Roosevelt",
    "Success is not final, failure is not fatal: It is the courage to continue that counts. – Winston Churchill",
    "You are never too old to set another goal or to dream a new dream. – C.S. Lewis",
    "Hardships often prepare ordinary people for an extraordinary destiny. – C.S. Lewis",
    "Don't watch the clock; do what it does. Keep going. – Sam Levenson",
    "Keep your face always toward the sunshine—and shadows will fall behind you. – Walt Whitman",
]

def rotate_chores(chores, seed):
    """
    Rotate chores based on a seed value (e.g., day of the year or week number).
    Ensures the chores change daily or weekly.
    """
    random.seed(seed)
    shuffled_chores = chores[:]
    random.shuffle(shuffled_chores)
    return shuffled_chores

def send_sms(phone_number, message):
    """
    Send an SMS message using Twilio.
    """
    client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
    try:
        message = client.messages.create(
            to=phone_number,
            from_=TWILIO_PHONE_NUMBER,
            body=message
        )
        print(f"Message sent to {phone_number}. SID: {message.sid}")
    except Exception as e:
        print(f"Failed to send message to {phone_number}: {e}")

def assign_and_notify():
    # Lists of chores
    daily_chores = [
        "dishes", "living room", "kitchen", "trash", "master bedroom",
        "mail", "feed Winston", "pick up clothes around house",
        "wash and dry one load of laundry", "fold and hang up one load of laundry",
        "cooking", "wipe off counters"
    ]
    weekly_chores = [
        "vacuum living room and kitchen", "vacuum bedrooms and hallway", "mop all floors",
        "grocery shopping", "grocery planning", "empty fridge", "clean toilets",
        "clean showers", "clean sinks and mirror", "dust house", "change sheets",
        "main trash", "clean back door windows", "sweep off front porch"
    ]

    # Names of the people
    person1 = "Shelby"
    person2 = "Dawson"

    # Determine the current day and week
    current_day = datetime.now().timetuple().tm_yday  # Day of the year (1-365)
    current_week = datetime.now().isocalendar()[1]    # Week of the year (1-52)

    # Rotate chores based on the current day and week
    rotated_daily_chores = rotate_chores(daily_chores, current_day)
    rotated_weekly_chores = rotate_chores(weekly_chores, current_week)

    # Assign daily chores alternately
    daily_assignments = {person1: [], person2: []}
    for i, chore in enumerate(rotated_daily_chores):
        if i % 2 == 0:
            daily_assignments[person1].append(chore)
        else:
            daily_assignments[person2].append(chore)

    # Assign weekly chores alternately
    weekly_assignments = {person1: [], person2: []}
    for i, chore in enumerate(rotated_weekly_chores):
        if i % 2 == 0:
            weekly_assignments[person1].append(chore)
        else:
            weekly_assignments[person2].append(chore)

    # Check if today is Monday, Wednesday, or Friday
    today = datetime.now().strftime("%A")
    add_quote = today in ["Monday", "Wednesday", "Friday"]

    # Format messages for each person
    messages = {}
    for person in [person1, person2]:
        daily_message = f"Good morning, {person}!\nToday's chores:\n" + \
                        "\n".join(f" - {chore}" for chore in daily_assignments[person])
        weekly_message = f"\nThis week's chores:\n" + \
                         "\n".join(f" - {chore}" for chore in weekly_assignments[person])
        messages[person] = daily_message + weekly_message
        if add_quote:
            messages[person] += f"\n\nToday's inspiration: \"{random.choice(QUOTES)}\""

    # Send messages via SMS
    send_sms(SHELBY_PHONE, messages[person1])
    send_sms(DAWSON_PHONE, messages[person2])

    print("\nMessages sent successfully.")

# Schedule the function for 9 AM Central Time
schedule.every().day.at("09:00").do(assign_and_notify)

print("Scheduler started. Messages will be sent daily at 9 AM Central Time.")

# Run the scheduler indefinitely
while True:
    schedule.run_pending()
    time.sleep(1)
