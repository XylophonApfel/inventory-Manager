import sqlite3
import os
import requests
import time
from datetime import datetime
from werkzeug.security import generate_password_hash
from werkzeug.security import check_password_hash
from database import *

# ==========================================
# BENUTZER LOGIK
# ==========================================

# Erstellt einen neuen Benutzer
def Benutzer_erstellen(Benutzername, Passwort, Passwort_confirm):
    wert = Benutzer_vorhanden(Benutzername)
    if Passwort != Passwort_confirm:
        wert = 2
        
    Passwort_Hash = generate_password_hash(Passwort)

    if wert == 0:
        Datenbank_Befehl_Ausfuehren(f"INSERT INTO benutzer (benutzername, passwort_hash) VALUES ('{Benutzername}','{Passwort_Hash}');")
        Fehler = ""
        return True, Fehler
    elif wert == 1:
        Fehler = "Benutzer bereits vorhanden!"
        return False, Fehler
    elif wert == 2:
        Fehler = "Passwörter stimmen nicht überein!"
        return False, Fehler

# Prüft ob Benutzer schon existiert
def Benutzer_vorhanden(Benutzername):
    Ergebniss = Datenbank_Befehl_Ausfuehren("SELECT benutzername FROM benutzer;")
    Liste_Benutzer = []

    if Ergebniss is not None:
        for i in Ergebniss:
            Liste_Benutzer.append(i[0])
        
    if Benutzername in Liste_Benutzer:
       wert = 1
    else:
       wert = 0
    return wert

# Loggt den Benutzer ein
def Benutzer_anmelden(Benutzername, Passwort):
    try:
        Ergebniss = Datenbank_Befehl_Ausfuehren(f"SELECT passwort_hash FROM benutzer WHERE benutzername ='{Benutzername}';")
        
        if Ergebniss is None or len(Ergebniss) == 0:
            Fehler = "Bitte geben Sie einen gültigen Benutzernamen ein!"
            return False, Fehler
            
        if check_password_hash(Ergebniss[0][0], Passwort):
            Fehler = ""
            return True, Fehler
        else:
            Fehler = "Bitte geben Sie ein gültiges Passwort ein!"
            return False, Fehler  
    except Exception as e:
        print(f"Fehler beim Anmelden: {e}")
        return False, "Systemfehler"

# Findet die ID eines Benutzers
def User_ID_Finden(Benutzername):
    Benutzer_ID = Datenbank_Befehl_Ausfuehren(f"SELECT benutzer_id FROM benutzer WHERE benutzername = '{Benutzername}';")
    return Benutzer_ID[0][0]

# Findet die ID einer Kiste
def Kiste_ID_Finden(Kiste):
    Kiste_ID = Datenbank_Befehl_Ausfuehren(f"SELECT item_id FROM gegenstand WHERE name = '{Kiste}';")
    return Kiste_ID[0][0]

# ==========================================
# INVENTAR LOGIK
# ==========================================

# Fügt Kisten hinzu oder updatet die Menge/Preis
def User_Kisten_hinzufuegen(Benutzer, Kiste, Anzahl, Kaufpreis):
    Benutzer_ID = User_ID_Finden(Benutzer)
    Kiste_ID = Kiste_ID_Finden(Kiste)
    Abfrage = Datenbank_Befehl_Ausfuehren(f"SELECT menge, kaufpreis_stueck FROM inventar WHERE benutzer_id = {Benutzer_ID} AND item_id = {Kiste_ID};")
    
    if Abfrage:
        aktuelle_anzahl = int(Abfrage[0][0])
        alter_kaufpreis = float(Abfrage[0][1])
        neue_anzahl = aktuelle_anzahl + int(Anzahl)
        
        Durchschnitt_Kaufpreis = ((alter_kaufpreis * aktuelle_anzahl) + (int(Anzahl) * float(Kaufpreis))) / neue_anzahl
        Durchschnitt_Kaufpreis = round(Durchschnitt_Kaufpreis, 2)
        
        Datenbank_Befehl_Ausfuehren(f"UPDATE inventar SET menge = {neue_anzahl}, kaufpreis_stueck = {Durchschnitt_Kaufpreis} WHERE benutzer_id = {Benutzer_ID} AND item_id = {Kiste_ID};")
    else:
        Datenbank_Befehl_Ausfuehren(f"INSERT INTO inventar (benutzer_id, item_id, menge, kaufpreis_stueck) VALUES({Benutzer_ID}, {Kiste_ID}, {Anzahl}, {Kaufpreis});")

