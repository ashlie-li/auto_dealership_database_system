With SingleColorSoldVehicles AS 
                (
                SELECT SalesEvents.Vin, SaleDate, VehicleColors.Colors AS Color
                FROM SalesEvents
                INNER JOIN VehicleColors ON VehicleColors.Vin = SalesEvents.Vin
                WHERE SalesEvents.Vin IN 
                (SELECT VIN FROM 
                (SELECT Vin, Count(*) AS ColorCount 
                FROM VehicleColors
                GROUP BY Vin HAVING ColorCount = 1) AS SingleColorVin
                )
                ),
                MultiColorSoldVehicles AS 
                (
                SELECT Vin, SaleDate FROM SalesEvents
                WHERE Vin NOT IN
                (SELECT VIN FROM SingleColorSoldVehicles)
                ),
                SingleColorVehicleMonthSalesByColor AS
                (
                	SELECT Color, Count(*) AS SaleCount FROM SingleColorSoldVehicles
                	WHERE  DATEDIFF(%s , SaleDate)  <= 30
                	GROUP BY Color
                ),
                SingleColorVehicleYearSalesByColor AS
                (	
                SELECT Color, Count(*) AS SaleCount FROM SingleColorSoldVehicles
                	WHERE DATEDIFF(%s  , SaleDate)  <= 365
                	GROUP BY Color
                ),
                SingleColorVehicleAllTimeSalesByColor AS
                (
                SELECT Color, Count(*) AS SaleCount FROM SingleColorSoldVehicles
                	GROUP BY Color
                )
                SELECT DISTINCT C.Color, 
                IFNULL (M.SaleCount,0) AS MonthlySales,
                IFNULL (Y.SaleCount,0) AS YearSales,
                IFNULL (A.SaleCount,0) AS AllTimeSales
                FROM Colors AS C
                LEFT OUTER JOIN SingleColorVehicleMonthSalesByColor AS M
                ON C.Color = M.Color
                LEFT OUTER JOIN SingleColorVehicleYearSalesByColor AS Y
                ON C.Color = Y.Color
                LEFT OUTER JOIN SingleColorVehicleAllTimeSalesByColor AS A
                ON C.Color = A.Color
                UNION ALL
                SELECT 'Multiple' AS Color,
                (SELECT COUNT(*) FROM MultiColorSoldVehicles 
                WHERE  DATEDIFF(%s  , SaleDate)  )  AS MonthlySales,
                (SELECT COUNT(*) FROM MultiColorSoldVehicles 
                WHERE DATEDIFF(%s , SaleDate)  )  AS YearSales,
                (SELECT COUNT(*) FROM MultiColorSoldVehicles)  AS AllTimeSales
                ORDER BY Color;