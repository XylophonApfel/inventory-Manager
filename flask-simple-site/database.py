import os
import sqlite3
import sys


#DB wird da angelegt wo die exe liegt 
def _db_path():
    if getattr(sys, "frozen", False):
        base_dir = os.path.dirname(sys.executable)
    else:
        base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    return os.path.join(base_dir, "inventar_manager.db")

# Erstellt lokale SQLite-Datenbank
# Tabellen anlegen

def Datenbank_Erstellen():
    con = sqlite3.connect(_db_path())
    cursor = con.cursor()
    cursor.execute("PRAGMA foreign_keys = ON;")

    cursor.execute('''CREATE TABLE IF NOT EXISTS benutzer (
        benutzer_id INTEGER PRIMARY KEY AUTOINCREMENT,
        benutzername TEXT UNIQUE NOT NULL,
        passwort_hash TEXT NOT NULL,
        erstellt_am TEXT DEFAULT CURRENT_TIMESTAMP)''')

    cursor.execute('''CREATE TABLE IF NOT EXISTS gegenstand (
        item_id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT UNIQUE NOT NULL,
        typ TEXT)''')

    # "ON DELETE CASCADE"Löscht auch kisten zu benutzer automatisch
    cursor.execute('''CREATE TABLE IF NOT EXISTS inventar (
        inventar_id INTEGER PRIMARY KEY AUTOINCREMENT,
        benutzer_id INTEGER NOT NULL,
        item_id INTEGER NOT NULL,
        menge INTEGER DEFAULT 1,
        kaufpreis_stueck REAL,
        FOREIGN KEY (benutzer_id) REFERENCES benutzer (benutzer_id) ON DELETE CASCADE, 
        FOREIGN KEY (item_id) REFERENCES gegenstand (item_id) ON DELETE CASCADE)''')

    cursor.execute('''CREATE TABLE IF NOT EXISTS preis_verlauf (
        preis_id INTEGER PRIMARY KEY AUTOINCREMENT,
        item_id INTEGER NOT NULL,
        preis REAL NOT NULL,
        zeitstempel INTEGER NOT NULL,
        FOREIGN KEY (item_id) REFERENCES gegenstand (item_id) ON DELETE CASCADE)''')

    con.commit()
    con.close()
    print("Datenbank und Tabellen wurden erfolgreich initialisiert!")


# SQL-Befehl ausführen mit SQL-Injection
def Datenbank_Befehl_Ausfuehren(Befehl, Parameter=()):
    con = sqlite3.connect(_db_path())
    cur = con.cursor()
    
    # Prüft, ob Parameter mitgegeben wurden
    if Parameter:
        Ergebniss = cur.execute(Befehl, Parameter)
    else:
        Ergebniss = cur.execute(Befehl)

    if Ergebniss.description is not None:
        daten = Ergebniss.fetchall()
        con.close()
        return daten

    con.commit()
    con.close()
    return

# Prüfen ob ein Preis vorhanden ist
def Preis_pruefen():
    Prüfung = Datenbank_Befehl_Ausfuehren("SELECT * From preis_verlauf;")
    if len(Prüfung) == 0:
        Wert = 1
    else:
        Wert = 0

    return Wert

