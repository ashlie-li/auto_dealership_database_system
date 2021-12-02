INSERT INTO RepairEvents (Vin, StartDate, EndDate, LaborCharge,
    Odometer, Description, CustomerID, Username) VALUES 
    (%s, (SELECT CURDATE()), NULL, '0.00', %s, NULL, %s, %s);