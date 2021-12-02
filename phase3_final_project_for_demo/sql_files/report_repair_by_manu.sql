WITH RepairInfo AS
(
SELECT RepairEvents.Vin, RepairEvents.StartDate, V.Manufacturer, LaborCharge, 
IFNULL(PA.PartCost, 0 ) AS PartCost,  
(IFNULL(PA.PartCost, 0) + LaborCharge ) AS PartLaborCost
FROM RepairEvents
LEFT JOIN 
(SELECT Vin, StartDate, SUM(QuantityUsed * Price) AS PartCost 
FROM Parts GROUP BY Vin, StartDate)  AS PA
ON RepairEvents.Vin = PA.Vin AND RepairEvents. StartDate = PA.StartDate
LEFT JOIN Vehicles AS V ON RepairEvents.Vin = V.Vin
)
SELECT M.ManufacturerName, IFNULL(RR.TotalRepairCount, 0), 
IFNULL(RR.TotalLaborCost, 0), IFNULL(RR.TotalPartCost, 0), 
IFNULL(RR.TotalLaborPartCost, 0)
FROM Manufacturer AS M 
LEFT OUTER JOIN 
(SELECT Manufacturer, Count(*) AS TotalRepairCount,
SUM(LaborCharge) AS TotalLaborCost, SUM(PartCost) AS TotalPartCost, 
SUM(PartLaborCost) AS TotalLaborPartCost
FROM RepairInfo
GROUP BY Manufacturer) AS RR
ON M.ManufacturerName =  RR.Manufacturer
ORDER BY ManufacturerName;
