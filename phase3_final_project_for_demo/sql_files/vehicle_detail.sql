With TypeInfo AS (
    	SELECT Vin, 'Car' AS Type FROM Cars
        UNION SELECT Vin, 'SUV' AS Type FROM SUVs
        UNION SELECT Vin, 'Van MiniVan' AS Type FROM VanMiniVans
        UNION	 SELECT Vin, 'Truck' AS Type FROM Trucks
        UNION SELECT Vin, 'Convertible' AS Type FROM Convertibles
        )
        SELECT V.Vin, Type, Manufacturer, ModelName AS Model, ModelYear, 
        CAST(1.25*InvoicePrice AS DECIMAL(10,2)) AS ListPrice, C.VColors AS Color, 
        IFNULL(Description, ''), InvoicePrice, DateAdded, 
	CONCAT(FirstName, ' ', LastName) AS ClerkName 
        FROM  Vehicles AS V
        LEFT OUTER JOIN
        (SELECT Vin, GROUP_CONCAT(Colors SEPARATOR ' ') AS VColors
        FROM VehicleColors GROUP BY Vin
        ) AS C ON C.Vin = V.Vin
        LEFT OUTER JOIN TypeInfo ON V.Vin = TypeInfo.Vin
	LEFT JOIN PriviledgedUsers AS P ON V.ClerkUsername = P.Username
        WHERE V.Vin = '{a}';