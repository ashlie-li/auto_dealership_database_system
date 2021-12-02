With CustomerInfo AS
                    ( 
                    SELECT  CONCAT(P.FirstName, ' ', P.LastName) AS Name , P.CustomerID 
                    FROM Persons AS P 
                    UNION ALL
                    SELECT Name , B.CustomerID 
                    FROM Business AS B 
                    ) 
                    SELECT CustomerInfo.Name, CONCAT(SW.FirstName, ' ', SW.LastName) AS ServiceWriterName,
                    R.StartDate, R.EndDate, R.Laborcharge, IFNULL(PA.PartCost, 0) AS PartCost, 
                    (IFNULL(PA.PartCost, 0) + R.LaborCharge) AS TotalCostTotalCost
                    FROM RepairEvents AS R
                    LEFT JOIN 
                    (SELECT Vin, StartDate, SUM(QuantityUsed * Price) AS PartCost 
                    FROM Parts GROUP BY Vin, StartDate )  AS PA
                    ON R.Vin = PA.Vin AND R. StartDate = PA.StartDate
                    INNER JOIN PrIviledgedUsers AS SW ON SW.Username = R.Username
                    INNER JOIN CustomerInfo ON R.CustomerID = CustomerInfo.CustomerID
                    WHERE R.Vin = '{a}';