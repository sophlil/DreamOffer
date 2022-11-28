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
            name = request.form["company"]  # Required
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

# 
# route for READ & CREATE Applications page
@app.route("/applications", methods=["POST", "GET"])
def applications():
    # Get Applications data to send to our template to display - READ
    if request.method == "GET":
        # mySQL query to grab all applications
        query = "SELECT applicationID, dateApplied, result, dateResult, Applicants.name, Positions.title FROM Applications INNER JOIN Applicants ON Applications.applicantID = Applicants.applicantID INNER JOIN Positions ON Applications.positionID = Positions.positionID;"
        cur = mysql.connection.cursor()
        cur.execute(query)
        data = cur.fetchall()

        # query to populate the Applicant Name dropdown for Search and Add forms
        query2 = "SELECT applicantID, name FROM Applicants;"
        cur = mysql.connection.cursor()
        cur.execute(query2)
        applicants_data = cur.fetchall()

        # query to populate the Position Title dropdown for Search and Add forms
        query3 = "SELECT positionID, title FROM Positions;"
        cur = mysql.connection.cursor()
        cur.execute(query3)
        positions_data = cur.fetchall()

        # query to populate the Companies Name dropdown for Search form
        query4 = "SELECT companyID, name FROM Companies;"
        cur = mysql.connection.cursor()
        cur.execute(query4)
        companies_data = cur.fetchall()

        # render Applications page passing our query data to the template
        return render_template("applications.j2", data=data, applicants=applicants_data, positions=positions_data, companies=companies_data)

    # Insert new Application into Applications entity - CREATE
    if request.method == "POST":
        # Fires off if user presses the Add Application button
        if request.form.get("Add_Application"):
            # Grabs user form inputs
            applicant = request.form["applicant"]  # Required
            position = request.form["position"]  # Required
            dateApplied = request.form["dateApplied"] # Required

            # This is the only query needed since each attribute is required
            query = "INSERT INTO Applications (dateApplied, applicantID, positionID) VALUES (%s, %s, %s);"
            cur = mysql.connection.cursor()
            cur.execute(query, (dateApplied, applicant, position))
            mysql.connection.commit()
        
            return redirect("/applications")

# route for SEARCH Applications page from Applications page
@app.route("/search-applications", methods=["POST", "GET"])
def search_applications():
    if request.method == "GET":
        applicant = request.args.get("applicant")
        query = "SELECT applicationID, dateApplied, result, dateResult, Applicants.name, Positions.title FROM Applications INNER JOIN Applicants ON Applications.applicantID = Applicants.applicantID INNER JOIN Positions ON Applications.positionID = Positions.positionID WHERE Applications.applicantID = %s;" % (applicant)
        cur = mysql.connection.cursor()
        cur.execute(query)
        data = cur.fetchall()

        return render_template("search_application.j2", search_data=data)

# route for SEARCH Applications page from Applicants page
@app.route("/search-applications/<int:id>", methods=["POST", "GET"])
def search_applications_from_applicant(id):
    if request.method == "GET":
        query = "SELECT applicationID, dateApplied, result, dateResult, Applicants.name, Positions.title FROM Applications INNER JOIN Applicants ON Applications.applicantID = Applicants.applicantID INNER JOIN Positions ON Applications.positionID = Positions.positionID WHERE Applications.applicantID = %s;" % (id)
        cur = mysql.connection.cursor()
        cur.execute(query)
        data = cur.fetchall()

        return render_template("search_application.j2", search_data=data)

