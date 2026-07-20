import os
import json

def save_json(data_list, filename):
    """
    Saves a list of OOP objects to a JSON file by calling their to_dict() method.
    Handles IOError and PermissionError.
    """
    try:
        # Create directories if they do not exist
        directory = os.path.dirname(filename)
        if directory and not os.path.exists(directory):
            os.makedirs(directory, exist_ok=True)
            
        dict_list = [obj.to_dict() for obj in data_list]
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(dict_list, f, indent=4)
        return True
    except (IOError, PermissionError) as e:
        print(f"Error saving to {filename}: {e}")
        return False

def load_json(filename, class_ref):
    """
    Loads data from a JSON file and reconstitutes it into objects of class_ref using from_dict().
    Handles FileNotFoundError, json.JSONDecodeError, and general OS errors.
    """
    if not os.path.exists(filename):
        return []
    
    # Check if the file is empty
    if os.path.getsize(filename) == 0:
        return []
        
    try:
        with open(filename, "r", encoding="utf-8") as f:
            data = json.load(f)
            
        if not isinstance(data, list):
            return []
            
        return [class_ref.from_dict(item) for item in data if isinstance(item, dict)]
    except json.JSONDecodeError as e:
        print(f"JSON decode error in {filename}: {e} - Returning empty list.")
        return []
    except FileNotFoundError:
        return []
    except Exception as e:
        print(f"Unexpected error loading {filename}: {e}")
        return []

def save_config(config_dict, filename):
    """
    Saves a configuration dictionary to a JSON file.
    """
    try:
        directory = os.path.dirname(filename)
        if directory and not os.path.exists(directory):
            os.makedirs(directory, exist_ok=True)
            
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(config_dict, f, indent=4)
        return True
    except Exception as e:
        print(f"Error saving config to {filename}: {e}")
        return False

def load_config(filename):
    """
    Loads a configuration dictionary from a JSON file. Returns a default dictionary if loading fails.
    """
    default_config = {
        "mess_name": "AIUB Blue Bird Mess",
        "meal_rate": 45.0
    }
    if not os.path.exists(filename):
        return default_config
    if os.path.getsize(filename) == 0:
        return default_config
        
    try:
        with open(filename, "r", encoding="utf-8") as f:
            config = json.load(f)
        if isinstance(config, dict):
            # Enforce types
            config["meal_rate"] = float(config.get("meal_rate", 45.0))
            config["mess_name"] = str(config.get("mess_name", "AIUB Blue Bird Mess"))
            return config
        return default_config
    except Exception as e:
        print(f"Error loading config from {filename}: {e}")
        return default_config
