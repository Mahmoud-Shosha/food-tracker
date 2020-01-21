from flask import Flask, render_template


# Create a flask app
app = Flask(__name__)


# Create a route for the home page
@app.route('/')
def home():
    """Return the home page which list all days and a summary details."""

    return render_template('home.html')


# Create a route for the day page
@app.route('/day')
def day():
    """
    Return the day page which list all data about food eaten in this day,
    and add new food to this day.
    """

    return render_template('day.html')


# Create a route for the foods page
@app.route('/foods')
def foods():
    """
    Return the foods page which list all foods in the app, and add new
    food to the app.
    """

    return render_template('foods.html')
