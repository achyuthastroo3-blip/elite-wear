from flask import Flask, render_template,request,redirect
import sqlite3
app = Flask(__name__)

def init_db():
    conn = sqlite3.connect('shop.db')
    cur = conn.cursor()

    cur.execute('''
    CREATE TABLE IF NOT EXISTS users(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        full_name TEXT,
        email TEXT,
        password TEXT
    )
    ''')

    conn.commit()
    conn.close()

init_db()


@app.route('/products')
def products():
    return render_template('products.html')

@app.route('/', methods=['GET', 'POST'])
def home():

    if request.method == 'POST':

        email = request.form['email']
        password = request.form['password']

        conn = sqlite3.connect('shop.db')
        cur = conn.cursor()

        cur.execute(
            """
            SELECT * FROM users
            WHERE email=? AND password=?
            """,
            (email, password)
        )

        user = cur.fetchone()

        conn.close()

        if user:
            return redirect('/products')

        else:
            return "Invalid Login ❌"

    return render_template('index.html')

@app.route('/createaccount', methods=['GET', 'POST'])
def createaccount():
    if request.method == 'POST':

        full_name = request.form['full_name']
        email = request.form['email']
        password = request.form['password']
        confirm_password = request.form['confirm_password']

        # CHECK PASSWORDS
        if password != confirm_password:
            return "Passwords do not match ❌"

        conn = sqlite3.connect('shop.db')
        cur = conn.cursor()

        cur.execute(
            """
            INSERT INTO users(
                full_name,
                email,
                password
            )
            VALUES(?,?,?)
            """,
            (
                full_name,
                email,
                password
            )
        )

        conn.commit()
        conn.close()

        return "Account Created Successfully 🔥"

    return render_template('createaccount.html')

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=10000)
