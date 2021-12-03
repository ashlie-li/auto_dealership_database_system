SELECT S.SaleDate, S.SalePrice, V.InvoicePrice, 
	CONCAT(ROUND((S.SalePrice / V.InvoicePrice )*100,2), '%') AS PriceRatio,
 	C.Name AS CustomerName , CONCAT(P.FirstName, ' ', P.LastName) AS SalespersonName
FROM SalesEvents AS S
INNER JOIN Vehicles AS V ON V.Vin = S.Vin
INNER JOIN
(
	SELECT CustomerID, CONCAT(FirstName, ' ', LastName) AS Name FROM Persons
UNION ALL
SELECT CustomerID, Name FROM Business
) AS C ON C.CustomerID = S.CustomerID
INNER JOIN PriviledgedUsers AS P ON P.Username = S.Username
WHERE S.SalePrice < V.InvoicePrice
ORDER BY S.SaleDate DESC, PriceRatio DESC;
