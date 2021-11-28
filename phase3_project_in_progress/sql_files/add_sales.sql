INSERT INTO SalesEvents (Vin, SaleDate, SalePrice, 
CustomerID, Username) VALUES (%s, (SELECT CURDATE()), 
%s, %s, %s);