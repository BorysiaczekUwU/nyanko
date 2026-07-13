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
tickets_col = db["tickets"] if db is not None else None
clans_col = db["clans"] if db is not None else None

# --- LISTY KOLORÓW ---
KAWAII_PINK = 0xFF69B4
KAWAII_RED = 0xFF0000
KAWAII_GOLD = 0xFFD700
KAWAII_BLUE = 0x87CEEB

# --- TOŻSAMOŚCI I ORIENTACJE ---
# "flag": to co pojawi się w nicku (może być kilka emotek).
# "emoji": to co idzie do ikonki na liście (MUSI być to JEDNA walidna emotka).
ORIENTATIONS = {
    "bi": {"flag": "💖💜💙", "emoji": "💖", "name": "Biseksualna", "color": KAWAII_PINK},
    "gej": {"flag": "🏳️‍🌈", "emoji": "🏳️‍🌈", "name": "Gejowska", "color": 0x00FF00}, 
    "les": {"flag": "🧡🤍💖", "emoji": "🧡", "name": "Lesbijska", "color": 0xFF8C00},
    "trans": {"flag": "🏳️‍⚧️", "emoji": "🏳️‍⚧️", "name": "Transpłciowa", "color": KAWAII_BLUE},
    "pan": {"flag": "💖💛💙", "emoji": "💛", "name": "Panseksualna", "color": 0xFFD700},
    "ace": {"flag": "🖤🩶🤍💜", "emoji": "🖤", "name": "Aseksualna", "color": 0x800080},
    "enby": {"flag": "💛🤍💜🖤", "emoji": "🤍", "name": "Niebinarna", "color": 0xFFFF00},
    "aro": {"flag": "💚🤍🩶🖤", "emoji": "💚", "name": "Aromantyczna", "color": 0x008000},
    "fluid": {"flag": "🩷🤍💜🖤💙", "emoji": "🩷", "name": "Genderfluid", "color": KAWAII_PINK},
    "femboy": {"flag": "🎀", "emoji": "🎀", "name": "Femboy", "color": KAWAII_PINK},
    "hetero": {"flag": "🖤🤍", "emoji": "🤍", "name": "Hetero", "color": 0xFFFFFF},
    "mazowsze": {"flag": "🇵🇱", "emoji": "🇵🇱", "name": "Mazowiecka", "color": 0xFF0000},
    "pionowa": {"flag": "🇮🇩", "emoji": "🇮🇩", "name": "Pionowa", "color": 0xFFFFFF},
    "pozioma": {"flag": "🇲🇨", "emoji": "🇲🇨", "name": "Pozioma", "color": 0xFF0000},
}

# --- PŁCIE ---
# "flag": to co pojawi się w nicku.
# "emoji": to co idzie do ikonki na liście (MUSI być to JEDNA walidna emotka).
GENDERS = {
    "chlopak": {"flag": "👦", "emoji": "👱‍♂️", "name": "Chłopak", "role_name": "—͟͞👦・Jegomość"},
    "dziewczyna": {"flag": "👧", "emoji": "👱‍♀️", "name": "Dziewczyna", "role_name": "—͟͞👧・Niewiasta"},
    "demigirl": {"flag": "💗🩶🤍", "emoji": "💗", "name": "Demigirl", "role_name": "—͟͞💗・Demigirl"},
    "demiboy": {"flag": "💙🩶🤍", "emoji": "💙", "name": "Demiboy", "role_name": "—͟͞💙・Demiboy"},
    "helicopter": {"flag": "🚁", "emoji": "🚁", "name": "Helikopter Bojowy", "role_name": "—͟͞👤・Helikopter Bojowy"},
    "tajemnica": {"flag": "👽", "emoji": "👽", "name": "Tajemnica", "role_name": None}
}

