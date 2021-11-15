from flask import Flask, render_template, request
from app import app
import runSQL
import os


@app.route('/report_customer_income', methods = ['GET', 'POST'])
def report_customer_income(): 

    with open(os.getcwd() + "\\sql_files\\report_customer_income.sql",
              "r", encoding='utf-8') as file:
        tmp = file.readlines()
    query = " ".join(tmp)
    print(query)
    

    
    res= runSQL.readSQL(query)

    col = ('Name', 'First Date', 'last Date', 'Number of Sales', 'Number of Repairs','Total Income')


  
    return render_template('report_customer_income.html', col = col, res = res)