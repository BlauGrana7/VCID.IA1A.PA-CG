create database if not exists survey_db;
use survey_db;
CREATE TABLE if not exists user (
    username VARCHAR(50),
    email VARCHAR(100) PRIMARY KEY NOT NULL,
    password VARCHAR(100) NOT NULL
);
CREATE TABLE if not exists survey (
   email VARCHAR(50) PRIMARY KEY ,
    username VARCHAR(50),
    `Zufriedenheit Ausbildung` VARCHAR(255),
    `Qualitaet Dozenten` VARCHAR(255),
    `Infrastruktur` VARCHAR(255),
    `Berufliche Ziele` VARCHAR(255),
	`Vorbereitung Zertifikat` VARCHAR(255),
    `Vorbereitung Praxisarbeit` VARCHAR(255),
    `Praxis/Theorie` VARCHAR(255),
	`Schweregrad Ausbildung` VARCHAR(255),
    `Beschaeftigungsgrad Aktuell` VARCHAR(255),
    `Beschaeftigungsgrad Empfehlung` VARCHAR(255),
    `Online Unterricht` VARCHAR(255),
    `Weiterempfehlung von 1-10` VARCHAR(500),
    `Faecher Nutzen` VARCHAR(500),
    `Fehlender Inhalt` VARCHAR(500),
    `Verbesserungsvorschlaege` VARCHAR(255),
    Foreign Key (Email) references user (email)
);

CREATE TABLE IF NOT EXISTS admin (
    email VARCHAR(255) NOT NULL Primary key,
    password VARCHAR(255) NOT NULL
);
INSERT INTO admin (email, password)
VALUES ('admin@gmail.com', 'pass');
