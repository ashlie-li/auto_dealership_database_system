from flask import Flask, render_template, request, session
from app import app
import runSQL
import os


@app.route('/report_sales_by_manufacturer', methods = ['GET', 'POST'])
def sales_by_manufacturer():
    if 'role' not in session or session['role'] not in ['Owner', 'Manager']:
        return render_template( 'error_handle.html', msg='You are not authorized to view this report', to_url = '/login')
    role = session['role']
    
    query0 = 'SELECT MAX(SaleDate) FROM SalesEvents;'
    lastSaleDate = runSQL.readSQL(query0)
    print(lastSaleDate[0][0])

    with open(os.path.join(os.getcwd(), 'sql_files', 'report_sales_by_manufacturer.sql'), "r") as file:
        tmp = file.readlines()
    query = "".join(tmp)
    print(query)


    res= runSQL.readSQL(query, [lastSaleDate, lastSaleDate])

    col = ('Manufacturer', 'Last Month Sales', 'Last Year Sales', 'All Time Sales')


    return render_template('report_sales_by_manufacturer.html', col = col, res = res, role=role)