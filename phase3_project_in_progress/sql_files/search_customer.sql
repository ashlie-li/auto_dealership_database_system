SELECT Name, Id, ContactName, ContactTitle, Address, PhoneNum, Email, CustomerID
                    FROM 
                    (
                    SELECT  CONCAT(P.FirstName, ' ', P.LastName) AS Name, P.License AS Id, C.CustomerID,
                    NULL AS ContactName, NULL AS ContactTitle,C.PhoneNum, C.Email,
                    CONCAT(C.Street, ', ', C.City, ', ', C.State, ', ', C.Zipcode) AS Address,  'Person' AS CustomerType
                    FROM Persons AS P 
                    INNER JOIN Customers AS C ON P.CustomerID = C.CustomerID 
                    UNION ALL
                    SELECT Name, TaxNum AS Id, C.CustomerID,
                    CONCAT(ContactFName, ' ', ContactLName) AS ContactName, ContactTitle, C.PhoneNum, C.Email,
                    CONCAT(C.Street, ', ', C.City, ', ', C.State, ', ', C.Zipcode) AS Address, 'Business' AS CustomerType 
                    FROM Business AS B 
                    INNER JOIN Customers AS C ON B.CustomerID = C.CustomerID 
                    ) AS U
                    WHERE CustomerType =  %s AND Id = %s;