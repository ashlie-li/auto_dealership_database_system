
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






--add constraints
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


--insert table
INSERT INTO priviledgedusers (Username,Firstname,Lastname,`Password`) VALUES ('owner1','Owner','One','abc123');
INSERT INTO priviledgedusers (Username,Firstname,Lastname,`Password`) VALUES ('clerk1','Clerk','One','abc123');
INSERT INTO priviledgedusers (Username,Firstname,Lastname,`Password`) VALUES ('clerk2','Clerk','Two','abc123');
INSERT INTO priviledgedusers (Username,Firstname,Lastname,`Password`) VALUES ('salesperson1','Sales','One','abc123');
INSERT INTO priviledgedusers (Username,Firstname,Lastname,`Password`) VALUES ('salesperson2','Sales','Two','abc123');
INSERT INTO priviledgedusers (Username,Firstname,Lastname,`Password`) VALUES ('salesperson3','Sales','Three','abc123');
INSERT INTO priviledgedusers (Username,Firstname,Lastname,`Password`) VALUES ('manager1','Manager','One','abc123');
INSERT INTO priviledgedusers (Username,Firstname,Lastname,`Password`) VALUES ('manager2','Manager','Two','abc123');
INSERT INTO priviledgedusers (Username,Firstname,Lastname,`Password`) VALUES ('writer1','Writer','One','abc123');
INSERT INTO priviledgedusers (Username,Firstname,Lastname,`Password`) VALUES ('writer2','Writer','Two','abc123');


INSERT INTO owner (Username) VALUES ('owner1');
INSERT INTO inventoryclerks  (Username) VALUES ('owner1');
INSERT INTO salespeople (Username) VALUES ('owner1');
INSERT INTO managers (Username) VALUES ('owner1');
INSERT INTO servicewriters (Username) VALUES ('owner1');
INSERT INTO inventoryclerks (Username) VALUES ('clerk1');
INSERT INTO inventoryclerks (Username) VALUES ('clerk2');
INSERT INTO salespeople (Username) VALUES ('salesperson1');
INSERT INTO salespeople (Username) VALUES ('salesperson2');
INSERT INTO salespeople (Username) VALUES ('salesperson3');
INSERT INTO managers (Username) VALUES ('manager1');
INSERT INTO managers (Username) VALUES ('manager2');
INSERT INTO servicewriters (Username) VALUES ('writer1');
INSERT INTO servicewriters (Username) VALUES ('writer2');


INSERT INTO manufacturer (manufacturername) VALUES ('Toyota');
INSERT INTO manufacturer (manufacturername) VALUES ('Honda');
INSERT INTO manufacturer (manufacturername) VALUES ('Nissan');
INSERT INTO manufacturer (manufacturername) VALUES ('Subaru');
INSERT INTO manufacturer (manufacturername) VALUES ('Mazda');
INSERT INTO manufacturer (manufacturername) VALUES ('Ford');
INSERT INTO manufacturer (manufacturername) VALUES ('RAM');
INSERT INTO manufacturer (manufacturername) VALUES ('Chevrolet');
INSERT INTO manufacturer (manufacturername) VALUES ('Cadillac');
INSERT INTO manufacturer (manufacturername) VALUES ('BMW');
INSERT INTO manufacturer (manufacturername) VALUES ('Benz');
INSERT INTO manufacturer (manufacturername) VALUES ('Audi');
INSERT INTO manufacturer (manufacturername) VALUES ('Volkswagen');
INSERT INTO manufacturer (manufacturername) VALUES ('Volvo');
INSERT INTO manufacturer (manufacturername) VALUES ('Tesla');
INSERT INTO manufacturer (manufacturername) VALUES ('Porsche');
INSERT INTO manufacturer (manufacturername) VALUES ('Mini');
INSERT INTO manufacturer (manufacturername) VALUES ('Range Rover');

INSERT INTO vehicles (Vin,ModelName,ModelYear,DateAdded,InvoicePrice,Description,Manufacturer,ClerkUsername) VALUES
	('CON1','Z4','2020','2021-11-1',70000,'fast','BMW','clerk1');
