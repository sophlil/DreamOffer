-- Group 58
-- Don Reniff and Sophia Lilienthal


SET FOREIGN_KEY_CHECKS=0;
SET AUTOCOMMIT = 0;

DROP TABLE IF EXISTS Applicants;
DROP TABLE IF EXISTS Applications;
DROP TABLE IF EXISTS Positions;
DROP TABLE IF EXISTS Companies;
DROP TABLE IF EXISTS CompanyRecruiters;
DROP TABLE IF EXISTS PositionsCompanyRecruiters;

CREATE TABLE Applicants (
    applicantID int(11) AUTO_INCREMENT NOT NULL UNIQUE,
    name varchar(50) NOT NULL,
    email varchar(50) NOT NULL,
    PRIMARY KEY (applicantID)
);

CREATE TABLE Companies (
    companyID int(11) AUTO_INCREMENT NOT NULL UNIQUE,
    name varchar(50) NOT NULL,
    description varchar(255),
    website varchar(100),
    PRIMARY KEY (companyID)
);

CREATE TABLE Positions (
    positionID int(11) AUTO_INCREMENT NOT NULL UNIQUE,
    title varchar(100) NOT NULL,
    location varchar(100),
    salary int(11),
    link varchar(100) NOT NULL,
    companyID int(11),
    PRIMARY KEY (positionID),
    FOREIGN KEY (companyID) REFERENCES Companies(companyID) ON DELETE CASCADE
);

CREATE TABLE Applications (
    applicationID int(11) AUTO_INCREMENT NOT NULL UNIQUE,
    dateApplied date NOT NULL,
    result tinyint(1) DEFAULT 0,
    dateResult date DEFAULT NULL,
    applicantID int(11) NOT NULL,
    positionID int(11) NOT NULL, 
    PRIMARY KEY (applicationID),
    FOREIGN KEY (applicantID) REFERENCES Applicants(applicantID) ON DELETE CASCADE,
    FOREIGN KEY (positionID) REFERENCES Positions(positionID) ON DELETE CASCADE
);

CREATE TABLE CompanyRecruiters (
    recruiterID int(11) AUTO_INCREMENT NOT NULL UNIQUE,
    name varchar(50) NOT NULL,
    email varchar(50),
    phone varchar(12),
    linkedin varchar(100) NOT NULL,
    lastContacted date NOT NULL,
    details varchar(500) NOT NULL,
    PRIMARY KEY (recruiterID)
);

CREATE TABLE PositionsCompanyRecruiters (
    positionsCompanyRecruitersID int(11) NOT NULL,
    positionID int(11) NOT NULL,
    recruiterID int(11) NOT NULL,
    PRIMARY KEY (positionsCompanyRecruitersID),
    FOREIGN KEY (positionID) REFERENCES Positions(positionID) ON DELETE CASCADE,
    FOREIGN KEY (recruiterID) REFERENCES CompanyRecruiters(recruiterID) ON DELETE CASCADE
);

INSERT INTO Applicants (applicantID, name, email) VALUES
(1, 'Jeff Johnson', 'jjohnson@gmail.com'),
(2, 'Taya Howard', 'tayah9@icloud.com'),
(3, 'Elise McKinley', 'elise@yahoo.com'),
(4, 'John Seward', 'j.seward@gmail.com'),
(5, 'Xochit Lowe', 'xl56@gmail.com');

INSERT INTO Companies (companyID, name, description, website) VALUES
(100, 'Aptiv', 'Global tech company that develops safer, greener solutions which enable future of mobility.', 'https://aptiv.com'),
(101, 'Garmin', 'GPS tech company that creates navigation and communication products.', 'https://garmin.com'),
(102, 'Apple', 'Hardware & software for personal computers, phones, tablets, etc.', 'https://apple.com');

