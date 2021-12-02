UPDATE RepairEvents SET EndDate = (SELECT CURDATE())
WHERE Vin = %s AND StartDate = %s;