INSERT INTO vehicles (Vin,ModelName,ModelYear,DateAdded,InvoicePrice,Description,Manufacturer,ClerkUsername) VALUES('CON2','CooperS','2021','2021-11-1',40000,'good car','Mini','clerk2');
INSERT INTO vehicles (Vin,ModelName,ModelYear,DateAdded,InvoicePrice,Description,Manufacturer,ClerkUsername) VALUES('CON3','911','2021','2021-10-1',120000,'fast','Porsche','clerk1');
INSERT INTO vehicles (Vin,ModelName,ModelYear,DateAdded,InvoicePrice,Description,Manufacturer,ClerkUsername) VALUES('CON4','A43','2019','2019-12-1',65000,'good Benz','Benz','clerk1');
INSERT INTO vehicles (Vin,ModelName,ModelYear,DateAdded,InvoicePrice,Description,Manufacturer,ClerkUsername) VALUES('CON5','86','1995','2020-5-1',35000,'classic','Toyota','clerk2');
INSERT INTO vehicles (Vin,ModelName,ModelYear,DateAdded,InvoicePrice,Description,Manufacturer,ClerkUsername) VALUES('CON6','TT','2022','2021-2-1',45000, 'good car','Audi','clerk1');
INSERT INTO vehicles (Vin,ModelName,ModelYear,DateAdded,InvoicePrice,Description,Manufacturer,ClerkUsername) VALUES('CAR1','Civic','2021','2021-10-1',18000,'good car','Honda','clerk1');
INSERT INTO vehicles (Vin,ModelName,ModelYear,DateAdded,InvoicePrice,Description,Manufacturer,ClerkUsername) VALUES('CAR2','Accord','2020','2021-1-1',28000,'good car','Honda','clerk2');
INSERT INTO vehicles (Vin,ModelName,ModelYear,DateAdded,InvoicePrice,Description,Manufacturer,ClerkUsername) VALUES('CAR3','Corona','2021','2021-11-1',18000,'good car','Toyota','clerk1');
INSERT INTO vehicles (Vin,ModelName,ModelYear,DateAdded,InvoicePrice,Description,Manufacturer,ClerkUsername) VALUES('CAR4','Corona','2022','2021-5-1',20000,'good car','Toyota','clerk2');
INSERT INTO vehicles (Vin,ModelName,ModelYear,DateAdded,InvoicePrice,Description,Manufacturer,ClerkUsername) VALUES('CAR5','Camry','2021','2020-12-1',32000,'good car','Toyota','clerk1');
INSERT INTO vehicles (Vin,ModelName,ModelYear,DateAdded,InvoicePrice,Description,Manufacturer,ClerkUsername) VALUES('CAR6','Altima','2019','2020-1-1',30000,'good car','Nissan','clerk2');
INSERT INTO vehicles (Vin,ModelName,ModelYear,DateAdded,InvoicePrice,Description,Manufacturer,ClerkUsername) VALUES('CAR7','340','2019','2020-5-1',40000,'fast','BMW','clerk1');
INSERT INTO vehicles (Vin,ModelName,ModelYear,DateAdded,InvoicePrice,Description,Manufacturer,ClerkUsername) VALUES('CAR8','530','2020','2021-1-1',60000,'good car','BMW','clerk2');
INSERT INTO vehicles (Vin,ModelName,ModelYear,DateAdded,InvoicePrice,Description,Manufacturer,ClerkUsername) VALUES('CAR9','S600','2018','2019-1-1',100000,'luxury','Benz','clerk1');
INSERT INTO vehicles (Vin,ModelName,ModelYear,DateAdded,InvoicePrice,Description,Manufacturer,ClerkUsername) VALUES('CAR10','C63','2020','2020-2-1',80000,'fast','Benz','clerk2');
INSERT INTO vehicles (Vin,ModelName,ModelYear,DateAdded,InvoicePrice,Description,Manufacturer,ClerkUsername) VALUES('CAR11','Focus','2015','2019-1-1',10000,'good car','Ford','clerk1');
INSERT INTO vehicles (Vin,ModelName,ModelYear,DateAdded,InvoicePrice,Description,Manufacturer,ClerkUsername) VALUES('CAR12','ModelS','2021','2021-2-1',60000,'good car','Tesla','clerk2');
INSERT INTO vehicles (Vin,ModelName,ModelYear,DateAdded,InvoicePrice,Description,Manufacturer,ClerkUsername) VALUES('VAN1','Alpha','2020','2021-1-1',60000,'good car','Toyota','clerk1');
INSERT INTO vehicles (Vin,ModelName,ModelYear,DateAdded,InvoicePrice,Description,Manufacturer,ClerkUsername) VALUES('VAN2','Siena','2019','2020-1-1',30000,'good car','Toyota','clerk2');
INSERT INTO vehicles (Vin,ModelName,ModelYear,DateAdded,InvoicePrice,Description,Manufacturer,ClerkUsername) VALUES('VAN3','VW','1970','2016-1-1',20000,'good car','Volkswagen','clerk2');
INSERT INTO vehicles (Vin,ModelName,ModelYear,DateAdded,InvoicePrice,Description,Manufacturer,ClerkUsername) VALUES('VAN4','VW','1980','2014-1-1',22000,'good car','Volkswagen','clerk1');
INSERT INTO vehicles (Vin,ModelName,ModelYear,DateAdded,InvoicePrice,Description,Manufacturer,ClerkUsername) VALUES('TRU1','XX','2019','2020-1-1',60000,'good car','Volvo','clerk2');
INSERT INTO vehicles (Vin,ModelName,ModelYear,DateAdded,InvoicePrice,Description,Manufacturer,ClerkUsername) VALUES('TRU2','F150','2018','2019-1-1',30000,'good car','Ford','clerk1');
INSERT INTO vehicles (Vin,ModelName,ModelYear,DateAdded,InvoicePrice,Description,Manufacturer,ClerkUsername) VALUES('TRU3','XX','2017','2018-1-1',40000,'good car','Volvo','clerk2');
INSERT INTO vehicles (Vin,ModelName,ModelYear,DateAdded,InvoicePrice,Description,Manufacturer,ClerkUsername) VALUES('TRU4','F150','2018','2018-1-1',28000,'good car','Ford','clerk1');
INSERT INTO vehicles (Vin,ModelName,ModelYear,DateAdded,InvoicePrice,Description,Manufacturer,ClerkUsername) VALUES('TRU5','KK','2020','2021-1-1',25000,'good car','RAM','clerk2');
INSERT INTO vehicles (Vin,ModelName,ModelYear,DateAdded,InvoicePrice,Description,Manufacturer,ClerkUsername) VALUES('TRU6','KK','2021','2021-1-1',24000,'good car','RAM','clerk1');
INSERT INTO vehicles (Vin,ModelName,ModelYear,DateAdded,InvoicePrice,Description,Manufacturer,ClerkUsername) VALUES('TRU7','ZZ','2020','2020-4-1',30000,'good car','Toyota','clerk2');
INSERT INTO vehicles (Vin,ModelName,ModelYear,DateAdded,InvoicePrice,Description,Manufacturer,ClerkUsername) VALUES('TRU8','YY','2020','2021-4-1',70000,'good car','Benz','clerk2');
INSERT INTO vehicles (Vin,ModelName,ModelYear,DateAdded,InvoicePrice,Description,Manufacturer,ClerkUsername) VALUES('TRU9','F250','2019','2020-1-1',31000,'cheap','Ford','clerk1');
INSERT INTO vehicles (Vin,ModelName,ModelYear,DateAdded,InvoicePrice,Description,Manufacturer,ClerkUsername) VALUES('SUV1','CRV','2018','2019-1-1',30000,'good car','Honda','clerk2');
INSERT INTO vehicles (Vin,ModelName,ModelYear,DateAdded,InvoicePrice,Description,Manufacturer,ClerkUsername) VALUES('SUV2','RAV4','2017','2018-1-1',32000,'good car','Toyota','clerk1');
INSERT INTO vehicles (Vin,ModelName,ModelYear,DateAdded,InvoicePrice,Description,Manufacturer,ClerkUsername) VALUES('SUV3','RAV4','2020','2021-4-1',35000,'good car','Toyota','clerk2');
INSERT INTO vehicles (Vin,ModelName,ModelYear,DateAdded,InvoicePrice,Description,Manufacturer,ClerkUsername) VALUES('SUV4','Highlander','2019','2019-1-1',40000,'good car','Toyota','clerk1');
INSERT INTO vehicles (Vin,ModelName,ModelYear,DateAdded,InvoicePrice,Description,Manufacturer,ClerkUsername) VALUES('SUV5','X3','2018','2018-1-1',38000,'good car','BMW','clerk2');
INSERT INTO vehicles (Vin,ModelName,ModelYear,DateAdded,InvoicePrice,Description,Manufacturer,ClerkUsername) VALUES('SUV6','X5','2021','2021-4-1',50000,'good car','BMW','clerk2');
INSERT INTO vehicles (Vin,ModelName,ModelYear,DateAdded,InvoicePrice,Description,Manufacturer,ClerkUsername) VALUES('SUV7','Q5','2020','2020-1-1',41000,'good car','Audi','clerk1');
INSERT INTO vehicles (Vin,ModelName,ModelYear,DateAdded,InvoicePrice,Description,Manufacturer,ClerkUsername) VALUES('SUV8','Q7','2020','2021-4-1',49000,'good car','Audi','clerk2');
INSERT INTO vehicles (Vin,ModelName,ModelYear,DateAdded,InvoicePrice,Description,Manufacturer,ClerkUsername) VALUES('SUV9','ModelY','2019','2020-1-1',50000,'electric','Tesla','clerk1');
INSERT INTO vehicles (Vin,ModelName,ModelYear,DateAdded,InvoicePrice,Description,Manufacturer,ClerkUsername) VALUES('SUV10','ModelY','2019','2020-1-1',52000,'electric','Tesla','clerk1');

