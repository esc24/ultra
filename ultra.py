"""
The beginnings of a web app that will help
me explore cloud technologies. It begins by
listing a store a  gpx files.

"""
import dateutil.parser
from flask import Flask, g, request, render_template, redirect, flash, url_for
from pymongo import MongoClient


app = Flask(__name__)

app.config.update(dict(
#    DATABASE=os.path.join(app.root_path, 'flaskr.db'),
#    DEBUG=True,
    SECRET_KEY='development key',
#    USERNAME='admin',
#    PASSWORD='default'
))

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
    entries = [dict(title=entry['file'], text=str(entry['dt'])) for
               entry in collection.find()]
    return  render_template('show_runs.html', entries=entries)


@app.route('/add', methods=['POST'])
def add_entry():

    try:
        dt = dateutil.parser.parse(request.form['text'])
    except ValueError:
        flash('Failed to parse datetime')
    else:
        db = get_db()
        db.runs.insert_one({'file': request.form['title'],
                            'dt': dt})
        flash('New entry was successfully posted')

    return redirect(url_for('show_runs'))


if __name__ == '__main__':
    app.run(debug=True)
