from flask import Flask, render_template, request, redirect, url_for, session
import runSQL
from app import app
import os



@app.route('/add_vehicle', methods = ['GET', 'POST'])
def add_vehicle():
    if 'role' in session:
        role = session['role']
    else:
        role = ''
        
    msg = ''
    msg2 =''
    
    queryColor = "SELECT Color FROM Colors;"
    dropColor = [row[0] for row in runSQL.readSQL(queryColor)]
    
    queryManu = "Select ManufacturerName FROM Manufacturer;"
    dropManu = [row[0] for row in runSQL.readSQL(queryManu)]
    
    queryType = '''SELECT 'Car' AS Type UNION SELECT 'SUV' UNION SELECT 'Truck' 
                    UNION SELECT 'Convertible' UNION SELECT 'Van MiniVan';
                    '''
    dropType = [row[0] for row in runSQL.readSQL(queryType)]

    
    if request.method == 'POST' and 'Vin' in request.form and 'Manu' in request.form\
        and 'ModelName' in request.form and 'ModelYear' in request.form\
        and 'InvoicePrice' in request.form and 'color' in request.form:
        Vin = request.form['Vin']
        Manu = request.form['Manu']
        ModelName = request.form['ModelName']
        ModelYear = request.form['ModelYear']
        InvoicePrice = request.form['InvoicePrice']
        Type = request.form['Type']
        
        if 'Description' in request.form and request.form['Description'] != "":
            Description = request.form['Description']
        else:
            Description = None
            
            
        query_check_Year = '''SELECT YEAR(CURDATE());'''
        cur_year = runSQL.readSQL(query_check_Year)[0][0]
        
        if int(ModelYear) > int(cur_year)+1:
            msg2 = 'Invalid Information for Model Year!'
            return render_template('add_vehicle.html', msg2 = msg2, alert0= msg2,dropColor = dropColor, dropManu=dropManu, dropType=dropType, role=role)
        
        
        query = '''INSERT INTO Vehicles (Vin, Manufacturer, ModelName, ModelYear, DateAdded, InvoicePrice, Description, 
            ClerkUsername) VALUES ('{a}', '{b}', '{c}', '{d}', (SELECT CURDATE()),'{e}', %s, '{f}');
            '''.format(a=Vin, b=Manu, c=ModelName, d=ModelYear,  e=InvoicePrice, f=session['username'])
                    
        res = runSQL.writeSQL(query, [Description])
        
        if res != 'query is executed':
            alert0 = "Invalid Information! Please check VIN or Description Input."
            return render_template('add_vehicle.html', msg2 =res, alert0 = alert0\
                                   , dropColor = dropColor, dropManu=dropManu, dropType=dropType, role=role)       
        
        
        
        Colors = request.form.getlist('color')
        
        queryAddColor = '''INSERT INTO VehicleColors (Vin, Colors) VALUES
                            (%s, %s);'''
        for C in Colors:
            res2 = runSQL.writeSQL(queryAddColor, [Vin, C])
            
        
        if res2 !='query is executed' :
            alert0 = "Invalid Information! Please check Color Inputs."
            
            query_delte2 = "delete from vehicles where vin = %s;"
            runSQL.writeSQL(query_delte2, [Vin])
            
            return render_template('add_vehicle.html', msg2 = res2, alert0 = alert0\
                                   , dropColor = dropColor, dropManu=dropManu, dropType=dropType, role=role)
            
        if Type == 'Car':
            query1 = "INSERT INTO Cars (Vin, NumOfDoors) VALUES (%s, %s);"
            NumDoor = request.form["NumDoor"]
            res3 = runSQL.writeSQL(query1, [Vin, NumDoor])
            
        elif Type == 'Truck':
            query1 = '''INSERT INTO Trucks (Vin, CargoCoverType, NumberOfRearAxies, 
            CargoCapacity) VALUES (%s, %s, %s, %s);'''
            NumAX = request.form["NumAX"]
            Capacity = request.form["Capacity"]
            if 'CargoT' in request.form or request.form['CargoT'] != '':
                CargoT = request.form['CargoT']
            else:
                CargoT = None
                                      
            res3 = runSQL.writeSQL(query1, [Vin, CargoT, NumAX, Capacity])
            
        elif Type == 'SUV':
            query1 = '''INSERT INTO SUVs (Vin, DrivetrainType, NumberOfCupHolders) 
                        VALUES (%s, %s, %s);'''
            NumCup = request.form["NumCup"]
            Drive = request.form["Drive"]
            res3 = runSQL.writeSQL(query1, [Vin, Drive, NumCup])
            
        elif Type == 'Convertible':
            query1 = "INSERT INTO Convertibles (Vin, RoofType, BackSeatCount) VALUES (%s, %s, %s);"
            CBack = request.form["CBack"]
            Roof = request.form["Roof"]
            res3 = runSQL.writeSQL(query1, [Vin, Roof, CBack])
            
        else:
            query1 = "INSERT INTO VanMiniVans (Vin, HasDriverSideBackDoor) VALUES (%s, %s);"
            Side = request.form["Side"]
            res3 = runSQL.writeSQL(query1, [Vin, Side])
            
        if res3 != 'query is executed' or res2 !='query is executed':
            query_delte1 = "delete from vehiclecolors where vin = %s;"
            query_delte2 = "delete from vehicles where vin = %s;"
            
            runSQL.writeSQL(query_delte1, [Vin])
            runSQL.writeSQL(query_delte2, [Vin])
            msg2 = 'Invalid Information for Type Attributes!'
            return render_template('add_vehicle.html', msg2 = res3, alert0=msg2\
                                   , dropColor = dropColor, dropManu=dropManu, dropType=dropType, role=role)
        else:
            return redirect('/vehicle_detail/' + Vin)       


        
        
    return render_template('add_vehicle.html', msg = msg, dropColor = dropColor, dropManu=dropManu, dropType=dropType,role=role)
    
