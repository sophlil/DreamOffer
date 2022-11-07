-- Group 58
-- Don Reniff and Sophia Lilienthal

--------------------------------------------------------------
-- Applicants page

-- Get all Applicants for Applicant table
SELECT applicantID, name, email FROM Applicants;

-- Add a new Applicant
INSERT INTO Applicants (name, email) VALUES (:name_Input, :email_Input);

-- Get a single Applicant's data for the Update Applicant form
SELECT applicantID, name, email FROM Applicants WHERE applicantID = :applicantID_selected_from_browse_applicants_page;

-- Update an Applicant's data based on submission of the Update Applicant form 
UPDATE Applicants SET name = :name_Input, email = :email_Input WHERE applicantID = :applicantID_from_the_update_form;

-- Get a single Applicant's data for the Delete Applicant form
SELECT applicantID, name FROM Applicants WHERE applicantID = :applicantID_selected_from_browse_applicants_page;

-- Delete an Applicant
DELETE FROM Applicants WHERE applicantID = :applicantID_selected_from_the_delete_form;

-- Get all the Applications for a single applicant
SELECT applicationID, dateApplied, result, dateResult, Applicants.name, Positions.title 
FROM Applications 
INNER JOIN Applicants ON Applications.applicantID = Applicants.applicantID
INNER JOIN Positions ON Applications.positionID = Positions.positionID
WHERE Applications.applicantID = :applicantID_selected_from_browse_applicants_page;

-----------------------------------------------------------------
-- Applications page

-- Get all Applications for Application table
SELECT applicationID, dateApplied, result, dateResult, Applicants.name, Positions.title 
FROM Applications 
INNER JOIN Applicants ON Applications.applicantID = Applicants.applicantID
INNER JOIN Positions ON Applications.positionID = Positions.positionID;

-- Get all Applicant IDs and Names to populate the Applicant Name dropdown
SELECT applicantID, name FROM Applicants;

-- Get all Position IDs and Titles to populate the Position Title dropdown
SELECT positionID, title FROM Positions;

-- Get all Company IDs and Names to populate the Company Name dropdown
SELECT companyID, name FROM Companies;

-- Get Applications from Search Applications form
SELECT applicationID, dateApplied, result, dateResult, Applicants.name, Positions.title 
FROM Applications 
INNER JOIN Applicants ON Applications.applicantID = Applicants.applicantID
INNER JOIN Positions ON Applications.positionID = Positions.positionID
WHERE Applications.applicantID = :applicantID_from_dropdown_Input
AND Positions.positionID = :positionID_from_dropdown_Input
AND Companies.companyID = :companyID_from_dropdown_Input;

-- Add a new Application
INSERT INTO Applications (dateApplied, applicantID, positionID) 
VALUES (:dateApplied_Input, :applicantID_from_dropdown_Input, :position_Input);

-- Get a single Application's data for the Update Application form
SELECT applicationID, applicantID, positionID, dateApplied, result, dateResult 
FROM Applications WHERE applicationID = :applicationID_selected_from_browse_applications_page;

-- Update an Application's data based on submission of the Update Application form 
UPDATE Applications SET applicantID = :applicantID_from_dropdown_Input, positionID = :position_Input, dateApplied = :dateApplied_Input, result = :result_from_dropdown_Input, dateResult = :dateResult_Input
WHERE applicationID = :applicationID_from_the_update_form;

-- Get a single Application's data for the Delete Application form
SELECT applicationID, Applicants.name, Positions.title 
FROM Applications 
INNER JOIN Applicants ON Applications.applicantID = Applicants.applicantID
INNER JOIN Positions ON Applications.positionID = Positions.positionID
WHERE Applications.applicantID = :applicantID_selected_from_browse_applications_page;

-- Delete an Application
DELETE FROM Applications WHERE applicationID = :applicantID_selected_from_the_delete_form;

-------------------------------------------------------------------------
-- Companies page

-- Get all Companies for Companies table
SELECT companyID, name, description, website FROM Companies;

-- Add a new Company
INSERT INTO Companies (name, website, description) VALUES (:name_Input, :website_Input, :description_Input);

-- Get a single Company's data for the Update Company form
SELECT companyID, name, website, description FROM Companies WHERE companyID = :companyID_selected_from_browse_companies_page;

-- Update an Company's data based on submission of the Update Company form 
UPDATE Companies SET name = :name_Input, website = :website_Input, description = :description_Input WHERE companyID = :companyID_from_the_update_form;

-- Get a single Company's data for the Delete Company form
SELECT companyID, name FROM Companies WHERE companyID = :companyID_selected_from_browse_companies_page;

-- Delete a Company
DELETE FROM Companies WHERE companyID = :companyID_selected_from_the_delete_form;

------------------------------------------------------------------------------
-- Positions & Company Recruiters Page

-- Show all Positions and their associated Companies for Positions table on 
-- PositionsCompanyRecruiters page

SELECT Companies.name, Positions.title, Positions.location, Positions.salary, Positions.link, Positions.positionID
FROM Positions
INNER JOIN Companies ON Companies.companyID = Positions.companyID; -- May need to change this to OUTER JOIN or RIGHT/LEFT OUTER JOIN?

