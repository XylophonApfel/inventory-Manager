import sqlite3
import os
import requests
import time
from datetime import datetime

def erstelle_datenbank():
    # 1. Verbindung zur lokalen SQLite-Datenbank herstellen (Datei wird erstellt, falls sie nicht existiert)
    con = sqlite3.connect('inventar_manager.db')
    cursor = con.cursor()

    # WICHTIG für SQLite: Fremdschlüssel (Foreign Keys) müssen manuell aktiviert werden!
    cursor.execute("PRAGMA foreign_keys = ON;")

    # 2. Tabelle: benutzer anlegen
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS benutzer (
            benutzer_id INTEGER PRIMARY KEY AUTOINCREMENT,
            benutzername TEXT UNIQUE NOT NULL,
            passwort_hash TEXT NOT NULL,
            erstellt_am TEXT DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    # 3. Tabelle: gegenstand anlegen (Der Item-Katalog)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS gegenstand (
            item_id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE NOT NULL,
            typ TEXT,
            icon_pfad TEXT
        )
    ''')

    # 4. Tabelle: inventar anlegen (Verknüpft Benutzer mit Gegenständen)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS inventar (
            inventar_id INTEGER PRIMARY KEY AUTOINCREMENT,
            benutzer_id INTEGER NOT NULL,
            item_id INTEGER NOT NULL,
            menge INTEGER DEFAULT 1,
            kaufpreis_stueck REAL,
            FOREIGN KEY (benutzer_id) REFERENCES benutzer (benutzer_id) ON DELETE CASCADE,
            FOREIGN KEY (item_id) REFERENCES gegenstand (item_id) ON DELETE CASCADE
        )
    ''')

    # 5. Tabelle: preis_verlauf anlegen (Für das Caching und die Diagramme)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS preis_verlauf (
            preis_id INTEGER PRIMARY KEY AUTOINCREMENT,
            item_id INTEGER NOT NULL,
            preis REAL NOT NULL,
            zeitstempel INTEGER NOT NULL,
            FOREIGN KEY (item_id) REFERENCES gegenstand (item_id) ON DELETE CASCADE
        )
    ''')

    # 6. Änderungen speichern und Verbindung schließen
    con.commit()
    con.close()
    print("Datenbank und Tabellen wurden erfolgreich initialisiert!")

def Datenbank_befhel_ausfuehren(Befehl):
    import sqlite3
    con = sqlite3.connect('inventar_manager.db')

    cur = con.cursor()
    Ergebniss = cur.execute(Befehl)

    # Bei SELECT-Abfragen die Daten zurückgeben, statt sie zu verwerfen.
    if Ergebniss.description is not None:
        daten = Ergebniss.fetchall()
        con.close()
        return daten

    con.commit()

    con.close()
    return

def Benutzer_erstellen(Benutzername, Passwort):
    wert = Benutzer_vorhanden(Benutzername)

    if wert == 0:
        print("Benutzer anlegen")
        Datenbank_befhel_ausfuehren(f"Insert INTO benutzer (benutzername, passwort_hash) Values ('{Benutzername}','{Passwort}');")

    elif wert == 1:
        print("Benutzer bereits vorhanden!")



def Benutzer_vorhanden(Benutzername):
    Ergebniss = Datenbank_befhel_ausfuehren("Select benutzername from benutzer;")
    Liste_Benutzer = []

    for i in Ergebniss:
        Liste_Benutzer.append(i[0])
        
    if Benutzername in Liste_Benutzer:
       print("Benutzer bereits vorhanden!")
       wert = 1
    else:
       print("Benutzer wird angelegt")
       wert = 0
    
    return wert


def Benutzer_anmelden(Benutzername, Passwort):
    Ergebniss = Datenbank_befhel_ausfuehren("Select * From benutzer;")
    print(Ergebniss)

def Inventar_Gesamtwert_berechnen():
    pass

def Item_Gesamtwert_berechnen():
    pass

def Kisten_In_Datenbanken_anlegen():

    csgo_cases = [
    # --- Klassische & Frühe Kisten ---
    "CS:GO Weapon Case",
    "CS:GO Weapon Case 2",
    "CS:GO Weapon Case 3",
    "Winter Offensive Weapon Case",
    
    # --- eSports Kisten ---
    "eSports 2013 Case",
    "eSports 2013 Winter Case",
    "eSports 2014 Summer Case",
    
    # --- Operations Kisten ---
    "Operation Bravo Case",
    "Operation Phoenix Weapon Case",
    "Operation Breakout Weapon Case",
    "Operation Vanguard Weapon Case",
    "Operation Wildfire Case",
    "Operation Hydra Case",
    "Shattered Web Case",
    "Operation Broken Fang Case",
    "Operation Riptide Case",
    
    # --- Standard / Community Kisten ---
    "Huntsman Weapon Case",
    "Chroma Case",
    "Chroma 2 Case",
    "Chroma 3 Case",
    "Falchion Case",
    "Shadow Case",
    "Revolver Case",
    "Gamma Case",
    "Gamma 2 Case",
    "Glove Case",
    "Spectrum Case",
    "Spectrum 2 Case",
    "Clutch Case",
    "Horizon Case",
    "Danger Zone Case",
    "Prisma Case",
    "CS20 Case",
    "Prisma 2 Case",
    "Fracture Case",
    "Snakebite Case",
    "Dreams & Nightmares Case",
    "Recoil Case",
    "Revolution Case",
    
    # --- CS2 Ära ---
    "Kilowatt Case",
    "Gallery Case"
]
    for i in csgo_cases:
        print(i)
        Datenbank_befhel_ausfuehren(f"INSERT OR IGNORE INTO gegenstand (name, typ) VALUES('{i}', 'Kiste');")



def Kisten_Preis():
    alle_daten = {}

    csgo_cases = [
    # --- Klassische & Frühe Kisten ---
    "CS:GO Weapon Case",
    "CS:GO Weapon Case 2",
    "CS:GO Weapon Case 3",
    "Winter Offensive Weapon Case",
    
    # --- eSports Kisten ---
    "eSports 2013 Case",
    "eSports 2013 Winter Case",
    "eSports 2014 Summer Case",
    
    # --- Operations Kisten ---
    "Operation Bravo Case",
    "Operation Phoenix Weapon Case",
    "Operation Breakout Weapon Case",
    "Operation Vanguard Weapon Case",
    "Operation Wildfire Case",
    "Operation Hydra Case",
    "Shattered Web Case",
    "Operation Broken Fang Case",
    "Operation Riptide Case",
    
    # --- Standard / Community Kisten ---
    "Huntsman Weapon Case",
    "Chroma Case",
    "Chroma 2 Case",
    "Chroma 3 Case",
    "Falchion Case",
    "Shadow Case",
    "Revolver Case",
    "Gamma Case",
    "Gamma 2 Case",
    "Glove Case",
    "Spectrum Case",
    "Spectrum 2 Case",
    "Clutch Case",
    "Horizon Case",
    "Danger Zone Case",
    "Prisma Case",
    "CS20 Case",
    "Prisma 2 Case",
    "Fracture Case",
    "Snakebite Case",
    "Dreams & Nightmares Case",
    "Recoil Case",
    "Revolution Case",
    
    # --- CS2 Ära ---
    "Kilowatt Case",
    "Gallery Case"
]

    for i in csgo_cases:
        print(i)
        url = f"https://steamcommunity.com/market/priceoverview/?appid=730&currency=3&market_hash_name={i}"
        
        try:
            antwort = requests.get(url)
            daten = antwort.json()
            
            # Prüfen, ob Steam uns den Preis geschickt hat
            if daten.get("success") == True:
                zeit_formatiert = datetime.now().strftime("%H:%M:%S")
                # Den niedrigsten Preis holen (oder "0,00€" falls er fehlt)
                roher_preis = daten.get("lowest_price", "0,00€")
                
                # Preis sauber machen: € weg, Striche zu Nullen, Komma zu Punkt
                sauber = roher_preis.replace('€', '').replace('-', '0').replace(',', '.').strip()
                preis_als_zahl = float(sauber)
                print(preis_als_zahl)
                print(zeit_formatiert)

                id_kiste = Datenbank_befhel_ausfuehren(f"SELECT item_id FROM gegenstand WHERE name = '{i}';")
                Datenbank_befhel_ausfuehren(f"INSERT OR IGNORE INTO preis_verlauf (item_id, preis, zeitstempel) VALUES('{id_kiste}', '{preis_als_zahl}', '{zeit_formatiert}');")
                print(f"{i} erledigt\n")
                
                
            else:
                print(f"[FEHLER] Steam hat '{i}' blockiert oder nicht gefunden.")
                alle_daten[i] = 0.00
                
        except Exception as e:
            print(f"[NETZWERKFEHLER] Bei {i}: {e}")
            alle_daten[i] = 0.00

        # WICHTIG: 2 Sekunden Pause, damit Steam uns nicht wegen Spam blockt!
        time.sleep(2)
        

if __name__ == "__main__":
    #Datenbank_befhel_ausfuehren(f"Insert INTO benutzer (benutzername, passwort_hash) Values ('Test2','123');")
    # print(Datenbank_befhel_ausfuehren("Select benutzername, passwort_hash From benutzer;"))
    os.system("cls")

