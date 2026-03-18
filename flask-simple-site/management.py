import sqlite3

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
    con = sqlite3.connect('inventar_manager.db')

    cur = con.cursor()
    Ergebniss = cur.execute(Befehl)
    con.commit()

    con.close()
    return (Ergebniss)

def Benutzer_erstellen(Benutzername, Passwort):
    wert = Benutzer_vorhanden(Benutzername)

    if wert == 0:
        Datenbank_befhel_ausfuehren(f"Insert INTO benutzer (benutzername, passwort_hash) Values ('{Benutzername}','{Passwort}');")
        Datenbank_befhel_ausfuehren(f"Insert INTO benutzer (benutzername, passwort_hash) Values ('Test','123');")

    elif wert == 1:
        print("Benutzer bereits vorhanden!")



def Benutzer_vorhanden(Benutzername):
    pass

def Benutzer_anmelden(Benutzername, Passwort):
    Ergebniss = Datenbank_befhel_ausfuehren("Select * From benutzer;")
    print(Ergebniss)

def Inventar_Gesamtwert_berechnen():
    pass

def Item_Gesamtwert_berechnen():
    pass