INSERT INTO convertibles (Vin,RoofType,BackSeatCount) VALUES('CON1','A',2);
INSERT INTO convertibles (Vin,RoofType,BackSeatCount) VALUES('CON2','A',3);
INSERT INTO convertibles (Vin,RoofType,BackSeatCount) VALUES('CON3','B',2);
INSERT INTO convertibles (Vin,RoofType,BackSeatCount) VALUES('CON4','A',0);
INSERT INTO convertibles (Vin,RoofType,BackSeatCount) VALUES('CON5','B',2);
INSERT INTO convertibles (Vin,RoofType,BackSeatCount) VALUES('CON6','B',0);

INSERT INTO cars (Vin,NumOfDoors) VALUES('CAR1',4);
INSERT INTO cars (Vin,NumOfDoors) VALUES('CAR2',4);
INSERT INTO cars (Vin,NumOfDoors) VALUES('CAR3',4);
INSERT INTO cars (Vin,NumOfDoors) VALUES('CAR4',2);
INSERT INTO cars (Vin,NumOfDoors) VALUES('CAR5',4);
INSERT INTO cars (Vin,NumOfDoors) VALUES('CAR6',4);
INSERT INTO cars (Vin,NumOfDoors) VALUES('CAR7',4);
INSERT INTO cars (Vin,NumOfDoors) VALUES('CAR8',4);
INSERT INTO cars (Vin,NumOfDoors) VALUES('CAR9',6);
INSERT INTO cars (Vin,NumOfDoors) VALUES('CAR10',4);
INSERT INTO cars (Vin,NumOfDoors) VALUES('CAR11',2);
INSERT INTO cars (Vin,NumOfDoors) VALUES('CAR12',4);

