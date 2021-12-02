from flask import Flask, render_template, request, redirect, url_for, session
import runSQL
from app import app
import os



@app.route('/login', methods = ['GET', 'POST'])
def login():
    msg = ''
    
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        enter_username = request.form['username']
        enter_password = request.form['password']
        query = 'SELECT * FROM PriviledgedUsers WHERE Username = %s AND Password = %s'
        user_info = runSQL.readSQL(query, (enter_username, enter_password))
        
        with open(os.path.join(os.getcwd(), "sql_files", "login.sql"),
          "r", encoding='utf-8') as file:
            tmp = file.readlines();
        query1 = " ".join(tmp).format(a=str(enter_username))
        role_info = runSQL.readSQL(query1)
    
        if user_info:
            session['loggedin'] = True
            session['username'] = user_info[0][0]
            session['full name'] = user_info[0][1] + user_info[0][3]
            
            if len(role_info) == 4:
                session['role'] = 'Owner'
            else:
                session['role'] = role_info[0][1]
            return redirect(url_for('search'))


        else:
            msg = 'Incorrect username or password!'

    return render_template('login.html', msg= msg)
    
