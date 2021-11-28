from flask import Flask, render_template, request, redirect, url_for, session
import runSQL
from app import app


@app.route('/logout')
def logout():
   session.pop('loggedin', None)
   session.pop('username', None)
   session.pop('full name', None)
   session.pop('role', None)
   return redirect(url_for('login'))