INSERT INTO suvs (Vin,DrivetrainType,NumberOfCupHolders) VALUES('SUV1','RWD',5);
INSERT INTO suvs (Vin,DrivetrainType,NumberOfCupholders) VALUES('SUV2','FWD',3);
INSERT INTO suvs (Vin,DrivetrainType,NumberOfCupholders) VALUES('SUV3','FWD',6);
INSERT INTO suvs (Vin,DrivetrainType,NumberOfCupholders) VALUES('SUV4','AWD',5);
INSERT INTO suvs (Vin,DrivetrainType,NumberOfCupholders) VALUES('SUV5','AWD',3);
INSERT INTO suvs (Vin,DrivetrainType,NumberOfCupholders) VALUES('SUV6','RWD',3);
INSERT INTO suvs (Vin,DrivetrainType,NumberOfCupholders) VALUES('SUV7','RWD',4);
INSERT INTO suvs (Vin,DrivetrainType,NumberOfCupholders) VALUES('SUV8','FWD',4);
INSERT INTO suvs (Vin,DrivetrainType,NumberOfCupholders) VALUES('SUV9','AWD',5);
INSERT INTO suvs (Vin,DrivetrainType,NumberOfCupholders) VALUES('SUV10','AWD',6);

INSERT INTO trucks (Vin,CargoCoverType,NumberOfRearAxies,CargoCapacity) VALUES('TRU1','hard',3,10);
INSERT INTO trucks (Vin,CargoCoverType,NumberOfRearAxies,CargoCapacity) VALUES('TRU2',NULL,2,6);
INSERT INTO trucks (Vin,CargoCoverType,NumberOfRearAxies,CargoCapacity) VALUES('TRU3','hard',4,20);
INSERT INTO trucks (Vin,CargoCoverType,NumberOfRearAxies,CargoCapacity) VALUES('TRU4',NULL,2,4);
INSERT INTO trucks (Vin,CargoCoverType,NumberOfRearAxies,CargoCapacity) VALUES('TRU5',NULL,1,2);
INSERT INTO trucks (Vin,CargoCoverType,NumberOfRearAxies,CargoCapacity) VALUES('TRU6','soft',1,2.5);
INSERT INTO trucks (Vin,CargoCoverType,NumberOfRearAxies,CargoCapacity) VALUES('TRU7','soft',2,8.5);
INSERT INTO trucks (Vin,CargoCoverType,NumberOfRearAxies,CargoCapacity) VALUES('TRU8','hard',3,14);
INSERT INTO trucks (Vin,CargoCoverType,NumberOfRearAxies,CargoCapacity) VALUES('TRU9','hard',2,7);

