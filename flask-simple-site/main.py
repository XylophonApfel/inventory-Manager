import os
from flask import Flask, render_template, request, session, redirect, url_for
from management import *
 
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
app = Flask(__name__, template_folder=os.path.join(BASE_DIR, "templates"))

# Passwort für Session
app.secret_key = "test"

#Hier wird die Login/Register-Seite als erste Seite beim Starten aufgerufen
@app.route("/")
def startseite():
    return render_template("LogInPage.html")

#Hier wird die abfrage der Login-Daten und die Weiterleitung zum Dashboard geregelt,
#sowie die Rückkehr zur Login-Seite, wenn die Daten falsch sind
@app.route("/login", methods=["GET", "POST"])
def einloggen():
    if request.method == "POST":
        Eingabe_Name = request.form.get("benutzername")
        Eingabe_Passwort = request.form.get("passwort")
        print(f"Veruschte Anmeldung von {Eingabe_Name}")
        Wert, Fehler = Benutzer_anmelden(Eingabe_Name, Eingabe_Passwort)
        if Wert == True:
            #Benutername Speichern
            session['benutzername'] = Eingabe_Name

            # Gesamtpreis berechen
            Gesamtpreis = Inventar_Gesamtwert_berechnen(session['benutzername'])
            if Gesamtpreis[0][0] == None:
                Gesamtpreis = 0.00
            else:
                Gesamtpreis = round(Gesamtpreis[0][0], 2)
            print(f"Gesamtpreis: {Gesamtpreis}")

            # Gesamtanzahl Items berechnen
            Gesamtanzahl = Gesamtanzahl_Items(session['benutzername'])
            Gesamtanzahl = Gesamtanzahl[0][0]
            if Gesamtanzahl == None:
                Gesamtanzahl = 0
            
            # Gewinn/Verlust berechnen
            Performance = Gewinn_Verlust(session['benutzername'])
            if Performance == None:
                Performance = 0.00
            
            # Gewinn/Verlust in Prozent
            Performance_prozent = Gewinn_Verlust_Prozent(session['benutzername'])
            if Performance_prozent == None:
                Performance_prozent = 0
            else: 
                Performance_prozent = round(Performance_prozent,2 )
            
            # Auflistung Kisten
            inventar_liste = User_Inventar_abrufen(session['benutzername'])
            if inventar_liste == None:
                inventar_liste = [("Keine Kisten", 0)]
            
            return render_template("DashboardPage.html", gesamtwert=Gesamtpreis, gesamt_items=Gesamtanzahl, gewinn=round(Performance, 2), gewinn_prozent=Performance_prozent, inv_liste=inventar_liste)
        
    return render_template("LogInPage.html", fehlermeldung=Fehler)

#Hier wird die abfrage der Registrierungs-Daten und die Weiterleitung zum Login geregelt
@app.route("/register", methods=["GET", "POST"])
def Registrieren():
    if request.method == "POST":
        Eingabe_Name = request.form.get("benutzername")
        Eingabe_Passwort = request.form.get("passwort")
        Eingabe_Passwort_confirm = request.form.get("passwort_confirm")
        print(f"Veruschte Registrierung von {Eingabe_Name}")
        Wert, Fehler = Benutzer_erstellen(Eingabe_Name, Eingabe_Passwort, Eingabe_Passwort_confirm)
        if Wert == True:
            return render_template("LogInPage.html")
        else:
            return render_template("RegisterPage.html", fehlermeldung=Fehler)
    return render_template("RegisterPage.html")

#Hier wird der Logout auf dem Dashboard geregelt, damit man sich aus seinem Account ausloggen kann
@app.route("/logout", methods=["GET"])
def logout():
    # Session Benutzer löschen
    session.pop('benutzername', None)
    return render_template("LogInPage.html")


@app.route("/item_hinzufuegen", methods=["POST", "GET"])
def item_hinzufuegen():
    # Abfrage wer der Aktuelle Benutzer ist
    aktueller_benutzer = session['benutzername']

    # Berechnung Gesamtpreis
    Gesamtpreis = Inventar_Gesamtwert_berechnen(aktueller_benutzer)
    if Gesamtpreis[0][0] == None:
        Gesamtpreis = 0.00
    else:
        Gesamtpreis = round(Gesamtpreis[0][0], 2)
    print(f"Gesamtpreis: {Gesamtpreis}")

    # Hinzufügen der Kisten
    Eingabe_kiste = request.form.get("ausgewaehlte_kiste")
    Anzahl = request.form.get("anzahl")
    Kaufpreis = request.form.get("kaufpreis")
    print(f"Es werden {Anzahl} {Eingabe_kiste} zu {aktueller_benutzer} hinzugefügt für einen Kaufpreis von {Kaufpreis} €.")
    User_Kisten_hinzufügen(aktueller_benutzer, Eingabe_kiste, Anzahl, Kaufpreis)

    # Gesamtanzahl Items berechnen
    Gesamtanzahl = Gesamtanzahl_Items(aktueller_benutzer)
    Gesamtanzahl = Gesamtanzahl[0][0]
    if Gesamtanzahl == None:
        Gesamtanzahl = 0
    
    # Gewinn/Verlust berechnen
    Performance = Gewinn_Verlust(aktueller_benutzer)
    if Performance == None:
        Performance = 0.00
    
    # Gewinn/Verlust in Prozent
    Performance_prozent = Gewinn_Verlust_Prozent(aktueller_benutzer)
    if Performance_prozent == None:
        Performance_prozent = 0
    else: 
        Performance_prozent = round(Performance_prozent,2 )

    # Auflistung Kisten
    inventar_liste = User_Inventar_abrufen(session['benutzername'])
    if inventar_liste == None:
        inventar_liste = [("Keine Kisten", 0)]
    
    return render_template("DashboardPage.html",gesamtwert=Gesamtpreis, gesamt_items=Gesamtanzahl, gewinn=round(Performance, 2), gewinn_prozent=Performance_prozent, inv_liste=inventar_liste)

def main():
    erstelle_datenbank()
    #Kisten_Preis()

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000)
    main()

