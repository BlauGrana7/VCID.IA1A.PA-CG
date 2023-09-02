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
    `Area of Computer Science Interest` VARCHAR(255),
    `Most Difficult Area of Computer Science` VARCHAR(255),
    `Quality of Teaching materials` VARCHAR(255),
    `Quality of Teaching` VARCHAR(255),
	`Satisfaction with Training Organization` VARCHAR(255),
    `Recommendation of Training` VARCHAR(255),
    `Level of Difficulty of Training` VARCHAR(255),
	`Frequency of Feeling Challenged by Training` VARCHAR(255),
    `Level of Preparation After Training` VARCHAR(255),
    `Diversity of Students in Training` VARCHAR(255),
    `Support from Faculty and Staff` VARCHAR(255),
    `Level of Recommendation of Company on 1-10 Scale` VARCHAR(500),
    `Strengths and Weaknesses` VARCHAR(500),
    `Wish for Future` VARCHAR(500),
    `To be Changed in Future` VARCHAR(255),
    Foreign Key (Email) references user (email)
);

CREATE TABLE IF NOT EXISTS admin (
    email VARCHAR(255) NOT NULL Primary key,
    password VARCHAR(255) NOT NULL
);
INSERT INTO admin (email, password)
VALUES ('admin@gmail.com', 'pass');
