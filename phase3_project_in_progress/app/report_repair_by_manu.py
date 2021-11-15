from flask import Flask, render_template, request
from app import app
import runSQL
import os


@app.route('/report_repair_by_manu', methods = ['GET', 'POST'])
def repair_by_manu(): 

    with open(os.getcwd() + "\\sql_files\\report_repair_by_manu.sql",
              "r", encoding='utf-8') as file:
        tmp = file.readlines()
    query = " ".join(tmp)
    print(query)
    

    
    res= runSQL.readSQL(query)

    col = (' Manufacturer Name', 'Total Repair Count', 'Total Labor Cost', 'Total Part Cost', 'Total Cost')


  
    return render_template('report_repair_by_manu.html', col = col, res = res)