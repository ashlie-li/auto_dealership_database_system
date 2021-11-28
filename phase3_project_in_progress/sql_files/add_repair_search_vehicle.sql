With TypeInfo AS (
                    	SELECT Vin, 'Car' AS Type FROM Cars
                        UNION SELECT Vin, 'SUV' AS Type FROM SUVs
                        UNION SELECT Vin, 'Van MiniVan' AS Type FROM VanMiniVans
                        UNION	 SELECT Vin, 'Truck' AS Type FROM Trucks
                        UNION SELECT Vin, 'Convertible' AS Type FROM Convertibles
                        )
                        SELECT Vehicles.Vin, T.Type, ModelYear,  Manufacturer, ModelName AS Model, 
                        C.VColors AS Colors
                        FROM Vehicles
                        JOIN (SELECT Vin, GROUP_CONCAT(Colors SEPARATOR ' ') AS VColors
                        FROM VehicleColors GROUP BY Vin
                        ) AS C ON C.Vin = Vehicles.Vin
                        JOIN TypeInfo AS T ON T.Vin =Vehicles.Vin
                        WHERE  Vehicles.Vin = %s