SELECT R.Vin, R.StartDate, R.Odometer, R.LaborCharge, IFNULL(PA.PartCost, 0) AS PartCost, 
(IFNULL(PA.PartCost, 0) + LaborCharge) AS TotalCost, Description
FROM RepairEvents AS R
LEFT JOIN (SELECT Vin, StartDate, SUM(QuantityUsed * Price) AS PartCost 
FROM Parts GROUP BY Vin, StartDate)  AS PA
ON R.Vin = PA.Vin AND R.StartDate = PA.StartDate
WHERE R.Vin = %s AND EndDate IS NULL;
