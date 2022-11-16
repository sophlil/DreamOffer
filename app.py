# Citation for the following file:
# 11/07/2022
# Based on:
# app.py from the Flask Starter App repo by Professor Michael Curry
# https://github.com/osu-cs340-ecampus/flask-starter-app/blob/master/bsg_people_app/app.py

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
app.config["MYSQL_USER"] = "cs340_OSUusername"
app.config["MYSQL_PASSWORD"] = "XXXX"
app.config["MYSQL_DB"] = "cs340_OSUusername"
app.config["MYSQL_CURSORCLASS"] = "DictCursor"

mysql = MySQL(app)

# Routes
# route for home page
@app.route("/")
def home():
    return render_template('index.html')

# route for READ & CREATE Applicants page
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
            name = request.form["name"]  # Required
            email = request.form["email"]  # Required

            # Since both name and email are required, this is the only query needed
            query = "INSERT INTO Applicants (name, email) VALUES (%s, %s)"
            cur = mysql.connection.cursor()
            cur.execute(query, (name, email))
            mysql.connection.commit()
        
            return redirect("/applicants")

# route for UPDATE Applicants page
@app.route("/edit-applicant/<int:id>", methods=["POST", "GET"])
def edit_applicant(id):
    # Displays the specific Applicant's existing attributes
    if request.method == "GET":
        # mySQL query to grab the info of the Applicant with the passed id
        query = "SELECT * FROM Applicants WHERE applicantID = %s" % (id)
        cur = mysql.connection.cursor()
        cur.execute(query)
        data = cur.fetchall()

        return render_template("edit_applicant.j2", data=data)

    # After user enters update info, updates Applicant in DB
    if request.method == "POST":
        # Fires off if user clicks the 'Update Applicant' button
        if request.form.get("Update_Applicant"):
            # Grabs user form inputs
            name = request.form["name"]  # Required
            email = request.form["email"]  # Required

            # Since both name and email are required, this is the only query needed
            query = "UPDATE Applicants SET name = %s, email = %s WHERE applicantID = %s"
            cur = mysql.connection.cursor()
            cur.execute(query, (name, email, id))
            mysql.connection.commit()
        
            return redirect("/applicants")

# route for DELETE Applicants form
@app.route("/delete-applicant/<int:id>", methods=["POST", "GET"])
def delete_applicant(id):
    if request.method == "GET":
        # mySQL query to grab Applicant-to-delete's attributes
        query = "SELECT applicantID, name FROM Applicants WHERE applicantID = %s" % (id)
        cur = mysql.connection.cursor()
        cur.execute(query)
        data = cur.fetchall()

        return render_template("delete_applicant.j2", data=data)

    if request.method == "POST":
        # mySQL query to delete the Applicant
        query = "DELETE FROM Applicants WHERE applicantID = %s"
        cur = mysql.connection.cursor()
        cur.execute(query, (id,))
        mysql.connection.commit()

        # redirect back to Applicants page
        return redirect("/applicants")

# route for READ & CREATE Companies page
@app.route("/companies", methods=["POST", "GET"])
def companies():
    # Grabs Companies data so we can send it to our template to display
    if request.method == "GET":
        # mySQL query to grab all the companies in Companies
        query = "SELECT companyID, name, description, website FROM Companies"
        cur = mysql.connection.cursor()
        cur.execute(query)
        data = cur.fetchall()

        return render_template("companies.j2", data=data)
    
    # Insert a company into the Companies entity
    if request.method == "POST":
        # Fires off if user presses the Add Company button
        if request.form.get("Add_Company"):
            # Grabs user form inputs
            name = request.form["name"]  # Required
            description = request.form["description"]  # Optional
            website = request.form["website"]  # Optional

            # NULL description AND NULL website
            if description == "" and website == "":
                # mySQL query to insert new Company into Companies with user form inputs
                query = "INSERT INTO Companies (name) VALUES (%s)"
                cur = mysql.connection.cursor()
                cur.execute(query, (name))
                mysql.connection.commit()
            
            # NULL description
            elif description == "":
                query = "INSERT INTO Companies (name, website) VALUES (%s, %s)"
                cur = mysql.connection.cursor()
                cur.execute(query, (name, website))
                mysql.connection.commit()
            
            # NULL website
            elif website == "":
                query = "INSERT INTO Companies (name, description) VALUES (%s, %s)"
                cur = mysql.connection.cursor()
                cur.execute(query, (name, description))
                mysql.connection.commit()

            # No NULL inputs
            else:
                query = "INSERT INTO Companies (name, description, website) VALUES (%s, %s, %s)"
                cur = mysql.connection.cursor()
                cur.execute(query, (name, description, website))
                mysql.connection.commit()
            
            # Redirect back to Companies page
            return redirect("/companies")

# route for UPDATE Companies page
@app.route("/edit-company/<int:id>", methods=["POST", "GET"])
def edit_company(id):
    # Displays the specific Company's existing attributes
    if request.method == "GET":
        # mySQL query to grab the info of the Company with the passed id
        query = "SELECT * FROM Companies WHERE companyID = %s" % (id)
        cur = mysql.connection.cursor()
        cur.execute(query)
        data = cur.fetchall()

        return render_template("edit_company.j2", data=data)

    # After user enters update info, updates specific Company in DB
    if request.method == "POST":
        # Fires off if user clicks the 'Update Company' button
        if request.form.get("Update_Company"):
            # Grabs user form inputs
            name = request.form["name"]  # Required
            description = request.form["description"]  # Optional
            website = request.form["website"]  # Optional

            # NULL description AND NULL website
            if (description == "" or description == "None") and (website == "" or website == "None"):
                query = "UPDATE Companies SET name = %s, description = NULL, website = NULL WHERE companyID = %s"
                cur = mysql.connection.cursor()
                cur.execute(query, (name, id))
                mysql.connection.commit()

            # NULL description
            elif description == "" or description == "None":
                query = "UPDATE Companies SET name = %s, description = NULL, website = %s WHERE companyID = %s"
                cur = mysql.connection.cursor()
                cur.execute(query, (name, website, id))
                mysql.connection.commit()
            
            # NULL website
            elif website == "" or website == "None":
                query = "UPDATE Companies SET name = %s, description = %s, website = NULL WHERE companyID = %s"
                cur = mysql.connection.cursor()
                cur.execute(query, (name, description, id))
                mysql.connection.commit()

            # No NULL inputs
            else:
                query = "UPDATE Companies SET name = %s, description = %s, website = %s WHERE companyID = %s"
                cur = mysql.connection.cursor()
                cur.execute(query, (name, description, website, id))
                mysql.connection.commit()
        
            return redirect("/companies")

# route for DELETE Company form
@app.route("/delete-company/<int:id>", methods=["POST", "GET"])
def delete_company(id):
    if request.method == "GET":
        # mySQL query to grab Company-to-delete's attributes
        query = "SELECT companyID, name FROM Companies WHERE companyID = %s" % (id)
        cur = mysql.connection.cursor()
        cur.execute(query)
        data = cur.fetchall()

        return render_template("delete_company.j2", data=data)

    if request.method == "POST":
        # mySQL query to delete the Company
        query = "DELETE FROM Companies WHERE companyID = %s"
        cur = mysql.connection.cursor()
        cur.execute(query, (id,))
        mysql.connection.commit()

        # redirect back to Companies page
        return redirect("/companies")


# Listener
if __name__ == "__main__":
    app.run(port=56423, debug=True)