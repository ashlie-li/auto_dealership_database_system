from flask import Flask, render_template, request
from app import app
import runSQL
import os


@app.route('/report_sales_by_type', methods = ['GET', 'POST'])
def sales_by_type():
    query0 = 'SELECT MAX(SaleDate) FROM SalesEvents;'
    lastSaleDate = runSQL.readSQL(query0)
    print(lastSaleDate[0][0])

    with open(os.path.join(os.getcwd(), 'sql_files', 'report_sales_by_type.sql'), "r") as file:
        tmp = file.readlines()
    query = "".join(tmp)
    print(query)


    res= runSQL.readSQL(query, [lastSaleDate, lastSaleDate])

    col = ('Type', 'Last Month Sales', 'Last Year Sales', 'All Time Sales')


    return render_template('report_sales_by_type.html', col = col, res = res)