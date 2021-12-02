SELECT VendorName,  SUM(QuantityUsed * Price) AS TotalCost, 
SUM(QuantityUsed) AS NumberOfPart
FROM Parts GROUP BY VendorName
ORDER BY TotalCost DESC;