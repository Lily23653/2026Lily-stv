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

#Main page for all fishing skills
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

#Main page for all planting information
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

#Main page for all Farm
@app.route("/Farm")
def farm_list():
    sql= "SELECT * FROM Farm;"
    farm = query_db(sql)
    return render_template("Farm.html",farm=farm)

# Going to a specific farm layout page
@app.route("/Farm/<int:id>")
def farm_detail(id):
    sql = """
                SELECT * FROM farm WHERE id=?;"""
    farm = query_db(sql, (id,), one=True)
    if not farm:
        abort(404)
    return render_template("FarmLayout.html", farm=farm)

#Main page for all NPC
@app.route("/NPC")
def npc_list():
    sql= "SELECT * FROM NPC;"
    npc = query_db(sql)
    return render_template("NPC.html",NPC=npc)

# Going to a specific NPC detail page
@app.route("/NPC/<int:id>")
def npc_detail(id):
    sql = """
                SELECT * FROM NPC WHERE id=?;"""
    npc = query_db(sql, (id,), one=True)
    if not npc:
        abort(404)
    return render_template("NPCdetail.html", npc=npc)

#filter content/Filter seaction route
@app.route("/season/<season_name>")
def season_filter(season_name):
#searching for fish and crops through seasons
    db = get_db()
    cursor = db.cursor()
    #relating to the fish table
    query_fish = """
        SELECT fish.*
        FROM fish
        JOIN seasons ON fish.season_id = seasons.id
        WHERE seasons.season_name = ?
    """
    cursor.execute(query_fish, (season_name,))
    fish_list = cursor.fetchall()

    #relating to the crops table
    query_crops = """
        SELECT planting.*
        FROM planting
        JOIN seasons ON planting.season_id = seasons.id
        WHERE seasons.season_name = ?
    """
    cursor.execute(query_crops, (season_name,))
    crop_list = cursor.fetchall()

    return render_template("season.html", season=season_name, fish_list=fish_list, crop_list=crop_list)

#Search bar section route
@app.route("/search")
def search():
    query = request.args.get('q', "").strip()
    results = {'fish': [], 'crops': [], 'npcs': [], 'farms': []}
    #search each 4 database in order
    if query:
        search_term = f"%{query}%"
        results['fish'] = query_db("SELECT * FROM fishing WHERE name LIKE ?;", (search_term,))
        results['crops'] = query_db("SELECT * FROM planting WHERE Seed LIKE ?;", (search_term,))
        results['npcs'] = query_db("SELECT * FROM NPC WHERE name LIKE ?;", (search_term,))
        results['farms'] = query_db("SELECT * FROM Farm WHERE name LIKE ?;", (search_term,))
    return render_template("search_results.html", query=query, results=results)


#If the entered web address is wrong
@app.errorhandler(404)#When the error is 404
def page_not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(500)#When the inner system went wrong (500)
def internal_server_error(e):
    return render_template('500.html'), 500


if __name__ == "__main__":
    app.run(debug=True)
