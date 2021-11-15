from flask import Flask, render_template, request
from app import app
import runSQL
import os


@app.route('/report_sales_by_color', methods = ['GET', 'POST'])
def sales_by_color(): 
    #return render_template('index.html')
    query0 = 'SELECT MAX(SaleDate) FROM SalesEvents;'
    lastSaleDate = runSQL.readSQL(query0)
    print(lastSaleDate[0][0])
    
    with open(os.getcwd() + "\\sql_files\\report_sales_by_color.sql", "r") as file:
        tmp = file.readlines()
    query = "".join(tmp)
    print(query)
    
    
    res= runSQL.readSQL(query, [lastSaleDate, lastSaleDate, lastSaleDate, lastSaleDate])

    col = ('Color', 'Last Month Sales', 'Last Year Sales', 'All Time Sales')

    
    return render_template('report_sales_by_color.html', col = col, res = res)