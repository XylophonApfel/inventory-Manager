from flask import Flask, render_template
from management import *
 

app = Flask(__name__)
 
@app.route("/")
def home():
    return render_template("startseite.html")

def main():
    Datenbank()

if __name__ == "__main__":
    app.run(debug=True)
    main()
    
