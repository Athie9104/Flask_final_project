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

    conn.execute('CREATE TABLE IF NOT EXISTS subscribe (name TEXT, lastname TEXT, cell TEXT, email TEXT)')
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

    if request.method == "POST":
        try:
            name = request.form['name']
            lastname =request.form['lastname']
            cell = request.form['cell']
            email = request.form['email']
            address = request.form['addr']
            zip_code = request.format['code']
            province = request.form['province']

            with sqlite3.connect('database.db') as con:
                cur = con.cursor()
                cur.execute("INSERT INTO subscribe (name, lastname, cell, email) VALUES (?, ?, ?, ?, ?, ?), ? ", (name, lastname, cell, email, address, zip_code, province))
                con.commit()
                msg = "successfully subscribed"

        except Exception as e:
            con.rollback()
            msg = "error occurred in insert operation" + e

        finally:
            con.close()
            return render_template('result.html', msg=msg)


    @app.route('/show-subscribers/', methods=['GET'])
    def show_subscribers():
        records = []
        try:
            with sqlite3.connect('database.db') as con:
                con.row_factory = dict_factory()
                cur = con.cursor()
                cur .execute("SELECT * FROM subscribe")
                records = cur.fetchall()

        except Exception as ex:
            con.rollback()
            print("There was an error fetching results from the database." + ex)
        finally:
            con.close()
            return jsonify(records)


if __name__ == "__main__":
    app.run(debug=True)


