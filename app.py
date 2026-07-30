from flask import Flask, g, render_template, redirect
import sqlite3

app = Flask(__name__)

DATABASE = 'database.db'

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

def query_db(query, args=(), one=False):
    cur = get_db().execute(query, args)
    rv = cur.fetchall()
    cur.close()
    return (rv[0] if rv else None) if one else rv

@app.route("/")
def hello_world():
    sql= "SELECT * FROM fishing;"
    items = query_db(sql)
    return render_template("home.html", items=items)
    
@app.route("/fish/<int:id>")
def fish_detail(id):
    sql = """
                SELECT * FROM fish WHERE id=?;"""
    fish = query_db(sql, (id,), one=True)
    return render_template("fishing.html", fish=fish)

@app.route("/Planting")
def Planting(id):
    sql= "SELECT * FROM planting;"
    items = query_db(sql)
    return render_template("planting.html",planting=planting)

@app.route("/Farm")
def Farm():
    sql= "SELECT * FROM Farm;"
    items = query_db(sql)
    return render_template("Farm.html",Farm=Farm)

@app.route("/items")
def Items(id):
    sql= "SELECT * FROM item;"
    items = query_db(sql)
    return render_template("items.html",items=items)

@app.route("/NPC")
def NPC(id):
    sql= "SELECT * FROM NPC;"
    NPC = query_db(sql)
    return render_template("NPC.html",NPC=NPC)


if __name__ == "__main__":
    app.run(debug=True)
    
