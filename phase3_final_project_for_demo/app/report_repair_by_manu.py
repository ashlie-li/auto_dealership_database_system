from flask import Flask, render_template, request, session
from app import app
import runSQL
import os


@app.route('/report_repair_by_manu', methods = ['GET', 'POST'])
def repair_by_manu(): 
    if 'role' not in session or session['role'] not in ['Owner', 'Manager']:
        return render_template( 'error_handle.html', msg='You are not authorized to view this report', to_url = '/login')
    role = session['role']
    with open(os.path.join(os.getcwd(), 'sql_files', 'report_repair_by_manu.sql'),
              "r", encoding='utf-8') as file:
        tmp = file.readlines()
    query = " ".join(tmp)
    
   
    res= runSQL.readSQL(query)
    col = (' Manufacturer Name', 'Total Repair Count', 'Total Labor Cost', 'Total Part Cost', 'Total Cost')


  
    return render_template('report_repair_by_manu.html', col = col, res = res, role=role)

@app.route('/report_repair_by_manu/<string:manu>', methods = ['GET', 'POST'])
def repair_manu_detail(manu):
    if 'role' not in session or session['role'] not in ['Owner', 'Manager']:
        return render_template( 'error_handle.html', msg='You are not authorized to view this report', to_url = '/login')
    role = session['role']
    # role = 'manager'

    with open(os.path.join(os.getcwd(), 'sql_files', 'report_repair_by_manu_detail.sql'), "r", encoding='utf-8') as file:
        tmp = file.readlines()
    query = " ".join(tmp)
    res= runSQL.readSQL(query, [manu, manu])
    col = ('Type', 'Model', 'Total Repair Count', 'Total Labor Cost', 'Total Part Cost', 'Total Part Labor Cost')
    return render_template('report_repair_by_manu_detail.html', col = col, res = res, role=role, manu=manu)