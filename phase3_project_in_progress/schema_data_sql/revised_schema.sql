
DROP DATABASE IF EXISTS cs6400_demodata;

CREATE DATABASE IF NOT EXISTS cs6400_demodata
    DEFAULT CHARACTER SET utf8mb4 
    DEFAULT COLLATE utf8mb4_unicode_ci;

USE cs6400_demodata;

CREATE TABLE PriviledgedUsers(
	Username varchar(50) NOT NULL,
	FirstName varchar(50) NOT NULL,
	LastName varchar(50) NOT NULL,
	Password varchar(50) NOT NULL,
	PRIMARY KEY (Username)
);


CREATE TABLE Owner (
Username varchar(50) NOT NULL,
PRIMARY KEY (Username)
);


CREATE TABLE Salespeople (
Username varchar(50) NOT NULL,
PRIMARY KEY (Username)
);


CREATE TABLE InventoryClerks (
Username varchar(50) NOT NULL,
PRIMARY KEY (Username)
);


CREATE TABLE ServiceWriters (
Username varchar(50) NOT NULL,
PRIMARY KEY (Username)
);


CREATE TABLE Managers (
Username varchar(50) NOT NULL,
PRIMARY KEY (Username)
);


CREATE TABLE Customers (
CustomerID int(16) NOT NULL AUTO_INCREMENT,
Street varchar(250) NOT NULL,
City varchar(50) NOT NULL,
State varchar(50) NOT NULL,
ZipCode varchar(10) NOT NULL,
Email varchar(250) DEFAULT NULL,
PhoneNum varchar(13) NOT NULL,
PRIMARY KEY (CustomerID)
);


CREATE TABLE Persons (
License varchar(25) NOT NULL,
Firstname varchar(50) NOT NULL,
LastName varchar(50) NOT NULL,
CustomerID int(16) NOT NULL,
PRIMARY KEY (License),
UNIQUE KEY CustomerID (CustomerID)
);


CREATE TABLE Business (
TaxNum varchar(11) NOT NULL,
Name varchar(50) NOT NULL,
ContactFName varchar(50) NOT NULL,
ContactLName varchar(50) NOT NULL,
ContactTitle varchar(50) NOT NULL,
CustomerID int(16) NOT NULL,
PRIMARY KEY (TaxNum),
UNIQUE KEY CustomerID (CustomerID)
);




CREATE TABLE Manufacturer (
ManufacturerName varchar(50) NOT NULL,
PRIMARY KEY (ManufacturerName)
);


CREATE TABLE Vehicles (
	Vin varchar(17)  NOT NULL,
	Manufacturer varchar(50) NOT NULL,
	ModelName varchar(50) NOT NULL,
	ModelYear year  NOT NULL,
	DateAdded date  NOT NULL,
	InvoicePrice decimal(10, 2) NOT NULL,
	Description varchar(1500)  DEFAULT NULL,
	ClerkUsername varchar(50)  NOT NULL,
	PRIMARY KEY (Vin),
	KEY Manufacturer (Manufacturer),
	KEY ClerkUsername (ClerkUsername)
);


CREATE TABLE VehicleColors (
	Vin varchar(17)  NOT NULL,
	Colors varchar(50) NOT NULL,
	PRIMARY KEY (Vin, Colors)
);

CREATE TABLE Colors(
	Color varchar(50) NOT NULL,
	PRIMARY KEY (Color)
);


CREATE TABLE Cars (
Vin varchar(17)  NOT NULL,
NumOfDoors int(16) NOT NULL ,
PRIMARY KEY (Vin)
);
 
CREATE TABLE Convertibles (
Vin varchar(17)  NOT NULL,
RoofType varchar(25) NOT NULL,
BackSeatCount int(16) NOT NULL,
PRIMARY KEY (Vin)
);
 
CREATE TABLE Trucks (
Vin varchar(17)  NOT NULL,
CargoCapacity decimal(10,2) NOT NULL,
CargoCoverType varchar(25) DEFAULT NULL,
NumberOfRearAxies int(16) NOT NULL,
PRIMARY KEY (Vin)
);
 
CREATE TABLE VanMiniVans (
Vin varchar(17)  NOT NULL,
HasDriverSideBackDoor boolean NOT NULL,
PRIMARY KEY (Vin)
);
 
CREATE TABLE SUVs (
Vin varchar(17)  NOT NULL,
DrivetrainType varchar(25) NOT NULL,
NumberOfCupHolders int(16) NOT NULL,
PRIMARY KEY (Vin)
);

CREATE TABLE SalesEvents(
Vin varchar(17)  NOT NULL,
SaleDate date NOT NULL,
SalePrice decimal(10, 2) NOT NULL,
CustomerID int(16) NOT NULL,
Username varchar(50) NOT NULL,
PRIMARY KEY (Vin),
KEY CustomerID (CustomerID),
KEY Username (Username)
);


