from flask import Flask, render_template, request
from management import *
 

app = Flask(__name__)
 
@app.route("/")
def startseite():
    return render_template("FirstPage.html")

@app.route("/login", methods=["GET", "POST"])
def einloggen():
    if request.method == "POST":
        Eingabe_Name = request.form.get("benutzername")
        Eingabe_Passwort = request.form.get("passwort")
        print(f"Veruschte Anmeldung von {Eingabe_Name}")
    return render_template("SecondPage.html")

def main():
    erstelle_datenbank()

if __name__ == "__main__":
    main()
    app.run(debug=True)
    