# Löscht eine komplette Kisten-Position
def User_Item_loeschen(Benutzername, Kisten_name):
    User_ID = User_ID_Finden(Benutzername)
    Kisten_ID = Kiste_ID_Finden(Kisten_name)
    Datenbank_Befehl_Ausfuehren(f"DELETE FROM inventar WHERE benutzer_id = {User_ID} AND item_id = {Kisten_ID};")

# Holt alle Items für die Liste
def User_Inventar_abrufen(Benutzername):
    User_ID = User_ID_Finden(Benutzername)
    Ergebnis = Datenbank_Befehl_Ausfuehren(f"SELECT g.name, i.menge, i.kaufpreis_stueck FROM inventar i JOIN gegenstand g ON i.item_id = g.item_id WHERE i.benutzer_id = {User_ID} ORDER BY i.menge DESC;")
    return Ergebnis

# ==========================================
# BERECHNUNGEN
# ==========================================

# Berechnet aktuellen Wert
def Inventar_Gesamtwert_berechnen(Benutzername):
    User_ID = User_ID_Finden(Benutzername)
    Gesamtwert = Datenbank_Befehl_Ausfuehren(f"SELECT SUM(i.menge * (SELECT p.preis FROM preis_verlauf p WHERE p.item_id = i.item_id ORDER BY p.zeitstempel DESC LIMIT 1)) FROM inventar i WHERE i.benutzer_id = {User_ID};")
    return Gesamtwert

# Berechnet ausgegebenes Geld
def Gesamtausgaben_berechnen(Benutzername):
    User_ID = User_ID_Finden(Benutzername)
    Gesamtausgaben = Datenbank_Befehl_Ausfuehren(f"SELECT SUM(menge*kaufpreis_stueck) AS Ausgaben FROM inventar WHERE benutzer_id = {User_ID};")
    return Gesamtausgaben

# Addiert alle Kistenmengen
def Gesamtanzahl_Items(Benutzername):
    User_ID = User_ID_Finden(Benutzername)
    Gesamtanzahl = Datenbank_Befehl_Ausfuehren(f"SELECT SUM(menge) AS 'Gesamtanzahl' FROM inventar WHERE benutzer_id = {User_ID};")
    return Gesamtanzahl

# Gewinn oder Verlust in Euro
def Gewinn_Verlust(Benutzername):
    Gesamtwert = Inventar_Gesamtwert_berechnen(Benutzername)[0][0]
    if Gesamtwert == None:
        Gesamtwert = 0
        
    Gesamtausgaben = Gesamtausgaben_berechnen(Benutzername)[0][0]
    if Gesamtausgaben == None:
        Gesamtausgaben = 0
        
    Berechnung = float(Gesamtwert) - float(Gesamtausgaben)
    return Berechnung

# Gewinn in Prozent
def Gewinn_Verlust_Prozent(Benutzername):
    Gesamtwert = Inventar_Gesamtwert_berechnen(Benutzername)[0][0]
    if Gesamtwert == None:
        Gesamtwert = 0
        
    Gesamtausgaben = Gesamtausgaben_berechnen(Benutzername)[0][0]
    if Gesamtausgaben == None:
        Gesamtausgaben = 0
        
    if Gesamtwert == 0 or Gesamtausgaben == 0:
        Prozent = 0
    else:
        Prozent = ((Gesamtwert - Gesamtausgaben) / Gesamtausgaben) * 100
    return Prozent

# Berechnet Historie für Chart.js
def Portfolio_Historie_berechnen(Benutzername):
    User_ID = User_ID_Finden(Benutzername)
    Befehl = f"""
        SELECT DATE(p.zeitstempel) as tag, SUM(i.menge * p.preis) as gesamt_wert
        FROM inventar i
        JOIN preis_verlauf p ON i.item_id = p.item_id
        WHERE i.benutzer_id = {User_ID}
        GROUP BY tag
        ORDER BY tag ASC
        LIMIT 7;
    """
    Ergebnis = Datenbank_Befehl_Ausfuehren(Befehl)
    
    labels = []
    werte = []
    
    if Ergebnis:
        for zeile in Ergebnis:
            labels.append(zeile[0])
            werte.append(round(zeile[1], 2))
            
    return labels, werte

