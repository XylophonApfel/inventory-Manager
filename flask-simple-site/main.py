import os
import json
from flask import Flask, render_template, request, session, redirect, url_for
from management import *
from database import *
 
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
app = Flask(__name__, template_folder=os.path.join(BASE_DIR, "templates"))

# Passwort für Session
app.secret_key = "test"

# Login/Register-Seite aufrufen
@app.route("/")
def startseite():
    return render_template("LogInPage.html")

# Logindaten abfragen
@app.route("/login", methods=["GET", "POST"])
def einloggen():
    if request.method == "POST":
        Eingabe_Name = request.form.get("benutzername")
        Eingabe_Passwort = request.form.get("passwort")
        
        Wert, Fehler = Benutzer_anmelden(Eingabe_Name, Eingabe_Passwort)
        
        if Wert == True:
            # Benutzername Speichern
            session['benutzername'] = Eingabe_Name
            
            return redirect(url_for('dashboard_anzeigen'))


    return render_template("LogInPage.html", fehlermeldung=Fehler)

# Registrierungs-Daten abfragen
@app.route("/register", methods=["GET", "POST"])
def Registrieren():
    if request.method == "POST":
        Eingabe_Name = request.form.get("benutzername")
        Eingabe_Passwort = request.form.get("passwort")
        Eingabe_Passwort_confirm = request.form.get("passwort_confirm")
        
        Wert, Fehler = Benutzer_erstellen(Eingabe_Name, Eingabe_Passwort, Eingabe_Passwort_confirm)
        
        if Wert == True:
            return render_template("LogInPage.html")
        else:
            return render_template("RegisterPage.html", fehlermeldung=Fehler)
            
    return render_template("RegisterPage.html")

@app.route("/dashboard")
def dashboard_anzeigen():
    if 'benutzername' not in session:
        return redirect(url_for('startseite'))
        
    aktueller_benutzer = session['benutzername']
    
    # Alle Werte für das Dashboard laden
    G_Preis, G_Anzahl, Perf, Perf_Proz, Inv_Liste, Labels, Werte = Dashboard_Werte_abrufen(aktueller_benutzer)
    return render_template("DashboardPage.html", gesamtwert=G_Preis, gesamt_items=G_Anzahl, gewinn=Perf, gewinn_prozent=Perf_Proz, inv_liste=Inv_Liste, chart_labels=json.dumps(Labels), chart_data=json.dumps(Werte))


# Session löschen und abmelden
@app.route("/logout", methods=["GET"])
def logout():
    session.pop('benutzername', None)
    return render_template("LogInPage.html")

# Kisten in Datenbank schreiben
@app.route("/item_hinzufuegen", methods=["POST", "GET"])
def item_hinzufuegen():
    aktueller_benutzer = session['benutzername']

    # Eingaben abfangen
    Eingabe_kiste = request.form.get("ausgewaehlte_kiste")
    Anzahl = request.form.get("anzahl")
    Kaufpreis = request.form.get("kaufpreis")
    
    # Kiste hinzufügen
    User_Kisten_hinzufuegen(aktueller_benutzer, Eingabe_kiste, Anzahl, Kaufpreis)

    return redirect(url_for('dashboard_anzeigen'))
    
# Kisten aus Datenbank löschen
@app.route("/item_loeschen", methods=["POST"])
def item_loeschen():
    if 'benutzername' not in session:
        return redirect(url_for('login'))
    
    kisten_name = request.form.get("kisten_name")
    aktueller_benutzer = session['benutzername']

    # Funktion zum Löschen aufrufen
    User_Item_loeschen(aktueller_benutzer, kisten_name)
    return redirect(url_for('dashboard_anzeigen'))
   
def main():
    Datenbank_Erstellen()
    # Kisten_Preis()

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000)
    main()

