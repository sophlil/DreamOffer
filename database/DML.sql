-- Group 58
-- Don Reniff and Sophia Lilienthal
-- CS340 Fall 2022
-- This DML contains all the SQL queries used in our server side code for our Portfolio project, DreamOffer

--------------------------------------------------------------
-- BROWSE/CREATE Applicants age

-- Get all Applicants for Applicant table
SELECT applicantID, name, email FROM Applicants;

-- Add a new Applicant
INSERT INTO Applicants (name, email) VALUES (:name_Input, :email_Input);

---------------------------------------------------------------
-- UPDATE Applicants Page

-- Get a single Applicant's data for the Update Applicant form
-- The user selects an Applicant's name, but the value of that input is the applicantID
SELECT * FROM Applicants WHERE applicantID = :applicantID_selected_from_browse_applicants_page;

-- Update an Applicant's data based on submission of the Update Applicant form 
UPDATE Applicants SET name = :name_Input, email = :email_Input WHERE applicantID = :applicantID_passed_to_route;

---------------------------------------------------------------
-- DELETE Applicants Page

-- Get a single Applicant's data for the Delete Applicant form
SELECT applicantID, name FROM Applicants WHERE applicantID = :applicantID_selected_from_browse_applicants_page;

-- Delete an Applicant
DELETE FROM Applicants WHERE applicantID = :applicantID_passed_to_route;

-----------------------------------------------------------------
-- BROWSE/CREATE Applications Page

-- Get all Applications for Application table
SELECT Applications.applicationID, Applications.dateApplied, Applications.result, 
Applications.dateResult, Applicants.name AS applicantName, Positions.title, Companies.name AS companyName
FROM Applications 
INNER JOIN Applicants ON Applications.applicantID = Applicants.applicantID 
INNER JOIN Positions ON Applications.positionID = Positions.positionID
LEFT JOIN Companies ON Positions.companyID = Companies.companyID;

-- Get all Applicant IDs and Names to populate the Applicant Name dropdown
SELECT applicantID, name FROM Applicants;

-- Get all Position IDs and Titles and all associated Company Names to populate the Position dropdown
SELECT Positions.positionID, Positions.title, Companies.name 
FROM Positions 
LEFT JOIN Companies ON Positions.companyID = Companies.companyID;

-- Get all Company IDs and Names to populate the Company Name dropdown
SELECT companyID, name FROM Companies;

-- Add a new Application
INSERT INTO Applications (dateApplied, applicantID, positionID) 
VALUES (:dateApplied_Input, :applicantID_from_dropdown_Input, :position_Input);

-----------------------------------------------------------------
-- SEARCH Applications Page (Same query used to search Applications for an Applicant on Applicants page)

-- Get Applications from Search Applications form
SELECT Applications.applicationID, Applications.dateApplied, Applications.result, Applications.dateResult, 
Applicants.name AS applicantName, Positions.title, Companies.name AS companyName 
FROM Applications 
INNER JOIN Applicants ON Applications.applicantID = Applicants.applicantID
INNER JOIN Positions ON Applications.positionID = Positions.positionID
LEFT JOIN Companies ON Positions.companyID = Companies.companyID
WHERE Applications.applicantID = :applicantID_from_input;

-----------------------------------------------------------------
-- UPDATE Application Page

-- Get a single Application's data for the Update Application form
SELECT applicationID, dateApplied, result, dateResult 
FROM Applications WHERE applicationID = :applicationID_selected_from_browse_applications_page;

-- Update an Application's data if NULL dateResult input
UPDATE Applications SET dateApplied = :dateApplied_Input, result = :result_from_dropdown_Input, dateResult = NULL
WHERE applicationID = :applicationID_passed_to_route;

-- Update an Application's data if no NULL inputs
UPDATE Applications SET dateApplied = :dateApplied_Input, result = :result_from_dropdown_Input, dateResult = :dateResult_Input
WHERE applicationID = :applicationID_passed_to_route;

-----------------------------------------------------------------
-- DELETE Application Page

-- Get a single Application's data for the Delete Application form
SELECT applicationID, Applicants.name AS applicantName, Positions.title AS positionTitle, Companies.name AS companyName
FROM Applications 
INNER JOIN Applicants ON Applications.applicantID = Applicants.applicantID
INNER JOIN Positions ON Applications.positionID = Positions.positionID
LEFT JOIN Companies ON Positions.companyID = Companies.companyID
WHERE Applications.applicantID = :applicantID_selected_from_browse_applications_page;

