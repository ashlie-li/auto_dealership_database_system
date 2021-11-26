SELECT RepairEvents.StartDate, EndDate, Odometer, LaborCharge, IFNULL(PA.PartCost,0) AS PartCost,
(IFNULL(PA.PartCost,0) + LaborCharge) AS TotalCharge,
CONCAT(PU.FirstName, ' ', PU.LastName) AS ServiceWriterName
FROM RepairEvents
LEFT JOIN
(SELECT Vin, StartDate, SUM(QuantityUsed * Price) AS PartCost
FROM Parts GROUP BY Vin, StartDate)  AS PA
ON RepairEvents.Vin = PA.Vin AND RepairEvents. StartDate = PA.StartDate
LEFT JOIN PriviledgedUsers AS PU ON PU.Username = RepairEvents.Username
WHERE RepairEvents.CustomerID = %s
ORDER BY StartDate DESC, EndDate IS NOT NULL, EndDate DESC, PA.Vin ASC;