# route for UPDATE Applications page
@app.route("/edit-application/<int:id>", methods=["POST", "GET"])
def edit_application(id):
    # Displays the specific Application's existing attributes
    if request.method == "GET":
        # mySQL query to grab the info of the Company with the passed id
        query = "SELECT applicationID, dateApplied, result, dateResult FROM Applications WHERE applicationID = %s" % (id)
        cur = mysql.connection.cursor()
        cur.execute(query)
        data = cur.fetchall()

        applicationResults = {
            0: "Submitted", 
            1: "In Process", 
            2: "Offer", 
            3: "Rejection"
        }

        return render_template("edit_application.j2", data=data, applicationResults=applicationResults)

    # After user enters update info, updates specific Application in DB
    if request.method == "POST":
        # Fires off if user clicks the 'Update Application' button
        if request.form.get("Update_Application"):
            # Grabs user form inputs
            dateApplied = request.form["dateApplied"]  # Required
            result = request.form["result"]  # Required
            dateResult = request.form["dateResult"]  # Optional

            # NULL dateResult
            if (dateResult == "" or dateResult == "None"):
                query = "UPDATE Applications SET dateApplied = %s, result = %s, dateResult = NULL WHERE applicationID = %s;"
                cur = mysql.connection.cursor()
                cur.execute(query, (dateApplied, result, id))
                mysql.connection.commit()

            # No NULL inputs
            else:
                query = "UPDATE Applications SET dateApplied = %s, result = %s, dateResult = %s WHERE applicationID = %s;"
                cur = mysql.connection.cursor()
                cur.execute(query, (dateApplied, result, dateResult, id))
                mysql.connection.commit()
        
            return redirect("/applications")

# route for DELETE Application form
@app.route("/delete-application/<int:id>", methods=["POST", "GET"])
def delete_application(id):
    if request.method == "GET":
        # mySQL query to grab Application-to-delete's attributes
        query = "SELECT applicationID, Applicants.name AS applicantName, Positions.title AS positionTitle, Companies.name AS companyName FROM Applications INNER JOIN Applicants ON Applications.applicantID = Applicants.applicantID INNER JOIN Positions ON Applications.positionID = Positions.positionID INNER JOIN Companies ON Positions.companyID = Companies.companyID WHERE Applications.applicationID = %s;" % (id)
        cur = mysql.connection.cursor()
        cur.execute(query)
        data = cur.fetchall()

        return render_template("delete_application.j2", data=data)

    if request.method == "POST":
        # mySQL query to delete the Application
        query = "DELETE FROM Applications WHERE applicationID = %s"
        cur = mysql.connection.cursor()
        cur.execute(query, (id,))
        mysql.connection.commit()

        # redirect back to Applications page
        return redirect("/applications")

