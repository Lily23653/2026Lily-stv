from flask import Flask, g, render_template, redirect, abort, request
import sqlite3

app = Flask(__name__)
DATABASE = 'database.db'

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
        db.row_factory = sqlite3.Row
    return db

#Building connection with database
def get_db_connection(exception):
    db= getattr(g, "_database", None)
    if db is not None:
        db.close()

def query_db(query, args=(), one=False):
    cur = get_db().execute(query, args)
    rv = cur.fetchall()
    cur.close()
    return (rv[0] if rv else None) if one else rv

#route to other pages
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
def plant_detail(id):
    sql = """
                SELECT * FROM planting WHERE id=?;"""
    plant = query_db(sql, (id,), one=True)
    if not plant:
        abort(404)
    return render_template("plant.html", plant=plant)

@app.route("/Farm")
def farm_list():
    sql= "SELECT * FROM Farm;"
    farm = query_db(sql)
    return render_template("Farm.html",farm=farm)

@app.route("/Farm/<int:id>")
def farm_detail(id):
    sql = """
                SELECT * FROM farm WHERE id=?;"""
    farm = query_db(sql, (id,), one=True)
    if not farm:
        abort(404)
    return render_template("Farm.html", farm=farm)

@app.route("/NPC")
def npc_list():
    sql= "SELECT * FROM NPC;"
    npc = query_db(sql)
    return render_template("NPC.html",NPC=npc)

@app.route("/NPC/<int:id>")
def npc_detail(id):
    sql = """
                SELECT * FROM NPC WHERE id=?;"""
    npc = query_db(sql, (id,), one=True)
    if not npc:
        abort(404)
    return render_template("NPC.html", npc=npc)

#filter content
@app.route("/season/<season_name>")
def season_filter(season_name):
    #searching for specofoc season and including "All" and "Any"
    sql_fish = """
    SELECT * FROM fishing 
    WHERE season LIKE ? OR Season LIKE '%All%' OR Season LIKE '%Any%';
    """
    fishes = query_db(sql_fish, ("%" + season_name + "%"))

    #search in planting
    sql_plant = """
    SELECT * FROM planting 
    WHERE season LIKE ? OR Season LIKE '%All%' OR Season LIKE '%Any%';
    """
    plants = query_db(sql_plant, ("%" + season_name + "%"))
    return render_template("season.html", season=season_name, fishes=fishes, plants=plants)

@app.route('/fish', methods=['GET'])
def search_for_fish():
    query = request.args.get('q', "").strip()[:50]
    season_item = request.args.get('season', '').strip()

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
        fish_list = query_db(sql, params)
    except sqlite3.Error:
        abort(500)

    return render_template('fish_list.html',fish_list=fish_list, query=query, selected_season=season_item)

#If the entered web address is wrong
@app.errorhandler(404)
def page_not_found(e):
    #When the error is 404
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_server_error(e):
    #When the inner system went wrong (500)
    return render_template('500.html'), 500


if __name__ == "__main__":
    app.run(debug=True)
