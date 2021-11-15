SELECT  Date_FORMAT(SaleDate, '%Y-%m') AS SaleYearMonth, COUNT(*) AS SaleCount, 
SUM(S.SalePrice) AS SaleIncome, (SUM(S.SalePrice) - SUM(V.InvoicePrice) ) AS SaleNetIncome,
(SUM(S.SalePrice) / SUM(V.InvoicePrice) ) AS SaleRatio 
FROM SalesEvents AS S
INNER JOIN Vehicles AS V
ON V.Vin = S.Vin
GROUP BY SaleYearMonth
ORDER BY SaleYearMonth DESC;