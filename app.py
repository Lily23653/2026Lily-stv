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
    
@app.route("/fishing")
def fishing():
    sql= "SELECT * FROM fishing;"
    items = query_db(sql)
    return render_template("fishing.html", items=items)

# Going to a specific fish page
@app.route("/fish/<int:id>")
def fish_detail(id):
    sql = """
                SELECT * FROM fishing WHERE id=?;"""
    fish = query_db(sql, (id,), one=True)
    if not fish:
        abort(404)
    return render_template("fish.html", fish=fish)

@app.route("/planting")
def planting():
    sql= "SELECT * FROM planting;"
    planting = query_db(sql)
    return render_template("Planting.html",planting=planting)

# Going to a specific planting page
@app.route("/planting/<int:id>")
def Plant():
    sql = """
                SELECT * FROM Planting WHERE id=?;"""
    plant = query_db(sql, (id,), one=True)
    if not plant:
        abort(404)
    return render_template("Planting.html", plant=plant)

@app.route("/Farm")
def Farm():
    sql= "SELECT * FROM Farm;"
    farm = query_db(sql)
    return render_template("Farm.html",farm=farm)

@app.route("/Farm/<int:id>")
def nongchang():
    sql = """
                SELECT * FROM farm WHERE id=?;"""
    farm = query_db(sql, (id,), one=True)
    if not farm:
        abort(404)
    return render_template("Farm.html", farm=farm)
#
@app.route("/NPC")
def NPC():
    sql= "SELECT * FROM NPC;"
    NPC = query_db(sql)
    return render_template("NPC.html",NPC=NPC)

@app.route("/NPC/<int:id>")
def NPc():
    sql = """
                SELECT * FROM NPC WHERE id=?;"""
    npc = query_db(sql, (id,), one=True)
    if not NPC:
        abort(404)
    return render_template("NPC.html", npc=npc)


if __name__ == "__main__":
    app.run(debug=True)
    