# 
# route for READ & CREATE Positions and Recruiters page
@app.route("/positionscompanyrecruiters", methods=["POST", "GET"])
def positionscompanyrecruiters():
    if request.method == "GET":
        # Get Positions data to send to our template to display - READ
        query1 = "SELECT Companies.name, Positions.title, Positions.location, Positions.salary, Positions.link, Positions.positionID FROM Positions LEFT JOIN Companies ON Companies.companyID = Positions.companyID;"
        cur = mysql.connection.cursor()
        cur.execute(query1)
        position_data = cur.fetchall()

        # Get PositionsCompanyRecruiters data to send to our template to display - READ
        query2 = "SELECT Companies.name, Positions.title, Positions.link, CompanyRecruiters.name, CompanyRecruiters.recruiterID, Positions.positionID, PositionsCompanyRecruiters.positionsCompanyRecruitersID FROM Positions INNER JOIN Companies ON Companies.companyID = Positions.companyID INNER JOIN PositionsCompanyRecruiters ON Positions.positionID = PositionsCompanyRecruiters.positionID INNER JOIN CompanyRecruiters ON PositionsCompanyRecruiters.recruiterID = CompanyRecruiters.recruiterID;"
        cur = mysql.connection.cursor()
        cur.execute(query2)
        affiliation_data = cur.fetchall()

        # Get Recruiters data to send to our template to display - READ
        query3 = "SELECT name, email, phone, linkedin, lastContacted, details, recruiterID FROM CompanyRecruiters;"
        cur = mysql.connection.cursor()
        cur.execute(query3)
        recruiter_data = cur.fetchall()

        # Get Companies data to send to our template to display - READ
        query4 = "SELECT companyID, name FROM Companies;"
        cur = mysql.connection.cursor()
        cur.execute(query4)
        company_data = cur.fetchall()

        return render_template("positionscompanyrecruiters.j2", position_data=position_data, affiliation_data=affiliation_data, recruiter_data=recruiter_data, company_data=company_data)

    # Insert new Position or Affiliation or Recruiter into respective entities - CREATE
    if request.method == "POST":
        # Fires off if user presses the Add Position button
        if request.form.get("Add_Position"):
            # Grabs user form inputs
            companyID = request.form["company-names"]  # Optional
            title = request.form["title"]  # Required
            location = request.form["location"] # Optional
            salary = request.form["salary"]  # Optional
            link = request.form["link"]  # Required

             # NULL companyID AND NULL location AND NULL salary
            if (companyID == "" or companyID == "None") and (location == "" or location == "None") and (salary == "" or salary == "None"):
                query = "INSERT INTO Positions (title, link) VALUES (%s, %s)"
                cur = mysql.connection.cursor()
                cur.execute(query, (title, link))
                mysql.connection.commit()

            # NULL companyID AND NULL location
            elif (companyID == "" or companyID == "None") and (location == "" or location == "None"):
                query = "INSERT INTO Positions (title, salary, link) VALUES (%s, %s, %s)"
                cur = mysql.connection.cursor()
                cur.execute(query, (title, salary, link))
                mysql.connection.commit()
            
            # NULL companyID AND NULL salary
            elif (companyID == "" or companyID == "None") and (salary == "" or salary == "None"):
                query = "INSERT INTO Positions (title, location, link) VALUES (%s, %s, %s)"
                cur = mysql.connection.cursor()
                cur.execute(query, (title, location, link))
                mysql.connection.commit()
            
            # NULL location AND NULL salary
            elif (location == "" or location == "None") and (salary == "" or salary == "None"):
                query = "INSERT INTO Positions (companyID, title, link) VALUES (%s, %s, %s)"
                cur = mysql.connection.cursor()
                cur.execute(query, (companyID, title, link))
                mysql.connection.commit()
            
            # NULL location
            elif location == "" or location == "None":
                query = "INSERT INTO Positions (companyID, title, salary, link) VALUES (%s, %s, %s, %s)"
                cur = mysql.connection.cursor()
                cur.execute(query, (companyID, title, salary, link))
                mysql.connection.commit()
            
            # NULL companyID
            elif companyID == "" or companyID == "None":
                query = "INSERT INTO Positions (title, location, salary, link) VALUES (%s, %s, %s, %s)"
                cur = mysql.connection.cursor()
                cur.execute(query, (title, location, salary, link))
                mysql.connection.commit()
            
            # NULL salary
            elif salary == "" or salary == "None":
                query = "INSERT INTO Positions (companyID, title, location, link) VALUES (%s, %s, %s, %s)"
                cur = mysql.connection.cursor()
                cur.execute(query, (companyID, title, location, link))
                mysql.connection.commit()

            # No NULL inputs
            else:
                query = "INSERT INTO Positions (companyID, title, location, salary, link) VALUES (%s, %s, %s, %s, %s)"
                cur = mysql.connection.cursor()
                cur.execute(query, (companyID, title, location, salary, link))
                mysql.connection.commit()
        
            return redirect("/positionscompanyrecruiters")

        # Fires off if user presses the Add Affiliation button
        if request.form.get("Add_Affiliation"):
            # Grabs user form inputs
            positionID = request.form["title"]  # Required
            recruiterID = request.form["name"]  # Required

             # Since both inputs are required, this is the only query
            
            query = "INSERT INTO PositionsCompanyRecruiters (positionID, recruiterID) VALUES (%s, %s)"
            cur = mysql.connection.cursor()
            cur.execute(query, (positionID, recruiterID))
            mysql.connection.commit()
        
            return redirect("/positionscompanyrecruiters")
        
       
    # Fires off if user presses the Add Recruiter button
        if request.form.get("Add_Recruiter"):
            # Grabs user form inputs
            name = request.form["name"]  # Required
            email = request.form["email"]  # Optional
            phone = request.form["phone"] # Optional
            linkedin = request.form["linkedin"]  # Required
            lastContacted = request.form["lastContacted"]  # Required
            details = request.form["details"]  # Required

            # NULL email AND NULL phone
            if (email == "" or email == "None") and (phone == "" or phone == "None"):
                query = "INSERT INTO CompanyRecruiters (name, linkedin, lastContacted, details) VALUES (%s, %s, %s, %s)"
                cur = mysql.connection.cursor()
                cur.execute(query, (name, linkedin, lastContacted, details))
                mysql.connection.commit()

            # NULL email
            elif email == "" or email == "None":
                query = "INSERT INTO CompanyRecruiters (name, phone, linkedin, lastContacted, details) VALUES (%s, %s, %s, %s, %s)"
                cur = mysql.connection.cursor()
                cur.execute(query, (name, phone, linkedin, lastContacted, details))
                mysql.connection.commit()
        
            # NULL phone
            elif phone == "" or phone == "None":
                query = "INSERT INTO CompanyRecruiters (name, email, linkedin, lastContacted, details) VALUES (%s, %s, %s, %s, %s)"
                cur = mysql.connection.cursor()
                cur.execute(query, (name, email, linkedin, lastContacted, details))
                mysql.connection.commit()

            # No NULL inputs
            else:
                query = "INSERT INTO CompanyRecruiters (name, email, phone, linkedin, lastContacted, details) VALUES (%s, %s, %s, %s, %s, %s)"
                cur = mysql.connection.cursor()
                cur.execute(query, (name, email, phone, linkedin, lastContacted, details))
                mysql.connection.commit()
    
            return redirect("/positionscompanyrecruiters")

