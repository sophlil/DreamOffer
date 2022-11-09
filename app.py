from flask import Flask, render_template, json, redirect
from flask_mysqldb import MySQL
from flask import request
import os

app = Flask(__name__)

# database connection
# Template:
# app.config["MYSQL_HOST"] = "classmysql.engr.oregonstate.edu"
# app.config["MYSQL_USER"] = "cs340_OSUusername"
# app.config["MYSQL_PASSWORD"] = "XXXX" | last 4 digits of OSU id
# app.config["MYSQL_DB"] = "cs340_OSUusername"
# app.config["MYSQL_CURSORCLASS"] = "DictCursor"

# database connection info
app.config["MYSQL_HOST"] = "classmysql.engr.oregonstate.edu"
app.config["MYSQL_USER"] = "cs340_lilients"
app.config["MYSQL_PASSWORD"] = "9464"
app.config["MYSQL_DB"] = "cs340_lilients"
app.config["MYSQL_CURSORCLASS"] = "DictCursor"

mysql = MySQL(app)

# Routes
# route for home page
@app.route("/")
def home():
    return render_template('index.html')

# route for Applicants page
@app.route("/applicants", methods=["POST", "GET"])
def applicants():
    # Get Applicants data to send to our template to display - READ
    if request.method == "GET":
        # mySQL query to grab all applicants
        query = "SELECT applicantID, name, email FROM Applicants;"
        cur = mysql.connection.cursor()
        cur.execute(query)
        data = cur.fetchall()

        # render Applicants page passing our query data to the template
        return render_template("applicants.j2", data=data)

    # Insert new Applicant into Applicants entity - CREATE
    if request.method == "POST":
        # Fires off if user presses the Add Applicant button
        if request.form.get("Add_Applicant"):
            # Grabs user form inputs
            name = request.form["name"]
            email = request.form["email"]

            # Since both name and email are required, this is the only query needed
            query = "INSERT INTO Applicants (name, email) VALUES (%s, %s)"
            cur = mysql.connection.cursor()
            cur.execute(query, (name, email))
            mysql.connection.commit()
        
            return redirect("/applicants")

# Listener
if __name__ == "__main__":
    app.run(port=56423, debug=True)