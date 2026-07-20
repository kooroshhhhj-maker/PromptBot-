import json
import os

FILE = "stats.json"

def load():
    if not os.path.exists(FILE):
        return {"users": []}

    with open(FILE, "r") as f:
        return json.load(f)

def save(data):
    with open(FILE, "w") as f:
        json.dump(data, f)

def add_user(user_id):
    data = load()

    if user_id not in data["users"]:
        data["users"].append(user_id)
        save(data)

def total_users():
    data = load()
    return len(data["users"])

