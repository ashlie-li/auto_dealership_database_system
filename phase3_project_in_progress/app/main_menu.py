from flask import Flask, render_template, request, redirect, url_for, session
import runSQL
from app import app
import os


@app.route('/main_menu')
def main_menu():
    if 'role' in session:
        role = session['role']
    else:
        role = ''
    return render_template("main_menu.html", role=role)