-- Delete an Application
DELETE FROM Applications WHERE applicationID = :applicantID_selected_from_the_delete_form;

-------------------------------------------------------------------------
-- BROWSE/CREATE Companies Page

-- Get all Companies for Companies table
SELECT companyID, name, description, website FROM Companies;

-- Add a new Company if NULL description AND website inputs
INSERT INTO Companies (name) VALUES (:name_Input);

-- Add a new Company if NULL description input
INSERT INTO Companies (name, website) VALUES (:name_Input, :website_Input);

-- Add a new Company if NULL website input
INSERT INTO Companies (name, description) VALUES (:name_Input, :description_Input);

-- Add a new Company if no NULL inputs
INSERT INTO Companies (name, website, description) VALUES (:name_Input, :website_Input, :description_Input);

-------------------------------------------------------------------------
-- UPDATE Companies Page

-- Get a single Company's data for the Update Company form
SELECT * FROM Companies WHERE companyID = :companyID_passed_to_route;

-- Update a Company's data if NULL description AND website inputs
UPDATE Companies SET name = :name_Input, website = NULL, description = NULL WHERE companyID = :companyID_from_the_update_form;

-- Update a Company's data if NULL description input
UPDATE Companies SET name = :name_Input, website = :website_Input, description = NULL WHERE companyID = :companyID_from_the_update_form;

-- Update a Company's data if NULL website input
UPDATE Companies SET name = :name_Input, website = NULL, description = :description_Input WHERE companyID = :companyID_from_the_update_form;

-- Update a Company's data if no NULL inputs
UPDATE Companies SET name = :name_Input, website = :website_Input, description = :description_Input WHERE companyID = :companyID_from_the_update_form;

-------------------------------------------------------------------------
-- DELETE Companies Page

-- Get a single Company's data for the Delete Company form
SELECT companyID, name FROM Companies WHERE companyID = :companyID_selected_from_browse_companies_page;

-- Delete a Company
DELETE FROM Companies WHERE companyID = :companyID_selected_from_the_delete_form;

------------------------------------------------------------------------------
-- BROWSE/CREATE Positions & Company Recruiters Page

-- Show all Positions and their associated Companies for Positions table and Positions dropdown
SELECT Companies.name, Positions.title, Positions.location, Positions.salary, Positions.link, Positions.positionID
FROM Positions
LEFT JOIN Companies ON Companies.companyID = Positions.companyID;

-- Show all relevant data for PositionsCompanyRecruiters Affiliation table
SELECT Companies.name, Positions.title, Positions.link, CompanyRecruiters.name,
CompanyRecruiters.recruiterID, Positions.positionID, PositionsCompanyRecruiters.positionsCompanyRecruitersID
FROM Positions
LEFT JOIN Companies ON Companies.companyID = Positions.companyID
INNER JOIN PositionsCompanyRecruiters ON Positions.positionID = PositionsCompanyRecruiters.positionID
INNER JOIN CompanyRecruiters ON PositionsCompanyRecruiters.recruiterID = CompanyRecruiters.recruiterID;

-- Show all Recruiters for Recruiters table and Recruiter dropdown
SELECT name, email, phone, linkedin, lastContacted, details, recruiterID
FROM CompanyRecruiters;

-- Show all Company names to populate the Company Name drop down
SELECT companyID, name FROM Companies;

-- Add a new Position if NULL companyID AND location AND salary inputs
INSERT INTO Positions (title, link)
VALUES (:title_Input, :link_Input);

-- Add a new Position if NULL companyID AND location inputs
INSERT INTO Positions (title, salary, link)
VALUES (:title_Input, :salary_Input, :link_Input);

-- Add a new Position if NULL companyID AND salary inputs
INSERT INTO Positions (title, location, link)
VALUES (:title_Input, :location_Input, :link_Input);

-- Add a new Position if NULL location AND salary inputs
INSERT INTO Positions (companyID, title, link)
VALUES (:companyID_from_dropdown_Input, :title_Input, :link_Input);

-- Add a new Position if NULL location input
INSERT INTO Positions (companyID, title, salary, link)
VALUES (:companyID_from_dropdown_Input, :title_Input, :salary_Input, :link_Input);

-- Add a new Position if NULL companyID input
INSERT INTO Positions (title, location, salary, link)
VALUES (:title_Input, :location_Input, :salary_Input, :link_Input);

