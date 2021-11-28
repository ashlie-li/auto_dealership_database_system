from flask import Flask, render_template, request, session
from app import app
import runSQL
import os


@app.route('/report_part_stats', methods = ['GET', 'POST'])
def part_stats(): 
    if 'role' not in session or session['role'] not in ['Owner', 'Manager']:
        return render_template( 'error_handle.html', msg='You are not authorized to view this report', to_url = '/login')
    role = session['role']
    
    with open(os.path.join(os.getcwd(), 'sql_files', 'report_part_stats.sql'),
          "r", encoding='utf-8') as file:
        tmp = file.readlines()
    query = " ".join(tmp)
    
    res = runSQL.readSQL(query)

        
    col = ('Vendor Name', 'Total Cost', 'Number of Part')

    
    return render_template('report_part_stats.html', col = col, res = res, role=role)