import os
import pymongo
import certifi
from pymongo import MongoClient

# --- KONFIGURACJA BAZY DANYCH (MONGODB) ---
# Pobieramy adres bazy z Environment Variables (tak jak Token)
MONGO_URL = os.environ.get("MONGO_URL")

# Połączenie z bazą
if not MONGO_URL:
    print("⚠️ OSTRZEŻENIE: Brak MONGO_URL! Dane nie będą zapisywane trwale (używam pamięci tymczasowej RAM).")
    # Fallback dla testów lokalnych bez bazy (resetuje się po wyłączeniu)
    cluster = None
    db = None
else:
    # Ustawiamy timeout na 5 sekund, żeby bot nie "wisiał" przy problemach z bazą
    cluster = MongoClient(MONGO_URL, tls=True, tlsAllowInvalidCertificates=True, serverSelectionTimeoutMS=5000)
    db = cluster["KawaiiBotDB"]

# Kolekcje (Tabele)
economy_col = db["economy"] if db is not None else None
levels_col = db["levels"] if db is not None else None
profiles_col = db["profiles"] if db is not None else None

# --- LISTY KOLORÓW ---
KAWAII_PINK = 0xFF69B4
KAWAII_RED = 0xFF0000
KAWAII_GOLD = 0xFFD700
KAWAII_BLUE = 0x87CEEB

# --- POMOCNICZE FUNKCJE DLA MONGODB ---
# Jeśli bazy brak, używamy słownika w RAM (dla bezpieczeństwa przed crashem)
ram_storage = {"economy": {}, "levels": {}, "profiles": {}}

def _get_doc(collection, col_name, user_id, default_doc):
    str_id = str(user_id)
    if collection is not None:
        try:
            data = collection.find_one({"_id": str_id})
            if not data:
                data = default_doc.copy()
                data["_id"] = str_id
                collection.insert_one(data)
            return data
        except Exception as e:
            print(f"⚠️ Błąd MongoDB (get): {e}. Używam RAM.")

    # Fallback RAM
    if str_id not in ram_storage[col_name]:
        ram_storage[col_name][str_id] = default_doc.copy()
    return ram_storage[col_name][str_id]

def _update_doc(collection, col_name, user_id, update_dict):
    str_id = str(user_id)
    if collection is not None:
        try:
            collection.update_one({"_id": str_id}, {"$set": update_dict}, upsert=True)
            return
        except Exception as e:
            print(f"⚠️ Błąd MongoDB (update): {e}. Używam RAM.")

    # Fallback RAM
    if str_id not in ram_storage[col_name]: ram_storage[col_name][str_id] = {}
    ram_storage[col_name][str_id].update(update_dict)

def _inc_doc(collection, col_name, user_id, field, amount):
    str_id = str(user_id)
    if collection is not None:
        try:
            collection.update_one({"_id": str_id}, {"$inc": {field: amount}}, upsert=True)
            return
        except Exception as e:
            print(f"⚠️ Błąd MongoDB (inc): {e}. Używam RAM.")

    # Fallback RAM logic
    if str_id not in ram_storage[col_name]: ram_storage[col_name][str_id] = {}

    current_val = ram_storage[col_name][str_id].get(field, 0)
    ram_storage[col_name][str_id][field] = current_val + amount

# --- EKONOMIA ---
def get_data(user_id):
    default = {"balance": 0, "last_daily": None, "inventory": {}}
    return _get_doc(economy_col, "economy", user_id, default)

def update_data(user_id, key, value, mode="set"):
    if mode == "set":
        _update_doc(economy_col, "economy", user_id, {key: value})
    elif mode == "add":
        # Dla inventory musimy pobrać i zapisać, bo struktura jest złożona
        if key == "inventory":
            data = get_data(user_id)
            data["inventory"] = value
            _update_doc(economy_col, "economy", user_id, {"inventory": value})
        else:
            # FIX: _inc_doc może nie działać jeśli dokument nie istnieje w bazie
            # więc najpierw upewniamy się, że istnieje przez get_data
            get_data(user_id)
            _inc_doc(economy_col, "economy", user_id, key, value)

def add_item(user_id, item_code):
    data = get_data(user_id)
    inventory = data.get("inventory", {})
    inventory[item_code] = inventory.get(item_code, 0) + 1
    update_data(user_id, "inventory", inventory, "set")

def remove_item(user_id, item_code):
    data = get_data(user_id)
    inventory = data.get("inventory", {})
    if inventory.get(item_code, 0) > 0:
        inventory[item_code] -= 1
        update_data(user_id, "inventory", inventory, "set")
        return True
    return False

# --- SYSTEM LEVELI ---
def get_level_data(user_id):
    default = {"xp": 0, "level": 1, "rep": 0, "last_rep": None}
    return _get_doc(levels_col, "levels", user_id, default)

def update_level_data(user_id, key, value, mode="set"):
    if mode == "set":
        _update_doc(levels_col, "levels", user_id, {key: value})
    elif mode == "add":
        get_level_data(user_id) # FIX: Upewnij się, że dokument istnieje
        _inc_doc(levels_col, "levels", user_id, key, value)

# --- SYSTEM PROFILI (BIO) ---
def get_profile_data(user_id):
    default = {
        "bio": "Jeszcze nic tu nie ma...", 
        "age": "Nieznany", 
        "gender": "Nieznana", 
        "color": "pink",
        "birthday": "Nie ustawiono",
        "partner": None,
        "pronouns": "Nieznane",
        "status": "Nieznany"
    }
    return _get_doc(profiles_col, "profiles", user_id, default)

def update_profile(user_id, key, value):
    _update_doc(profiles_col, "profiles", user_id, {key: value})