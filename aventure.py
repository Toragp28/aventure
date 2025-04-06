import random
import time
import json
import os
from colorama import init, Fore

init(autoreset=True)
green = Fore.GREEN

SAVE_FILE = "save.json"

zones = ["Forêt 🌲", "Désert 🏜️", "Donjon 🕸️", "Montagnes 🗻", "Marais ☠️"]
items = ["Potion de vie", "Épée magique", "Clé mystérieuse", "Pierre étrange", "Amulette de feu"]
pnjs = ["Sage du désert", "Forgeron perdu", "Marchand fou", "Vieille sorcière"]
bosses = [
    {"name": "Dragon de flammes", "hp": 150, "attack": 25},
    {"name": "Golem de pierre", "hp": 200, "attack": 15},
    {"name": "Roi des ombres", "hp": 180, "attack": 20}
]

player = {
    "name": "Héros",
    "hp": 100,
    "attack": 10,
    "inventory": [],
    "xp": 0,
    "level": 1,
    "zone": "Forêt 🌲"
}

def slow_print(text):
    for char in text:
        print(green + char, end='', flush=True)
        time.sleep(0.01)
    print()

def save_game():
    with open(SAVE_FILE, "w") as f:
        json.dump(player, f)
    slow_print("💾 Sauvegarde réussie.")

def load_game():
    if os.path.exists(SAVE_FILE):
        with open(SAVE_FILE, "r") as f:
            data = json.load(f)
            player.update(data)
        slow_print("📂 Sauvegarde chargée.")

def gain_xp(amount):
    player["xp"] += amount
    slow_print(f"✨ Tu gagnes {amount} XP !")
    if player["xp"] >= player["level"] * 50:
        player["level"] += 1
        player["hp"] += 20
        player["attack"] += 5
        player["xp"] = 0
        slow_print(f"🆙 Tu montes au niveau {player['level']} ! (+20 PV, +5 ATQ)")

def random_quest():
    actions = ["tuer un monstre", "récupérer un objet", "parler à un PNJ", "explorer une zone"]
    obj = random.choice(items)
    zone = random.choice(zones)
    action = random.choice(actions)
    return f"{action} dans {zone} et obtenir {obj}"

def explore():
    event = random.choice(["pnj", "item", "boss", "vide", "quête"])
    if event == "pnj":
        pnj = random.choice(pnjs)
        obj = random.choice(items)
        player["inventory"].append(obj)
        slow_print(f"🤝 Tu rencontres {pnj}, il t’offre un objet : {obj}")
        gain_xp(10)
    elif event == "item":
        obj = random.choice(items)
        player["inventory"].append(obj)
        slow_print(f"🧪 Tu trouves un objet : {obj}")
        gain_xp(5)
    elif event == "boss":
        boss = random.choice(bosses)
        fight_boss(boss)
    elif event == "quête":
        quest = random_quest()
        slow_print(f"📜 Nouvelle quête : {quest}")
        if random.randint(0, 1):
            reward = random.choice(items)
            slow_print(f"✅ Quête accomplie ! Récompense : {reward}")
            player["inventory"].append(reward)
            gain_xp(20)
        else:
            slow_print("❌ Tu n’as pas réussi cette fois...")
    else:
        slow_print("Rien ici... continue ton chemin.")

def fight_boss(boss):
    slow_print(f"⚔️ Combat contre {boss['name']} !")
    boss_hp = boss["hp"]
    while boss_hp > 0 and player["hp"] > 0:
        action = input(green + "1: Attaquer / 2: Fuir > ")
        if action == "1":
            dmg = player["attack"] + random.randint(0, 5)
            boss_hp -= dmg
            slow_print(f"💥 Tu infliges {dmg} à {boss['name']}")
        elif action == "2":
            slow_print("🏃‍♂️ Tu fuis...")
            return
        else:
            slow_print("❓ Action invalide.")
            continue
        if boss_hp > 0:
            dmg = boss["attack"] + random.randint(0, 5)
            player["hp"] -= dmg
            slow_print(f"{boss['name']} t'inflige {dmg} dégâts !")
    if player["hp"] <= 0:
        slow_print("💀 Tu es tombé, mais la magie te ressuscite.")
        player["hp"] = 100
    else:
        slow_print(f"🏆 Tu as vaincu {boss['name']} !")
        gain_xp(30)

def show_stats():
    slow_print(f"❤️ PV : {player['hp']} | 🗡️ ATQ : {player['attack']} | 🌟 Niv: {player['level']} | XP: {player['xp']}/50")
    slow_print(f"📦 Inventaire : {', '.join(player['inventory']) if player['inventory'] else 'Vide'}")
    slow_print(f"📍 Zone actuelle : {player['zone']}")

def change_zone():
    slow_print("🔄 Zones disponibles :")
    for i, z in enumerate(zones):
        slow_print(f"{i + 1}. {z}")
    choice = input(green + "Choisis ta destination > ")
    if choice.isdigit() and 1 <= int(choice) <= len(zones):
        player["zone"] = zones[int(choice) - 1]
        slow_print(f"🌍 Tu voyages vers : {player['zone']}")
    else:
        slow_print("❌ Zone inconnue.")

def main():
    load_game()
    slow_print("🌟 Bienvenue dans l'Aventure Mystique Évolutive !")
    while True:
        slow_print("\n1. Explorer\n2. Voir mes stats\n3. Changer de zone\n4. Sauvegarder\n5. Quitter")
        choix = input(green + "> ")
        if choix == "1":
            explore()
        elif choix == "2":
            show_stats()
        elif choix == "3":
            change_zone()
        elif choix == "4":
            save_game()
        elif choix == "5":
            save_game()
            slow_print("À bientôt, aventurier !")
            break
        else:
            slow_print("❓ Choix invalide.")

if __name__ == "__main__":
    main()