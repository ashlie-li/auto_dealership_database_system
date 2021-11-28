from flask import Flask, render_template, request, redirect, url_for, session
import runSQL
from app import app
import os


@app.route('/add_repair/search_vehicle2', methods = ['GET', 'POST']) ###########
def add_repair_search_vehicle2(): ##############
    if 'role' in session:
        role = session['role']
    else:
        role = ''
    
    msg = ''
    msg2 = '' ##############
    if request.method == 'POST' and 'Vin' in request.form and 'CustomerID' not in request.form: #####################
        Vin = request.form['Vin']
        

        query0 = '''SELECT (%s IN (SELECT Vin FROM SalesEvents) );'''

        res0 = runSQL.readSQL(query0, [Vin])[0][0]
        res0 = int(res0)

        if res0 == 0:
            return render_template('pre_repair2.html', msg='The vehicle is not sold or not in inventory.', status= 'none', role=role) #*************

        else:
            msg2 = 'Vechile is found:'
            with open(os.path.join(os.getcwd(),  "sql_files", "add_repair_search_vehicle.sql"),
              "r", encoding='utf-8') as file:
                tmp = file.readlines();
            query1 = " ".join(tmp)
            
            res1 = runSQL.readSQL(query1, [Vin])
            col1 = ('Vin', 'Type', 'Model Year', 'Manufacturr', 'Model', 'Color(s)')
            
            
            query_check_open = '''SELECT %s IN (SELECT Vin FROM RepairEvents WHERE EndDate IS NULL);'''
            res_check_open = int(runSQL.readSQL(query_check_open, [Vin])[0][0] )
            
            if res_check_open == 0: ##### if no open repair
                query_check_same_day = '''SELECT * FROM RepairEvents WHERE Vin =%s and StartDate = CURDATE()'''
                
                res_check_same_day = runSQL.readSQL(query_check_same_day, [Vin])
                if len(res_check_same_day) >0:
                    msg = '''One repair has been created today. You are not allowed to create two repairs on the same day!'''
                    return render_template( 'error_handle.html', \
                                           msg=msg, to_url = '/add_repair/search_vehicle') # Repair has been created in the same day, raise error message
                
                else:
                    msg2 = 'The vehicle information is found:'
                    msg3 = 'No open repair. To create a repair, please end the odometer and select the customer.'
                    return render_template('pre_repair2.html', msg=msg, msg2=msg2,msg3=msg3, status ='create', res1=res1, col1=col1, \
                                           Vin=Vin, Act="add_repair2", role=role) ####### col name changed, need the html to enter odometer
                                                #### use create to show res1 and hide res2, if not define res2 or use more indicator
                                                #### after enter the odometer, the html pass Vin, odometer back to this function
                                                #### create a repair tuple with odometer, Vin and Startdate, then go to search customer html
            else: ## if there is open repair
                msg2 = 'The vehicle information is found:'
                msg3='You can update this open repair:'
                with open(os.path.join(os.getcwd(), "sql_files", "add_repair_check_repair.sql"),
                  "r", encoding='utf-8') as file:
                    tmp = file.readlines();
                query2 = " ".join(tmp)
                res2 = runSQL.readSQL(query2, [Vin])
                col2 = ('Vin', 'Start Date', 'Odometer', 'Labor Charge', 'Part Cost', 'Total Cost', 'Description')
                query_CID = '''SELECT CustomerID FROM RepairEvents WHERE Vin = %s AND EndDate IS NULL;'''
                CustomerID = runSQL.readSQL(query_CID, [Vin])[0][0]
                return render_template('pre_repair2.html', msg=msg, msg2=msg2, msg3=msg3, status ='update', res1=res1, col1=col1, \
                       res2=res2, col2=col2, Vin=Vin, CustomerID=CustomerID, role=role)  ## show the button in the hmtl to update this repair, once click, go to the update
                                            ## python function, don't need the create variable
                

    if request.method == 'POST' and 'Vin' in request.form and 'CustomerID' in request.form: #####################
        Vin = request.form['Vin']
        CustomerID = request.form['CustomerID']
        return render_template('pass_to_act.html', CustomerID=CustomerID, Vin=Vin, Act="add_repair2")

    return render_template('pre_repair2.html', status= 'none', role=role)

@app.route('/add_repair2/<string:Vin>', methods = ['GET', 'POST'])   
def add_repair2(Vin):
    if 'role' in session:
        role = session['role']
    else:
        role = ''
    msg = ''
    if request.method == 'POST' and 'CustomerID' in request.form:
        CustomerID = request.form['CustomerID']
        if 'odometer' in request.form:
            msg = 'Please view this open repair:'
            odometer = request.form['odometer']
            with open(os.path.join(os.getcwd(), "sql_files", "add_repair_new_repair.sql"),
              "r", encoding='utf-8') as file:
                tmp = file.readlines();
            query_create_repair = " ".join(tmp)
            res_create_repair = runSQL.writeSQL(query_create_repair, [ Vin, odometer, CustomerID, session['username']])
            
            if res_create_repair == 'query is executed':
                with open(os.path.join(os.getcwd(), "sql_files", "add_repair_check_repair.sql"),
                  "r", encoding='utf-8') as file:
                    tmp = file.readlines();
                query1 = " ".join(tmp)
                res1 = runSQL.readSQL(query1, [Vin])
                col = ('Vin', 'Start Date', 'Odometer', 'Labor Charge', 'Part Cost', 'Total Cost', 'Description')
            else:
                return render_template( 'error_handle.html', msg='Invalid information. Please retry!', to_url = '/add_repair/search_vehicle')

        else:
            msg = 'Please view this open repair:'
            with open(os.path.join(os.getcwd(), "sql_files", "add_repair_check_repair.sql"),
              "r", encoding='utf-8') as file:                
                tmp = file.readlines();
            query1 = " ".join(tmp)
            res1 = runSQL.readSQL(query1, [Vin])
            col = ('Vin', 'Start Date', 'Odometer', 'Labor Charge', 'Part Cost', 'Total Cost', 'Description')
        return render_template('repair2.html', Vin=Vin, msg=msg, create='no', res1=res1, col=col, CustomerID=CustomerID, role=role)
    
    return redirect(url_for('add_repair_search_vehicle'))


