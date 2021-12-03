With CustomerInfo AS
                    ( 
                    SELECT  CONCAT(P.FirstName, ' ', P.LastName) AS Name, NULL AS ContactName, 
                    NULL AS ContactTitle,C.PhoneNum AS Phone, 
		    IFNULL(C.Email, '') AS Email, P.CustomerID,
                    CONCAT(C.Street, ', ', C.City, ', ', C.State, ', ', C.Zipcode) AS Address
                    FROM Persons AS P 
                    INNER JOIN Customers AS C ON P.CustomerID = C.CustomerID 
                    UNION ALL
                    SELECT Name, CONCAT(ContactFName, ' ', ContactLName) AS ContactName, 
                    ContactTitle, C.PhoneNum AS Phone, IFNULL(C.Email, '') AS Email, B.CustomerID,
                    CONCAT(C.Street, ', ', C.City, ', ', C.State, ', ', C.Zipcode) AS Address
                    FROM Business AS B 
                    INNER JOIN Customers AS C ON B.CustomerID = C.CustomerID 
                    ) 
                    SELECT SalePrice, SaleDate, CONCAT(SP.FirstName, ' ', SP.LastName) AS SalespersonName,
                    CustomerInfo.Name, CustomerInfo.ContactName, CustomerInfo.ContactTitle,
                    CustomerInfo.Phone, CustomerInfo.Email, CustomerInfo.Address
                    FROM SalesEvents
                    INNER JOIN PrIviledgedUsers AS SP ON SP.Username = SalesEvents.Username
                    INNER JOIN CustomerInfo ON SalesEvents.CustomerID = CustomerInfo.CustomerID
                    WHERE SalesEvents.Vin = '{a}';