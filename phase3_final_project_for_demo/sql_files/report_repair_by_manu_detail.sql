With TypeInfo AS (
	SELECT Vin, 'Car' AS Type FROM Cars
UNION SELECT Vin, 'SUV' AS Type FROM SUVs
UNION SELECT Vin, 'Van MiniVan' AS Type FROM VanMiniVans
UNION	 SELECT Vin, 'Truck' AS Type FROM Trucks
UNION SELECT Vin, 'Convertible' AS Type FROM Convertibles
),
VehiclesWithType AS
(
SELECT Vs.Vin, ModelName, ModelYear, DateAdded, InvoicePrice,Manufacturer,
ClerkUsername, Description , T.Type FROM Vehicles AS Vs
JOIN TypeInfo AS T ON T.Vin =Vs.Vin
),
RepairInfo AS
(
SELECT RepairEvents.Vin, RepairEvents.StartDate, V.Manufacturer, LaborCharge,
IFNULL(PA.PartCost, 0) AS PartCost,
(IFNULL(PA.PartCost, 0) + LaborCharge) AS PartLaborCost, ModelName AS Model, Type
FROM RepairEvents
LEFT JOIN
(SELECT Vin, StartDate, SUM(QuantityUsed * Price) AS PartCost
FROM Parts GROUP BY Vin, StartDate)  AS PA
ON RepairEvents.Vin = PA.Vin AND RepairEvents. StartDate = PA.StartDate
LEFT JOIN VehiclesWithType  AS V ON RepairEvents.Vin = V.Vin
),
TypeCount AS(
SELECT Type, '' AS Model, Count(*) AS TotalRepairCount,
SUM(LaborCharge) AS TotalLaborCost, SUM(PartCost) AS TotalPartCost,
SUM(PartLaborCost) AS TotalPartLaborCost, Count(*) AS TypeRepairCount
FROM RepairInfo
WHERE Manufacturer = %s
GROUP BY Type),
ModelCount AS(
SELECT Type, Model, Count(*) AS TotalRepairCount,
SUM(LaborCharge) AS TotalLaborCost, SUM(PartCost) AS TotalPartCost,
SUM(PartLaborCost) AS TotalPartLaborCost
FROM RepairInfo
WHERE Manufacturer = %s
GROUP BY Type, Model
),
ModelTypeCount AS (
SELECT M.Type, M.Model, M.TotalRepairCount, M.TotalLaborCost, M.TotalPartCost,
M.TotalPartLaborCost, T.TypeRepairCount
FROM ModelCount AS M
LEFT JOIN TypeCount AS T ON T.Type = M.Type
),
SortTable AS (
SELECT Type, Model, TotalRepairCount,TotalLaborCost,
TotalPartCost, TotalPartLaborCost, TypeRepairCount FROM ModelTypeCount
UNION ALL 
SELECT Type, Model, TotalRepairCount,TotalLaborCost,
TotalPartCost, TotalPartLaborCost, TypeRepairCount FROM TypeCount
ORDER BY TypeRepairCount DESC, Type, Model !='', TotalRepairCount DESC
)
SELECT Type, Model, TotalRepairCount,TotalLaborCost,
TotalPartCost, TotalPartLaborCost FROM SortTable;

