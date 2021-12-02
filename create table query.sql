-- CREATE USER COMMANS
--create table users (
--	id nvarchar(100) primary key,
--	status bit not null,
--	name varchar(255) not null,
--	email nvarchar(255) unique not null,
--	password nvarchar(MAX)not null,
--	department nvarchar(100) not null,
--	designation nvarchar(100) not null,
--	role nvarchar(100) not null,
--	date_created date
--)







-- CREATE DOCUMENT COMMAND
--create table document(
--	id INT NOT NULL IDENTITY(1,1),
--	department varchar(10) not null,
--	created_by_user nvarchar(100) not null,
--	created_by_name nvarchar(255) not null,
--	created_by_department nvarchar(255) not null,
--	target_user nvarchar(100) not null,
--	isCompleted bit not null,
--	archived bit not null,
--	target_department nvarchar(100) not null,
--	description nvarchar(max),
--	date_created date,
--	primary key (id, department)
--)


-- CREATE DEPARTMENT TABLE
--create table department(
--	id int not null identity(1,1) primary key,
--	depHOD varchar(255) not null,
--	about nvarchar(max)
--)

-- CREATE USER APPROVED DOCUMENT
--create table approved_document_sequence (
--	uname nvarchar(100) not null,
--	docID int not null,
--	docDep varchar(100) not null
--)




-- CREATE user_notifications 
--create table user_notifications(
--	uname nvarchar(100) not null,
--	title nvarchar(255) not null,
--	docID int not null,
--	docDep nvarchar(100) not null,
--	msg nvarchar(max) not null,
--	icon nvarchar(100) not null,
--	time datetime not null,
--	category nvarchar(100) not null
--)


-- CREATE TABLE LOG
--create table logs(
--	docID int not null,
--	docDep nvarchar(100) not null,
--	forwardedToUname nvarchar(100) not null,
--	forwardedDep nvarchar(100) not null,
--	objection nvarchar(max) not null,
--	comments nvarchar(max) not null,
--	date date not null
--)


--CREATE TABLE SUQUENCE
--create table log_sequences(
--	docID int not null,
--	docDep nvarchar(100) not null,
--	sequence varchar(100) not null
--)