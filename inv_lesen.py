import requests
import time
import os
import re

# DEINE DATEN
STEAM_ID = "76561198132160922" 
APP_ID = "730"
CONTEXT_ID = "2"

def clean_price(price_str):
    """Wandelt '1,25€' oder '0.50$' in eine Floatzahl (1.25) um."""
    if not price_str or not isinstance(price_str, str):
        return 0.0
    # Entfernt alles außer Zahlen, Komma und Punkt
    cleaned = re.sub(r'[^\d,.]', '', price_str)
    # Ersetzt europäisches Komma durch Punkt für Python
    cleaned = cleaned.replace(',', '.')
    try:
        return float(cleaned)
    except ValueError:
        return 0.0

def get_cs_inventory(steam_id):
    # Nutze f-string mit dem Parameter steam_id, statt hartcodierter URL
    url = f"https://steamcommunity.com/inventory/76561198800951908/730/2?l=german"
    try:
        response = requests.get(url)
        if response.status_code != 200:
            print(f"Fehler beim Laden des Inventars: {response.status_code}")
            return None
        
        data = response.json()
        inventory_counts = {}
        
        # Beschreibungen zuordnen
        descriptions = {d['classid']: d['market_hash_name'] for d in data['descriptions'] if d.get('marketable')}
        
        # Items zählen (wichtig für Gesamtwert!)
        for asset in data['assets']:
            classid = asset['classid']
            if classid in descriptions:
                name = descriptions[classid]
                inventory_counts[name] = inventory_counts.get(name, 0) + 1
                
        return inventory_counts
    except Exception as e:
        print(f"Ein Fehler ist aufgetreten: {e}")
        return None

def get_item_price(item_name):
    url = "https://steamcommunity.com/market/priceoverview/"
    params = {'appid': 730, 'currency': 3, 'market_hash_name': item_name}
    
    try:
        res = requests.get(url, params=params)
        if res.status_code == 200:
            return res.json().get('lowest_price')
        elif res.status_code == 429:
            return "RATE_LIMIT"
    except:
        return None
    return None

# --- MAIN ---
os.system("cls" if os.name == "nt" else "clear")
print("Lade Inventar...")
inventory = get_cs_inventory(STEAM_ID)

total_value = 0.0

if inventory:
    item_list = list(inventory.items())
    print(f"Gefundene verschiedene Items: {len(item_list)}")
    print("-" * 50)

    for name, count in item_list:
        raw_price = get_item_price(name)
        
        if raw_price == "RATE_LIMIT":
            print("\n[!] Steam Rate Limit erreicht. Warte 60 Sekunden...")
            time.sleep(60)
            raw_price = get_item_price(name) # Zweiter Versuch

        price_value = clean_price(raw_price)
        subtotal = price_value * count
        total_value += subtotal
        
        status = f"{raw_price}" if raw_price else "N/A"
        print(f"{count:3}x {name[:30]:30} | Einzel: {status:>8} | Gesamt: {subtotal:6.2f}€")
        
        # 3 Sekunden sind bei vielen Items sehr lang, aber sicher.
        # Bei mehr als 20 Items wirst du trotzdem ggf. geblockt.
        time.sleep(3.5)

    print("-" * 50)
    print(f"GESAMTWERT DES INVENTARS: {total_value:.2f} €")
else:
    print("Inventar konnte nicht geladen werden (Privatsphäre auf Öffentlich?)")