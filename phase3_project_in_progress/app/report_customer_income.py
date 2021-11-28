from flask import Flask, render_template, request, session
from app import app
import runSQL
import os


@app.route('/report_customer_income', methods = ['GET', 'POST'])
def report_customer_income(): 
    if 'role' not in session or session['role'] not in ['Owner', 'Manager']:
        return render_template( 'error_handle.html', msg='You are not authorized to view this report', to_url = '/login')
    role = session['role']
    
    with open(os.path.join(os.getcwd(), "sql_files", "report_customer_income.sql"),
              "r", encoding='utf-8') as file:
        tmp = file.readlines()
    query = " ".join(tmp)
    
    tmp = runSQL.readSQL(query)
    
    res = []
    
    for row in tmp:
        a = row[0]
        b = row[1:] 
        res.append([a, b])
    
    

    col = ('Name', 'First Date', 'Last Date', 'Number of Sales', 'Number of Repairs','Total Income')


    return render_template('report_customer_income.html', col = col, res = res, role=role)


@app.route('/report_customer_income/<string:CustomerID>/<string:Name>', methods = ['GET', 'POST'])
def customer_income_detail(CustomerID, Name):
    if 'role' not in session or session['role'] not in ['Owner', 'Manager']:
        return render_template( 'error_handle.html', msg='You are not authorized to view this report', to_url = '/login')
    role = session['role']

    with open(os.path.join(os.getcwd(), "sql_files", "report_customer_income_sale.sql"),
              "r", encoding='utf-8') as file:
        tmp = file.readlines()
    query_sale = " ".join(tmp)
    
    res_sale = runSQL.readSQL(query_sale, [CustomerID])
    if len(res_sale) == 0:
        show_sale = 'no'
    else:
        show_sale = 'yes'
        
    col_sale = ('Sale Date', 'Sale Price', 'Vin', 'Model Year', 'Manufacturer', 'Model', 'Salesperson')

    with open(os.path.join(os.getcwd(), "sql_files", "report_customer_income_repair.sql"),
              "r", encoding='utf-8') as file:
        tmp = file.readlines()
    query_repair= " ".join(tmp)
    
    res_repair = runSQL.readSQL(query_repair, [CustomerID])
    col_repair = ('Start Date', 'End Date', 'Odometer', 'Labor Charge', 'Part Cost', 'Total Cost', 'Service Writer')
    
    if len(res_repair) == 0:
        show_repair = 'no'
    else:
        show_repair = 'yes'    
    
    return render_template('report_customer_income_detail.html', res_sale = res_sale, col_sale = col_sale, \
                           res_repair=res_repair, col_repair=col_repair,show_sale=show_sale, show_repair=show_repair,\
                           role=role, CustomerID=CustomerID, Name=Name)