# --- POMOCNICZE FUNKCJE DLA MONGODB ---
# Jeśli bazy brak, używamy słownika w RAM (dla bezpieczeństwa przed crashem)
ram_storage = {"economy": {}, "levels": {}, "profiles": {}, "tickets": {}, "clans": {}}

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
def get_market_data():
    default = {
        "companies": {
            "TECH": {"name": "TechCorp", "price": 100.0, "history": []},
            "ECO": {"name": "GreenEnergy", "price": 50.0, "history": []},
            "FOOD": {"name": "FoodCo", "price": 30.0, "history": []},
            "SPACE": {"name": "SpaceX", "price": 200.0, "history": []}
        },
        "last_update": None
    }
    return _get_doc(economy_col, "economy", "global_market", default)

def update_market_data(companies):
    # Aktualizujemy cały obiekt companies
    _update_doc(economy_col, "economy", "global_market", {"companies": companies})

def get_data(user_id):
    default = {
        "balance": 0,
        "last_daily": None,
        "inventory": {},
        "stocks": {},
        "tycoon": {
            "machines": {},
            "last_collection": None,
            "stored_cash": 0.0
        }
    }
    data = _get_doc(economy_col, "economy", user_id, default)
    # Zabezpieczenie dla starych użytkowników (brakujące pola)
    if "stocks" not in data: data["stocks"] = {}
    if "tycoon" not in data: data["tycoon"] = {"machines": {}, "last_collection": None, "stored_cash": 0.0}
    return data

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

def get_all_economy_users():
    users = []
    if economy_col is not None:
        try:
            for doc in economy_col.find({}):
                # Ignoruj globalne dokumenty jak global_market
                if doc.get("_id") != "global_market":
                    users.append(doc.get("_id"))
        except Exception as e:
            print(f"Błąd db: {e}")
    else:
        for user_id in ram_storage["economy"].keys():
            if user_id != "global_market":
                users.append(user_id)
    return users

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
        "status": "Nieznany",
        "clan": None
    }
    return _get_doc(profiles_col, "profiles", user_id, default)

def update_profile(user_id, key, value):
    _update_doc(profiles_col, "profiles", user_id, {key: value})

# --- SYSTEM TICKETÓW ---
def get_ticket_user(user_id):
    default = {
        "has_opened_ticket": False
    }
    return _get_doc(tickets_col, "tickets", user_id, default)

def update_ticket_user(user_id, key, value):
    _update_doc(tickets_col, "tickets", user_id, {key: value})

# --- SYSTEM KLANÓW ---
def get_clan_data(clan_name):
    default = {
        "name": clan_name,
        "owner_id": None,
        "members": [],
        "level": 1,
        "xp": 0,
        "description": "Brak opisu klanu.",
        "channel_id": None,
        "role_id": None
    }
    return _get_doc(clans_col, "clans", clan_name, default)

def update_clan_data(clan_name, key, value, mode="set"):
    if mode == "set":
        _update_doc(clans_col, "clans", clan_name, {key: value})
    elif mode == "add":
        get_clan_data(clan_name)  # Upewnij się, że dokument istnieje
        _inc_doc(clans_col, "clans", clan_name, key, value)
    elif mode == "push":
        # Hack dla mongodb $push
        data = get_clan_data(clan_name)
        if isinstance(data.get(key), list):
            if value not in data[key]:
                data[key].append(value)
                _update_doc(clans_col, "clans", clan_name, {key: data[key]})
    elif mode == "pull":
        data = get_clan_data(clan_name)
        if isinstance(data.get(key), list):
            if value in data[key]:
                data[key].remove(value)
                _update_doc(clans_col, "clans", clan_name, {key: data[key]})

def delete_clan(clan_name):
    if clans_col is not None:
        try:
            clans_col.delete_one({"_id": clan_name})
        except: pass
    if clan_name in ram_storage["clans"]:
        del ram_storage["clans"][clan_name]

def get_all_clans():
    clans = []
    if clans_col is not None:
        try:
            for doc in clans_col.find({}):
                clans.append(doc)
        except Exception as e:
            print(f"Błąd db: {e}")
    else:
        for clan_data in ram_storage["clans"].values():
            clans.append(clan_data)
    return clans