import sqlite3
from flask import Flask, render_template, request, redirect, url_for, flash

app = Flask(__name__)
app.secret_key = "street_legends_secret"


def get_db_connection():
    conn = sqlite3.connect('motorshow.db')
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_db_connection()
    conn.execute("""
        CREATE TABLE IF NOT EXISTS motorshow(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            first_name TEXT, last_name TEXT, email TEXT,
            vehicle_brand TEXT, vehicle_model TEXT,
            plate_number TEXT, registration_date TEXT
        )
    """)
    conn.commit()
    conn.close()


# ROUTE 1: THE REGISTRATION FORM
@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        data = (
            request.form.get("first_name").strip(),
            request.form.get("last_name").strip(),
            request.form.get("email").strip(),
            request.form.get("vehicle_brand").strip(),
            request.form.get("vehicle_model").strip(),
            request.form.get("plate_number").strip().upper(),
            request.form.get("registration_date")
        )

        if all(data):
            conn = get_db_connection()
            conn.execute(
                "INSERT INTO motorshow (first_name, last_name, email, vehicle_brand, vehicle_model, plate_number, registration_date) VALUES (?, ?, ?, ?, ?, ?, ?)",
                data)
            conn.commit()
            conn.close()
            flash("Success! You are registered.", "success")
            return redirect(url_for("entry_list"))  # Redirect to the list after clicking button
        else:
            flash("All fields are required.", "danger")

    return render_template("index.html")


# ROUTE 2: THE ENTRY LIST
@app.route("/entries")
def entry_list():
    conn = get_db_connection()
    search_query = request.args.get('search', '').strip()

    if search_query:
        query = "SELECT * FROM motorshow WHERE first_name LIKE ? OR vehicle_brand LIKE ? OR plate_number LIKE ? ORDER BY id DESC"
        val = f"%{search_query}%"
        records = conn.execute(query, (val, val, val)).fetchall()
    else:
        records = conn.execute("SELECT * FROM motorshow ORDER BY id DESC").fetchall()

    conn.close()
    return render_template("entry.html", records=records, search_query=search_query)


@app.route("/delete/<int:id>")
def delete(id):
    conn = get_db_connection()
    conn.execute("DELETE FROM motorshow WHERE id = ?", (id,))
    conn.commit()
    conn.close()
    flash("Entry removed.", "warning")
    return redirect(url_for("entry_list"))


if __name__ == "__main__":
    init_db()
    app.run(debug=True)