@app.route('/add_repair2/<string:Vin>/update_repair/<string:CustomerID>', methods = ['GET', 'POST'])   
def add_repair_update_repair2(Vin, CustomerID):
    if 'role' in session:
        role = session['role']
    else:
        role = ''
        
    with open(os.path.join(os.getcwd(), "sql_files", "add_repair_check_repair.sql"),
      "r", encoding='utf-8') as file:
        tmp = file.readlines();
    query1 = " ".join(tmp)
    res1 = runSQL.readSQL(query1, [Vin])
    col = ('Vin', 'Start Date', 'Odometer', 'Labor Charge', 'Part Cost', 'Total Cost', 'Description')
    msg= 'Please view this open repair:'
    
    if request.method == 'POST' and 'UpdateVin' in request.form:
        StartDate =  request.form["StartDate"]
        if "description" in request.form:
            description = request.form["description"]
            print(description)
            query_update = '''UPDATE RepairEvents SET Description = %s WHERE Vin = %s AND StartDate = %s;'''
            msg2 = runSQL.writeSQL(query_update, [description, Vin, StartDate])
            if msg2 == 'query is executed':
                res1 = runSQL.readSQL(query1, [Vin])
                return render_template('repair2.html', Vin=Vin, msg=msg, msg2=msg2+', description is updated',\
                           res1=res1, col=col, CustomerID=CustomerID, show='yes', role=role)
            else:
                res1 = runSQL.readSQL(query1, [Vin])
                return render_template('repair2.html', Vin=Vin, msg=msg, msg2=msg2,\
                           res1=res1, col=col, CustomerID=CustomerID, show='yes', role=role)
        
        if request.method == 'POST' and  "labor" in request.form:
            try:
                labor = float(request.form['labor'])
            except:
                return render_template('repair2.html', Vin=Vin, msg=msg, msg2="Invalid Information",\
                                       res1=res1, col=col, CustomerID=CustomerID, show='yes', role=role)                
            OldLabor = float(request.form['OldLabor'])
            if labor <= OldLabor and session['role']!='Owner':
                return render_template('repair2.html', Vin=Vin, msg=msg, msg2="Can only enter higher labor charge.",\
                                       res1=res1, col=col, CustomerID=CustomerID, show='yes', role=role)
            else:
                query_update = '''UPDATE RepairEvents SET LaborCharge =  %s WHERE Vin = %s AND StartDate = %s;'''
                msg2 = runSQL.writeSQL(query_update, [labor, Vin, StartDate])
                if msg2 == 'query is executed':
                    res1 = runSQL.readSQL(query1, [Vin])
                    return render_template('repair2.html', Vin=Vin, msg=msg, msg2=msg2+', labor charge is updated',\
                               res1=res1, col=col, CustomerID=CustomerID, show='yes', role=role)
                else:
                    return render_template('repair2.html', Vin=Vin, msg=msg, msg2=msg2,\
                               res1=res1, col=col, CustomerID=CustomerID, show='yes', role=role)  
                    
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
                return render_template('repair2.html', Vin=Vin, msg=msg, msg2=msg2+', new parts are added',\
                           res1=res1, col=col, CustomerID=CustomerID, show='yes', role=role)
            else:
                return render_template('repair2.html', Vin=Vin, msg=msg, msg2=msg2,\
                           res1=res1, col=col, CustomerID=CustomerID, show='yes', role=role) 
        
        if request.method == 'POST' and  "number2" in request.form:
            number2 = request.form['number2']
            quantity2 = request.form['quantity2']
            
            query_update = '''UPDATE Parts SET QuantityUsed = %s
                            WHERE Vin = %s AND StartDate = %s AND Number = %s;'''
            msg2 = runSQL.writeSQL(query_update, [quantity2, Vin, StartDate, number2]) 
            if msg2 == 'query is executed':
                res1 = runSQL.readSQL(query1, [Vin])
                return render_template('repair2.html', Vin=Vin, msg=msg, msg2=msg2+', parts are updated',\
                           res1=res1, col=col, CustomerID=CustomerID, show='yes', role=role)
            else:
                return render_template('repair2.html', Vin=Vin, msg=msg, msg2=msg2,\
                           res1=res1, col=col, CustomerID=CustomerID, show='yes', role=role)    
        
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
                return render_template('repair2.html', Vin=Vin, msg=msg, msg2=msg2,\
                           res1=res1, col=col, CustomerID=CustomerID, show='yes', role=role)
            else:
                return render_template('error_handle.html', msg="Repair is closed.", to_url = "/main_menu")
            

    return render_template('repair2.html', Vin=Vin, msg=msg, res1=res1, col=col, CustomerID=CustomerID, show='yes', role=role)







