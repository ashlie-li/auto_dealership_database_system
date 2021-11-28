from flask import Flask, render_template, request, redirect, url_for, session
import runSQL
from app import app
import os



@app.route('/add_repair/search_vehicle', methods = ['GET', 'POST'])
def add_repair_search_vehicle():
    msg = ''
    if request.method == 'POST' and 'Vin' in request.form:
        Vin = request.form['Vin']
        

        query0 = '''SELECT (%s IN (SELECT Vin FROM SalesEvents) );'''

        res0 = runSQL.readSQL(query0, [Vin])[0][0]
        res0 = int(res0)

        if res0 == 0:
            # require odometer, hmtl require odometer
            return render_template('pre_repair.html', msg='The vehicle is not sold or not in inventory.')
        else:
            with open(os.path.join(os.getcwd(),  "sql_files", "add_repair_search_vehicle.sql"),
              "r", encoding='utf-8') as file:
                
                tmp = file.readlines();
            query1 = " ".join(tmp)
            
            res1 = runSQL.readSQL(query1, [Vin])
            col = ('Vin', 'Type', 'Model Year', 'Manufacturer', 'Model', 'Color(s)')
        
            return render_template('pre_repair.html', msg='The vehicle information is found', col=col, res1=res1, Vin=Vin, Act="add_repair")

    return render_template('pre_repair.html')


@app.route('/add_repair/<string:Vin>', methods = ['GET', 'POST'])   
def add_repair(Vin):
    if 'role' not in session or session['role'] not in ['Owner', 'Service Writer']:
        return render_template( 'error_handle.html', msg='You are not authorized to repair a vehicle', to_url = '/')
    
    if request.method == 'POST' and 'CustomerID' in request.form:
        CustomerID = request.form['CustomerID']
        print("kkkk", CustomerID)    
        query0 = '''SELECT %s IN (SELECT Vin FROM RepairEvents WHERE EndDate IS NULL);'''
        
        res0 = int(runSQL.readSQL(query0, [Vin])[0][0] )
        msg = ['There is no open repair. Please create one.', 'Please check the open repair:'][res0]
        if res0 == 0:
            query00 = '''SELECT * FROM RepairEvents WHERE Vin =%s and StartDate = CURDATE()'''
            res00 = runSQL.readSQL(query00, [Vin])
            if len(res00) >0:
                msg = '''One repair has been created today. You are not allowed to create two repairs on the same day!'''
                return render_template( 'error_handle.html', msg=msg, to_url = '/add_repair/search_vehicle')
        
            return render_template('repair.html', Vin=Vin, msg=msg, create='yes', \
                                   CustomerID=CustomerID)
        if res0 == 1:
            with open( os.path.join(os.getcwd(), "sql_files", "add_repair_check_repair.sql"),
              "r", encoding='utf-8') as file:
                tmp = file.readlines();
            query1 = " ".join(tmp)
            res1 = runSQL.readSQL(query1, [Vin])
            col = ('Vin', 'Start Date', 'Odometer', 'Labor Charge', 'Part Cost', 'Total Cost')
            return render_template('repair.html', Vin=Vin, msg=msg, create='no', res1=res1, col=col, CustomerID=CustomerID)
        
       
        
    return redirect(url_for('add_repair_search_vehicle'))



@app.route('/add_repair/<string:Vin>/new_repair/<string:CID>', methods = ['GET', 'POST'])   
def add_repair_new_repair(Vin, CID):
    with open(os.path.join(os.getcwd(), "sql_files", "add_repair_new_repair.sql"),
      "r", encoding='utf-8') as file:
        tmp = file.readlines();
    query = " ".join(tmp)
    
    odo = request.form['new_odo']
    res = runSQL.writeSQL(query, [ Vin, odo, CID, session['username']])
    
    if res == 'query is executed':
        with open(os.path.join(os.getcwd(), "sql_files", "add_repair_check_repair.sql"),
          "r", encoding='utf-8') as file:
            tmp = file.readlines();
        query1 = " ".join(tmp)
        res1 = runSQL.readSQL(query1, [Vin])
        col = ('Vin', 'Start Date', 'Odometer', 'Labor Charge', 'Part Cost', 'Total Cost')
        msg='Please check the open repair:'
        return render_template('repair.html', Vin=Vin, msg=msg, create='no', res1=res1, col=col, CustomerID=CID)
    else:
        return render_template('repair.html', Vin=Vin, msg=res, create='yes', CustomerID=CID)


