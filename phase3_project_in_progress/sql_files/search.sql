With TypeInfo AS (
SELECT Vin, 'Car' AS Type FROM Cars
UNION SELECT Vin, 'SUV' AS Type FROM SUVs
UNION SELECT Vin, 'Van MiniVan' AS Type FROM VanMiniVans
UNION	 SELECT Vin, 'Truck' AS Type FROM Trucks
UNION SELECT Vin, 'Convertible' AS Type FROM Convertibles
),
SearchResult AS (
SELECT Vehicles.Vin, T.Type, ModelYear,  Manufacturer, ModelName AS Model, 
C.VColors AS Colors, InvoicePrice * 1.25 AS ListPrice, S.SaleDate, Description
FROM Vehicles
LEFT OUTER JOIN
(SELECT Vin, GROUP_CONCAT(Colors SEPARATOR ' ') AS VColors
FROM VehicleColors GROUP BY Vin
) AS C ON C.Vin = Vehicles.Vin
LEFT OUTER JOIN SalesEvents AS S ON S.Vin = Vehicles.Vin
JOIN TypeInfo AS T ON T.Vin =Vehicles.Vin
WHERE TRUE AND 
(CASE WHEN %s IS NOT NULL 
THEN Type = '{t}' ELSE TRUE END) 
AND
(CASE WHEN %s IS NOT NULL 
THEN Manufacturer = '{m}' ELSE TRUE END)
AND
(CASE WHEN %s IS NOT NULL 
 THEN ModelYear = '{y}' ELSE TRUE END)
AND
(CASE WHEN %s IS NOT NULL 
THEN InvoicePrice * 1.25  <=  '{maxp}'  ELSE TRUE END) 
AND
(CASE WHEN %s IS NOT NULL 
THEN InvoicePrice * 1.25 >=  '{minp}' ELSE TRUE END)
AND
(CASE WHEN %s IS NOT NULL 
THEN C.VColors = '{c}' OR C.VColors LIKE %s
ELSE TRUE END) 
AND
(CASE WHEN %s IS NOT NULL 
THEN  Manufacturer LIKE %s OR ModelName LIKE %s
OR ModelYear LIKE %s OR Description LIKE %s
ELSE TRUE END))
SELECT Vin, Type, ModelYear,  Manufacturer, Model, Colors, 
CAST(ListPrice as DECIMAL(10,2)), 
(CASE WHEN %s IS NOT NULL AND Description LIKE %s
THEN "X" ELSE " " END) AS MatchDescription
FROM SearchResult WHERE TRUE AND
(CASE WHEN %s IS NOT NULL THEN Vin = '{v}' ELSE TRUE END)
AND
(CASE WHEN '{IsM}' IS FALSE THEN SaleDate IS NULL
ELSE (CASE WHEN '{f}' = 'sold' THEN SaleDate IS NOT NULL
WHEN '{f}' = 'unsold' THEN SaleDate IS NULL
ELSE TRUE END) END)
ORDER BY Vin;
