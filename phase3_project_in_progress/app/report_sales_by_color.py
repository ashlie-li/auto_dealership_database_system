from flask import Flask, render_template, request, session
from app import app
import runSQL
import os


@app.route('/report_sales_by_color', methods = ['GET', 'POST'])
def sales_by_color():
    if 'role' not in session or session['role'] not in ['Owner', 'Manager']:
        return render_template( 'error_handle.html', msg='You are not authorized to view this report', to_url = '/login')
    role = session['role']

    #return render_template('index.html')
    query0 = 'SELECT MAX(SaleDate) FROM SalesEvents;'
    lastSaleDate = runSQL.readSQL(query0)
    print(lastSaleDate[0][0])

    with open(os.path.join(os.getcwd(), 'sql_files', 'report_sales_by_color.sql'), "r") as file:
        tmp = file.readlines()
    query = "".join(tmp)
    print(query)


    res= runSQL.readSQL(query, [lastSaleDate, lastSaleDate, lastSaleDate, lastSaleDate])

    col = ('Color', 'Last Month Sales', 'Last Year Sales', 'All Time Sales')


    return render_template('report_sales_by_color.html', col = col, res = res)