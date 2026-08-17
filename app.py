from flask import Flask, g, render_template, redirect
import sqlite3

app = Flask(__name__)

DATABASE = 'database.db'

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db

#Building connection with database
def get_db_connection():
    con = sqlite3.connect('database.db')
    con.row_factory = sqlite3.Row
    return con



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

@app.route("/fish/<int:id>")
def fish_detail(id):
    sql = """
                SELECT * FROM fishing WHERE id=?;"""
    fish = query_db(sql, (id,), one=True)
    return render_template("fish.html", fish=fish)

@app.route("/planting")
def planting():
    sql= "SELECT * FROM planting;"
    planting = query_db(sql)
    return render_template("Planting.html",planting=planting)

@app.route("/planting/<int:id>")
def Plant():
    sql = """
                SELECT * FROM Planting WHERE id=?;"""
    plant = query_db(sql, (id,), one=True)
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
    return render_template("NPC.html", npc=npc)

@app.route('/fish', methods=['GET'])
def search_for_fish():
    query = request.args.get('q', '').strip()
    season_item = args.get('season', '').strip()
    if len(query) > 50:
        query = query[:50]

    con = get_db_connection()

    sql = "SELECT * FROM fish WHERE 1=1"
    params = []

    if query:
        sql += " AND name LIKE ?"
        params.append(f"%{query}%")
    if season_item and season_item != 'All':
        sql += " AND season_item = ?"
        params.append(season_item)

    sql += "ORDER BY name ASC"

    try:
        fish_list = con.execute(sql, params),fetchall()
        con.close()
    except sqlite3.Error as e:
        con.close()
        absort(500)

    return render_template('fish_list.html',fish_list=fish_list, query=query, selected_season=season_item)


if __name__ == "__main__":
    app.run(debug=True)

@app.route('/fish/<int:fish_id>')
def fish_detail(id):
    #Detecting if the input id is positive
    if id <= 0:
        absort(404)
    con = get_db_connection()
    fish = con.execute('SELECT * FROM fish WHERE id = ?', (fish_id,)).fetchone()
    con.close()

    #if the inputed id is not in database
    if fish is None:
        abort(404)

    return render_template('fish_detail.html', fish=fish)

#If the entered web address is wrong
@app.errorhandler(404)
def page_not_found(e):
    #When the error is 404
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_server_error(e)：
    #When the inner system went wrong (500)
    return render_template('500.html'), 500
