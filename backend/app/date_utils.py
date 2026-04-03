from datetime import datetime, timedelta
from dateutil import parser


def parse_deadline(text: str):

    if text is None:
        return None

    text = text.lower()

    today = datetime.utcnow().date()

    # tomorrow
    if text == "tomorrow":
        return today + timedelta(days=1)

    # in X days
    if text.startswith("in "):
        try:
            days = int(text.split()[1])
            return today + timedelta(days=days)
        except:
            return None

    # weekday names
    weekdays = {
        "monday": 0,
        "tuesday": 1,
        "wednesday": 2,
        "thursday": 3,
        "friday": 4,
        "saturday": 5,
        "sunday": 6
    }

    if text in weekdays:
        target_day = weekdays[text]
        days_ahead = target_day - today.weekday()

        if days_ahead <= 0:
            days_ahead += 7

        return today + timedelta(days=days_ahead)

    # general parsing
    try:
        return parser.parse(text).date()
    except:
        return None