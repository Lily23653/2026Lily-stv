from flask import Flask, g, render_template, redirect, abort, request
import sqlite3

#initialize the Flask application instance
app = Flask(__name__)
DATABASE = 'database.db' #Database file location constant

#Helper function to establish and manage SQLite database connections
def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
        # Enable foreign key constraints to maintain relational integrity
        db.execute('PRAGMA foreign_keys = ON;')
        #enable accessing query results as dictionary rows
        db.row_factory = sqlite3.Row
    return db

#automatically close satabase connection when request context ends
@app.teardown_appcontext
def close_db_connection(exception):
    db= getattr(g, "_database", None)
    if db is not None:
        db.close()


#generic helper function for executing SQL queries safely with parameterized inputs (?,)
# Prevents SQL Injection security vulnerabilities
def query_db(query, args=(), one=False):
    cur = get_db().execute(query, args)
    rv = cur.fetchall()
    cur.close()
    return (rv[0] if rv else None) if one else rv

#Detail routes:

#homepage route that fetches overview item records for display
@app.route("/")
def hello_world():
    sql= "SELECT * FROM fishing;"
    items = query_db(sql)
    return render_template("home.html", items=items)

#main fishing list route, fetches all catchable fish records
@app.route("/fishing")
def fishing():
    sql= "SELECT * FROM fishing;"
    items = query_db(sql)
    return render_template("fishing.html", items=items)

# Going to a specific fish detail route, uses parameterized ID query and aborts to 404 if record is missing
@app.route("/fish/<int:id>")
def fish_detail(id):
    sql = """
                SELECT * FROM fishing WHERE id=?;"""
    fish = query_db(sql, (id,), one=True)
    if not fish:
        abort(404)
    return render_template("fish.html", fish=fish)

#Main planting page route, fetches all crop and seed data
@app.route("/planting")
def planting():
    sql= "SELECT * FROM planting;"
    planting = query_db(sql)
    return render_template("plantings.html",planting=planting)

#Individual planting detail route: displays specific crop details or returns 404
@app.route("/planting/<int:id>")
def plant_detail(id):
    sql = """
                SELECT * FROM planting WHERE id=?;"""
    plant = query_db(sql, (id,), one=True)
    if not plant:
        abort(404)
    return render_template("plant.html", plant=plant)

#Main farm layout list route, fetches all available farm setups
@app.route("/farm")
def farm_list():
    sql= "SELECT * FROM farm;"
    farm = query_db(sql)
    return render_template("farms.html",farm=farm)

#Individual farm detail route: fetches specifications for a selected farm layout ID
@app.route("/farm/<int:id>")
def farm_detail(id):
    sql = """
                SELECT * FROM farm WHERE id=?;"""
    farm = query_db(sql, (id,), one=True)
    if not farm:
        abort(404)
    return render_template("farmlayouts.html", farm=farm)

#Main villager list route, fetches all NPC data from the database
@app.route("/npc")
def npc_list():
    sql= "SELECT * FROM npc;"
    npc = query_db(sql)
    return render_template("npcs.html",NPC=npc)

#Individual NPC detail route, fetches gift preferences and location data for a villager ID
@app.route("/npc/<int:id>")
def npc_detail(id):
    sql = """
                SELECT * FROM npc WHERE id=?;"""
    npc = query_db(sql, (id,), one=True)
    if not npc:
        abort(404)
    return render_template("npcdetails.html", npc=npc)

#filter content/Filter seaction route, queries fish and crops using SQL INNER JOINs across related tables
@app.route("/season/<season_name>")
def season_filter(season_name):
#searching for fish and crops through seasons
    db = get_db()
    cursor = db.cursor()
    #query fish filtered by season through foreign key relationship
    query_fish = """
        SELECT fishing.*
        FROM fishing
        JOIN seasons ON fishing.season_id = seasons.id
        WHERE seasons.season_name = ?
    """
    cursor.execute(query_fish, (season_name,))
    fish_list = cursor.fetchall()

    #query crops filtered by season through foreign key relationship
    query_crops = """
        SELECT planting.*
        FROM planting
        JOIN seasons ON planting.season_id = seasons.id
        WHERE seasons.season_name = ?
    """
    cursor.execute(query_crops, (season_name,))
    crop_list = cursor.fetchall()

    return render_template("season.html", season=season_name, fish_list=fish_list, crop_list=crop_list)

# Global search route that performs case-insensitive fuzzy searches across all 4 database tables
def search():
    query = request.args.get('q', "").strip()
    results = {'fish': [], 'crops': [], 'npcs': [], 'farms': []}
    #execute parameterized LIKE queries only if user input is not empty
    if query:
        search_term = f"%{query}%"
        results['fish'] = query_db("SELECT * FROM fishing WHERE name LIKE ?;", (search_term,))
        results['crops'] = query_db("SELECT * FROM planting WHERE name LIKE ?;", (search_term,))
        results['npcs'] = query_db("SELECT * FROM npc WHERE name LIKE ?;", (search_term,))
        results['farms'] = query_db("SELECT * FROM farm WHERE name LIKE ?;", (search_term,))
    return render_template("search_results.html", query=query, results=results)


#Error Handlers:
#Custom 404 handler
#gracefully displays user-friendly error page for invalid URLs or missing IDs
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

#Custom 500 handler
#handles internal server crashes smoothly without exposing system tracebacks
@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500

#running the application server in debug mode
if __name__ == "__main__":
    app.run(debug=True)
