from flask import Flask, render_template, request, redirect, url_for, session
import runSQL
from app import app
import os


@app.route('/vehicle_detail/<string:Vin>')
def vehicle_detail(Vin):
    if 'role' in session:
        role = session['role']
    else:
        role = ''
        
    with open(os.path.join(os.getcwd(), 'sql_files', 'vehicle_detail.sql'),
              "r", encoding='utf-8') as file:
        tmp = file.readlines()
    query = " ".join(tmp).format(a = Vin)
        
    
    res = runSQL.readSQL(query)[0]
    
    
    
    col = ('VIN', 'Type','Manufacturer', 'Model', 'Model Year', 'List Pice', 'Color(s)', 'Description')
    

    
    
    Type = res[1]
    if Type == 'Car':
        query_type = '''SELECT NumOfDoors FROM Cars WHERE VIN = '{a}';'''.format(a = Vin)
        col2 = ['Number of Doors']
    elif Type == 'SUV':
        query_type =  '''SELECT DrivetrainType, NumberOfCupholders FROM SUVs WHERE VIN = '{a}';'''.format(a = Vin)
        col2 = ['Drivetrain Type', 'Number of Cupholders']
    elif Type == 'Van MiniVan':
        query_type = '''SELECT HasDriverSideBackDoor FROM VanMiniVans WHERE VIN = '{a}';'''.format(a = Vin) 
        col2 = ['Has Driver Side Back Door']
    elif Type == 'Truck':
        query_type =  '''SELECT CargoCoverType, NumberOfRearAxies, CargoCapacity
                        FROM Trucks WHERE VIN = '{a}';'''.format(a = Vin)
        col2 =  ['Cargo Cover Type', 'Number of Rear Axles', 'Cargo Capacity']
    else:
        query_type =  '''SELECT BackSeatCount, RoofType FROM Convertibles WHERE VIN = '{a}';'''.format(a = Vin)
        col2 = ['Back Seat Count', 'Roof Type']
        
        
    res2 =  runSQL.readSQL(query_type)
    if Type == 'Van MiniVan':
        if res2[0][0] == "1" or res2[0][0] == 1:
            res2 = [["YES"]]
        else: res2 = [["NO"]]

    with open(os.path.join(os.getcwd(), 'sql_files', 'vehicle_detail_sale_section.sql'),
              "r", encoding='utf-8') as file:
        tmp = file.readlines()
    query_sale = " ".join(tmp).format(a = Vin)
                    
    res_sale = runSQL.readSQL(query_sale)
    col_sale = ('Sale Price', 'Sale Date', 'Salesperson', 'Customer', 'Contact Name', 'Contact Title', 'Phone', \
                'Email', 'Address')
    
    if len(res_sale) == 0:
        res_sale = [[] for _ in range(9)]
        dsply_sale = "show"
    else:
        dsply_sale = "";
    
    with open(os.path.join(os.getcwd(), 'sql_files', 'vehicle_detail_repair_section.sql'),
              "r", encoding='utf-8') as file:
        tmp = file.readlines()
    query_repair = " ".join(tmp).format(a = Vin)
                    
    res_repair = runSQL.readSQL(query_repair)
    col_repair = ( 'Customer', 'Service Writer', 'Start Date', 'End Date', 'Labor Cost', \
                'Part Cost', 'Total Cost')
    print(res_repair)
    if len(res_repair) == 0:
        dsply_repair = ""
    else:
        dsply_repair = "show";
        
    
    return render_template('vehicle_detail.html', col=col, res=[res], col2=col2, res2 = res2,\
                           col_sale=col_sale, res_sale=res_sale, col_repair=col_repair, res_repair=res_repair,\
                           dsply_sale = dsply_sale, dsply_repair=dsply_repair, Vin=Vin, role=role)
