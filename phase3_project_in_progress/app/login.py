from flask import Flask, render_template, request, redirect, url_for, session
import runSQL
from app import app



@app.route('/login', methods = ['GET', 'POST'])
def login():
    msg = ''
    
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        enter_username = request.form['username']
        enter_password = request.form['password']
        
        
        
        query = 'SELECT * FROM PriviledgedUsers WHERE Username = %s AND Password = %s'
        user_info = runSQL.readSQL(query, (enter_username, enter_password))
    
        if user_info:
            session['loggedin'] = True
            session['id'] = user_info[0][0]
            session['username'] = user_info[0][3]
            msg =  user_info[0][1]+ ' ' + user_info[0][2] + ' has logged in.'
        else:
            msg = 'Incorrect username or password!'

    return render_template('login.html', msg= msg)
    