-- Show all titles, companies, links, recruiter names, emails, and linkedins for 
-- PositionsCompanyRecruiters table on PositionsCompanyRecruiters page

SELECT Companies.name, Positions.title, Positions.link, CompanyRecruiters.name,
CompanyRecruiters.recruiterID, Positions.positionID
FROM Positions
INNER JOIN Companies ON Companies.companyID = Positions.companyID -- May need to change this to OUTER JOIN or RIGHT/LEFT OUTER JOIN?
INNER JOIN PositionsCompanyRecruiters ON Positions.positionID = PositionsCompanyRecruiters.positionID
INNER JOIN CompanyRecruiters ON PositionsCompanyRecruiters.recruiterID = CompanyRecruiters.recruiterID;

-- Show all Recruiters and their respective Company name for Recruiters table on PositionsCompanyRecruiters page
SELECT name, email, phone, linkedin, lastContacted, details, recruiterID
FROM CompanyRecruiters;

-- Show all Company names to populate the Company Name drop down
SELECT companyID, name FROM Companies;

-- Show all Position Titles to populate the Position Title drop down
SELECT positionID, title FROM Positions;

-- Search Positions by associated Company name
SELECT Companies.name, Positions.title, Positions.locations, Positions.salary, Positions.link
FROM Positions
INNER JOIN Companies ON Companies.companyID = Positions.companyID -- May need to change this to OUTER JOIN or RIGHT/LEFT OUTER JOIN?
WHERE Companies.name = :company_name_from_dropdown_Input;

-- Search Positions by Positions Title
SELECT Companies.name, Positions.title, Positions.locations, Positions.salary, Positions.link
FROM Positions
INNER JOIN Companies ON Companies.companyID = Positions.companyID -- May need to change this to OUTER JOIN or RIGHT/LEFT OUTER JOIN?
WHERE Positions.title = :position_title_from_dropdown_Input;

-- Add a new Position
INSERT INTO Positions (companyID, title, location, salary, link)
VALUES (:companyID_or_NULL_from_dropdown_Input, :title_Input, :location_Input, :salary_Input, :link_Input);

-- Show all Position Titles and their respective Company names to populate Company & Position Title drop down
SELECT Companies.name, Positions.title
FROM Positions
INNER JOIN Companies ON Companies.companyID = Positions.companyID; -- May need to change this to OUTER JOIN or RIGHT/LEFT OUTER JOIN?

-- Show all Recruiters names to populate the Recruiter Name drop down
SELECT recruiterID, name FROM CompanyRecruiters;

-- Add a new Position with an associated Recruiter
INSERT INTO PositionsCompanyRecruiters (positionID, recruiterID)
VALUES (:positionID_from_the_add_form, :recruiterID_from_the_add_form);

-- Add a new Recruiter
INSERT INTO CompanyRecruiters (name, email, phone, linkedin, lastContacted, details)
VALUES (:name_Input, :email_Input, :phone_Input, :linkedin_Input, :lastContacted_Input, :details_Input);

-- Get a single Position's data for the Update Position form
SELECT Positions.positionID, Companies.name, Positions.title, Positions.location, Positions.salary, Positions.link 
FROM Positions 
INNER JOIN Companies ON Companies.companyID = Positions.companyID -- May need to change this to OUTER JOIN or RIGHT/LEFT OUTER JOIN?
WHERE positionID = :positionID_selected_from_browse_positions_page;

-- Update an Position's data based on submission of the Update Position form 
UPDATE Positions SET companyID = :companyID_from_dropdown_Input, title = :title_Input, location = :location_Input, salary = :salary_Input, link = :link_Input 
WHERE positionID = :positionID_from_the_update_form;

-- Get a single Recruiter's data for the Update Recruiter form
SELECT recruiterID, name, email, phone, linkedin, lastContacted, details
FROM CompanyRecruiters
WHERE recruiterID = :recruiterID_selected_from_browse_recruiters_page;

-- Update an Recruiter's data based on submission of the Update Recruiter form 
UPDATE CompanyRecruiters 
SET name = :name_Input, email = :email_Input, phone = :phone_Input, linkedin = :linkedin_Input, lastContacted = :lastContacted_Input, details = :details_Input 
WHERE recruiterID = :recruiterID_from_the_update_form;

-- Get a single Position and Recruiter's Affiliation data for the Delete Position and Recruiter Affiliation form
SELECT Positions.positionID, Positions.title, CompanyRecruiters.recruiterID, CompanyRecruiters.name
FROM Positions
INNER JOIN PositionsCompanyRecruiters ON PositionsCompanyRecruiters.positionID = Positions.positionID
INNER JOIN CompanyRecruiters ON PositionsCompanyRecruiters.recruiterID = CompanyRecruiters.recruiterID
WHERE PositionsCompanyRecruiters.positionsCompanyRecruitersID = :positionsCompanyRecruitersID_selected_from_browse_position_and_recruiter_affiliation_page;

-- Delete a Position and Recruiter Affiliation data
DELETE FROM positionsCompanyRecruiters 
WHERE positionsCompanyRecruitersID = :positionsCompanyRecruitersID_selected_from_the_delete_form;