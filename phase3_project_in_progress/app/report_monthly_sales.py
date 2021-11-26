from flask import Flask, render_template, request, session
from app import app
import runSQL
import os


@app.route('/report_montly_sales', methods = ['GET', 'POST'])
def monthly_sales():
    if 'role' not in session or session['role'] not in ['Owner', 'Manager']:
        return render_template( 'error_handle.html', msg='You are not authorized to view this report', to_url = '/login')
    role = session['role']

    with open(os.path.join(os.getcwd(), 'sql_files', 'report_monthly_sales.sql'), "r", encoding='utf-8') as file:
        tmp = file.readlines()
    query = " ".join(tmp)
    print(query)



    res= runSQL.readSQL(query)

    col = ('Year Month', 'Sale Count', 'Sale Income', 'Sale Net Income', 'Sale Ratio')



    return render_template('report_monthly_sales.html', col = col, res = res)