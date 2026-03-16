import sqlite3

def Datenbank():
    con = sqlite3.connect("Managment.db")

    cur = con.cursor()
    cur.execute("CREATE TABLE movie(title, year, score)")
    con.commit()

    con.close()

    return
