from flask import Flask, render_template, request
from app import app
import runSQL
import os


@app.route('/report_montly_sales', methods = ['GET', 'POST'])
def monthly_sales(): 

    with open(os.getcwd() + "\\sql_files\\report_monthly_sales.sql",
              "r", encoding='utf-8') as file:
        tmp = file.readlines()
    query = " ".join(tmp)
    print(query)
    

    
    res= runSQL.readSQL(query)

    col = ('Year Month', 'Sale Count', 'Sale Income', 'Sale Net Income', 'Sale Ratio')


  
    return render_template('report_monthly_sales.html', col = col, res = res)