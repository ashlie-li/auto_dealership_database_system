from flask import Flask, render_template, request
from app import app
import runSQL
import os


@app.route('/report_below_cost_sales', methods = ['GET', 'POST'])
def below_cost_sales():

    with open(os.path.join(os.getcwd(), 'sql_files', 'report_below_cost_sales.sql'), "r", encoding='utf-8') as file:
        tmp = file.readlines()
    query = "".join(tmp)
    print(query)


    res= runSQL.readSQL(query)

    col = ('Sale Date', 'Sale Price', 'Invoice Price', 'Price Ratio', 'Customer Name', 'Salesperson Name')


    return render_template('report_below_cost_sales.html', col = col, res = res)