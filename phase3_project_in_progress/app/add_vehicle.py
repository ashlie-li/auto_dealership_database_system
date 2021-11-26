from flask import Flask, render_template, request, redirect, url_for, session
import runSQL
from app import app
import os



@app.route('/add_vehicle', methods = ['GET', 'POST'])
def add_vehicle():
    msg = ''
    
    
    queryColor = "SELECT Color FROM Colors;"
    
    dropColor = [row[0] for row in runSQL.readSQL(queryColor)]
         
    
    if request.method == 'POST' and 'Vin' in request.form and 'Manu' in request.form\
        and 'ModelName' in request.form and 'ModelYear' in request.form and 'InvoicePrice' in request.form\
        and 'ClerkUsername' in request.form and 'color' in request.form:
        Vin = request.form['Vin']
        Manu = request.form['Manu']
        ModelName = request.form['ModelName']
        ModelYear = request.form['ModelYear']
        InvoicePrice = request.form['InvoicePrice']
        ClerkUsername = request.form['ClerkUsername']
        
        if 'Description' in request.form:
            Description = request.form['Description']
        else:
            Description = None
        
        
        query = '''INSERT INTO Vehicles (Vin, Manufacturer, ModelName, ModelYear, DateAdded, InvoicePrice, Description, 
            ClerkUsername) VALUES ('{a}', '{b}', '{c}', '{d}', (SELECT CURDATE()),'{e}', %s, '{f}');
            '''.format(a=Vin, b=Manu, c=ModelName, d=ModelYear,  e=InvoicePrice, f=ClerkUsername)
                    
        res = runSQL.writeSQL(query, [Description])
        print(res)
        msg = res

        
        Colors = request.form.getlist('color')
        print(Colors)
        
        queryAddColor = '''INSERT INTO VehicleColors (Vin, Colors) VALUES
                            (%s, %s)'''
        for C in Colors:
            res2 = runSQL.writeSQL(queryAddColor, [Vin, C])
            print(res2)

    dropType = ['Car','SUV','VanMinVan','Convertible','Truck']
    vehicleType = request.form.getlist('dropType')
    print(vehicleType)

    if request.method == 'POST' and 'Vin' in request.form and 'NumOfDoors' in request.form:
        Vin = request.form['Vin']
        NumOfDoors = request.form['NumOfDoors']
                    
        query3 = '''INSERT INTO Cars (Vin, NumOfDoors) VALUES ('{a}', '{b}');
                '''.format(a=Vin, b=NumOfDoors)

        res3 = runSQL.writeSQL(query3)
        print(res3)


    if request.method == 'POST' and 'Vin' in request.form and 'DrivetrainType' in request.form and 'NumberOfCupholders'in request.form:
        Vin = request.form['Vin']
        DrivetrainType = request.form['DrivetrainType']
        NumberOfCupholders = request.form['NumberOfCupholders']
                    
        query4 = '''INSERT INTO SUVs (Vin, DrivetrainType, NumberOfCupholders) VALUES ('{a}', '{b}', '{c}');
        '''.format(a=Vin, b=DrivetrainType, c=NumberOfCupholders)
                        
        res4 = runSQL.writeSQL(query4)
        print(res4)


    if request.method == 'POST' and 'Vin' in request.form and 'DrivetrainType' in request.form and 'NumberOfCupholders' in request.form:
        Vin = request.form['Vin']
        HasDriverSideBackDoor = request.form['HasDriverSideBackDoor']
                    
        query5 = '''INSERT INTO VanMinVans (Vin, HasDriverSideBackDoor) VALUES ('{a}', '{b}');
        '''.format(a=Vin, b=HasDriverSideBackDoor)
                        
        res5 = runSQL.writeSQL(query5)
        print(res5)


    if request.method == 'POST' and 'Vin' in request.form and 'RoofType' in request.form and 'BackSeatCount' in request.form:
        Vin = request.form['Vin']
        RoofType = request.form['RoofType']
        BackSeatCount = request.form['BackSeatCount']
                    
        query6 = '''INSERT INTO Convertibles (Vin, RoofType, BackSeatCount) VALUES ('{a}', '{b}', '{c}');
        '''.format(a=Vin, b=RoofType, c=BackSeatCount)
                        
        res6 = runSQL.writeSQL(query6)
        print(res6)


    if request.method == 'POST' and 'Vin' in request.form and 'CargoCoverType' in request.form\
        and 'NumberOfRearAxles' in request.form and 'CargoCapacity' in request.form:
        Vin = request.form['Vin']
        CargoCoverType = request.form['CargoCoverType']
        NumberOfRearAxles = request.form['NumberOfRearAxles']
        CargoCapacity = request.form['CargoCapacity']
                    
        query7 = '''INSERT INTO Trucks (Vin, CargoCoverType, NumberOfRearAxles, CargoCapacity) VALUES ('{a}', '{b}', '{c}', '{d}');
        '''.format(a=Vin, b=CargoCoverType, c=NumberOfRearAxles, d=CargoCapacity)
                        
        res7 = runSQL.writeSQL(query7)
        print(res7)


    return render_template('add_vehicle.html', msg = msg, dropColor = dropColor, dropType = dropType)
    