@app.route('/add_repair/<string:Vin>/update_repair/<string:CID>', methods = ['GET', 'POST'])   
def add_repair_update_repair(Vin, CID):
    with open(os.path.join(os.getcwd() + "sql_files", "add_repair_check_repair.sql"),
      "r", encoding='utf-8') as file:
        tmp = file.readlines();
    query1 = " ".join(tmp)
    res1 = runSQL.readSQL(query1, [Vin])
    col = ('Vin', 'Start Date', 'Odometer', 'Labor Charge', 'Part Cost', 'Total Cost')
    msg='Please check the open repair:'
    
    if request.method == 'POST' and 'UpdateVin' in request.form:
        StartDate =  request.form["StartDate"]
        if "description" in request.form:
            description = request.form["description"]
            query_update = '''UPDATE RepairEvents SET Description = %s WHERE Vin = %s AND StartDate = %s;'''
            msg2 = runSQL.writeSQL(query_update, [description, Vin, StartDate])
            if msg2 == 'query is executed':
                return render_template('repair.html', Vin=Vin, msg=msg, msg2=msg2+', description is updated',\
                           create='no', res1=res1, col=col, CustomerID=CID, show='yes')
            else:
                return render_template('repair.html', Vin=Vin, msg=msg, msg2=msg2,\
                           create='no', res1=res1, col=col, CustomerID=CID, show='yes')
                
        if request.method == 'POST' and  "odometer" in request.form:
            odometer = request.form['odometer']
            query_update = '''UPDATE RepairEvents SET Odometer = %s WHERE Vin = %s AND StartDate = %s;'''
            msg2 = runSQL.writeSQL(query_update, [odometer, Vin, StartDate])
            if msg2 == 'query is executed':
                res1 = runSQL.readSQL(query1, [Vin])
                return render_template('repair.html', Vin=Vin, msg=msg, msg2=msg2+', odometer is updated',\
                           create='no', res1=res1, col=col, CustomerID=CID, show='yes')
            else:
                return render_template('repair.html', Vin=Vin, msg=msg, msg2=msg2,\
                           create='no', res1=res1, col=col, CustomerID=CID, show='yes')
        
        if request.method == 'POST' and  "labor" in request.form:
            try:
                labor = float(request.form['labor'])
            except:
                return render_template('repair.html', Vin=Vin, msg=msg, msg2="Invalid Information",\
                                       create='no', res1=res1, col=col, CustomerID=CID, show='yes')                
            OldLabor = float(request.form['OldLabor'])
            if labor <= OldLabor and session['role']!='Owner':
                return render_template('repair.html', Vin=Vin, msg=msg, msg2="Can only enter higher labor charge.",\
                                       create='no', res1=res1, col=col, CustomerID=CID, show='yes')
            else:
                query_update = '''UPDATE RepairEvents SET LaborCharge =  %s WHERE Vin = %s AND StartDate = %s;'''
                msg2 = runSQL.writeSQL(query_update, [labor, Vin, StartDate])
                if msg2 == 'query is executed':
                    res1 = runSQL.readSQL(query1, [Vin])
                    return render_template('repair.html', Vin=Vin, msg=msg, msg2=msg2+', labor charge is updated',\
                               create='no', res1=res1, col=col, CustomerID=CID, show='yes')
                else:
                    return render_template('repair.html', Vin=Vin, msg=msg, msg2=msg2,\
                               create='no', res1=res1, col=col, CustomerID=CID, show='yes')  
                    
        if request.method == 'POST' and  "vendor" in request.form:
            vendor = request.form['vendor']
            number = request.form['number']
            price = request.form['price']
            quantity = request.form['quantity']
            
            query_update = '''INSERT INTO Parts (Vin, StartDate, Price, Number, QuantityUsed, 
                                VendorName) VALUES (%s, %s, %s, %s, %s, %s);'''
            msg2 = runSQL.writeSQL(query_update, [Vin, StartDate, price, number, quantity, vendor]) 
            if msg2 == 'query is executed':
                res1 = runSQL.readSQL(query1, [Vin])
                return render_template('repair.html', Vin=Vin, msg=msg, msg2=msg2+', new parts are added',\
                           create='no', res1=res1, col=col, CustomerID=CID, show='yes')
            else:
                return render_template('repair.html', Vin=Vin, msg=msg, msg2=msg2,\
                           create='no', res1=res1, col=col, CustomerID=CID, show='yes') 
        
        if request.method == 'POST' and  "number2" in request.form:
            number2 = request.form['number2']
            quantity2 = request.form['quantity2']
            
            query_update = '''UPDATE Parts SET QuantityUsed = %s
                            WHERE Vin = %s AND StartDate = %s AND Number = %s;'''
            msg2 = runSQL.writeSQL(query_update, [quantity2, Vin, StartDate, number2]) 
            if msg2 == 'query is executed':
                res1 = runSQL.readSQL(query1, [Vin])
                return render_template('repair.html', Vin=Vin, msg=msg, msg2=msg2+', new parts are added',\
                           create='no', res1=res1, col=col, CustomerID=CID, show='yes')
            else:
                return render_template('repair.html', Vin=Vin, msg=msg, msg2=msg2,\
                           create='no', res1=res1, col=col, CustomerID=CID, show='yes')    
        
        if request.method == 'POST' and  "close" in request.form:
            query_check_close = ''' SELECT ENDDATE IS NOT NULL FROM REPAIREVENTS WHERE 
                                    VIN = %s AND STARTDATE = %s;'''
            res_check_close = runSQL.readSQL(query_check_close, [Vin, StartDate])
            if int(res_check_close[0][0]) == 1:
                return render_template( 'error_handle.html', msg='The repair has been closed!', to_url = '/add_repair/search_vehicle')
                                
            
            query_close = '''UPDATE RepairEvents SET EndDate = (SELECT CURDATE())
                        WHERE Vin = %s AND StartDate = %s;'''
            msg2 = runSQL.writeSQL(query_close, [Vin, StartDate])
            if msg2 != 'query is executed':
                return render_template('repair.html', Vin=Vin, msg=msg, msg2=msg2,\
                           create='no', res1=res1, col=col, CustomerID=CID, show='yes')
            else:
                return render_template('pre_repair.html')
            

    return render_template('repair.html', Vin=Vin, msg=msg, create='no', res1=res1, col=col, CustomerID=CID, show='yes')