INSERT INTO CompanyRecruiters (recruiterID, name, email, phone, linkedin, lastContacted, details) VALUES
(300, 'Kelsey Wang', 'kwang.1@gmail.com', '318-995-8456', 'linkedin.com/kwang', '2022-10-01', 'Met at OSU Career Fair.'),
(301, 'Adrian Portillo', 'portilloa@garmin.com', NULL, 'linkedin.com/aportillo', '2022-09-29', 'Messaged me on Handshake.'),
(302, 'Daenerys Targaryen', 'targaryensrule@apple.com', NULL, 'linkedin.com/targaryensrule', '2022-01-11', 'Reached out on Linkedin.'),
(303, 'Jon Snow', 'jsnow@aptiv.com', '694-856-3144', 'linkedin.com/snow', '2022-11-25', 'Found on Aptiv website');

INSERT INTO Positions (positionID, title, location, salary, link, companyID) VALUES
(200, 'Software Engineer Intern', 'San Jose', NULL, 'aptiv.com/software-engineer-intern', (SELECT companyID FROM Companies WHERE name='Aptiv')),
(201, 'Application Developer', 'New York', 90000, 'aptiv.com/application-developer', (SELECT companyID FROM Companies WHERE name='Aptiv')),
(202, 'New Grad SWE', 'Seattle', 120000, 'garmin.com/new-grad-SWE', (SELECT companyID FROM Companies WHERE name='Garmin')),
(203, 'Data Engineer Intern', 'San Diego', 55000, 'apple.com/data-engineer-intern', (SELECT companyID FROM Companies WHERE name='Apple')),
(204, 'Database Administrator', 'Denver', 115000, 'garmin.com/database-administrator', (SELECT companyID FROM Companies WHERE name='Garmin')),
(205, 'Front-end Software Engineer', 'Remote', 35000, 'fiverr.com/front-end-software-engineer', NULL);

INSERT INTO Applications (applicationID, dateApplied, result, dateResult, applicantID, positionID) VALUES
(1, '2022-06-04', 3, '2022-06-29', (SELECT applicantID FROM Applicants WHERE email='jjohnson@gmail.com'), (SELECT positionID FROM Positions WHERE link='apple.com/data-engineer-intern')),
(2, '2022-07-15', 2, '2022-10-18', (SELECT applicantID FROM Applicants WHERE email='xl56@gmail.com'), (SELECT positionID FROM Positions WHERE link='aptiv.com/software-engineer-intern')),
(3, '2021-12-30', 3, '2022-05-30', (SELECT applicantID FROM Applicants WHERE email='tayah9@icloud.com'), (SELECT positionID FROM Positions WHERE link='garmin.com/database-administrator')),
(4, '2022-10-01', 1, '2022-10-05', (SELECT applicantID FROM Applicants WHERE email='j.seward@gmail.com'), (SELECT positionID FROM Positions WHERE link='garmin.com/database-administrator')),
(5, '2022-09-23', 0, NULL, (SELECT applicantID FROM Applicants WHERE email='jjohnson@gmail.com'), (SELECT positionID FROM Positions WHERE link='aptiv.com/application-developer'));

INSERT INTO PositionsCompanyRecruiters (positionsCompanyRecruitersID, positionID, recruiterID) VALUES
(1, (SELECT positionID FROM Positions WHERE link='aptiv.com/software-engineer-intern'), (SELECT recruiterID FROM CompanyRecruiters WHERE name='Kelsey Wang')),
(2, (SELECT positionID FROM Positions WHERE link='aptiv.com/software-engineer-intern'), (SELECT recruiterID FROM CompanyRecruiters WHERE name='Jon Snow')),
(3, (SELECT positionID FROM Positions WHERE link='garmin.com/database-administrator'), (SELECT recruiterID FROM CompanyRecruiters WHERE name='Adrian Portillo')),
(4, (SELECT positionID FROM Positions WHERE link='garmin.com/new-grad-SWE'), (SELECT recruiterID FROM CompanyRecruiters WHERE name='Adrian Portillo'));

SET FOREIGN_KEY_CHECKS=1;
COMMIT;