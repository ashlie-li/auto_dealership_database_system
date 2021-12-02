from flask import Flask, render_template, request, redirect, url_for, session
import runSQL
from app import app
import os



@app.route('/<string:Act>/search_add_customer/<string:Vin>', methods = ['GET', 'POST'])
def search_customer(Act, Vin):  
    if 'role' in session:
        role = session['role']
    else:
        role = ''
    msg1 = ''
    if request.method == 'POST' and 'odometer' in request.form:
        odometer = request.form['odometer']
    else:
        odometer = ''
    print(request.form)
    
    if request.method == 'POST' and 'c_type' in request.form and 'input_id' in request.form:
        c_type = request.form['c_type']
        input_id = request.form['input_id']
        
        with open(os.path.join(os.getcwd(), "sql_files", "search_customer.sql"),
              "r", encoding='utf-8') as file:
            tmp = file.readlines();
        query = " ".join(tmp)
    
    
        res = []
        
        res = runSQL.readSQL(query, [c_type, input_id])
        
        if res:
            CID = res[0][-1]
            res = [res[0][:-1]]
            msg1 =  'The customer is:'
            col = ('Name', 'ID', 'Contact Name', 'Contact Title', 'Address','Phone', 'Email')
            
            return render_template('search_add_customer.html', msg1 = msg1, res=res, col = col, CID=CID, Vin=Vin, Act=Act, odometer=odometer,role=role)
        else:
            msg1 = 'No result, search again.'
            return render_template('search_add_customer.html', msg1 = msg1, odometer=odometer,role=role) ################
        
    return render_template('search_add_customer.html', msg1=msg1, Vin=Vin, Act=Act, odometer=odometer,role=role) ####################        
        

@app.route('/<string:Act>/search_add_customer/add/<string:Vin>', methods = ['GET', 'POST'])
def add_customer(Act,Vin):
    if 'role' in session:
        role = session['role']
    else:
        role = ''
    msg1 = ''
    if request.method == 'POST' and 'odometer' in request.form:
        odometer = request.form['odometer']
    else:
        odometer = ''

    if request.method == 'POST' and 'Phone' in request.form:
        query_addCustomer = '''INSERT INTO Customers (Street, City, State, 
                                ZipCode, Email, PhoneNum) VALUES (%s, 
                                %s, %s, %s, %s, %s);'''
        
        
        Phone = request.form['Phone']
        street = request.form['street']
        city = request.form['city']
        state = request.form['state']
        zipcode = request.form['zipcode']
        
        if 'Email' in request.form and len(request.form['Email'])>0:
            Email = request.form['Email']
        else:
            Email = None
            
        
        
        res2 = runSQL.writeSQL(query_addCustomer, [street, city, state, zipcode, Email, Phone])
        if res2 == 'query is executed':
            res2 = 'General information is correct.'
            newCID = runSQL.readSQL("SELECT LAST_INSERT_ID();")[0][0]
            newCID = int(newCID) 
        else:
            return render_template('search_add_customer.html', msg2=res2, alert0= "Invalid General Infomration!",Vin=Vin, Act=Act, odometer=odometer,role=role) ###################
                
        if 'TaxNum' in request.form:
            TaxNum = request.form['TaxNum']
            ComName = request.form['ComName']
            cfname = request.form['cfname']
            clname = request.form['clname']
            ctitle = request.form['ctitle']
            
            query_addBusiness = '''INSERT INTO Business (TaxNum, Name, ContactFName, 
                                    ContactLName, ContactTitle, CustomerID) VALUES 
                                    (%s, %s, %s, %s, %s, %s);'''
            res3 = runSQL.writeSQL(query_addBusiness, [TaxNum, ComName, cfname, clname, ctitle, newCID])
            if res3 == 'query is executed':
                return render_template('pass_to_act.html', CustomerID=newCID, Vin=Vin, Act=Act, odometer=odometer) ####??????
            else:
                runSQL.writeSQL("DELETE FROM Customers WHERE CustomerID = '{a}';".format(a=newCID))
                return render_template('search_add_customer.html', msg2=res2, msg3='Business infomation '+res3, alert0="Invalid Business Information!"\
                                       ,Vin=Vin, Act=Act, odometer=odometer,role=role) ##########
            
        else:
            lic = request.form['license']
            fname = request.form['fname']
            lname = request.form['lname']

            query_addPerson = '''INSERT INTO Persons (License, FirstName, 
                            LastName, CustomerID) VALUES (%s, %s, %s, %s);'''      
            res3 = runSQL.writeSQL(query_addPerson, [lic,fname, lname, newCID])
                        
            if res3 == 'query is executed':
                return render_template('pass_to_act.html', CustomerID=newCID, Vin=Vin, Act=Act, odometer=odometer) ####??????
            else:
                runSQL.writeSQL("DELETE FROM Customers WHERE CustomerID = '{a}';".format(a=newCID))
                return render_template('search_add_customer.html', msg2=res2, msg3='Person infomation '+res3,alert0="Invalid Person Information!",\
                                       Vin=Vin, Act=Act, odometer=odometer,role=role) ##########
        
        
        return render_template('search_add_customer.html', msg2=res2,role=role) ###################
    
    return render_template('search_add_customer.html', Vin=Vin, Act=Act, msg1=msg1, odometer=odometer,role=role)

    