CREATE TABLE RepairEvents(
Vin varchar(17)  NOT NULL,
StartDate date NOT NULL,
EndDate date DEFAULT NULL,
LaborCharge decimal(10, 2) NOT NULL DEFAULT 0.00,
Odometer int(16) NOT NULL,
Description varchar(1500)  DEFAULT NULL,
CustomerID int(16) NOT NULL,
Username varchar(50) NOT NULL,
PRIMARY KEY (Vin, StartDate),
KEY Vin (Vin),
KEY CustomerID(CustomerID),
KEY Username (Username)
);


CREATE TABLE Parts(
Vin varchar(17)  NOT NULL,
StartDate date NOT NULL,
Number varchar(50) NOT NULL,
Price decimal(10, 2) NOT NULL,
VendorName varchar(50) NOT NULL,
QuantityUsed int(16) NOT NULL,
PRIMARY KEY (Vin, StartDate,Number)
);


ALTER TABLE Owner
	ADD CONSTRAINT fk_owner_user FOREIGN KEY (Username) REFERENCES PriviledgedUsers (Username);


ALTER TABLE Salespeople
	ADD CONSTRAINT fk_salespeople_user FOREIGN KEY (Username) REFERENCES PriviledgedUsers (Username);


ALTER TABLE ServiceWriters
	ADD CONSTRAINT fk_servicewriters_user FOREIGN KEY (Username) REFERENCES PriviledgedUsers (Username);


ALTER TABLE InventoryClerks
	ADD CONSTRAINT fk_inventoryclerks_user FOREIGN KEY (Username) REFERENCES PriviledgedUsers (Username);


ALTER TABLE Managers
	ADD CONSTRAINT fk_managers_user FOREIGN KEY (Username) REFERENCES PriviledgedUsers (Username);

ALTER TABLE Vehicles
	ADD CONSTRAINT fk_vehicles_manufactrurer FOREIGN KEY (Manufacturer) REFERENCES Manufacturer (ManufacturerName),
	ADD CONSTRAINT fk_vehicles_clerk FOREIGN KEY (ClerkUsername) REFERENCES InventoryClerks (Username);


ALTER TABLE VehicleColors
	ADD CONSTRAINT fk_vehiclecolors_vehicles FOREIGN KEY (Vin) REFERENCES Vehicles(Vin),
	ADD CONSTRAINT fk_vehiclecolors_colorss FOREIGN KEY (Colors) REFERENCES Colors(Color);

ALTER TABLE Cars
ADD CONSTRAINT fk_cars_vehicles FOREIGN KEY (Vin) REFERENCES Vehicles(Vin);


ALTER TABLE Trucks
ADD CONSTRAINT fk_trucks_vehicles FOREIGN KEY (Vin) REFERENCES Vehicles(Vin);


ALTER TABLE Convertibles
ADD CONSTRAINT fk_convertibles_vehicles FOREIGN KEY (Vin) REFERENCES Vehicles(Vin);


ALTER TABLE VanMiniVans
ADD CONSTRAINT fk_vanminivans_vehicles FOREIGN KEY (Vin) REFERENCES Vehicles(Vin);


ALTER TABLE SUVs
ADD CONSTRAINT fk_suvs_vehicles FOREIGN KEY (Vin) REFERENCES Vehicles(Vin);


ALTER TABLE Persons
ADD CONSTRAINT Persons_CustomerID FOREIGN KEY (CustomerID) REFERENCES Customers (CustomerID);
 

ALTER TABLE Business
ADD CONSTRAINT Business_CustomerID FOREIGN KEY (CustomerID) REFERENCES Customers (CustomerID);


ALTER TABLE SalesEvents
	ADD CONSTRAINT fk_sales_vehicles FOREIGN KEY (Vin) REFERENCES Vehicles (Vin),
	ADD CONSTRAINT fk_sales_salespeople FOREIGN KEY (Username) REFERENCES Salespeople (Username),
	ADD CONSTRAINT fk_sales_customers FOREIGN KEY (CustomerID) REFERENCES Customers (CustomerID);

ALTER TABLE RepairEvents
	ADD CONSTRAINT fk_repairs_vehicles FOREIGN KEY (Vin) REFERENCES Vehicles (Vin) ON DELETE CASCADE ON UPDATE CASCADE,
	ADD CONSTRAINT fk_repairs_servicewriters FOREIGN KEY (Username) REFERENCES ServiceWriters (Username),
	ADD CONSTRAINT fk_repairs_customers FOREIGN KEY (CustomerID) REFERENCES Customers (CustomerID);

ALTER TABLE Parts
	ADD CONSTRAINT fk_parts_repairs FOREIGN KEY (Vin, StartDate) REFERENCES RepairEvents (Vin, StartDate) ON DELETE CASCADE ON UPDATE CASCADE;

