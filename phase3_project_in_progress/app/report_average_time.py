from flask import Flask, render_template, request, session
from app import app
import runSQL
import os

@app.route('/report_average_time', methods = ['GET', 'POST'])
def average_time(): 
    if 'role' not in session or session['role'] not in ['Owner', 'Manager']:
        return render_template( 'error_handle.html', msg='You are not authorized to view this report', to_url = '/login')
    role = session['role']
    
    with open(os.path.join(os.getcwd(), 'sql_files', 'report_average_time.sql'),
              "r", encoding='utf-8') as file:
        tmp = file.readlines()
    query = " ".join(tmp)

    
    res= runSQL.readSQL(query)

    col = ('Vendor Name', 'Average Time In Inventory')

    
    return render_template('report_average_time.html', col = col, res = res, role=role)