# route for UPDATE Position page
@app.route("/edit-position/<int:id>", methods=["POST", "GET"])
def edit_position(id):
    # Displays the specific Position's existing attributes
    if request.method == "GET":
        # mySQL query to grab the info of the Position with the passed id
        query = "SELECT Positions.positionID, Positions.companyID, Companies.name, Positions.title, Positions.location, Positions.salary, Positions.link FROM Positions INNER JOIN Companies ON Companies.companyID = Positions.companyID WHERE positionID = %s;" % (id)
        cur = mysql.connection.cursor()
        cur.execute(query)
        data = cur.fetchall()

        # Show all Company names to populate the Company Name drop down
        query2 = "SELECT companyID, name FROM Companies;"
        cur = mysql.connection.cursor()
        cur.execute(query2)
        companies_data = cur.fetchall()

        return render_template("edit_position.j2", data=data, companies_data=companies_data)

    # After user enters update info, updates specific Position in DB
    if request.method == "POST":
        # Fires off if user clicks the 'Update Position' button
        if request.form.get("Update_Position"):
            # Grabs user form inputs
            company = request.form["company"] # Required
            title = request.form["title"]  # Required
            location = request.form["location"]  # Optional
            salary = request.form["salary"]  # Optional
            link = request.form["link"] # Required

            # NULL location and NULL salary
            if (location == "" or location == "None") and (salary == "" or salary == "None"):
                query = "UPDATE Positions SET companyID = %s, title = %s, location = NULL, salary = NULL, link = %s WHERE positionID = %s;"
                cur = mysql.connection.cursor()
                cur.execute(query, (company, title, link, id))
                mysql.connection.commit()

            # NULL location
            elif (location == "" or location == "None"):
                query = "UPDATE Positions SET companyID = %s, title = %s, location = NULL, salary = %s, link = %s WHERE positionID = %s;"
                cur = mysql.connection.cursor()
                cur.execute(query, (company, title, salary, link, id))
                mysql.connection.commit()

            # NULL salary
            elif (salary == "" or salary == "None"):
                query = "UPDATE Positions SET companyID = %s, title = %s, location = %s, salary = NULL, link = %s WHERE positionID = %s;"
                cur = mysql.connection.cursor()
                cur.execute(query, (company, title, location, link, id))
                mysql.connection.commit()

            # No NULL inputs
            else:
                query = "UPDATE Positions SET companyID = %s, title = %s, location = %s, salary = %s, link = %s WHERE positionID = %s;"
                cur = mysql.connection.cursor()
                cur.execute(query, (company, title, location, salary, link, id))
                mysql.connection.commit()
            
            return redirect("/positionscompanyrecruiters")