INSERT INTO vanminivans (Vin,HasDriverSideBackDoor) VALUES('VAN1',TRUE);
INSERT INTO vanminivans (Vin,HasDriverSideBackDoor) VALUES('VAN2',TRUE);
INSERT INTO vanminivans (Vin,HasDriverSideBackDoor) VALUES('VAN3',FALSE);
INSERT INTO vanminivans (Vin,HasDriverSideBackDoor) VALUES('VAN4',TRUE);


INSERT INTO customers (Street,City,State,ZipCode,Email,PhoneNum) VALUES ('1 1st Street','Atlanta','GA','30001','abc@z.com','7700000001');
INSERT INTO customers (Street,City,State,ZipCode,Email,PhoneNum) VALUES ('1 1st Street','Sandy Spring','GA','30002','abc@z.com','7701011111');
INSERT INTO customers (Street,City,State,ZipCode,Email,PhoneNum) VALUES ('32 Piedmont Rd Apt 51','Marietta','GA','30003','def@z.com','4400100002');
INSERT INTO customers (Street,City,State,ZipCode,Email,PhoneNum) VALUES ('400 Peachtree Rd','Atlanta','GA','30004','k123@z.com','4400000040');
INSERT INTO customers (Street,City,State,ZipCode,Email,PhoneNum) VALUES ('320 Peachtree St','Atlanta','GA','30005','p123@y.com','6788888888');
INSERT INTO customers (Street,City,State,ZipCode,Email,PhoneNum) VALUES ('123 Roswell Rd','Sandy Spring','GA','30006','8191@qq.com','6781238888');
INSERT INTO customers (Street,City,State,ZipCode,Email,PhoneNum) VALUES ('40 MLK Rd','Atlanta','GA','30001','kkk@y.com','7708881238');
INSERT INTO customers (Street,City,State,ZipCode,Email,PhoneNum) VALUES ('21 Northside Dr','Marietta','GA','30030','q123@z.com','7707777324');

INSERT INTO persons (License,Firstname,Lastname,CustomerID) VALUES ('111','Adam','Johnson',1);
INSERT INTO persons (License,Firstname,Lastname,CustomerID) VALUES ('222','Jane','Miller',2);
INSERT INTO persons (License,Firstname,Lastname,CustomerID) VALUES ('333','David','Zhang',3);
INSERT INTO persons (License,Firstname,Lastname,CustomerID) VALUES ('444','Lisa','Jackson',4);
INSERT INTO persons (License,Firstname,Lastname,CustomerID) VALUES ('555','Tim','Dias',5);

INSERT INTO business (TaxNum,Name,ContactFName,ContactLName,ContactTitle,CustomerID) VALUES ('666','A company','Jack','Goodman','Manager',6);
INSERT INTO business (TaxNum,Name,ContactFName,ContactLName,ContactTitle,CustomerID) VALUES ('777','B company','Mary','May','Director',7);
INSERT INTO business (TaxNum,Name,ContactFName,ContactLName,ContactTitle,CustomerID) VALUES ('888','C company','Bruno','Silva','Head',8);                                                                                          

