from flask import Flask, render_template, request, redirect, url_for, flash
from db_config import get_db_connection

app = Flask(__name__)
app.secret_key = "secret123"


def init_db():
    """Create table if it does not exist"""
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS motorshow(
            id INT AUTO_INCREMENT PRIMARY KEY,
            first_name VARCHAR(100),
            last_name VARCHAR(100),
            email VARCHAR(150),
            vehicle_brand VARCHAR(100),
            vehicle_model VARCHAR(100),
            plate_number VARCHAR(50),
            registration_date DATE
        )
    """)

    conn.commit()
    cursor.close()
    conn.close()


@app.route("/", methods=["GET", "POST"])
def index():
    init_db()  # ensure table exists

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    if request.method == "POST":
        data = (
            request.form["first_name"].strip(),
            request.form["last_name"].strip(),
            request.form["email"].strip(),
            request.form["vehicle_brand"].strip(),
            request.form["vehicle_model"].strip(),
            request.form["plate_number"].strip(),
            request.form["registration_date"]
        )

        # validation
        if any(x == "" for x in data):
            flash("All fields are required.", "danger")
        else:
            cursor.execute("""
                INSERT INTO motorshow
                (first_name, last_name, email, vehicle_brand, vehicle_model, plate_number, registration_date)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """, data)
            conn.commit()
            flash("Vehicle registered successfully!", "success")

    cursor.execute("SELECT * FROM motorshow ORDER BY id DESC")
    records = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template("index.html", records=records)


@app.route("/delete/<int:id>")
def delete(id):
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("DELETE FROM motorshow WHERE id = %s", (id,))
    conn.commit()

    cursor.close()
    conn.close()

    flash("Entry deleted successfully.", "warning")
    return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(debug=True)
