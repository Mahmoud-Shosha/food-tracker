# Food Tracker

A python web application using flask framework to create a list of days and for each day you will know how many protein, carbohydrates, fats and calories were consumed on it.
The application consists of:
- A home page for listing all dates.
- A detail page for each day to list foods eaten in this day.
- A food page to add foods data.


## Prerequisites

- Python
- Flask
- DBMS (sqlite3)
- HTML, CSS, Bootstrap

## Installation

- [Download python3.6](https://www.python.org/downloads/)
- Install sqlite3  
`sudo apt-get install sqlite3`
- create the database   
`sqlite3 food_tracker.db < food_tracker.sql`  
- Install dependencies  
`pip3 install virtualenv`  
`virtualenv -p python3 venv`  
`source venv/bin/activate`  
`pip3 install -r requirements.txt`  
- Download the repository

## Getting started

- Run Flask  
`export FLASK_APP=app.py`  
`flask run`