INSERT INTO salesevents (Vin,Username,SaleDate,SalePrice,CustomerID) VALUES ('CON1','salesperson1','2021-05-01',81000,1);
INSERT INTO salesevents (Vin,Username,SaleDate,SalePrice,CustomerID) VALUES ('CON4','salesperson2','2020-01-01',80000,1);
INSERT INTO salesevents (Vin,Username,SaleDate,SalePrice,CustomerID) VALUES ('CON5','owner1','2021-01-01',34000,4);
INSERT INTO salesevents (Vin,Username,SaleDate,SalePrice,CustomerID) VALUES ('CAR2','salesperson2','2021-02-01',37000,3);
INSERT INTO salesevents (Vin,Username,SaleDate,SalePrice,CustomerID) VALUES ('CAR6','salesperson2','2021-03-01',29000,7);
INSERT INTO salesevents (Vin,Username,SaleDate,SalePrice,CustomerID) VALUES ('CAR7','salesperson1','2020-12-01',52500,4);
INSERT INTO salesevents (Vin,Username,SaleDate,SalePrice,CustomerID) VALUES ('CAR8','salesperson3','2020-04-01',59000,2);
INSERT INTO salesevents (Vin,Username,SaleDate,SalePrice,CustomerID) VALUES ('CAR9','salesperson1','2020-01-01',120000,2);
INSERT INTO salesevents (Vin,Username,SaleDate,SalePrice,CustomerID) VALUES ('CAR10','salesperson2','2021-01-01',85000,1);
INSERT INTO salesevents (Vin,Username,SaleDate,SalePrice,CustomerID) VALUES ('CAR11','salesperson1','2019-10-01',12000,6);
INSERT INTO salesevents (Vin,Username,SaleDate,SalePrice,CustomerID) VALUES ('VAN2','salesperson2','2021-01-01',33000,5);
INSERT INTO salesevents (Vin,Username,SaleDate,SalePrice,CustomerID) VALUES ('VAN3','salesperson1','2017-02-01',25000,8);
INSERT INTO salesevents (Vin,Username,SaleDate,SalePrice,CustomerID) VALUES ('VAN4','salesperson2','2019-01-01',21000,7);
INSERT INTO salesevents (Vin,Username,SaleDate,SalePrice,CustomerID) VALUES ('TRU1','salesperson3','2021-01-01',61201.15,6);
INSERT INTO salesevents (Vin,Username,SaleDate,SalePrice,CustomerID) VALUES ('TRU2','salesperson3','2020-02-01',29999.05,5);
INSERT INTO salesevents (Vin,Username,SaleDate,SalePrice,CustomerID) VALUES ('TRU3','owner1','2019-02-01',35005.62,4);
INSERT INTO salesevents (Vin,Username,SaleDate,SalePrice,CustomerID) VALUES ('TRU4','salesperson3','2019-03-01',38000,3);
INSERT INTO salesevents (Vin,Username,SaleDate,SalePrice,CustomerID) VALUES ('TRU9','salesperson2','2021-01-01',31001.01,2);
INSERT INTO salesevents (Vin,Username,SaleDate,SalePrice,CustomerID) VALUES ('SUV1','salesperson2','2020-01-01',31000,1);
INSERT INTO salesevents (Vin,Username,SaleDate,SalePrice,CustomerID) VALUES ('SUV2','salesperson3','2021-02-01',49000,8);
INSERT INTO salesevents (Vin,Username,SaleDate,SalePrice,CustomerID) VALUES ('SUV4','salesperson1','2021-03-01',50000,3);
INSERT INTO salesevents (Vin,Username,SaleDate,SalePrice,CustomerID) VALUES ('SUV5','owner1','2019-04-01',34000,4);
INSERT INTO salesevents (Vin,Username,SaleDate,SalePrice,CustomerID) VALUES ('SUV9','salesperson1','2021-05-01',76000,2);
INSERT INTO salesevents (Vin,Username,SaleDate,SalePrice,CustomerID) VALUES ('SUV10','salesperson1','2020-09-01',60000,1);

INSERT INTO colors (Color) VALUES ('Grey');
INSERT INTO colors (Color) VALUES ('Red');
INSERT INTO colors (Color) VALUES ('Blue');
INSERT INTO colors (Color) VALUES ('White');
INSERT INTO colors (Color) VALUES ('Black');
INSERT INTO colors (Color) VALUES ('Yellow');
INSERT INTO colors (Color) VALUES ('Gold');
INSERT INTO colors (Color) VALUES ('Orange');
INSERT INTO colors (Color) VALUES ('Silver');
INSERT INTO colors (Color) VALUES ('Green');
INSERT INTO colors (Color) VALUES ('Brown');


