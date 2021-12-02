With ManuSoldVehicles AS
(
SELECT SalesEvents.Vin, SaleDate, Vehicles.Manufacturer FROM SalesEvents
INNER JOIN Vehicles ON Vehicles.Vin = SalesEvents.Vin
),
VehicleMonthSalesByManu AS
(
	SELECT Manufacturer, Count(*) AS SaleCount FROM ManuSoldVehicles
	WHERE DATEDIFF((SELECT MAX(SaleDate) FROM SalesEvents) , SaleDate)  <= 30
	GROUP BY Manufacturer
),
VehicleYearSalesByManu AS
(
SELECT Manufacturer, Count(*) AS SaleCount FROM ManuSoldVehicles
	WHERE DATEDIFF((SELECT MAX(SaleDate) FROM SalesEvents) , SaleDate)  <= 365
	GROUP BY Manufacturer
),
VehicleAllTimeSalesByManu AS
(
SELECT Manufacturer, Count(*) AS SaleCount FROM ManuSoldVehicles
	GROUP BY Manufacturer
)
SELECT ManufacturerName,
IFNULL (M.SaleCount,0) AS MonthlySales,
IFNULL (Y.SaleCount,0) AS YearSales,
IFNULL (A.SaleCount,0) AS AllTimeSales
FROM Manufacturer AS Manu
LEFT OUTER JOIN VehicleMonthSalesByManu AS M
ON Manu.ManufacturerName = M.Manufacturer
LEFT OUTER JOIN VehicleYearSalesByManu AS Y
ON Manu.ManufacturerName = Y.Manufacturer
LEFT OUTER JOIN VehicleAllTimeSalesByManu AS A
 ON Manu.ManufacturerName = A.Manufacturer
WHERE M.SaleCount IS NOT NULL  OR A.SaleCount IS NOT NULL   OR Y.SaleCount IS NOT NULL
ORDER BY ManufacturerName;