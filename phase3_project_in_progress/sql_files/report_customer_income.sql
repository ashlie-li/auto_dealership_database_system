WITH CustomerInfo AS
(
SELECT CustomerID, CONCAT(FirstName, ' ', LastName) AS Name FROM Persons AS P
UNION ALL
SELECT CustomerID, Name FROM Business
),
SalesInfo AS
(
SELECT CustomerID, SUM(SalePrice) AS SalesIncome, Count(*) AS SalesNumber,
MAX(SaleDate) AS LastSalesDate, MIN(SaleDate) AS FirstSalesDate
FROM SalesEvents
GROUP BY CustomerID
),
RepairInfo AS
(
SELECT CustomerID, SUM(LaborCharge) + SUM(IFNULL(PA.PartCost,0) ) AS RepairIncome,
Count(*) AS RepairNumber, MAX(RepairEvents.StartDate) AS LastRepairDate, MIN(RepairEvents.StartDate) AS FirstRepairDate
FROM RepairEvents
LEFT JOIN
(SELECT Vin, StartDate, SUM(QuantityUsed * Price) AS PartCost
FROM Parts GROUP BY Vin, StartDate)  AS PA
ON RepairEvents.Vin = PA.Vin AND RepairEvents. StartDate = PA.StartDate
GROUP BY CustomerID
)
SELECT C.Name, CASE WHEN R.FirstRepairDate < S.FirstSalesDate THEN R.FirstRepairDate ELSE S.FirstSalesDate END AS FirstDate, CASE WHEN R.LastRepairDate >  S.LastSalesDate THEN R.LastRepairDate ELSE S.LastSalesDate END AS LastDate, S.SalesNumber, R.RepairNumber,
IFNULL(R.RepairIncome,0) + IFNULL(S.SalesIncome,0) AS TotalIncome
FROM CustomerInfo AS C
LEFT OUTER JOIN SalesInfo AS S ON C.CustomerID = S.CustomerID
LEFT OUTER JOIN RepairInfo AS R ON C.CustomerID =   R.CustomerID
ORDER BY TotalIncome DESC, LastDate DESC
LIMIT 15;


