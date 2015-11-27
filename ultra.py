"""
The beginnings of a web app that will help
me explore cloud technologies. It begins by
listing a store a  gpx files.

"""
from flask import Flask, g
from pymongo import MongoClient


app = Flask(__name__)


def connect_db():
    """
    Connects to the database.

    """
    client = MongoClient()
    db = client.runs_db
    return db


def get_db():
    """
    Returns the db connection, opening a new database connection
    if necessary.

    """
    if not hasattr(g, 'db'):
        g.db = connect_db()
    return g.db


@app.route('/')
def show_runs():
    db = get_db()
    collection = db.runs
    entries = collection.find()
    val = ''
    for run in entries:
        val += str(run)

    return  val
    #return render_template('show_entries.html', entries=entries)

if __name__ == '__main__':
    app.run()
