import sqlite3
import os
import requests
import time
from datetime import datetime
from werkzeug.security import generate_password_hash
from werkzeug.security import check_password_hash

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

def Datenbank_befehl_ausfuehren(Befehl):
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

def Benutzer_erstellen(Benutzername, Passwort, Passwort_confirm):
    wert = Benutzer_vorhanden(Benutzername)
    if Passwort != Passwort_confirm:
        wert = 2
    Passwort_Hash = generate_password_hash(Passwort)

    if wert == 0:
        print("Benutzer anlegen")
        Datenbank_befehl_ausfuehren(f"Insert INTO benutzer (benutzername, passwort_hash) Values ('{Benutzername}','{Passwort_Hash}');")
        Fehler = ""
        return 1, Fehler

    elif wert == 1:
        print("Benutzer bereits vorhanden!")
        Fehler = "Benutzer bereits vorhanden!"
        return 0, Fehler
    
    elif wert == 2:
        print("Passwort ist nicht gleich!")
        Fehler = "Passwort ist nicht gleich!"
        return 0, Fehler



def Benutzer_vorhanden(Benutzername):
    Ergebniss = Datenbank_befehl_ausfuehren("Select benutzername from benutzer;")
    Liste_Benutzer = []

    if Ergebniss is not None:
        for i in Ergebniss:
            Liste_Benutzer.append(i[0])
        
    if Benutzername in Liste_Benutzer:
       print("Benutzer bereits vorhanden!")
       wert = 1
    else:
       print("Benutzer noch nicht vorhanden")
       wert = 0
    
    return wert


def Benutzer_anmelden(Benutzername, Passwort):
    #Passwort_hash = hash(Passwort)
    print(Benutzername)
    try:
        Ergebniss = Datenbank_befehl_ausfuehren(f"Select passwort_hash From benutzer Where benutzername ='{Benutzername}';")
        print(Ergebniss)
        #print(Passwort_hash)
        if Ergebniss is None or len(Ergebniss) == 0:
            print("Bitte geben Sie einen gültigen Benutzernamen ein!")
            Fehler = "Bitte geben Sie einen gültigen Benutzernamen ein!"
            return 0, Fehler
        print(f"Gefundenes Passwort-Hash: {Ergebniss[0][0]}")
        if check_password_hash(Ergebniss[0][0], Passwort):
            print("Richtig!")
            Fehler= ""
            return 1, Fehler
        else:
            print("Bitte geben Sie ein gültiges Passwort ein!")
            Fehler = "Bitte geben Sie ein gültiges Passwort ein!"
            return 0, Fehler  
    except Exception as e:
        print(f"Fehler beim Anmelden: {e}")
        return 0

def Inventar_Gesamtwert_berechnen(Benutzername):
    User_ID = User_ID_Finden(Benutzername)
    Gesamtwert = Datenbank_befehl_ausfuehren(f"SELECT SUM(i.menge * (SELECT p.preis FROM preis_verlauf p WHERE p.item_id = i.item_id ORDER BY p.zeitstempel DESC LIMIT 1)) FROM inventar i WHERE i.benutzer_id = {User_ID};")
    return Gesamtwert

def Gesamtausgaben_berechnen(Benutzername):
    User_ID = User_ID_Finden(Benutzername)
    Gesamtausgaben = Datenbank_befehl_ausfuehren(f"SELECT SUM(menge*kaufpreis_stueck) AS Ausgaben From inventar WHERE benutzer_id = {User_ID};")
    return Gesamtausgaben

def Gewinn_Verlust(Benutzername):
    Gesamtwert = Inventar_Gesamtwert_berechnen(Benutzername)
    Gesamtwert = Gesamtwert[0][0]
    Gesamtausgaben = Gesamtausgaben_berechnen(Benutzername)
    Gesamtausgaben = Gesamtausgaben[0][0]
    Berechnung = float(Gesamtwert) - float(Gesamtausgaben)
    return Berechnung


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
        Datenbank_befehl_ausfuehren(f"INSERT OR IGNORE INTO gegenstand (name, typ) VALUES('{i}', 'Kiste');")


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
        print(f"Lade Daten für: {i}")
        url = f"https://steamcommunity.com/market/priceoverview/?appid=730&currency=3&market_hash_name={i}"
        
        try:
            antwort = requests.get(url)
            daten = antwort.json()
            
            # Prüfen, ob Steam uns den Preis geschickt hat
            if daten.get("success") == True:
                # 1. Daten für die Speicherung vorbereiten
                zeit_formatiert = datetime.now().strftime("%Y-%m-%d %H:%M:%S") # Z.B. 2026-04-10 14:30:00
                heute_datum = datetime.now().strftime("%Y-%m-%d")               # Z.B. 2026-04-10
                
                # Den niedrigsten Preis holen (oder "0,00€" falls er fehlt)
                roher_preis = daten.get("lowest_price", "0,00€")
                
                # Preis sauber machen: € weg, Striche zu Nullen, Komma zu Punkt
                sauber = roher_preis.replace('€', '').replace('-', '0').replace(',', '.').strip()
                preis_als_zahl = float(sauber)
                
                print(f"Gefundener Preis bei Steam: {preis_als_zahl}€")

                # 2. ID der Kiste suchen
                ergebnis = Datenbank_befehl_ausfuehren(f"SELECT item_id FROM gegenstand WHERE name = '{i}';")
                
                if ergebnis:
                    # Die nackte ID aus der Tupel/Listen-Antwort extrahieren
                    if isinstance(ergebnis, list) and len(ergebnis) > 0:
                        id_kiste = ergebnis[0][0]
                    elif isinstance(ergebnis, tuple):
                        id_kiste = ergebnis[0]
                    else:
                        id_kiste = ergebnis
                        
                    # Prüfen, ob heute schon ein Preis existiert
                    check_heute = Datenbank_befehl_ausfuehren(f"SELECT preis_id FROM preis_verlauf WHERE item_id = {id_kiste} AND zeitstempel LIKE '{heute_datum}%';")
                    
                    if not check_heute: # Wenn die Liste leer ist (also noch kein Preis da)
                        Datenbank_befehl_ausfuehren(f"INSERT INTO preis_verlauf (item_id, preis, zeitstempel) VALUES ({id_kiste}, {preis_als_zahl}, '{zeit_formatiert}');")
                        print(f"[{i}] -> NEUER Preis für heute ({heute_datum}) in DB gespeichert!\n")
                    else:
                        print(f"[{i}] -> Übersprungen: Für heute existiert bereits ein Preis!\n")
                        
                else:
                    print(f"[WARNUNG] Kiste '{i}' existiert noch nicht in der Tabelle 'gegenstand'! Bitte erst anlegen.\n")
                    
            else:
                print(f"[FEHLER] Steam hat '{i}' blockiert oder nicht gefunden.\n")
                alle_daten[i] = 0.00
                
        except Exception as e:
            print(f"[NETZWERKFEHLER] Bei {i}: {e}\n")
            alle_daten[i] = 0.00

        # WICHTIG: 2 Sekunden Pause, damit Steam uns nicht wegen Spam blockt!
        time.sleep(2)