-- Add a new Position if NULL salary input
INSERT INTO Positions (companyID, title, location, link)
VALUES (:companyID_from_dropdown_Input, :title_Input, :location_Input, :link_Input);

-- Add a new Position if no NULL inputs
INSERT INTO Positions (companyID, title, location, salary, link)
VALUES (:companyID_from_dropdown_Input, :title_Input, :location_Input, :salary_Input, :link_Input);

-- Add a new Affiliation to intersection table if Recruiter selected from drop down during CREATE Position
INSERT INTO PositionsCompanyRecruiters (positionID, recruiterID)
VALUES ((SELECT positionID FROM Positions WHERE link = :link_Input), :recruiter_affiliation_from_dropdown_Input);

-- Add a new Position and Recruiter Affiliation into intersection table
INSERT INTO PositionsCompanyRecruiters (positionID, recruiterID)
VALUES (:positionID_from_the_add_form, :recruiterID_from_the_add_form);

-- Add a new Recruiter if NULL email AND phone inputs
INSERT INTO CompanyRecruiters (name, linkedin, lastContacted, details)
VALUES (:name_Input, :linkedin_Input, :lastContacted_Input, :details_Input);

-- Add a new Recruiter if NULL email input
INSERT INTO CompanyRecruiters (name, phone, linkedin, lastContacted, details)
VALUES (:name_Input, :phone_Input, :linkedin_Input, :lastContacted_Input, :details_Input);

-- Add a new Recruiter if NULL phone input
INSERT INTO CompanyRecruiters (name, email, linkedin, lastContacted, details)
VALUES (:name_Input, :email_Input, :linkedin_Input, :lastContacted_Input, :details_Input);

-- Add a new Recruiter if no NULL inputs
INSERT INTO CompanyRecruiters (name, email, phone, linkedin, lastContacted, details)
VALUES (:name_Input, :email_Input, :phone_Input, :linkedin_Input, :lastContacted_Input, :details_Input);

-- Add a new Affiliation to intersection table if Position selected from drop down during CREATE Recruiter
INSERT INTO PositionsCompanyRecruiters (positionID, recruiterID)
VALUES (:position_affiliation_from_dropdown_Input, (SELECT recruiterID FROM CompanyRecruiters WHERE linkedin = :linkedin_Input));

------------------------------------------------------------------------------
-- SEARCH Positions on Positions & Company Recruiters Page

-- Search Positions by associated Company name
-- The user sees the Company name in the drop down, but the associated value that is searched is the companyID
SELECT Companies.name, Positions.title, Positions.location, Positions.salary, Positions.link, Positions.positionID
FROM Positions
INNER JOIN Companies ON Companies.companyID = Positions.companyID
WHERE Companies.companyID = :companyID_from_dropdown_Input;

------------------------------------------------------------------------------
-- UPDATE Position Page

-- Get a single Position's data for the Update Position form
SELECT Positions.positionID, Positions.companyID, Companies.name, Positions.title, 
Positions.location, Positions.salary, Positions.link 
FROM Positions 
LEFT JOIN Companies ON Companies.companyID = Positions.companyID
WHERE Positions.positionID = :positionID_passed_to_route;

-- Get all Company names and IDs to populate the Company Name drop down within the UPDATE Position form
SELECT companyID, name FROM Companies;

-- Update a Position's data if NULL companyID AND location AND salary inputs
UPDATE Positions SET companyID = NULL, title = :title_Input, location = NULL, salary = NULL, link = :link_Input 
WHERE positionID = :positionID_from_the_update_form;

-- Update a Position's data if NULL location AND salary inputs
UPDATE Positions SET companyID = :companyID_from_dropdown_Input, title = :title_Input, location = NULL, salary = NULL, link = :link_Input 
WHERE positionID = :positionID_from_the_update_form;

-- Update a Position's data if NULL companyID AND location inputs
UPDATE Positions SET companyID = NULL, title = :title_Input, location = NULL, salary = :salary_Input, link = :link_Input 
WHERE positionID = :positionID_from_the_update_form;

-- Update a Position's data if NULL companyID AND salary inputs
UPDATE Positions SET companyID = NULL, title = :title_Input, location = :location_Input, salary = NULL, link = :link_Input 
WHERE positionID = :positionID_from_the_update_form;

