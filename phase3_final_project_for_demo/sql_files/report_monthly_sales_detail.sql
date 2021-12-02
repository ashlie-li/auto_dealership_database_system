SELECT CONCAT(P.FirstName, ' ',P.LastName) AS SalespersonName, COUNT(*) AS SaleCount,
SUM(S.SalePrice) AS SalespersonIncome
FROM SalesEvents AS S
INNER JOIN PriviledgedUsers AS P
ON P.Username = S.Username
WHERE YEAR( S.SaleDate) = YEAR( CONCAT(%s,  '-01'))
AND MONTH( S.SaleDate) = MONTH(CONCAT(%s,  '-01'))
GROUP BY P.Username
ORDER BY SaleCount DESC, SalespersonIncome DESC;
