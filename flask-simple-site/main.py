from flask import Flask, render_template
from management import *
 

app = Flask(__name__)
 
@app.route("/")
def home():
    return render_template("startseite.html")

def main():
    erstelle_datenbank()

if __name__ == "__main__":
    main()
    app.run(debug=True)
    
