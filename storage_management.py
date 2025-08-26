import json
import os


filePath = "storage/playerData.json"
players = 0
def initializeJSON():
    global players
    if os.path.exists(filePath):
        with open(filePath, "r") as file:
            try:
                content = file.read().strip()
                if content:
                    players = json.loads(content)
                else:
                    print("File was empty. Starting fresh.")
                    players = {}
                print("JSON file successfully reinitiated")
            except json.JSONDecodeError:
                print("Invalid JSON detected. Reinitializing with empty data.")
                players = {}

def clearJSON():
    with open(filePath, "w") as file:
        json.dump({}, file, indent=4)
    print(f"{filePath} has been cleared.")

def updateValue(key, value):
    global players
    players[key] = value
    with open(filePath, "w") as file:
        json.dump(players, file, indent=4)

