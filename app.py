from flask import Flask, render_template, redirect, url_for, request, g
import sqlite3


# Create a flask app
app = Flask(__name__)


# Database helper functions
###############################################################################


def connect_db():
    """Returns a connection to the DB."""

    db = sqlite3.connect("food_tracker.db")
    db.row_factory = sqlite3.Row

    return db


def get_db():
    """Returns the current the current DB connection."""

    if not hasattr(g, 'db'):
        g.db = connect_db()

    return g.db


@app.teardown_appcontext
def close_db(error):
    """Close the DB connection if exists when the application context ends."""

    if hasattr(g, 'db'):
        g.db.close()


###############################################################################


# Routes Functions
###############################################################################


@app.route('/')
def home():
    """Return the home page which list all days and a summary details."""

    return render_template('home.html')


@app.route('/day')
def day():
    """
    Return the day page which list all data about food eaten in this day,
    and add new food to this day.
    """

    return render_template('day.html')


@app.route('/foods', methods=['GET', 'POST'])
def foods():
    """
    Return the foods page which list all foods in the app, and add new
    food to the app.
    """

    # Creating a DB connection
    db = get_db()

    if request.method == 'POST':
        # Getting the form data in local vars
        name = request.form['name']
        protein = int(request.form['protein'])
        carbohydrates = int(request.form['carbohydrates'])
        fat = int(request.form['fat'])
        calories = 4 * protein + 4 * carbohydrates + 9 * fat
        # Debugging form data in console
        # print("name: {}, protein: {}, carbohydrates: {}, fat: {}".format(
        #     name, protein, carbohydrates, fat))
        # Storing the form data in the DB
        db.execute("""insert into food (name, protein, carbohydrates, fat, calories)
                   values (?, ?, ?, ?, ?);""",
                   [name, protein, carbohydrates, fat, calories])
        db.commit()
        return redirect(url_for('foods'))
    else:
        # Getting all foods from the DB
        cursor = db.execute("select * from food;")
        foods = cursor.fetchall()
        return render_template('foods.html', foods=foods)


###############################################################################
