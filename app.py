import sqlite3
from hashids import Hashids
from flask import Flask, render_template, request, flash, redirect, url_for

def get_db_connection():
    """
        Opens a connection to the db file and then sets
        row row_factory attribute to sqlite3.Row to have
        name-based access o columns.

        The db will return rows that behave like regular python dicts.
    """
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

# Init app
app = Flask(__name__)
# Set secret key
app.config['SECRET_KEY'] = 'SecretRandomString'
# Generate hash given a salt
hashids = Hashids(min_length=4, salt=app.config['SECRET_KEY'])


@app.route('/', methods=('GET', 'POST'))
def index():
    """
        Decorated flask view function. Its return value gets converted into
        an HTTP response which the HTTP client displays.
        This route accept both GET and POST requests.
    """
    conn = get_db_connection()

    if request.method == 'POST':
        # Save url submitted by the user
        url = request.form['url']

        if not url:
            # flash a message to the user
            flash('The url is required')
            return redirect(url_for('index'))

        # Save in db og url
        url_data = conn.execute('INSERT INTO urls (original_url) VALUES(?)',
                                (url,))
        conn.commit()
        conn.close()

        url_id = url_data.lastrowid
        hashid = hashids.encode(url_id)
        #? request.host_url is an attribute that Flask's request obj provides
        short_url = request.host_url + hashid

        return render_template('index.html', short_url=short_url)

    return render_template('index.html')




