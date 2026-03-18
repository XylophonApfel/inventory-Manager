import sqlite3
import os

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

if __name__ == "__main__":
    #Datenbank_befhel_ausfuehren(f"Insert INTO benutzer (benutzername, passwort_hash) Values ('Test2','123');")
    # print(Datenbank_befhel_ausfuehren("Select benutzername, passwort_hash From benutzer;"))
    os.system("cls")
    Benutzer_erstellen("Aron", "123")
