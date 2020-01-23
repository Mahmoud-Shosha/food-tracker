import sqlite3
from flask import g


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


###############################################################################
