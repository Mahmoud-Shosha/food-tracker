from flask import Flask, render_template, redirect, url_for, request, g
import sqlite3
from datetime import datetime


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


@app.route('/', methods=['GET', 'POST'])
def home():
    """Return the home page which list all days and a summary details."""

    # Getting the DB connection
    db = get_db()

    if request.method == 'POST':
        # Getting the form data in loacal vars
        date = request.form['date']
        date = datetime.strptime(date, '%Y-%m-%d')
        database_date = datetime.strftime(date, '%Y%m%d')
        # Debugging database_date in the console
        # print(database_date)
        # Storing the date in the DB
        db.execute("insert into date_log (date_log) values (?);",
                   [database_date])
        db.commit()
        # Redirecting to the home page after adding a date
        return redirect(url_for('home'))
    else:
        # Getting all dates from the DB
        cursor = db.execute("""select sum(food.protein) as protein,
                            sum(food.carbohydrates) as carbohydrates,
                            sum(food.fat) as fat,
                            sum(food.calories) as calories,
                            date_log.date_log as date
                            from date_log left join date_food
                            on date_food.date_log_id = date_log.id
                            left join food on food.id = date_food.food_id
                            group by date_log.id order by date_log.date_log desc""")
        dates = cursor.fetchall()
        template_dates = []    # dates formatted as needed in the template
        # Formatting the date as needed in a conventient format
        for date in dates:
            template_date = {}
            template_date['protein'] = date['protein']
            template_date['carbohydrates'] = date['carbohydrates']
            template_date['fat'] = date['fat']
            template_date['calories'] = date['calories']
            template_date['date'] = date['date']
            pretty_date = datetime.strptime(str(date['date']), '%Y%m%d')
            pretty_date = datetime.strftime(pretty_date, '%B %d, %Y')
            template_date['pretty_date'] = pretty_date
            template_dates.append(template_date)
        # Debugging the needed date format in the console
        # print(template_dates)
        # Returning the home page with add dates in the DB
        return render_template('home.html', dates=template_dates)


@app.route('/day/<date>', methods=['GET', 'POST'])
def day(date):
    """
    Return the day page which list all data about food eaten in this day,
    and add new food to this day.
    """

    # Getting the DB connection
    db = get_db()

    # Getting the date from the DB
    cursor = db.execute("select * from date_log where date_log = ?;",
                        [date])
    date = cursor.fetchone()

    if request.method == 'POST':
        date_id = date['id']
        food_id = request.form['food_item']
        # Debugging date_id and food_id
        # print(date_id, food_id)
        # Storing the food to the date in the DB
        db.execute("insert into date_food values (?, ?)", [date_id, food_id])
        db.commit()
        # Redirecting to the day page after adding a food to the date
        return redirect(url_for('day', date=date['date_log']))
    else:
        # Formating the date as needed in the template
        template_date = datetime.strptime(str(date['date_log']), "%Y%m%d")
        template_date = datetime.strftime(template_date, "%B %d, %Y")
        template_date = {'template_date': template_date,
                         'date': date['date_log']}
        # Debugging the requested date in the console
        # print(date['date_log'])
        # Getting a list of foods in the DB
        cursor = db.execute("select id, name from food;")
        foods = cursor.fetchall()
        # Getting the foods in this date
        cursor = db.execute("""select food.name, food.protein, food.carbohydrates, food.fat, food.calories
                            from date_food join food
                            on food.id = date_food.food_id
                            where date_food.date_log_id = ?""",
                            [date['id']])
        day_foods = cursor.fetchall()
        # Calculating the totals  for protein, carbohydrates, fat, calories
        totals = {'protein': 0, 'carbohydrates': 0, 'fat': 0, 'calories': 0}
        for food in day_foods:
            totals['protein'] += food['protein']
            totals['carbohydrates'] += food['carbohydrates']
            totals['fat'] += food['fat']
            totals['calories'] += food['calories']
        # Returning the day page with all the day detail
        return render_template('day.html', date=template_date, foods=foods,
                               day_foods=day_foods, totals=totals)


@app.route('/foods', methods=['GET', 'POST'])
def foods():
    """
    Return the foods page which list all foods in the app, and add new
    food to the app.
    """

    # Getting the DB connection
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
        # Redirecting to the foods page after adding a food
        return redirect(url_for('foods'))
    else:
        # Getting all foods from the DB
        cursor = db.execute("select * from food;")
        foods = cursor.fetchall()
        # Returning the foods page with all foods in the DB
        return render_template('foods.html', foods=foods)


###############################################################################