INSERT INTO vehiclecolors (Vin, Colors) VALUES ('CON1','Red');
INSERT INTO vehiclecolors (Vin, Colors) VALUES ('CON2','Black');
INSERT INTO vehiclecolors (Vin, Colors) VALUES ('CON3','Silver');
INSERT INTO vehiclecolors (Vin, Colors) VALUES ('CON4','Black');
INSERT INTO vehiclecolors (Vin, Colors) VALUES ('CON5','White');
INSERT INTO vehiclecolors (Vin, Colors) VALUES ('CON6','Silver');
INSERT INTO vehiclecolors (Vin, Colors) VALUES ('CON6','Black');
INSERT INTO vehiclecolors (Vin, Colors) VALUES ('CAR1','White');
INSERT INTO vehiclecolors (Vin, Colors) VALUES ('CAR2','Blue');
INSERT INTO vehiclecolors (Vin, Colors) VALUES ('CAR3','Red');
INSERT INTO vehiclecolors (Vin, Colors) VALUES ('CAR4','Blue');
INSERT INTO vehiclecolors (Vin, Colors) VALUES ('CAR5','Grey');
INSERT INTO vehiclecolors (Vin, Colors) VALUES ('CAR6','Silver');
INSERT INTO vehiclecolors (Vin, Colors) VALUES ('CAR7','White');
INSERT INTO vehiclecolors (Vin, Colors) VALUES ('CAR8','Grey');
INSERT INTO vehiclecolors (Vin, Colors) VALUES ('CAR9','Black');
INSERT INTO vehiclecolors (Vin, Colors) VALUES ('CAR10','Black');
INSERT INTO vehiclecolors (Vin, Colors) VALUES ('CAR11','Blue');
INSERT INTO vehiclecolors (Vin, Colors) VALUES ('CAR12','Red');
INSERT INTO vehiclecolors (Vin, Colors) VALUES ('VAN1','Black');
INSERT INTO vehiclecolors (Vin, Colors) VALUES ('VAN2','Silver');
INSERT INTO vehiclecolors (Vin, Colors) VALUES ('VAN3','Orange');
INSERT INTO vehiclecolors (Vin, Colors) VALUES ('VAN3','White');
INSERT INTO vehiclecolors (Vin, Colors) VALUES ('VAN4','Green');
INSERT INTO vehiclecolors (Vin, Colors) VALUES ('TRU1','Green');
INSERT INTO vehiclecolors (Vin, Colors) VALUES ('TRU2','Yellow');
INSERT INTO vehiclecolors (Vin, Colors) VALUES ('TRU3','Black');
INSERT INTO vehiclecolors (Vin, Colors) VALUES ('TRU4','Black');
INSERT INTO vehiclecolors (Vin, Colors) VALUES ('TRU4','Red');
INSERT INTO vehiclecolors (Vin, Colors) VALUES ('TRU4','Blue');
INSERT INTO vehiclecolors (Vin, Colors) VALUES ('TRU5','Red');
INSERT INTO vehiclecolors (Vin, Colors) VALUES ('TRU6','Blue');
INSERT INTO vehiclecolors (Vin, Colors) VALUES ('TRU7','White');
INSERT INTO vehiclecolors (Vin, Colors) VALUES ('TRU8','Black');
INSERT INTO vehiclecolors (Vin, Colors) VALUES ('TRU8','Blue');
INSERT INTO vehiclecolors (Vin, Colors) VALUES ('TRU9','Black');
INSERT INTO vehiclecolors (Vin, Colors) VALUES ('SUV1','White');
INSERT INTO vehiclecolors (Vin, Colors) VALUES ('SUV2','Blue');
INSERT INTO vehiclecolors (Vin, Colors) VALUES ('SUV3','Red');
INSERT INTO vehiclecolors (Vin, Colors) VALUES ('SUV4','Grey');
INSERT INTO vehiclecolors (Vin, Colors) VALUES ('SUV5','Yellow');
INSERT INTO vehiclecolors (Vin, Colors) VALUES ('SUV6','Black');
INSERT INTO vehiclecolors (Vin, Colors) VALUES ('SUV7','Black');
INSERT INTO vehiclecolors (Vin, Colors) VALUES ('SUV8','Red');
INSERT INTO vehiclecolors (Vin, Colors) VALUES ('SUV9','White');
INSERT INTO vehiclecolors (Vin, Colors) VALUES ('SUV10','Red');