# Bündelt alle Werte für die Routen in main.py
def Dashboard_Werte_abrufen(Benutzername):
    Gesamtpreis_Roh = Inventar_Gesamtwert_berechnen(Benutzername)[0][0]
    if Gesamtpreis_Roh == None:
        Gesamtpreis = 0.00
    else:
        Gesamtpreis = round(Gesamtpreis_Roh, 2)
        
    Gesamtanzahl_Roh = Gesamtanzahl_Items(Benutzername)[0][0]
    if Gesamtanzahl_Roh == None:
        Gesamtanzahl = 0
    else:
        Gesamtanzahl = Gesamtanzahl_Roh

    Performance_Roh = Gewinn_Verlust(Benutzername)
    if Performance_Roh == None:
        Performance = 0.00
    else:
        Performance = round(Performance_Roh, 2)

    Performance_prozent_Roh = Gewinn_Verlust_Prozent(Benutzername)
    if Performance_prozent_Roh == None:
        Performance_prozent = 0
    else:
        Performance_prozent = round(Performance_prozent_Roh, 2)

    inventar_liste = User_Inventar_abrufen(Benutzername)
    if inventar_liste == None:
        inventar_liste = [("Keine Kisten", 0, 0.00)]
        
    labels, werte = Portfolio_Historie_berechnen(Benutzername)
    
    return Gesamtpreis, Gesamtanzahl, Performance, Performance_prozent, inventar_liste, labels, werte

# ==========================================
# STEAM API
# ==========================================

csgo_cases = [
    "Chroma Case", "Chroma 2 Case", "Chroma 3 Case", "Clutch Case", 
    "CS20 Case", "CS:GO Weapon Case", "CS:GO Weapon Case 2", "CS:GO Weapon Case 3", 
    "Danger Zone Case", "Dreams & Nightmares Case", "eSports 2013 Case", 
    "eSports 2013 Winter Case", "eSports 2014 Summer Case", "Falchion Case", 
    "Fracture Case", "Gallery Case", "Gamma Case", "Gamma 2 Case", 
    "Glove Case", "Horizon Case", "Huntsman Weapon Case", "Kilowatt Case", 
    "Operation Bravo Case", "Operation Breakout Weapon Case", "Operation Broken Fang Case", 
    "Operation Hydra Case", "Operation Phoenix Weapon Case", "Operation Riptide Case", 
    "Operation Vanguard Weapon Case", "Operation Wildfire Case", "Prisma Case", 
    "Prisma 2 Case", "Recoil Case", "Revolution Case", "Revolver Case", 
    "Shadow Case", "Shattered Web Case", "Snakebite Case", "Spectrum Case", 
    "Spectrum 2 Case", "Winter Offensive Weapon Case"
]

def Kisten_In_Datenbanken_anlegen():
    for i in csgo_cases:
        Datenbank_Befehl_Ausfuehren(f"INSERT OR IGNORE INTO gegenstand (name, typ) VALUES('{i}', 'Kiste');")

def Kisten_Preis():
    for i in csgo_cases:
        print(f"Lade Daten für: {i}")
        url = f"https://steamcommunity.com/market/priceoverview/?appid=730&currency=3&market_hash_name={i}"
        try:
            antwort = requests.get(url).json()
            if antwort.get("success") == True:
                preis = float(antwort.get("lowest_price", "0,00€").replace('€', '').replace('-', '0').replace(',', '.').strip())
                id_kiste = Kiste_ID_Finden(i)
                heute = datetime.now().strftime("%Y-%m-%d")
                
                check = Datenbank_Befehl_Ausfuehren(f"SELECT preis_id FROM preis_verlauf WHERE item_id = {id_kiste} AND zeitstempel LIKE '{heute}%';")
                if not check:
                    Datenbank_Befehl_Ausfuehren(f"INSERT INTO preis_verlauf (item_id, preis, zeitstempel) VALUES ({id_kiste}, {preis}, '{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}');")
        except Exception as e:
            pass
        time.sleep(2)