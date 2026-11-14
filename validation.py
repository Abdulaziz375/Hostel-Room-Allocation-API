"""Input validation for the Room entity. Returns (clean_data, errors)."""
import re

REQUIRED_FIELDS = ["room_no", "block", "capacity", "occupants", "monthly_fee"]
ROOM_NO_PATTERN = re.compile(r"^[A-Z0-9]+(-[A-Z0-9]+)*$")      # letters, digits, single hyphens
BLOCKS = ["A", "B", "C", "D", "E", "F"]
CAPACITY_MIN, CAPACITY_MAX = 1, 6
FEE_MIN, FEE_MAX = 500, 50000


def _is_whole_number(value) -> bool:
    return isinstance(value, int) and not isinstance(value, bool)


def validate_room(data):
    errors, clean = {}, {}

    for field in REQUIRED_FIELDS:
        if field not in data or data[field] is None:
            errors[field] = "This field is required"

    if "room_no" not in errors:
        value = data["room_no"]
        if not isinstance(value, str):
            errors["room_no"] = "Must be text"
        else:
            room_no = value.strip().upper()                       # "a-101" is stored as "A-101"
            if 2 <= len(room_no) <= 10 and ROOM_NO_PATTERN.match(room_no):
                clean["room_no"] = room_no
            else:
                errors["room_no"] = "Must be 2-10 letters/digits with optional hyphens (example: A-101)"

    if "block" not in errors:
        value = data["block"]
        block = value.strip().upper() if isinstance(value, str) else None
        if block in BLOCKS:
            clean["block"] = block
        else:
            errors["block"] = f"Must be one of {', '.join(BLOCKS)}"

    if "capacity" not in errors:
        value = data["capacity"]
        if not _is_whole_number(value):
            errors["capacity"] = "Must be a whole number"
        elif not CAPACITY_MIN <= value <= CAPACITY_MAX:
            errors["capacity"] = f"Must be between {CAPACITY_MIN} and {CAPACITY_MAX}"
        else:
            clean["capacity"] = value

    if "occupants" not in errors:
        value = data["occupants"]
        if not _is_whole_number(value):
            errors["occupants"] = "Must be a whole number"
        elif value < 0:
            errors["occupants"] = "Cannot be negative"
        elif "capacity" in clean and value > clean["capacity"]:
            errors["occupants"] = f"Cannot be more than the room capacity ({clean['capacity']})"
        else:
            clean["occupants"] = value

    if "monthly_fee" not in errors:
        value = data["monthly_fee"]
        if not _is_whole_number(value):
            errors["monthly_fee"] = "Must be a whole number (PKR)"
        elif not FEE_MIN <= value <= FEE_MAX:
            errors["monthly_fee"] = f"Must be between {FEE_MIN} and {FEE_MAX}"
        else:
            clean["monthly_fee"] = value

    return clean, errors