-- Update a Position's data if NULL location input
UPDATE Positions SET companyID = :companyID_from_dropdown_Input, title = :title_Input, location = NULL, salary = :salary_Input, link = :link_Input 
WHERE positionID = :positionID_from_the_update_form;

-- Update a Position's data if NULL salary input
UPDATE Positions SET companyID = :companyID_from_dropdown_Input, title = :title_Input, location = :location_Input, salary = NULL, link = :link_Input 
WHERE positionID = :positionID_from_the_update_form;

-- Update a Position's data if NULL companyID input
UPDATE Positions SET companyID = NULL, title = :title_Input, location = :location_Input, salary = :salary_Input, link = :link_Input 
WHERE positionID = :positionID_from_the_update_form;

-- Update a Position's data if no NULL inputs
UPDATE Positions SET companyID = :companyID_from_dropdown_Input, title = :title_Input, location = :location_Input, salary = :salary_Input, link = :link_Input 
WHERE positionID = :positionID_from_the_update_form;

------------------------------------------------------------------------------
-- UPDATE Recruiter Page

-- Get a single Recruiter's data for the Update Recruiter form
SELECT recruiterID, name, email, phone, linkedin, lastContacted, details
FROM CompanyRecruiters
WHERE recruiterID = :recruiterID_passed_to_route;

-- Update a Recruiter's data if NULL email and phone inputs
UPDATE CompanyRecruiters 
SET name = :name_Input, email = NULL, phone = NULL, linkedin = :linkedin_Input, lastContacted = :lastContacted_Input, details = :details_Input 
WHERE recruiterID = :recruiterID_from_the_update_form;

-- Update a Recruiter's data if NULL email input
UPDATE CompanyRecruiters 
SET name = :name_Input, email = NULL, phone = :phone_Input, linkedin = :linkedin_Input, lastContacted = :lastContacted_Input, details = :details_Input 
WHERE recruiterID = :recruiterID_from_the_update_form;

-- Update a Recruiter's data if NULL phone input
UPDATE CompanyRecruiters 
SET name = :name_Input, email = :email_Input, phone = NULL, linkedin = :linkedin_Input, lastContacted = :lastContacted_Input, details = :details_Input 
WHERE recruiterID = :recruiterID_from_the_update_form;

-- Update a Recruiter's data if no NULL inputs
UPDATE CompanyRecruiters 
SET name = :name_Input, email = :email_Input, phone = :phone_Input, linkedin = :linkedin_Input, lastContacted = :lastContacted_Input, details = :details_Input 
WHERE recruiterID = :recruiterID_from_the_update_form;

------------------------------------------------------------------------------
-- DELETE Affiliation Page

-- Get a single Position and Recruiter's Affiliation data for the DELETE Affiliation form
SELECT PositionsCompanyRecruiters.positionID, Positions.title, PositionsCompanyRecruiters.recruiterID, 
CompanyRecruiters.name, PositionsCompanyRecruiters.positionsCompanyRecruitersID
FROM PositionsCompanyRecruiters
INNER JOIN Positions ON PositionsCompanyRecruiters.positionID = Positions.positionID
INNER JOIN CompanyRecruiters ON PositionsCompanyRecruiters.recruiterID = CompanyRecruiters.recruiterID
WHERE PositionsCompanyRecruiters.positionsCompanyRecruitersID = :positionsCompanyRecruitersID_passed_to_route;

-- Delete a Position and Recruiter Affiliation from intersection table
DELETE FROM positionsCompanyRecruiters 
WHERE positionsCompanyRecruitersID = :positionsCompanyRecruitersID_selected_from_the_delete_form;

------------------------------------------------------------------------------
-- DELETE Position Page

-- Get a single Position's data for the DELETE Position form
SELECT positionID, title FROM Positions WHERE positionID = :positionID_passed_to_route;

-- Delete a Position from Positions table
DELETE FROM Positions WHERE Position.positionID = :positionsCompanyRecruitersID_selected_from_the_delete_form;

------------------------------------------------------------------------------
-- DELETE Recruiter Page

-- Get a single Recruiter's data for the DELET Recruiter form
SELECT recruiterID, name FROM CompanyRecruiters WHERE recruiterID = :recruiterID_passed_to_route;

-- Delete a Recruiter from the Company Recruiters table
DELETE FROM CompanyRecruiters WHERE recruiterID = :positionsCompanyRecruitersID_selected_from_the_delete_form;

