from flask import Flask, render_template, request, redirect, url_for, session
import runSQL
from app import app
import os



@app.route('/add_sales/<string:Vin>', methods = ['GET', 'POST'])
def add_sales(Vin):
    if 'role' not in session or session['role'] not in ['Owner', 'Salesperson']:
        return render_template( 'error_handle.html', msg='You are not authorized to sell a vehicle', to_url = '/')
    if 'role' in session:
        role = session['role']
    else:
        role = ''
    
    msg = ''
    if request.method == 'POST' and 'CustomerID' in request.form:
        CustomerID = request.form['CustomerID']
        
        query_customer = '''SELECT Name FROM Business WHERE CustomerID = '{a}' UNION ALL SELECT CONCAT(FirstName, ' ', LastName) 
                                AS NAME FROM Persons WHERE CustomerID = '{a}'; '''.format(a=CustomerID)
        customerName = runSQL.readSQL(query_customer)[0][0]
        print(CustomerID, customerName)
        
        if 'SalePrice' not in request.form:
            return render_template('sales.html', CustomerID=CustomerID, Vin=Vin, msg=msg, role=role, customerName=customerName)
        
        else:
            SalePrice = request.form['SalePrice']
 
            query_check_price = '''SELECT 0.95 * %s > InvoicePrice FROM Vehicles WHERE Vin = %s;'''
            res0 = runSQL.readSQL(query_check_price, [SalePrice, Vin])[0][0]
            if int(res0) == 0 and session['role'] != 'Owner':
                return render_template('sales.html', CustomerID=CustomerID, Vin=Vin, msg='', alert0 = 'Price too low!', role=role, customerName=customerName)
            
            with open(os.path.join(os.getcwd(), 'sql_files', 'add_sales.sql'),
              "r", encoding='utf-8') as file:
                tmp = file.readlines()
            query = " ".join(tmp)
    
            
            res = runSQL.writeSQL(query, [Vin, SalePrice, CustomerID, session['username']])
            
            return render_template('error_handle.html', msg="Sale has been filed.", to_url = "/vehicle_detail/"+Vin)
    
    else:
        return render_template('pre_sales.html', Vin=Vin, Act="add_sales", role=role)
    
