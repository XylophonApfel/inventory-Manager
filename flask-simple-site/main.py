import os
from flask import Flask, render_template, request
from management import *
 
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
app = Flask(__name__, template_folder=os.path.join(BASE_DIR, "templates"))
 
@app.route("/")
def startseite():
    return render_template("LogInPage.html")

@app.route("/login", methods=["GET", "POST"])
def einloggen():
    if request.method == "POST":
        Eingabe_Name = request.form.get("benutzername")
        Eingabe_Passwort = request.form.get("passwort")
        print(f"Veruschte Anmeldung von {Eingabe_Name}")
        Wert = Benutzer_anmelden(Eingabe_Name, Eingabe_Passwort)
        if Wert == True:
            return render_template("DashboardPage.html")
        
    return render_template("LogInPage.html")

@app.route("/register", methods=["GET", "POST"])
def Registrieren():
    if request.method == "POST":
        Eingabe_Name = request.form.get("benutzername")
        Eingabe_Passwort = request.form.get("passwort")
        Eingabe_Passwort_confirm = request.form.get("passwort_confirm")
        print(f"Veruschte Registrierung von {Eingabe_Name}")
        Wert = Benutzer_erstellen(Eingabe_Name, Eingabe_Passwort, Eingabe_Passwort_confirm)
        if Wert == True:
            return render_template("LogInPage.html")
    return render_template("RegisterPage.html")

@app.route("/item_hinzufuegen", methods=["POST", "GET"])
def item_hinzufuegen():
    Eingabe = request.form.get("ausgewaehlte_kiste")
    print(Eingabe)
    return render_template("DashboardPage.html")

def main():
    erstelle_datenbank()

if __name__ == "__main__":
    main()
    app.run(host="127.0.0.1", port=5000)

