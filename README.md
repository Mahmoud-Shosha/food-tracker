# Food Tracker

A python web application using flask framework to create a list of dates and for each date you will know how many protein, carbohydrates and fats were consumed on it.
The application consists of:
- A home page for listing all dates.
- A detail page for each date to list foods eaten in  this date.
- A food page to add foods data.


## Prerequisites

- Python
- Flask
- DBMS

## Installation

- [Download python3.6](https://www.python.org/downloads/)
- Install sqlite3  
`sudo apt-get install sqlite3`
- Install Flask  
`pip install flask`
- Download the repository

## Getting started

- Run Flask  
`export FLASK_APP=app.py`  
`flask run`

## More info

- The database name: news
- The database tables:
    1. authors: id, name, bio
    2. articles: id, author, title, slug, lead, body
    3. log: id, ip, path, method, status, time

