WITH ManagersRole AS 
(SELECT Username, 'Manager'  AS Role FROM Managers),
InventoryClkerksRole AS 
(SELECT Username, 'Inventory Clerk'  AS Role FROM InventoryClerks),
SalespeopleRole AS 
(SELECT Username, 'Salesperson' AS Role FROM Salespeople),
ServiceWritersRole AS 
(SELECT Username, 'Service Writer' AS Role FROM ServiceWriters)
SELECT PU.Username, R.Role FROM PriviledgedUsers AS PU
JOIN (SELECT * FROM ManagersRole UNION SELECT * FROM  InventoryClkerksRole 
UNION SELECT * FROM  SalespeopleRole UNION SELECT * FROM ServiceWritersRole) AS R
ON PU.Username = R.Username
WHERE PU.Username = '{a}';