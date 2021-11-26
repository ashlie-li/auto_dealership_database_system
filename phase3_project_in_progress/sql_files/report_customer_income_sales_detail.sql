SELECT  SaleDate, SalePrice, V.Vin, V.ModelYear AS YEAR, V.Manufacturer,
V.ModelName AS Model,  CONCAT(PU.FirstName, ' ', PU.LastName) AS SalespersonName
FROM SalesEvents
LEFT JOIN Vehicles AS V ON V.Vin = SalesEvents.Vin
LEFT JOIN PriviledgedUsers AS PU ON PU.Username = SalesEvents.Username
WHERE SalesEvents.CustomerID = %s
ORDER BY SaleDate DESC, Vin ASC;
