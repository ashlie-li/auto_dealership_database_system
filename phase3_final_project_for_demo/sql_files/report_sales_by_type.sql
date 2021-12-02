With TypeInfo AS (
	SELECT Vin, 'Car' AS Type FROM Cars
UNION SELECT Vin, 'SUV' AS Type FROM SUVs
UNION SELECT Vin, 'Van MiniVan' AS Type FROM VanMiniVans
UNION	 SELECT Vin, 'Truck' AS Type FROM Trucks
UNION SELECT Vin, 'Convertible' AS Type FROM Convertibles
),
VehiclesWithType AS
(
SELECT Vs.Vin, T.Type FROM Vehicles AS Vs
JOIN TypeInfo AS T ON T.Vin =Vs.Vin
),
TypeSoldVehicles AS
(
SELECT SalesEvents.Vin, SaleDate, VT.Type FROM SalesEvents
INNER JOIN VehiclesWithType AS VT ON SalesEvents .Vin = VT.Vin
),
VehicleMonthSalesByType AS
(
	SELECT Type, Count(*) AS SaleCount FROM TypeSoldVehicles
	WHERE DATEDIFF((SELECT MAX(SaleDate) FROM SalesEvents) , SaleDate)  <= 30
	GROUP BY Type
),
VehicleYearSalesByType AS
(
SELECT Type, Count(*) AS SaleCount FROM TypeSoldVehicles
	WHERE DATEDIFF((SELECT MAX(SaleDate) FROM SalesEvents) , SaleDate)  <= 365
	GROUP BY Type
),
VehicleAllTimeSalesByType AS
(
SELECT Type, Count(*) AS SaleCount FROM TypeSoldVehicles
	GROUP BY Type
),
AllTypes AS (
SELECT 'Car' AS Type UNION SELECT 'SUV' UNION SELECT 'Truck'
UNION SELECT 'Convertible' UNION SELECT 'Van MiniVan'
)
SELECT T.Type,
  IFNULL (M.SaleCount,0) AS MonthlySales,
  IFNULL (Y.SaleCount,0) AS YearSales,
  IFNULL (A.SaleCount,0) AS AllTimeSales
FROM AllTypes AS T
LEFT OUTER JOIN VehicleMonthSalesByType AS M ON T.Type = M.Type
LEFT OUTER JOIN VehicleYearSalesByType AS Y ON T.Type = Y.Type
LEFT OUTER JOIN VehicleAllTimeSalesByType AS A ON T.Type = A.Type
ORDER BY Type;

