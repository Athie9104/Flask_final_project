import sqlite3
from flask import Flask, render_template, request, jsonify
from flask_cors import CORS


def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d


def init_sqlite_db():
    conn = sqlite3.connect('database.db')
    print("Opened database successfully")

    conn.execute('CREATE TABLE IF NOT EXISTS subscribe (name TEXT, lastname TEXT, cell INT, email TEXT)')
    print("Table created successfully")
    conn.close()


init_sqlite_db()

app = Flask(__name__)
CORS(app)


@app.route('/')
@app.route('/enter-new/')
def enter_new():
    return render_template('subscribe.html')


@app.route('/add-new-subscriber/', methods=['POST'])
def add_new_subscriber():
    msg = None
    try:
        post_data = request.get_json()
        name = post_data['name']
        lastname =post_data['lastname']
        email = post_data['email']
        cell = post_data['cell']


        with sqlite3.connect('database.db') as con:
            cur = con.cursor()
            cur.execute("INSERT INTO subscribe (name, lastname, email, cell) VALUES (?, ?, ?, ?)", (name, lastname, email, cell))
            con.commit()
            msg = "successfully subscribed"

    except Exception as e:
        con.rollback()
        msg = "error occurred in insert operation" + e

    finally:
        return jsonify(msg)
        con.close()


@app.route('/show-subscribers/', methods=['GET'])
def show_subscribers():
    try:
        with sqlite3.connect('database.db') as con:
            con.row_factory = dict_factory
            con = sqlite3.connect('database.db')
            cur = con.cursor()
            cur.execute("SELECT * FROM subscribe")
            records = cur.fetchall()

    except Exception as ex:
        con.rollback()
        print("There was an error fetching results from the database." + ex)
    finally:
        con.close()
        return jsonify(records)


if __name__ == "__main__":
    app.run(debug=True)
