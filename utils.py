import json
import os

ECONOMY_FILE = "economy.json"

# --- LISTY ---
KAWAII_PINK = 0xFF69B4
KAWAII_RED = 0xFF0000
KAWAII_GOLD = 0xFFD700
KAWAII_BLUE = 0x87CEEB

def load_economy():
    if not os.path.exists(ECONOMY_FILE):
        return {}
    with open(ECONOMY_FILE, "r") as f:
        return json.load(f)

def save_economy(data):
    with open(ECONOMY_FILE, "w") as f:
        json.dump(data, f, indent=4)

def get_data(user_id):
    data = load_economy()
    str_id = str(user_id)
    if str_id not in data:
        data[str_id] = {"balance": 0, "last_daily": None, "inventory": {}}
    return data[str_id]

def update_data(user_id, key, value, mode="set"):
    data = load_economy()
    str_id = str(user_id)
    if str_id not in data:
        data[str_id] = {"balance": 0, "last_daily": None, "inventory": {}}
    
    if mode == "add":
        data[str_id][key] += value
    elif mode == "set":
        data[str_id][key] = value
    save_economy(data)

def add_item(user_id, item_code):
    data = load_economy()
    str_id = str(user_id)
    if str_id not in data: get_data(user_id) # Init
    
    inventory = data[str_id].get("inventory", {})
    inventory[item_code] = inventory.get(item_code, 0) + 1
    data[str_id]["inventory"] = inventory
    save_economy(data)

def remove_item(user_id, item_code):
    data = load_economy()
    str_id = str(user_id)
    if str_id not in data: return False
    inventory = data[str_id].get("inventory", {})
    
    if inventory.get(item_code, 0) > 0:
        inventory[item_code] -= 1
        data[str_id]["inventory"] = inventory
        save_economy(data)
        return True
    return False