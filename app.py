from flask import Flask, render_template, g
import sqlite3


# Create a flask app
app = Flask(__name__)


# Database helper functions
###############################################################################


def connect_db():
    """Returns a connection to the DB."""

    db = sqlite3.connect("data.db")
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


@app.route('/foods')
def foods():
    """
    Return the foods page which list all foods in the app, and add new
    food to the app.
    """

    return render_template('foods.html')


###############################################################################