def hash(passwort):
    sicherer_hash = generate_password_hash(passwort)
    return sicherer_hash

def User_Kisten_hinzufügen(Benutzer, Kiste, Anzahl, Kaufpreis):
    Benutzer_ID = User_ID_Finden(Benutzer)
    Kiste_ID = Kiste_ID_Finden(Kiste)
    Abfrage_ob_kiste_vorhanden = Datenbank_befehl_ausfuehren(f"SELECT * FROM inventar WHERE benutzer_id = {Benutzer_ID} AND item_id = {Kiste_ID};")
    print(f"länge: {len(Abfrage_ob_kiste_vorhanden)}")
    if len(Abfrage_ob_kiste_vorhanden) >= 1:
        aktuelle_anzahl = Datenbank_befehl_ausfuehren(f"SELECT menge FROM inventar WHERE benutzer_id = {Benutzer_ID} AND item_id = {Kiste_ID};")
        neue_anzahl = int(aktuelle_anzahl[0][0]) + int(Anzahl)
        Abfrage_Kaufpreis = Datenbank_befehl_ausfuehren(f"SELECT kaufpreis_stueck FROM inventar WHERE benutzer_id = {Benutzer_ID} AND item_id = {Kiste_ID};")
        Durchschnitt_Kaufpreis = ((float(Abfrage_Kaufpreis[0][0]) * int(aktuelle_anzahl[0][0])) + (int(Anzahl) * float(Kaufpreis)))/int(neue_anzahl)
        Durchschnitt_Kaufpreis = round(Durchschnitt_Kaufpreis, 2)
        print(Durchschnitt_Kaufpreis)
        Datenbank_befehl_ausfuehren(f"UPDATE inventar SET menge = {neue_anzahl}, kaufpreis_stueck = {Durchschnitt_Kaufpreis}  WHERE benutzer_id = {Benutzer_ID} and item_id = {Kiste_ID};")
        print("Die Kisten wurden geändert")
    else:
        Datenbank_befehl_ausfuehren(f"INSERT INTO inventar (benutzer_id, item_id, menge, kaufpreis_stueck) VALUES({Benutzer_ID}, {Kiste_ID}, {Anzahl}, {Kaufpreis});")
        print("Die Kisten wurden hinzugefügt")

def User_ID_Finden(Benutzername):
    Benutzer_ID = Datenbank_befehl_ausfuehren(f"SELECT benutzer_id FROM benutzer WHERE benutzername = '{Benutzername}';")
    Benutzer_ID = Benutzer_ID[0][0]
    print(f"Die Benutzer ID ist {Benutzer_ID}.")
    return Benutzer_ID

def Kiste_ID_Finden(Kiste):
    Kiste_ID = Datenbank_befehl_ausfuehren(f"SELECT item_id FROM gegenstand WHERE name = '{Kiste}';")
    Kiste_ID = Kiste_ID[0][0]
    print(f"Die Kisten ID ist {Kiste_ID}.")
    return Kiste_ID

def Gesamtanzahl_Items(Benutzername):
    User_ID = User_ID_Finden(Benutzername)
    Gesamtanzahl = Datenbank_befehl_ausfuehren(f"SELECT SUM(menge) AS 'Gesamtanzahl' From inventar WHERE benutzer_id = {User_ID};")
    return Gesamtanzahl

if __name__ == "__main__":
    #Datenbank_befhel_ausfuehren(f"Insert INTO benutzer (benutzername, passwort_hash) Values ('Test2','123');")
    # print(Datenbank_befhel_ausfuehren("Select benutzername, passwort_hash From benutzer;"))
    # Benutzer_anmelden("Test", "123")
    #Benutzer_erstellen("Admin1", "Admin123")
    #User_ID_Finden("Aron")
    #Kiste_ID_Finden("eSports 2013 Case")
    #User_Kisten_hinzufügen("Aron", "Revolution Case", 5, 3.42)
    os.system("cls")