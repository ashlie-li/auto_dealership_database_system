from flask import Flask, render_template, request, redirect, url_for, session
import runSQL
from app import app



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
        
        
        Colors = request.form.getlist('color')
        print(Colors)
        
        queryAddColor = '''INSERT INTO VehicleColors (Vin, Colors) VALUES
                            (%s, %s)'''
        for C in Colors:
            res2 = runSQL.writeSQL(queryAddColor, [Vin, C])
            print(res2)
            
        
        msg = res

        


    return render_template('add_vehicle.html', msg = msg, dropColor = dropColor)
    
