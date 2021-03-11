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
    print("Subscriber table created successfully")
    conn.execute('CREATE TABLE IF NOT EXISTS images (title TEXT, subtitle TEXT, description TEXT, image TEXT)')
    print("Images table created successfully")
    conn.execute('CREATE TABLE IF NOT EXISTS sending_mail (firstname TEXT, email TEXT, subject TEXT)')
    print("Images table created successfully")
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
            cur.execute("INSERT INTO subscribe (name, lastname, cell, email) VALUES (?, ?, ?, ?)", (name, lastname, cell, email))
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

#
# @app.route('/blogs/')
# def insert_blogs():
#     try:
#         with sqlite3.connect('database.db') as con:
#             con.row_factory = dict_factory
#             cur = con.cursor()
#             cur.execute("INSERT INTO images(title, subtitle, description, image) VALUES('Umsebenzi', 'subtitle', 'descript', 'https://i.postimg.cc/7hnJGvXc/my-people.jpg')")
#             cur.execute("INSERT INTO images(title, subtitle, description, image) VALUES('Umsebenzi', 'subtitle', 'descript', 'https://i.postimg.cc/VL038YGD/umqombothi.jpg')")
#             cur.execute("INSERT INTO images(title, subtitle, description, image) VALUES('Umsebenzi', 'subtitle', 'descript', 'https://i.postimg.cc/HxKBZMgH/goat-slaughter.jpg')")
#             cur.execute("INSERT INTO images(title, subtitle, description, image) VALUES('Umsebenzi', 'subtitle', 'descript', 'https://i.postimg.cc/P5pf0sYj/swazi-food.jpg')")
#             cur.execute("INSERT INTO images(title, subtitle, description, image) VALUES('Umsebenzi', 'subtitle', 'descript', 'https://i.postimg.cc/Y0YfdyRf/isonka-samanzi.jpg')")
#             cur.execute("INSERT INTO images(title, subtitle, description, image) VALUES('Umsebenzi', 'subtitle', 'descript', 'https://i.postimg.cc/3JqfWgGh/bean-soup.jpg')")
#             cur.execute("INSERT INTO images(title, subtitle, description, image) VALUES('Umsebenzi', 'subtitle', 'descript', 'https://i.postimg.cc/bJLyczvm/umngqungqo.jpg')")
#             cur.execute("INSERT INTO images(title, subtitle, description, image) VALUES('Umsebenzi', 'subtitle', 'descript', 'https://i.postimg.cc/BbQwk38c/iduli.jpg')")
#             cur.execute("INSERT INTO images(title, subtitle, description, image) VALUES('Umsebenzi', 'subtitle', 'descript', 'https://i.postimg.cc/PxFmfn3M/lobola.jpg')")
#             cur.execute("INSERT INTO images(title, subtitle, description, image) VALUES('Umsebenzi', 'subtitle', 'descript', 'https://i.postimg.cc/SKS118nY/ulwaluko.jpg')")
#             cur.execute("INSERT INTO images(title, subtitle, description, image) VALUES('Umsebenzi', 'subtitle', 'descript', 'https://i.postimg.cc/VLS84xxP/beauty-of-EC.jpg')")
#             con.commit()
#             msg = "record added successfully"
#     except Exception as e:
#         con.rollback()
#         msg = "Error occurred in insert operation" + str(e)
#     finally:
#         con.close()
#         return jsonify(msg)
#
#
# @app.route('/show-images/', methods=['GET'])
# def show_images():
#     data = []
#     try:
#         with sqlite3.connect('database.db') as con:
#             con.row_factory = dict_factory
#             cur = con.cursor()
#             cur.execute('SELECT * FROM images')
#             data = cur.fetchall()
#     except Exception as e:
#         con.rollback()
#         print("There was an error fetching products from the database") + e
#     finally:
#         con.close()
#         return jsonify(data)



if __name__ == "__main__":
    app.run(debug=True)
