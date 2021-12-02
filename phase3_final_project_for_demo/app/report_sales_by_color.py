from flask import Flask, render_template, request, session
from app import app
import runSQL
import os


@app.route('/report_sales_by_color', methods = ['GET', 'POST'])
def sales_by_color(): 
    if 'role' not in session or session['role'] not in ['Owner', 'Manager']:
        return render_template( 'error_handle.html', msg='You are not authorized to view this report', to_url = '/login')
    role = session['role']


    with open(os.path.join(os.getcwd(), 'sql_files', 'report_sales_by_color.sql'), "r") as file:
        tmp = file.readlines()
    query = "".join(tmp)
    
    
    res= runSQL.readSQL(query)

    col = ('Color', 'Last 30 Days Sales', 'Last Year Sales', 'All Time Sales')

    
    return render_template('report_sales_by_color.html', col = col, res = res, role=role)