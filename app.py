import sqlite3
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)


def get_db_connection():
    """Connects to SQLite database and configures rows as dictionaries."""
    conn = sqlite3.connect("contacts.db")
    conn.row_factory = sqlite3.Row
    return conn


@app.route("/")
def index():
    """Displays all contacts from the database."""
    conn = get_db_connection()
    contacts = conn.execute("SELECT * FROM contacts").fetchall()
    conn.close()
    return render_template("index.html", contacts=contacts)


@app.route("/add", methods=["POST"])
def add_contact():
    """Inserts a new contact from the web form into the database."""
    name = request.form["name"]
    relation = request.form["relation"]
    special_day = request.form["special_day"]
    occasion = request.form["occasion"]
    phone = request.form["phone"]
    delivery_pref = request.form["delivery_pref"]

    conn = get_db_connection()
    conn.execute(
        """
        INSERT INTO contacts (name, relation, special_day, occasion, phone, delivery_pref)
        VALUES (?, ?, ?, ?, ?, ?)
        """,
        (name, relation, special_day, occasion, phone, delivery_pref),
    )
    conn.commit()
    conn.close()

    return redirect(url_for("index"))


@app.route("/edit/<int:id>", methods=["POST"])
def edit_contact(id):
    """Updates an existing contact record in the database."""
    name = request.form["name"]
    relation = request.form["relation"]
    special_day = request.form["special_day"]
    occasion = request.form["occasion"]
    phone = request.form["phone"]
    delivery_pref = request.form["delivery_pref"]

    conn = get_db_connection()
    conn.execute(
        """
        UPDATE contacts
        SET name = ?, relation = ?, special_day = ?, occasion = ?, phone = ?, delivery_pref = ?
        WHERE id = ?
        """,
        (name, relation, special_day, occasion, phone, delivery_pref, id),
    )
    conn.commit()
    conn.close()

    return redirect(url_for("index"))


@app.route("/delete/<int:id>", methods=["POST"])
def delete_contact(id):
    """Deletes a contact by ID from the database."""
    conn = get_db_connection()
    conn.execute("DELETE FROM contacts WHERE id = ?", (id,))
    conn.commit()
    conn.close()

    return redirect(url_for("index"))


if __name__ == "__main__":
    print("🌐 Starting Flask Web Dashboard at http://127.0.0.1:5000")
    app.run(debug=True, port=5000)
    import os
import sqlite3
from flask import Flask, render_template, request, redirect, url_for
from apscheduler.schedulers.background import BackgroundScheduler
from reminder import check_special_days

app = Flask(__name__)

# --- Initialize Database Table on Startup ---
def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS contacts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            relation TEXT NOT NULL,
            special_day TEXT NOT NULL,
            occasion TEXT NOT NULL,
            phone TEXT NOT NULL,
            delivery_pref TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()

init_db()

def get_db_connection():
    conn = sqlite3.connect("contacts.db")
    conn.row_factory = sqlite3.Row
    return conn

# --- Start Background Scheduler ---
scheduler = BackgroundScheduler(daemon=True)
scheduler.add_job(check_special_days, trigger='cron', hour=8, minute=0)
scheduler.start()

@app.route("/")
def index():
    conn = get_db_connection()
    contacts = conn.execute("SELECT * FROM contacts").fetchall()
    conn.close()
    return render_template("index.html", contacts=contacts)

@app.route("/add", methods=["POST"])
def add_contact():
    name = request.form["name"]
    relation = request.form["relation"]
    special_day = request.form["special_day"]
    occasion = request.form["occasion"]
    phone = request.form["phone"]
    delivery_pref = request.form["delivery_pref"]

    conn = get_db_connection()
    conn.execute(
        """
        INSERT INTO contacts (name, relation, special_day, occasion, phone, delivery_pref)
        VALUES (?, ?, ?, ?, ?, ?)
        """,
        (name, relation, special_day, occasion, phone, delivery_pref)
    )
    conn.commit()
    conn.close()
    return redirect(url_for("index"))

@app.route("/edit/<int:id>", methods=["POST"])
def edit_contact(id):
    name = request.form["name"]
    relation = request.form["relation"]
    special_day = request.form["special_day"]
    occasion = request.form["occasion"]
    phone = request.form["phone"]
    delivery_pref = request.form["delivery_pref"]

    conn = get_db_connection()
    conn.execute(
        """
        UPDATE contacts
        SET name = ?, relation = ?, special_day = ?, occasion = ?, phone = ?, delivery_pref = ?
        WHERE id = ?
        """,
        (name, relation, special_day, occasion, phone, delivery_pref, id)
    )
    conn.commit()
    conn.close()
    return redirect(url_for("index"))

@app.route("/delete/<int:id>", methods=["POST"])
def delete_contact(id):
    conn = get_db_connection()
    conn.execute("DELETE FROM contacts WHERE id = ?", (id,))
    conn.commit()
    conn.close()
    return redirect(url_for("index"))

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
    import os
import sqlite3

DB_PATH = os.environ.get("DB_PATH", "contacts.db")

# Automatically create folder directory if using custom path like /var/data/
db_dir = os.path.dirname(DB_PATH)
if db_dir and not os.path.exists(db_dir):
    os.makedirs(db_dir, exist_ok=True)


def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn