import re
from datetime import datetime

def validate_student_id(sid, id_set, is_edit=False):
    if not sid:
        raise ValueError("Student ID cannot be empty.")
    sid_clean = str(sid).strip()
    if not sid_clean:
        raise ValueError("Student ID cannot be empty.")
    if len(sid_clean) > 10:
        raise ValueError("Student ID cannot exceed 10 characters.")
    if not sid_clean.isalnum():
        raise ValueError("Student ID must be alphanumeric (letters and numbers only).")
    if not is_edit and sid_clean in id_set:
        raise ValueError(f"Student ID '{sid_clean}' already exists in records.")
    return sid_clean

def validate_name(name):
    if not name:
        raise ValueError("Name cannot be empty.")
    name_clean = str(name).strip()
    if not name_clean:
        raise ValueError("Name cannot be empty.")
    # Allow letters, spaces, and periods
    if not re.match(r"^[a-zA-Z\s\.]+$", name_clean):
        raise ValueError("Name can only contain alphabetic characters, spaces, or periods.")
    return name_clean

def validate_phone(phone):
    if not phone:
        raise ValueError("Phone number cannot be empty.")
    phone_clean = str(phone).strip()
    if not re.match(r"^01\d{9}$", phone_clean):
        raise ValueError("Phone number must be exactly 11 digits and start with '01' (e.g., 01712345678).")
    return phone_clean

def validate_password(pwd):
    if not pwd:
        raise ValueError("Password cannot be empty.")
    pwd_clean = str(pwd)
    if len(pwd_clean) < 4:
        raise ValueError("Password must be at least 4 characters long.")
    return pwd_clean

def validate_amount(amount_str):
    if not amount_str:
        raise ValueError("Amount cannot be empty.")
    try:
        val = float(amount_str)
    except ValueError:
        raise ValueError("Amount must be a numeric value.")
    
    if val <= 0:
        raise ValueError("Amount must be greater than zero.")
    return val

def validate_date(date_str):
    if not date_str:
        raise ValueError("Date cannot be empty.")
    date_clean = str(date_str).strip()
    try:
        dt = datetime.strptime(date_clean, "%Y-%m-%d")
    except ValueError:
        raise ValueError("Date must be in YYYY-MM-DD format (e.g., 2025-07-01).")
    return date_clean

def validate_dish_name(dish):
    if not dish:
        raise ValueError("Dish name cannot be empty.")
    dish_clean = str(dish).strip()
    if len(dish_clean) < 3:
        raise ValueError("Dish name must be at least 3 characters long.")
    return dish_clean

def validate_meal_choice(choice, valid=("1", "2", "3")):
    choice_clean = str(choice).strip()
    if choice_clean not in valid:
        raise ValueError(f"Choice must be one of the valid options: {', '.join(valid)}")
    return choice_clean
