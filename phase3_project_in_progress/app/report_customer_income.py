from flask import Flask, render_template, request, session
from app import app
import runSQL
import os


@app.route('/report_customer_income', methods = ['GET', 'POST'])
def report_customer_income():
    # if 'role' not in session or session['role'] not in ['Owner', 'Manager']:
    #     return render_template( 'error_handle.html', msg='You are not authorized to view this report', to_url = '/login')
    # role = session['role']
    role = "manager"

    with open(os.path.join(os.getcwd(), "sql_files", "report_customer_income.sql"),
              "r", encoding='utf-8') as file:
        tmp = file.readlines()
    query = " ".join(tmp)
    print(query)



    res= runSQL.readSQL(query)

    res_list = []
    for row in res:
        r = list(row)
        res_list.append(r)

    col = ('Name', 'First Date', 'last Date', 'Number of Sales', 'Number of Repairs','Total Income')


    return render_template('report_customer_income.html', col = col, res = res_list, role=role)

@app.route('/report_customer_income/sales/<string:id>', methods = ['GET', 'POST'])
def sales_detail(id):
    # if 'role' not in session or session['role'] not in ['Owner', 'Manager']:
    #     return render_template( 'error_handle.html', msg='You are not authorized to view this report', to_url = '/login')
    # role = session['role']
    role = 'manager'

    with open(os.path.join(os.getcwd(), 'sql_files', 'report_customer_income_sales_detail.sql'), "r", encoding='utf-8') as file:
        tmp = file.readlines()
    query = " ".join(tmp)
    res= runSQL.readSQL(query, [id])
    col = ('Sale Date', 'Sale Price', 'Vin', 'Year', 'Manufacturer', 'Model', 'Salesperson Name')
    return render_template('report_customer_income_sales_detail.html', col = col, res = res, role=role)

@app.route('/report_customer_income/repair/<string:id>', methods = ['GET', 'POST'])
def repair_detail(id):
    if 'role' not in session or session['role'] not in ['Owner', 'Manager']:
        return render_template( 'error_handle.html', msg='You are not authorized to view this report', to_url = '/login')
    role = session['role']
    # role = 'manager'

    with open(os.path.join(os.getcwd(), 'sql_files', 'report_customer_income_repair_detail.sql'), "r", encoding='utf-8') as file:
        tmp = file.readlines()
    query = " ".join(tmp)
    res= runSQL.readSQL(query, [id])
    col = ('Start Date', 'End Price', 'Odometer', 'Labor Charge', 'Part Cost', 'Total Charge', 'Service Write Name')
    return render_template('report_customer_income_repair_detail.html', col = col, res = res, role=role)