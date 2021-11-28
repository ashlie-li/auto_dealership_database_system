With AllTypes AS (
SELECT 'Car' AS Type UNION SELECT 'SUV' UNION SELECT 'Truck' 
UNION SELECT 'Convertible' UNION SELECT 'Van MiniVan' 
),
TypeInfo AS (
	SELECT Vin, 'Car' AS Type FROM Cars
UNION SELECT Vin, 'SUV' AS Type FROM SUVs
UNION SELECT Vin, 'Van MiniVan' AS Type FROM VanMiniVans
UNION	 SELECT Vin, 'Truck' AS Type FROM Trucks
UNION SELECT Vin, 'Convertible' AS Type FROM Convertibles
)
SELECT AllTypes.Type, IFNULL(A.AverageTime, 'N/A') AS AverageTimeInInventory
FROM AllTypes
LEFT OUTER JOIN
(SELECT T.Type, AVG(DATEDIFF(S.SaleDate, DATE_ADD(DateAdded, INTERVAL 1 DAY)) ) AS AverageTime
FROM Vehicles 
INNER JOIN SalesEvents AS S ON Vehicles.Vin = S.Vin
INNER JOIN TypeInfo AS T ON T.Vin =Vehicles.Vin
GROUP BY Type) AS A
ON AllTypes.Type = A.Type
ORDER BY Type ASC;