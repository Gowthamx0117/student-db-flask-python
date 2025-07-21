from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)
DB = "student_data.db"

def get_db_connection():
    conn = sqlite3.connect(DB)
    conn.row_factory = sqlite3.Row
    return conn

# --- View all students ---
@app.route("/")
def index():
    conn = get_db_connection()
    students = conn.execute("SELECT * FROM students").fetchall()
    conn.close()
    return render_template("index.html", students=students)

# --- Add student ---
@app.route("/add", methods=["GET", "POST"])
def add_student():
    if request.method == "POST":
        regno = request.form['regno']
        name = request.form['name']
        dept = request.form['dept']
        cgpa = float(request.form['cgpa'])
        hist_arrear = request.form['hist_arrear']
        placement_eligible = (cgpa > 7.5 and hist_arrear == 'No')
        risk_group = "High" if cgpa < 6 else "Low"

        conn = get_db_connection()
        conn.execute("INSERT INTO students (regno, name, dept, cgpa, hist_arrear, placement_eligible, risk_group) VALUES (?, ?, ?, ?, ?, ?, ?)",
                     (regno, name, dept, cgpa, hist_arrear, placement_eligible, risk_group))
        conn.commit()
        conn.close()
        return redirect(url_for('index'))

    return render_template("add.html")

# --- Update student ---
@app.route("/update/<int:regno>", methods=["GET", "POST"])
def update_student(regno):
    conn = get_db_connection()
    student = conn.execute("SELECT * FROM students WHERE regno = ?", (regno,)).fetchone()

    if request.method == "POST":
        name = request.form['name']
        dept = request.form['dept']
        cgpa = float(request.form['cgpa'])
        hist_arrear = request.form['hist_arrear']
        placement_eligible = (cgpa > 7.5 and hist_arrear == 'No')
        risk_group = "High" if cgpa < 6 else "Low"

        conn.execute("UPDATE students SET name=?, dept=?, cgpa=?, hist_arrear=?, placement_eligible=?, risk_group=? WHERE regno=?",
                     (name, dept, cgpa, hist_arrear, placement_eligible, risk_group, regno))
        conn.commit()
        conn.close()
        return redirect(url_for('index'))

    conn.close()
    return render_template("update.html", student=student)

# --- Delete student ---
@app.route("/delete/<int:regno>")
def delete_student(regno):
    conn = get_db_connection()
    conn.execute("DELETE FROM students WHERE regno = ?", (regno,))
    conn.commit()
    conn.close()
    return redirect(url_for('index'))

if __name__ == "__main__":
    app.run(debug=True)
