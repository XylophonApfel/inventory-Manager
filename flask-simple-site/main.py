from flask import Flask, render_template
from management import *
 

app = Flask(__name__)
 
@app.route("/")
def startseite():
    return render_template("FirstPage.html")

@app.route("/login")
def einloggen():
    return render_template("SecondPage.html")

@app.route("/signin")
def dashboard():
    return render_template("ThirdPage.html")

def main():
    erstelle_datenbank()

if __name__ == "__main__":
    main()
    app.run(debug=True)
    