INSERT INTO repairevents (Vin,StartDate,EndDate,Username,LaborCharge,Odometer,Description,CustomerID) VALUES ('CON1','2021-06-01','2021-06-02','writer1',621.41,1000,'done',1);
INSERT INTO repairevents (Vin,StartDate,EndDate,Username,LaborCharge,Odometer,Description,CustomerID) VALUES ('CON1','2021-07-01','2021-07-02','writer2',500,1000,'done',1);
INSERT INTO repairevents (Vin,StartDate,EndDate,Username,LaborCharge,Odometer,Description,CustomerID) VALUES ('CON1','2021-08-01',NULL,'writer1',300,1000,'not done',2);
INSERT INTO repairevents (Vin,StartDate,EndDate,Username,LaborCharge,Odometer,Description,CustomerID) VALUES ('CON5','2021-05-01','2021-05-02','writer2',2010.5,1000,'done',4);
INSERT INTO repairevents (Vin,StartDate,EndDate,Username,LaborCharge,Odometer,Description,CustomerID) VALUES ('CAR2','2021-06-01','2021-06-02','owner1',100,1000,'done',2);
INSERT INTO repairevents (Vin,StartDate,EndDate,Username,LaborCharge,Odometer,Description,CustomerID) VALUES ('CAR6','2021-05-01','2021-05-02','writer1',2000,1000,'done',7);
INSERT INTO repairevents (Vin,StartDate,EndDate,Username,LaborCharge,Odometer,Description,CustomerID) VALUES ('CAR6','2021-07-01','2021-07-02','writer2',100.5,1000,'done',8);
INSERT INTO repairevents (Vin,StartDate,EndDate,Username,LaborCharge,Odometer,Description,CustomerID) VALUES ('CAR10','2021-09-01','2021-09-02','writer1',1000,1000,'done',2);
INSERT INTO repairevents (Vin,StartDate,EndDate,Username,LaborCharge,Odometer,Description,CustomerID) VALUES ('CAR11','2020-01-01','2020-01-02','writer2',120,1000,'done',6);
INSERT INTO repairevents (Vin,StartDate,EndDate,Username,LaborCharge,Odometer,Description,CustomerID) VALUES ('VAN2','2021-10-01', NULL,'writer1',550.5,1000,'not done',5);
INSERT INTO repairevents (Vin,StartDate,EndDate,Username,LaborCharge,Odometer,Description,CustomerID) VALUES ('VAN3','2018-01-01','2018-01-02','writer2',222.2,1000,'done',7);
INSERT INTO repairevents (Vin,StartDate,EndDate,Username,LaborCharge,Odometer,Description,CustomerID) VALUES ('VAN3','2019-01-01','2019-01-02','owner1',333.3,1000,'done',7);
INSERT INTO repairevents (Vin,StartDate,EndDate,Username,LaborCharge,Odometer,Description,CustomerID) VALUES ('TRU3','2020-01-01','2020-01-02','writer1',0,1000,'done',4);
INSERT INTO repairevents (Vin,StartDate,EndDate,Username,LaborCharge,Odometer,Description,CustomerID) VALUES ('TRU3','2020-10-01','2020-10-02','writer2',250,1000,'done',4);
INSERT INTO repairevents (Vin,StartDate,EndDate,Username,LaborCharge,Odometer,Description,CustomerID) VALUES ('TRU9','2021-05-01','2021-05-02','owner1',300,1000,'done',1);
INSERT INTO repairevents (Vin,StartDate,EndDate,Username,LaborCharge,Odometer,Description,CustomerID) VALUES ('SUV2','2021-03-01','2021-03-02','writer1',200,1000,'done',8);
INSERT INTO repairevents (Vin,StartDate,EndDate,Username,LaborCharge,Odometer,Description,CustomerID) VALUES ('SUV4','2021-04-01','2021-04-02','writer2',500,1000,'done',3);
INSERT INTO repairevents (Vin,StartDate,EndDate,Username,LaborCharge,Odometer,Description,CustomerID) VALUES ('SUV4','2021-05-01','2021-05-02','writer1',200,1000,'done',2);
INSERT INTO repairevents (Vin,StartDate,EndDate,Username,LaborCharge,Odometer,Description,CustomerID) VALUES ('SUV9','2021-06-01',NULL,'writer2',100,1000,'not done',2);
INSERT INTO repairevents (Vin,StartDate,EndDate,Username,LaborCharge,Odometer,Description,CustomerID) VALUES ('SUV10','2020-12-01','2020-12-02','writer1',100,1000,'done',1);