# route for UPDATE Recruiter page
@app.route("/edit-recruiter/<int:id>", methods=["POST", "GET"])
def edit_recruiter(id):
    # Displays the specific Recruiter's existing attributes
    if request.method == "GET":
        #mySQL query to grab the info of the Recruiter with the passed id
        query = "SELECT recruiterID, name, email, phone, linkedin, lastContacted, details FROM CompanyRecruiters WHERE recruiterID = %s;" % (id)
        cur = mysql.connection.cursor()
        cur.execute(query)
        data = cur.fetchall()

        return render_template("edit_recruiter.j2", data=data)

    # After user enters update info, updates specific Recruiter in DB
    if request.method == "POST":
        # Fires off if user clicks the 'Update Recruiter' button
        if request.form.get("Update_Recruiter"):
            # Grabs user form inputs
            name = request.form["name"] # Required
            email = request.form["email"]  # Optional
            phone = request.form["phone"]  # Optional
            linkedin = request.form["linkedin"]  # Required
            lastContacted = request.form["lastContacted"] # Required
            details = request.form["details"] # Required

            # NULL email AND NULL phone
            if (email == "" or email == "None") and (phone == "" or phone == "None"):
                query = "UPDATE CompanyRecruiters SET name = %s, email = NULL, phone = NULL, linkedin = %s, lastContacted = %s, details = %s WHERE recruiterID = %s;"
                cur = mysql.connection.cursor()
                cur.execute(query, (name, linkedin, lastContacted, details, id))
                mysql.connection.commit()

            # NULL email
            elif email == "" or email == "None":
                query = "UPDATE CompanyRecruiters SET name = %s, email = NULL, phone = %s, linkedin = %s, lastContacted = %s, details = %s WHERE recruiterID = %s;"
                cur = mysql.connection.cursor()
                cur.execute(query, (name, phone, linkedin, lastContacted, details, id))
                mysql.connection.commit()
        
            # NULL phone
            elif phone == "" or phone == "None":
                query = "UPDATE CompanyRecruiters SET name = %s, email = %s, phone = NULL, linkedin = %s, lastContacted = %s, details = %s WHERE recruiterID = %s;"
                cur = mysql.connection.cursor()
                cur.execute(query, (name, email, linkedin, lastContacted, details, id))
                mysql.connection.commit()

            # No NULL inputs
            else:
                query = "UPDATE CompanyRecruiters SET name = %s, email = %s, phone = %s, linkedin = %s, lastContacted = %s, details = %s WHERE recruiterID = %s;"
                cur = mysql.connection.cursor()
                cur.execute(query, (name, email, phone, linkedin, lastContacted, details, id))
                mysql.connection.commit()
    
            return redirect("/positionscompanyrecruiters")

# route for DELETE Affiliation form
@app.route("/delete-affiliation/<int:id>", methods=["POST", "GET"])
def delete_affiliation(id):
    if request.method == "GET":
        # mySQL query to grab Affiliation-to-delete's attributes
        query = "SELECT PositionsCompanyRecruiters.positionID, Positions.title, PositionsCompanyRecruiters.recruiterID, CompanyRecruiters.name, PositionsCompanyRecruiters.positionsCompanyRecruitersID FROM PositionsCompanyRecruiters INNER JOIN Positions ON Positions.positionID = PositionsCompanyRecruiters.positionID INNER JOIN CompanyRecruiters ON CompanyRecruiters.recruiterID = PositionsCompanyRecruiters.recruiterID WHERE PositionsCompanyRecruiters.positionsCompanyRecruitersID = %s;" % (id)
        cur = mysql.connection.cursor()
        cur.execute(query)
        data = cur.fetchall()

        return render_template("delete_positionsrecruiters.j2", data=data)

    if request.method == "POST":
        # mySQL query to delete the Affiliation
        query = "DELETE FROM PositionsCompanyRecruiters WHERE positionsCompanyRecruitersID = %s;"
        cur = mysql.connection.cursor()
        cur.execute(query, (id,))
        mysql.connection.commit()

        # redirect back to Applications page
        return redirect("/positionscompanyrecruiters")

# route for SEARCH Positions page
@app.route("/search-positions", methods=["POST", "GET"])
def search_positions():
    if request.method == "GET":
        company = request.args.get("company-name")
        query = "SELECT Companies.name, Positions.title, Positions.location, Positions.salary, Positions.link, Positions.positionID FROM Positions INNER JOIN Companies ON Companies.companyID = Positions.companyID WHERE Companies.companyID = %s;" % (company)
        cur = mysql.connection.cursor()
        cur.execute(query)
        data = cur.fetchall()

        return render_template("search_positions.j2", search_data=data)

# Listener
if __name__ == "__main__":
    app.run(port=56429, debug=True)
    